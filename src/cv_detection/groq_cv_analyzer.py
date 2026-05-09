"""
Enhanced CV Analysis using Groq LLM for intelligent image interpretation.
This module supplements the traditional CV detection with Groq's reasoning capabilities.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()


class GroqCVAnalyzer:
    """
    Intelligent CV analysis using Groq LLM.
    Enhances image captions and anomaly scores with semantic reasoning.
    """
    
    def __init__(self):
        self.llm = None
        self.setup_llm()
    
    def setup_llm(self):
        """Setup Groq with the SMARTEST available model: llama-3.1-70b-versatile"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")
        
        print("🚀 Initializing Groq CV Analyzer (Smartest Available Model)...")
        # llama-3.1-70b-versatile: 70B parameters for superior reasoning
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-70b-versatile",  # Smartest available model
            temperature=0.1,  # Very low for precise analysis
            max_tokens=500,
            timeout=30
        )
        print("✅ Groq CV Analyzer ready (llama-3.1-70b-versatile - SMARTEST AVAILABLE)")
    
    def analyze_image_caption(self, caption: str, anomaly_score: float, location: str) -> dict:
        """
        Use Groq to intelligently analyze image caption and anomaly score.
        
        Args:
            caption: Image description from BLIP model
            anomaly_score: Anomaly detection score from CLIP
            location: Where the image was captured
        
        Returns:
            Dictionary with enhanced analysis
        """
        prompt = PromptTemplate.from_template("""You are a campus safety expert analyzing computer vision output.

IMAGE CAPTION (from vision AI): {caption}

ANOMALY SCORE: {anomaly_score:.2f} (0.0=normal, 1.0=highly anomalous)

LOCATION: {location}

ANALYSIS TASK:
1. Interpret what the image shows in context of campus safety
2. Identify any concerning behaviors or unusual patterns
3. Rate the incident severity
4. Provide a professional assessment

RESPONSE (JSON FORMAT):
{{
    "interpretation": "Clear, concise description of what's happening",
    "concerning_behaviors": ["behavior1", "behavior2"],
    "severity": "LOW|MEDIUM|HIGH|CRITICAL",
    "is_emergency": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of the assessment"
}}

Be precise and concise.""")
        
        formatted_prompt = prompt.format(
            caption=caption,
            anomaly_score=anomaly_score,
            location=location
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            content = response.content.strip()
            
            # Try to parse as JSON, otherwise return structured response
            import json
            try:
                # Extract JSON from response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    analysis = json.loads(json_str)
                else:
                    analysis = self._create_default_analysis(caption, anomaly_score)
            except json.JSONDecodeError:
                analysis = self._create_default_analysis(caption, anomaly_score)
            
            print(f"✅ Groq Analysis: {analysis['severity']} severity - {analysis['interpretation']}")
            return analysis
            
        except Exception as e:
            print(f"⚠️  Groq analysis error: {e}")
            return self._create_default_analysis(caption, anomaly_score)
    
    def refine_event_description(self, raw_event: dict) -> dict:
        """
        Use Groq to refine and enhance the event description with intelligence.
        
        Args:
            raw_event: Event dict from CampusAnomalyDetector
        
        Returns:
            Enhanced event dict with Groq analysis
        """
        prompt = PromptTemplate.from_template("""You are a campus safety professional reviewing automated incident reports.

INCIDENT REPORT:
- Type: {event_type}
- Location: {location}
- Risk Level: {risk_level}
- Confidence: {confidence}
- Description: {description}
- Risky Actions: {risky_actions}

TASK: Provide an enhanced, professional assessment suitable for campus security.

RESPONSE (JSON FORMAT):
{{
    "enhanced_summary": "Professional, one-sentence summary",
    "threat_assessment": "LOW|MEDIUM|HIGH|CRITICAL",
    "recommended_response": ["action1", "action2", "action3"],
    "evidence_strength": "WEAK|MODERATE|STRONG",
    "suggested_protocols": ["protocol1", "protocol2"]
}}

Be precise and actionable.""")
        
        formatted_prompt = prompt.format(
            event_type=raw_event.get('event', 'Unknown'),
            location=raw_event.get('location', 'Unknown'),
            risk_level=raw_event.get('risk_level', 'LOW'),
            confidence=raw_event.get('confidence', 0.0),
            description=raw_event.get('description', ''),
            risky_actions=", ".join(raw_event.get('risky_actions', []))
        )
        
        try:
            response = self.llm.invoke(formatted_prompt)
            content = response.content.strip()
            
            import json
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    analysis = json.loads(json_str)
                    
                    # Enhance the original event
                    enhanced_event = raw_event.copy()
                    enhanced_event['groq_summary'] = analysis.get('enhanced_summary', '')
                    enhanced_event['threat_level'] = analysis.get('threat_assessment', raw_event.get('risk_level'))
                    enhanced_event['recommended_actions'] = analysis.get('recommended_response', [])
                    enhanced_event['evidence'] = analysis.get('evidence_strength', 'UNKNOWN')
                    enhanced_event['groq_enhanced'] = True
                    
                    return enhanced_event
                else:
                    raw_event['groq_enhanced'] = False
                    return raw_event
            except json.JSONDecodeError:
                raw_event['groq_enhanced'] = False
                return raw_event
                
        except Exception as e:
            print(f"⚠️ Groq refinement error: {e}")
            raw_event['groq_enhanced'] = False
            return raw_event
    
    def _create_default_analysis(self, caption: str, anomaly_score: float) -> dict:
        """Create default analysis structure when Groq fails or returns unparseable output"""
        
        # Simple heuristic-based analysis
        if anomaly_score > 0.8:
            severity = "HIGH"
            is_emergency = True
        elif anomaly_score > 0.6:
            severity = "MEDIUM"
            is_emergency = False
        else:
            severity = "LOW"
            is_emergency = False
        
        return {
            "interpretation": f"Computer vision detected: {caption}",
            "concerning_behaviors": [],
            "severity": severity,
            "is_emergency": is_emergency,
            "confidence": anomaly_score,
            "reasoning": f"Based on anomaly score of {anomaly_score:.2f}"
        }


# Test module
if __name__ == "__main__":
    print("🧪 Testing Groq CV Analyzer\n")
    
    analyzer = GroqCVAnalyzer()
    
    # Test caption analysis
    test_caption = "A group of people running quickly towards the exit in a crowded hallway"
    test_score = 0.85
    test_location = "Building A, 3rd floor corridor"
    
    print("\n📊 Analyzing image caption with Groq...")
    analysis = analyzer.analyze_image_caption(test_caption, test_score, test_location)
    print(f"Analysis result: {analysis}")
    
    # Test event refinement
    test_event = {
        'event': 'Abnormal activity / possible emergency',
        'location': 'Building A, 3rd floor corridor',
        'risk_level': 'HIGH',
        'confidence': 0.85,
        'description': 'People running in panic',
        'risky_actions': ['possible evacuation', 'crowd disturbance']
    }
    
    print("\n📋 Refining event with Groq intelligence...")
    refined = analyzer.refine_event_description(test_event)
    print(f"Refined event: {refined}")
