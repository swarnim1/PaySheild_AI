# backend/rag_pipeline.py

import os
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document

#from config.settings import GEMINI_API_KEY

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Settings
VECTORSTORE_PATH = "embeddings/"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
# -----------------------------

# Load embedding model once
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

# Initialize Gemini once
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# -----------------------------

def load_vectorstore(api_name, doc_type):
    """
    Load specific FAISS vectorstore:
    - api_name: 'stripe' or 'adyen'
    - doc_type: 'business' or 'technical'
    """
    folder_path = os.path.join(VECTORSTORE_PATH, f"{api_name}_{doc_type}_vectorstore")
    
    # Correct loading style for LangChain 0.2.x
    return FAISS.load_local(
        folder_path=folder_path,
        embeddings=embedding_model,
        allow_dangerous_deserialization=True
    )

def retrieve_context(user_query, vectorstore):
    """Given user query, fetch top relevant chunks."""
    docs = vectorstore.similarity_search(user_query, k=5)
    return docs

def ask_gemini(context_docs, user_query , previous_chats):
    """
    Send context + user query to Gemini, get an answer.
    """
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    print(f"-------------------------------previous chatv {previous_chats}--------------------------------")

    prompt = f"""
You are a highly skilled technical assistant specializing in Payment API integrations.

Use the following extracted documentation context to answer the user query.
If the user asks about implementation, **always respond with proper, runnable code snippets** inside markdown (using ```language) .
✅ Prefer Python code if no language specified.
✅ If user specifies Node.js / Java, respond in that language.

Context:
{context_text}

Question:
{user_query}

Rules:
- If answering with code, format it properly inside ```code blocks``` so that it looks clean.
- If you don't see answer in context then try to it by own but keep your answer around (stripe and adeyns) only and  if the question deviate from payment api documentation tell them polietly to ask relevent question
- If user is asking incomplete question like "tell me how to use payment system in python code" and no payment system like(Strype or Adeyns) 
or some other important information that in required to extract relevent data from vectorstore and the information not in context also,  then you pilotely ask to specify the misiing detail 

some previous chat for context {previous_chats}

Now write the best answer:
"""


    response = gemini_model.generate_content(prompt)
    return response.text

# -----------------------------
# Main RAG pipeline


#It detect the stage your llm is in
def detect_stage(user_query, previous_chats):
    """
    Intelligent detection of stage (business or technical) from user query + chat history.
    """
    prompt = f"""
You are a smart assistant.

Decide whether the user's query is BUSINESS LEVEL (choosing payment provider, comparing options, pricing, general setup) 
OR TECHNICAL LEVEL (asking for integration code, API endpoints, programming languages).

Give your answer strictly as one of these three words:
- "business"
- "technical"
- "ambiguous"

CONVERSATION HISTORY (last few messages):
{previous_chats}

CURRENT USER QUERY:
{user_query}

Your final classification (one word only):
"""
    model = "gemini-1.5-flash-8b"
    response = genai.GenerativeModel(model).generate_content(prompt)
    detected_stage = response.text.strip().lower()

    # Safety check
    if detected_stage not in ["business", "technical", "ambiguous"]:
        detected_stage = "ambiguous"

    print(f"🛠️ DETECTED STAGE from mini LLM: {detected_stage.upper()}")
    return detected_stage

def rag_answer(user_query, user_selected_api=None, previous_chats=None , detected_stage = 'Ambiguous'):
    """
    Dynamic RAG based on detected user stage.
    """

    if detected_stage == "business":
        print("🔵 System chose BUSINESS mode based on user query.")
        
        vectorstore_stripe = load_vectorstore(api_name="stripe", doc_type="business")
        vectorstore_adyen = load_vectorstore(api_name="adyen", doc_type="business")

        docs_stripe = retrieve_context(user_query, vectorstore_stripe)
        docs_adyen = retrieve_context(user_query, vectorstore_adyen)

        combined_context = docs_stripe + docs_adyen

        chatbot_response = ask_gemini(combined_context, user_query, previous_chats)
        return chatbot_response

    elif detected_stage == "technical":
        print("🟠 System chose TECHNICAL mode based on user query.")

        if not user_selected_api:
            print("⚠️ No API selected. Cannot proceed to technical retrieval.")
            return "Please select a Payment API first to proceed with technical integration questions."

        vectorstore = load_vectorstore(api_name=user_selected_api, doc_type="technical")
        context_docs = retrieve_context(user_query, vectorstore)

        chatbot_response = ask_gemini(context_docs, user_query, previous_chats)
        return chatbot_response

    else:
        print("🟣 System detected AMBIGUOUS intent. Using both BUSINESS and TECHNICAL documents.")

        vectorstore_business_stripe = load_vectorstore(api_name="stripe", doc_type="business")
        vectorstore_business_adyen = load_vectorstore(api_name="adyen", doc_type="business")
        vectorstore_tech_stripe = load_vectorstore(api_name="stripe", doc_type="technical")
        vectorstore_tech_adyen = load_vectorstore(api_name="adyen", doc_type="technical")

        # Retrieve from all
        docs_b_stripe = retrieve_context(user_query, vectorstore_business_stripe)
        docs_b_adyen = retrieve_context(user_query, vectorstore_business_adyen)
        docs_t_stripe = retrieve_context(user_query, vectorstore_tech_stripe)
        docs_t_adyen = retrieve_context(user_query, vectorstore_tech_adyen)

        combined_context = docs_b_stripe + docs_b_adyen + docs_t_stripe + docs_t_adyen

        chatbot_response = ask_gemini(combined_context, user_query, previous_chats)
        return chatbot_response

    