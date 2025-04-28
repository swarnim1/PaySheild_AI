# PayShield AI 💳🛡️

**Smart Payment API Advisor Chatbot**

PayShield AI is an intelligent, cloud-deployable chatbot that helps developers and businesses select, integrate, and code with payment APIs like **Stripe** and **Adyen**. Built using a Retrieval-Augmented Generation (RAG) architecture combined with **Gemini 1.5 Pro**, it makes setting up payment solutions easier, faster, and smarter.

---

## 🔍 Key Features
- **RAG System**: Retrieves the most relevant documentation chunks using FAISS vector stores.
- **Smart State Detection**: Automatically detects whether the user query is "business" or "technical" stage.
- **Partial Chat Memory**: Considers last conversation context while generating better answers.
- **Embeddings Precomputed**: Fast startup without heavy compute.
- **Streamlit Frontend**: Simple, elegant user interface.
- **Typing Animation and Chat History**: Smooth user experience.
- **Reset Button**: Restart the conversation anytime.

---

## 📘 Project Structure
```
PayShield_AI/
├── app.py
├── backend/
│   ├── __init__.py
│   ├── rag_pipeline.py
├── config/
│   ├── __init__.py
│   ├── settings.py
├── data/
│   ├── processed_chunks/ (optional)
├── embeddings/
│   ├── stripe_business_vectorstore/
│   ├── adyen_business_vectorstore/
│   ├── stripe_technical_vectorstore/
│   ├── adyen_technical_vectorstore/
├── requirements.txt
└── .streamlit/
    └── config.toml
```

---

## 🚀 How to Run Locally

1. Clone the repository:
```bash
git clone https://github.com/your-username/PayShield_AI.git
cd PayShield_AI
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your Gemini API Key:
```bash
export GEMINI_API_KEY='your-gemini-api-key'  # On Windows: set GEMINI_API_KEY=your-gemini-api-key
```

5. Run the app:
```bash
streamlit run app.py
```

---

## 🌐 Deploy to Streamlit Cloud
- Upload entire project to GitHub (including embeddings folder).
- In Streamlit Cloud, create a new app and connect your GitHub repo.
- Set `GEMINI_API_KEY` in the "Secrets" tab.
- Deploy!

---

## 💼 Tech Stack
- Python 3.10+
- Streamlit
- LangChain
- Huggingface Sentence Transformers
- FAISS
- Gemini 1.5 Pro (Google Generative AI)

---

## 🌟 Future Improvements
- Support for more payment APIs (e.g., Razorpay, PayPal)
- Full conversation memory
- Fine-tuned LLM for faster stage detection
- Docker-based deployment

---

## 💪 Built with passion to simplify API integration!  
_"Choose, integrate, and code smarter."_

