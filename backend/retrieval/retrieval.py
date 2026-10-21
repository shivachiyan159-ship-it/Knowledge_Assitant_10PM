from operator import itemgetter

from backend.utils.model_loader import ModelLoader
from backend.utils.config_loader import load_config
from backend.logger import GLOBAL_LOGGER as log
from backend.exception.custom_exception import CustomException
from langchain_qdrant import QdrantVectorStore
from langchain_core.output_parsers import StrOutputParser
from backend.prompts.prompt import PROMPT_REGISTRY
import sys


class ConversationalRAG:
    def __init__(self):
        try:
            # build retrieval
            self.embed_model = ModelLoader().load_embedding()
            self.config = load_config()
            self.llm = self.__load_llm()
            self.retriever = self.__load_qdrant_retriever()
            log.info("retriever created successfully")

            # build prompt
            log.info("building lcel chain")
            self.chain = None
            if self.retriever is not None:
                pass

        except Exception as e:
            pass

    def __load_qdrant_retriever(self):
        try:
            vectorstore = QdrantVectorStore.from_existing_collection(
                embedding=self.embed_model,
                path="qdranttdb",
                collection_name="knowledge_assitant"
            )

            topk = self.config["retriever"]["top_k"]
            retriever = vectorstore.as_retriever(search_kwargs={"k": topk})
            return retriever
        except Exception as e:
            log.error("retriever created failed", error=str(e))
            raise CustomException("retriever created failed", sys)

    def __load_llm(self):
        llm = ModelLoader().load_llm()
        if not llm:
            raise ValueError("LLM could not be found")
        log.info("LLM loaded successfully")
        return llm

    def __format_docs(self, docs):
        context = " ".join([doc.page_content for doc in docs])
        return context

    def __build_lcel_chain(self):
        try:
            # 1. rewrite user question with chathistory context
            question_rewriter = context_question_prompt = PROMPT_REGISTRY["contextualize_question"]
            (
                {"input": itemgetter(
                    "input"), "chat_history": itemgetter("chat_history")}
                | context_question_prompt
                | self.llm
                | StrOutputParser()
            )

            # newquestion=question_rewriter.invoke({"input":input,"chat_history":chathistpry})
            # chunks=self.retriever.invoke(newquestion)
            # retriuveddocs=self.__format_docs(chunks)

            retreveddocs = question_rewriter | self.retriever | self.__format_docs

            log.info("similarty chunk result", context=retreveddocs)

            # 2.Answer using retrieved context + qiuestion rewriter
            context_qa_prompt = PROMPT_REGISTRY["context_qa"]

            self.chain = (
                {"context": retreveddocs, "input": itemgetter("input")}
                | context_qa_prompt
                | self.llm
                | StrOutputParser()
            )

            log.info("LCEL graph build successfully")

        except Exception as e:
            log.error("failed to build LCEL cjain in ConverstaionalRAG", str(e))
            raise CustomException(
                "failed to build LCEL cjain in ConverstaionalRAG")

    def chat(self):
        pass
