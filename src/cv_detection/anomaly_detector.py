


# -*- coding: utf-8 -*-
import os
from pathlib import Path
from anomalib.data import UCSDped
from anomalib.models import Patchcore
from anomalib.engine import Engine
from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import torch
from datetime import datetime

class CampusAnomalyDetector:
    def __init__(self, data_root="data/raw/ucsd"):
        self.data_root = Path(data_root)
        self.model = None
        self.engine = None
        self.datamodule = None
        
        # Vision models for image processing
        self.caption_processor = None
        self.caption_model = None
        self.clip_processor = None
        self.clip_model = None
        
    def setup_datamodule(self, scene="UCSDped2"):
        """Setup UCSD Pedestrian datamodule (video anomaly detection)"""
        print(f"Setting up UCSD {scene} datamodule...")
        
        # Correct way for current Anomalib version
        self.datamodule = UCSDped(
            root=self.data_root,
            category=scene,                    # "UCSDped1" or "UCSDped2"
            clip_length_in_frames=2,           # Number of frames per clip
            frames_between_clips=10,
            target_frame="last",               # or VideoTargetFrame.LAST if import needed
            train_batch_size=4,                # Smaller batch size for CPU
            eval_batch_size=4,
            num_workers=2,                     # Lower for university server
        )
        
        print(f"UCSD {scene} datamodule ready")
        print(f"   Root path: {self.datamodule.root}")
        return self.datamodule
    
    def _load_caption_model(self):
        """Lazy load BLIP captioning model"""
        if self.caption_processor is None:
            print("Loading BLIP image captioning model...")
            self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            print("OK Captioning model ready")
    
    def _load_clip_model(self):
        """Lazy load CLIP model for anomaly scoring"""
        if self.clip_processor is None:
            print("Loading Loading CLIP model for anomaly detection...")
            self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            print("OK CLIP model ready")
    
    def refine_caption_with_action(self, image, raw_caption: str) -> str:
        """Refine the BLIP caption by checking action keywords with CLIP zero-shot labels."""
        self._load_clip_model()
        action_labels = [
            "people running away in panic",
            "a crowd fleeing in fear",
            "people scared and running",
            "people moving quickly in fear",
            "a group of people dancing in a large room",
            "a celebration party with dancing people",
            "a calm group of people standing",
            "a crowded hallway with normal walking"
        ]

        try:
            inputs = self.clip_processor(text=action_labels, images=image, return_tensors="pt", padding=True)
            outputs = self.clip_model(**inputs)
            probs = outputs.logits_per_image.softmax(dim=1)[0]
            sorted_scores = sorted(enumerate(probs.tolist()), key=lambda x: x[1], reverse=True)
            best_idx, best_score = sorted_scores[0]
            second_idx, second_score = sorted_scores[1]
            best_label = action_labels[best_idx]
            second_label = action_labels[second_idx]

            print(f"Action CLIP top label: {best_label} ({best_score:.3f}), second: {second_label} ({second_score:.3f})")

            danger_keywords = ["running", "fleeing", "panic", "scared", "fear"]
            is_dangerous = any(keyword in best_label for keyword in danger_keywords)
            is_dancing = "dancing" in best_label or "celebration" in best_label
            raw_lower = raw_caption.lower()

            if "dancing" in raw_lower and any(keyword in raw_lower for keyword in ["panic", "running", "flee", "scared", "terrified"]):
                return f"{raw_caption}. The scene appears to show people running away in alarm or fear."

            if is_dangerous and best_score > 0.35:
                if is_dancing and best_score - second_score < 0.08:
                    return f"{raw_caption}. The scene appears to show people running away in alarm or fear."
                return f"{raw_caption}. The scene appears to show people running away in alarm or fear."

            if is_dancing and best_score > 0.45:
                if "running" in raw_lower or "panic" in raw_lower or "flee" in raw_lower:
                    return f"{raw_caption}. The scene appears to show people running away in alarm or fear."
                return f"{raw_caption}. The scene looks like people dancing in a large room."

        except Exception as e:
            print(f"Error refining caption: {e}")

        return raw_caption

    def generate_image_caption(self, image_path: str) -> str:
        """Generate descriptive caption for uploaded image"""
        self._load_caption_model()
        
        try:
            image = Image.open(image_path).convert('RGB')
            
            inputs = self.caption_processor(image, return_tensors="pt")
            out = self.caption_model.generate(
                **inputs,
                max_length=100,
                num_beams=5,
                early_stopping=True,
            )
            caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
            caption = self.refine_caption_with_action(image, caption)
            
            print(f"Caption Generated Caption: {caption}")
            return caption
            
        except Exception as e:
            print(f"Error Error generating caption: {e}")
            return "Unable to generate caption for the image"
    
    def compute_anomaly_score(self, image_path: str) -> float:
        """Compute anomaly score using CLIP zero-shot classification"""
        self._load_clip_model()
        
        try:
            image = Image.open(image_path).convert('RGB')
            
            # Define normal vs anomalous text prompts
            normal_prompts = [
                "normal people walking on campus",
                "students studying in library",
                "people having normal conversation",
                "regular pedestrian activity",
                "normal university scene"
            ]
            
            anomalous_prompts = [
                "people fighting or arguing violently",
                "a crowd fleeing in panic",
                "people running away in fear",
                "suspicious person lurking",
                "unattended suspicious package",
                "person with weapon",
                "emergency situation",
                "abnormal crowd behavior",
                "intruder in restricted area"
            ]
            
            # Get image features
            inputs = self.clip_processor(text=normal_prompts + anomalous_prompts, images=image, return_tensors="pt", padding=True)
            outputs = self.clip_model(**inputs)
            
            # Compute similarities
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            
            # Average probability for normal prompts
            normal_score = probs[0][:len(normal_prompts)].mean().item()
            
            # Average probability for anomalous prompts
            anomalous_score = probs[0][len(normal_prompts):].mean().item()
            
            # Anomaly score: higher means more anomalous
            anomaly_score = anomalous_score / (normal_score + anomalous_score + 1e-6)
            anomaly_score = min(anomaly_score, 0.95)  # Cap at 0.95
            
            print(f"Analysis Anomaly Score: {anomaly_score:.3f} (Normal: {normal_score:.3f}, Anomalous: {anomalous_score:.3f})")
            return anomaly_score
            
        except Exception as e:
            print(f"Error Error computing anomaly score: {e}")
            return 0.5  # Default neutral score
    
    def process_image_and_generate_event(self, image_path: str, location: str = "Campus area"):
        """Complete pipeline: caption image, compute anomaly score, generate event description"""
        print(f"Image Processing image: {image_path}")
        
        # Generate caption
        caption = self.generate_image_caption(image_path)
        
        # Compute anomaly score
        anomaly_score = self.compute_anomaly_score(image_path)
        
        # Identify risky actions from the caption and anomaly score
        risk_info = self.identify_risky_actions(caption, anomaly_score)
        
        # Generate event description using existing method and include caption details
        event_dict = self.generate_event_description(
            anomaly_score=anomaly_score,
            location=location,
            caption=caption,
            risk_info=risk_info
        )
        
        event_dict["caption"] = caption
        event_dict["risk_level"] = risk_info.get("risk_level", "UNKNOWN")
        event_dict["risk_actions"] = risk_info.get("risky_actions", [])
        event_dict["source"] = "Computer Vision - Image Analysis (BLIP + CLIP)"

        return event_dict
    
    def identify_risky_actions(self, caption: str, anomaly_score: float) -> dict:
        """Infer risky or abnormal actions from the generated caption."""
        text = caption.lower() if caption else ""
        risky_actions = []

        checks = [
            ("potential assault or fight", ["fight", "punch", "attack", "assault", "knife", "weapon", "gun", "shouting", "screaming", "yelling", "hitting", "kicking"]),
            ("possible fall or injury", ["fell", "falling", "fall", "slip", "tripped", "collapsed", "injured", "hurt"]),
            ("crowd disturbance or panic", ["crowd", "running", "running away", "fleeing", "panic", "terrified", "scared", "chased", "escaping", "shoving", "pushing"]),
            ("suspicious person or intruder", ["intruder", "suspicious", "unauthorized", "trespasser", "loitering", "hiding"]),
        ]

        for label, keywords in checks:
            if any(keyword in text for keyword in keywords):
                risky_actions.append(label)

        if not risky_actions:
            if anomaly_score > 0.8:
                risky_actions.append("highly anomalous activity")
            elif anomaly_score > 0.5:
                risky_actions.append("suspicious behavior")

        if anomaly_score > 0.75:
            risk_level = "HIGH"
        elif anomaly_score > 0.45:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risky_actions": risky_actions,
            "risk_level": risk_level,
            "anomaly_score": anomaly_score,
        }

    def generate_event_description(self, anomaly_score: float = 0.8, location: str = "Building walkway", caption: str = None, risk_info: dict | None = None):
        """Convert anomaly detection score into structured event for RAG"""
        if anomaly_score > 0.75:
            event_type = "Abnormal activity / possible intruder or non-pedestrian object"
            confidence = min(anomaly_score, 0.95)
        elif anomaly_score > 0.45:
            event_type = "Suspicious or unusual movement detected"
            confidence = anomaly_score
        else:
            event_type = "Normal pedestrian flow"
            confidence = 1.0 - anomaly_score
        
        if risk_info is None:
            risk_info = self.identify_risky_actions(caption or "", anomaly_score)

        actions = risk_info.get("risky_actions", [])
        risk_level = risk_info.get("risk_level", "LOW")
        actions_text = ", ".join(actions) if actions else "general abnormal activity"

        if caption:
            description = (
                f"{caption}. Detected as {event_type.lower()} in {location}. "
                f"Risk level: {risk_level}. Confidence: {confidence:.2f}. "
                f"This image appears to show {caption.lower()}, suggesting {actions_text}."
            )
        else:
            description = (
                f"{event_type} in {location}. Confidence: {confidence:.2f}. "
                f"Risk level: {risk_level}. "
                f"This appears to be {actions_text}."
            )
        
        event_dict = {
            "event": event_type,
            "location": location,
            "confidence": round(confidence, 2),
            "time": datetime.now().strftime("%H:%M:%S"),
            "source": "Computer Vision - Image Analysis (BLIP + CLIP)",
            "description": description,
            "risk_level": risk_level,
            "risky_actions": actions,
        }
        
        if caption:
            event_dict["caption"] = caption
        
        print(f"Alert CV Generated Event: {description}")
        return event_dict

# ============================
# Quick Test
# ============================
if __name__ == "__main__":
    print("🧪 Testing Campus Anomaly Detector (CV Part)\n")
    
    detector = CampusAnomalyDetector(data_root="data/raw/ucsd")
    
    # Setup datamodule (this should work now)
    datamodule = detector.setup_datamodule(scene="UCSDped2")
    
    # Test with sample image (you'll need to provide an image path)
    # sample_image = "path/to/sample/image.jpg"
    # event = detector.process_image_and_generate_event(sample_image, location="Building A entrance")
    
    # For now, test the old method
    sample_event = detector.generate_event_description(anomaly_score=0.82, location="Building A entrance")
    
    print("\nOK UCSD setup successful!")
    print("Next steps:")
    print("   - Train model: detector.train_model()  (may take time on CPU)")
    print("   - Connect output to RAG pipeline for safety recommendations")
    print("   - Test image processing: detector.process_image_and_generate_event('image.jpg')")
    