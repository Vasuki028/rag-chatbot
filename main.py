import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from pdf_processor import process_pdf
from embeddings import store_chunks, search_similar_chunks
from groq_client import get_answer_streaming

load_dotenv()

app = FastAPI(title="RAG Chatbot", description="Chat with your PDF using Groq + ChromaDB")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Folder to temporarily store uploaded PDFs
UPLOAD_DIR = "uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Track if a PDF has been uploaded and processed
pdf_processed = {"status": False, "filename": ""}


# ─── Request Models ────────────────────────────────────────────

class QuestionRequest(BaseModel):
    question: str


# ─── Routes ────────────────────────────────────────────────────

@app.get("/")
def serve_frontend():
    """Serve the frontend UI"""
    return FileResponse("frontend/index.html")


@app.get("/health")
def health_check():
    """Check if the server is running"""
    return {"status": "running", "message": "RAG Chatbot is live! 🚀"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file → extract text → chunk it → embed it → store in ChromaDB
    """

    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed!")

    try:
        # Save uploaded PDF to disk
        pdf_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(pdf_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"PDF saved to: {pdf_path} ✅")

        # Process: extract text + chunk
        chunks = process_pdf(pdf_path)

        if not chunks:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF!")

        # Embed chunks and store in ChromaDB
        store_chunks(chunks)

        # Mark PDF as processed
        pdf_processed["status"] = True
        pdf_processed["filename"] = file.filename

        return {
            "message": f"PDF processed successfully! ✅",
            "filename": file.filename,
            "total_chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/chat")
async def chat(request: QuestionRequest):
    """
    Take a question → find relevant chunks → stream Groq's answer
    """

    # Make sure a PDF has been uploaded first
    if not pdf_processed["status"]:
        raise HTTPException(status_code=400, detail="Please upload a PDF first!")

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty!")

    try:
        # Find most relevant chunks from ChromaDB
        relevant_chunks = search_similar_chunks(query=request.question)

        if not relevant_chunks:
            raise HTTPException(status_code=404, detail="No relevant content found in PDF!")

        # Stream the answer from Groq
        return StreamingResponse(
            get_answer_streaming(request.question, relevant_chunks),
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting answer: {str(e)}")


@app.get("/status")
def get_status():
    """Check if a PDF has been uploaded and processed"""
    return {
        "pdf_uploaded": pdf_processed["status"],
        "filename": pdf_processed["filename"] if pdf_processed["status"] else None
    }