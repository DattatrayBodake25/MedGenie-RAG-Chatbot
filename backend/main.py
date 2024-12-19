import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing_extensions import TypedDict, List
from fastapi.responses import FileResponse


import logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate the API keys
if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key is missing! Please check your .env file.")
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing! Please check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to handle requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict this to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files from the frontend directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Pinecone setup with the updated initialization method
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-rag-chatbot"
index = pc.Index(index_name)

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Set up the VectorStore
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# Initialize the Gemini API key for authentication
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY, temperature=0)

# Define the state of the application
class State(TypedDict):
    question: str
    context: List[str]  # List of documents (content)
    answer: str

# Define a Pydantic model for the query input
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# Root endpoint to serve the index.html
@app.get("/")
def root():
    return FileResponse("frontend/index.html")

# Retrieval route
@app.post("/retrieve")
def retrieve_docs(request: QueryRequest):
    try:
        # Perform similarity search to retrieve relevant documents
        retrieved_docs = vector_store.similarity_search(request.query, k=request.top_k)

        # Return the retrieved documents
        return {
            "query": request.query,
            "retrieved_docs": [doc.page_content for doc in retrieved_docs],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Answer generation step
@app.post("/answer")
def generate_answer(request: QueryRequest):
    try:
        # Perform retrieval step
        retrieved_docs = vector_store.similarity_search(request.query, k=request.top_k)

        # If no relevant documents are found
        if not retrieved_docs:
            return {"answer": "Sorry, no relevant documents found. Please refine your query."}

        # Combine retrieved documents into a single string for the context
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # Create a prompt for the LLM (Google Gemini)
        prompt = f"""
        You are a medical assistant trained to answer questions based on the following context. 
        If you do not know the answer or if the context does not seem relevant, please respond with:
        "Sorry, I couldn't find relevant information. Please refine your query to be more related to medical topics."

        Question: {request.query}
        Context: {context}
        Answer:
        """

        # Generate the answer using the LLM (Google Gemini)
        response = llm.invoke(prompt)

        # Access the generated content
        answer_content = response.content.strip()

        return {"answer": answer_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))