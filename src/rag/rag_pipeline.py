import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

class UniversitySafetyRAG:
    """
    University Safety RAG Pipeline with Authenticated HuggingFace Embeddings
    and Groq's Smartest LLM: llama-3.1-405b-reasoning
    """
    
    def __init__(self, knowledge_base_path="data/knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        
        self.setup_embeddings()
        self.setup_llm()
        
    def setup_embeddings(self):
        """Setup authenticated HuggingFace embeddings with HF_TOKEN"""
        print("🔧 Loading HuggingFace embeddings with authentication...")
        
        # HF_TOKEN should be set in .env for authenticated requests
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            os.environ['HF_TOKEN'] = hf_token
            print("✅ HuggingFace token configured for authenticated requests")
        else:
            print("⚠️  HF_TOKEN not found in .env - using unauthenticated requests")
            print("   Add HF_TOKEN to .env for higher rate limits: https://huggingface.co/settings/tokens")
        
        # Using BGE (Better Generic Embeddings) - superior model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={"normalize_embeddings": True}
        )
        print("✅ BGE Embeddings ready (BAAI/bge-small-en-v1.5)")
    
    def setup_llm(self):
        """Setup Groq with the SMARTEST available model: llama-3.1-70b-versatile"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY not found in .env file!")
        
        print("🚀 Connecting to Groq LLM (Smartest Available Model)...")
        # llama-3.1-70b-versatile is Groq's most capable publicly available model
        # - 70B parameters (highly capable)
        # - Advanced reasoning capabilities
        # - Better context understanding (8k tokens)
        # - Perfect for safety-critical decisions
        self.llm = ChatGroq(
            groq_api_key=api_key,
            model_name="llama-3.1-70b-versatile",  # Smartest available model
            temperature=0.2,  # Low for reliable safety decisions
            max_tokens=1500,   # Comprehensive analysis
            top_p=0.95,        # Quality control
            timeout=30
        )
        print("✅ Groq LLM connected (llama-3.1-70b-versatile - SMARTEST AVAILABLE)")
    
    def load_vectorstore(self):
        index_path = "data/processed/faiss_index"
        if os.path.exists(index_path):
            print("📂 Loading FAISS index...")
            self.vectorstore = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("🏗️ Building FAISS index...")
            loader = DirectoryLoader(self.knowledge_base_path, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
            splits = splitter.split_documents(docs)
            self.vectorstore = FAISS.from_documents(splits, self.embeddings)
            self.vectorstore.save_local(index_path)
            print(f"✅ Built index with {len(splits)} chunks")
    
    def get_safety_recommendation(self, incident_description: str):
        """Enhanced safety recommendation using Groq's reasoning and context awareness"""
        self.load_vectorstore()
        
        # Retrieve relevant documents with higher relevance
        docs = self.vectorstore.similarity_search(incident_description, k=5)
        context = "\n\n".join([f"[Protocol {i+1}]: {doc.page_content}" for i, doc in enumerate(docs)])
        
        # IMPROVED PROMPT: More structured, context-aware, and safety-critical
        prompt = PromptTemplate.from_template("""You are a highly experienced university campus safety AI assistant with deep knowledge of emergency response protocols.

CONTEXT FROM SAFETY PROTOCOLS:
{context}

INCIDENT REPORT:
{incident}

ANALYSIS REQUIREMENTS:
1. Assess the severity level (LOW/MEDIUM/HIGH/CRITICAL)
2. Identify the specific safety concern and potential risks
3. Reference applicable safety protocols from the context above
4. Provide immediate, actionable response recommendations
5. Consider de-escalation and student/staff welfare

RESPONSE FORMAT (Be precise and professional):

🚨 SEVERITY LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]

📋 INCIDENT SUMMARY:
[One sentence describing the abnormal activity and key risk factors]

🔍 ANALYSIS:
[2-3 sentences analyzing the incident based on safety protocols]

✅ RECOMMENDED IMMEDIATE ACTIONS:
• [Action 1 - Most urgent] (Timeline: ___)
• [Action 2] (Timeline: ___)
• [Action 3] (Timeline: ___)
• [Action 4 - Communication/Documentation] (Timeline: ___)

⚠️ SAFETY PRIORITIES:
• [Priority 1]
• [Priority 2]
• [Priority 3]

Remember: Prioritize human safety, de-escalation, proper documentation, and adherence to university emergency protocols.""")

        formatted_prompt = prompt.format(context=context, incident=incident_description)
        
        print(f"\n🚨 GROQ SAFETY ANALYSIS ENGINE:")
        print(f"Processing incident: {incident_description[:80]}...")
        response = self.llm.invoke(formatted_prompt)
        
        print("\n📢 GROQ-POWERED SAFETY ALERT (Enhanced):")
        print("="*70)
        print(response.content)
        print("="*70)
        
        return {"result": response.content, "model": "llama-3.3-70b-versatile"}

# Test
if __name__ == "__main__":
    print("🧪 Testing Groq RAG Pipeline")
    rag = UniversitySafetyRAG()
    test = "Possible fight detected near Building A entrance. 4 people involved. Confidence: 0.88"
    rag.get_safety_recommendation(test)