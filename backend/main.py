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
from cachetools import TTLCache
import asyncio

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Retrieve API keys from environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API key is missing! Please check your .env file.")
if not GEMINI_API_KEY:
    raise ValueError("Google Gemini API key is missing! Please check your .env file.")

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to handle requests from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Pinecone setup
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medical-rag-chatbot"
index = pc.Index(index_name)

# Load embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# Set up the VectorStore
vector_store = PineconeVectorStore(embedding=embeddings, index=index)

# Initialize the Gemini API with temperature adjustment
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GEMINI_API_KEY, temperature=0.2)

# Define the state of the application
class State(TypedDict):
    question: str
    context: List[str]
    answer: str

# Define a Pydantic model for the query input
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# Cache for frequently asked questions
cache = TTLCache(maxsize=100, ttl=300)  # Cache for 5 minutes

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.post("/retrieve")
def retrieve_docs(request: QueryRequest):
    try:
        # Check cache for query
        if request.query in cache:
            logging.info("Cache hit for query.")
            return {"query": request.query, "retrieved_docs": cache[request.query]}

        # Perform similarity search
        retrieved_docs = vector_store.similarity_search(request.query, k=request.top_k)
        retrieved_contents = [doc.page_content for doc in retrieved_docs]

        # Cache results
        cache[request.query] = retrieved_contents

        return {"query": request.query, "retrieved_docs": retrieved_contents}

    except Exception as e:
        logging.error(f"Error during retrieval: {e}")
        raise HTTPException(status_code=500, detail="Error during document retrieval.")

@app.post("/answer")
def generate_answer(request: QueryRequest):
    try:
        # Perform retrieval
        retrieved_docs = vector_store.similarity_search(request.query, k=request.top_k)

        if not retrieved_docs:
            return {"answer": "Sorry, no relevant documents found. Please refine your query."}

        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        # Create a prompt for the LLM
        prompt = f"""
        You are a concise and accurate medical assistant. Based on the following context, provide a clear and precise answer. Avoid including any unnecessary formatting or symbols.

        Question: {request.query}
        Context: {context}
        Answer:
        """

        # Generate the answer
        response = llm.invoke(prompt)
        answer_content = response.content.strip()

        # Post-process answer to clean up formatting
        cleaned_answer = answer_content.replace("**", "")

        return {"answer": cleaned_answer}

    except Exception as e:
        logging.error(f"Error during answer generation: {e}")
        raise HTTPException(status_code=500, detail="Error during answer generation.")

@app.on_event("startup")
async def warm_up():
    logging.info("Warming up the application...")
    try:
        await asyncio.to_thread(vector_store.similarity_search, "test", k=1)
        logging.info("Warm-up complete.")
    except Exception as e:
        logging.error(f"Warm-up failed: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)