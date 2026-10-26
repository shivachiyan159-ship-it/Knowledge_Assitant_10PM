import os
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.params import File
from backend.ingestion.document_ingestion import DocumentIngestion
from backend.logger import GLOBAL_LOGGER as log
from backend.utils.file_ops import FastAPIFileAdapter

load_dotenv()

FileUploadPath = os.getenv("File_Upload_Path")

app = FastAPI()


@app.get("/")
def getinfo():
    return "Welcome to FastAPI"


@app.post("/chat/ingestion")
def chat_ingestion(files: List[UploadFile] = File(...),
                   chunk_size=Form(1000),
                   chunk_overlap=Form(200)):
    try:
        log.info("document ingetion started")
        wrapped = [FastAPIFileAdapter(file) for file in files]

        docIngestion = DocumentIngestion()
        docIngestion.insertvectordb(
            wrapped, FileUploadPath, int(chunk_size), int(chunk_overlap))
        log.info("Document Ingestion Successfully completed")
        return {"response": "Document ingestion completed successfully"}

    except Exception as e:
        log.error("Document ingestio failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")
