from pathlib import Path
import sys
from typing import Iterable, List
from backend.logger import GLOBAL_LOGGER as log
from backend.exception.custom_exception import CustomException
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from fastapi import UploadFile
import re
import uuid


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def save_upload_files(uploadfiles: Iterable, targetdir: Path):
    try:
        # convert string to Path
        targetdir = Path(targetdir)
        targetdir.mkdir(exist_ok=True)
        saved: List[Path] = []

        for uf in uploadfiles:
            name = getattr(uf, "name", "file1.pdf")
            ext = Path(name).suffix.lower()
            if ext not in SUPPORTED_EXTENSIONS:
                log.warning("unsupported file", filename=name)
                continue
            # pythontutrial_text.pdf
            safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_',
                               Path(name).stem).lower()
            filename = f"{safe_name}_{uuid.uuid4().hex[:6]}{ext}"

            out = targetdir/filename

            with open(out, "wb") as f:
                if hasattr(uf, "read"):
                    f.write(uf.read())
                else:
                    f.write(uf.getbuffer())

            saved.append(out)
            return saved

    except Exception as e:
        log.error("failed to save upload files",
                  error=str(e), dir=str(targetdir))
        raise CustomException("failed to save uplaod files", sys)


def load_documents(paths: Iterable[Path]):
    docs: List[any] = []
    for p in paths:
        ext = p.suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(str(p))
        elif ext == ".docx":
            loader = Docx2txtLoader(str(p))
        elif ext == ".txt":
            loader = TextLoader(str(p))
        else:
            log.warning("unsupported extension", path=str(p))

        docs.extend(loader.load())
    log.info("Document successfully loaded", count=len(docs))
    return docs


class FastAPIFileAdapter:
    def __init__(self, uf: UploadFile):
        self.uf = uf
        self.name = uf.filename

    def getbuffer(self):
        self.uf.file.seek(0)
        return self.uf.file.read()
