import os
from datasets import load_dataset
import pandas as pd

print("🚀 Starting dataset preparation for Smart University Safety & Emergency System")

def setup_directories():
    """Create all necessary directories"""
    dirs = [
        "data/raw",
        "data/raw/ucsd",
        "data/raw/shanghaitech",
        "data/raw/ucf-crime",
        "data/processed",
        "data/knowledge_base"
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print("✅ Directories created/verified")

def download_crisisnlp():
    """Download CrisisNLP dataset - useful for emergency text understanding"""
    print("\n📥 Downloading CrisisNLP dataset (for RAG knowledge base)...")
    
    try:
        # Load the dataset from Hugging Face
        dataset = load_dataset("QCRI/CrisisBench-all-lang", split="train")
        df = dataset.to_pandas()
        
        # Save to knowledge base folder
        output_path = "data/knowledge_base/crisisnlp.csv"
        df.to_csv(output_path, index=False)
        
        print(f"✅ CrisisNLP downloaded successfully!")
        print(f"   Saved to: {output_path}")
        print(f"   Total samples: {len(df):,}")
        print(f"   Columns: {df.columns.tolist()}")
        
    except Exception as e:
        print(f"❌ Error downloading CrisisNLP: {e}")
        print("   You can continue with sample documents for now.")

def create_sample_safety_knowledge_base():
    """Create sample campus safety documents (you can add real PDFs later)"""
    print("\n📄 Creating sample campus safety knowledge base...")
    
    safety_docs = [
        {
            "title": "Physical Altercation Response Protocol",
            "content": """Campus Physical Altercation Protocol:

1. Ensure your own safety first - move away if possible.
2. Immediately call Campus Security at extension 5555 or use emergency button.
3. Provide clear information: Location (e.g., Building A entrance), number of people involved, description of incident.
4. Do not attempt to physically intervene unless you are trained security personnel.
5. If safe, try to de-escalate verbally while waiting for security.
6. After incident, provide statement to security team."""
        },
        {
            "title": "Building Evacuation Guidelines",
            "content": """Evacuation Procedures for University Buildings:

- Activate the nearest fire alarm pull station if there is immediate danger.
- Proceed calmly to the nearest exit. Do not use elevators.
- Assist persons with disabilities if possible.
- Assembly point: Main University Courtyard or designated parking area.
- Security and emergency services will conduct headcount at assembly point.
- Do not re-enter the building until given official all-clear."""
        },
        {
            "title": "Suspicious Behavior and Threat Reporting",
            "content": """Report Suspicious Behavior Immediately:

Examples to report:
- Persons loitering in restricted areas or near building entrances
- Unattended bags, packages, or backpacks
- Aggressive arguments or physical fights
- Unauthorized access attempts to buildings or labs
- Anyone behaving unusually nervous or avoiding eye contact while carrying heavy items

When reporting:
- Give exact location and time
- Describe individuals (clothing, height, age range)
- Note any vehicles involved
- Call Campus Security immediately"""
        }
    ]
    
    for i, doc in enumerate(safety_docs):
        filename = f"data/knowledge_base/campus_safety_{i+1}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Title: {doc['title']}\n\n{doc['content']}")
        print(f"   Created: {filename}")
    
    print("✅ Sample safety knowledge base created!")

if __name__ == "__main__":
    setup_directories()
    download_crisisnlp()
    create_sample_safety_knowledge_base()
    
    print("\n🎉 Dataset preparation completed!")
    print("Next steps:")
    print("   1. Add your university's actual safety PDFs to data/knowledge_base/")
    print("   2. Download video datasets (UCF-Crime, UCSD, ShanghaiTech) into data/raw/ucf-crime, data/raw/ucsd, data/raw/shanghaitech")
    print("   3. Place one sample frame in each dataset folder as .png/.jpg/.tif for dashboard testing")
    print("   4. Proceed to build the RAG pipeline")