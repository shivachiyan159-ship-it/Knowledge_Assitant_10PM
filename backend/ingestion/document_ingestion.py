from backend.utils.config_loader import load_config
from backend.utils.model_loader import ModelLoader
from backend.utils.file_ops import save_upload_files, load_documents
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.exception.custom_exception import CustomException
from backend.logger import GLOBAL_LOGGER as log
from langchain_qdrant import QdrantVectorStore
import sys


class DocumentIngestion:
    # attributes
    # methods
    # special method (constructor)
    def __init__(self):
        self.model_loader = ModelLoader()
        self.config = load_config()

    def _splitchunks(self, docs, chunksize=1000, chunkoverlap=200):
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunksize=chunksize,
                chunkoverlap=chunkoverlap,
                splitters=["\n\n", "\n", " "]
            )
            chunks = splitter.split_documents(docs)
            log.info("Document split completed")
            return chunks
        except Exception as e:
            log.error("failed chunking")
            raise CustomException("error converting chunks", sys)

    def _storevectordb(self, chunks):
        try:
            embed_model = self.model_loader.load_embedding()

            vectorstore = QdrantVectorStore.from_documents(
                documents=chunks,
                embedding=embed_model,
                path="qdranttdb",
                collection_name="knowledge_assitant"
            )
            log.info("successfully insetted chunks into vectordb")
            return vectorstore

        except Exception as e:
            log.error("failed storing vectordb", error=str(e))
            raise CustomException("failed storing vectordb", sys)

    def insertvectordb(self, uploadfiles, targetpath, chunksize, chunkoverlap):
        try:
            # load documents or read documents
            paths = save_upload_files(uploadfiles, targetpath)
            docs = load_documents(paths)

            # split chunks
            chunks = self._splitchunks(docs, chunksize, chunkoverlap)

            # convert chunks into embedinggs and store into vectordb
            self._storevectordb(chunks)

        except Exception as e:
            log.error("failed storing vectordb", error=str(e))
            raise CustomException("Error storing vectordb")


