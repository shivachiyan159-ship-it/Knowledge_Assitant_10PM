import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from backend.ingestion.document_ingestion import DocumentIngestion
from backend.logger import GLOBAL_LOGGER as log
from backend.retrieval.retrieval import ConversationalRAG
from backend.utils.file_ops import FastAPIFileAdapter

load_dotenv()

FileUploadPath = os.getenv("File_Upload_Path")

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# C:\Users\Admin\OneDrive\Desktop\Knowledge_Assitant_10PM

# C:\Users\Admin\OneDrive\Desktop\Knowledge_Assitant_10PM\fronend
UI_DIR = BASE_DIR/"frontend"

app.mount(
    "/static",
    StaticFiles(directory=UI_DIR/"static"),
    name="static"
)


@app.get("/")
def getinfo():
    return FileResponse(UI_DIR/"index.html")


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
        return {"Response": "Document ingestion completed successfully"}

    except Exception as e:
        log.error("Document ingestio failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")


@app.post("/chat/query")
def ChatQuery(question=Form(...)):
    try:
        log.info("calling chatquery method")
        cr = ConversationalRAG()
        # fetching history from database
        chat_history = ""

        answer = cr.chat(question, chat_history)
        # insert chat history into database
        log.info("completed chat method calling")
        log.info("get the response successfully")
        return {
            "answer": answer
        }

    except Exception as e:
        log.error(f"chat query failed: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"chat query failed: {str(e)}")
