from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .chat import router as chat_router
from .translate import router as translate_router

load_dotenv()

app = FastAPI(
    title="Integrated RAG Chatbot API",
    description="API for the Docusaurus RAG Chatbot, handling content ingestion and user queries.",
    version="1.0.0",
)

# Configure CORS middleware based on research.md
# Allow all origins for development, refine for production
origins = [
    "http://localhost",
    "http://localhost:3000", # Docusaurus frontend development server
    "http://localhost:3001", # Docusaurus frontend development server (alternate port)
    # Add your production Docusaurus domain here when deployed
    # os.getenv("FRONTEND_URL") # Example for dynamic origin from env
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router) # Include the chat router here
app.include_router(translate_router, prefix="/api", tags=["translation"]) # Translation API

@app.get("/")
async def root():
    return {"message": "Integrated RAG Chatbot API is running!"}

