from backend.utils.config_loader import load_config
from backend.logger import GLOBAL_LOGGER as log
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from backend.exception.custom_exception import CustomException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import sys
import os


class ModelLoader:
    def __init__(self):
        load_dotenv()
        log.info("loading config")
        self.config = load_config()
        log.info(self.config)

    def load_embedding(self):
        try:
            embed_model_name = self.config["embedding_model"]["model_name"]
            log.info("loaded embedding model", model=embed_model_name)
            return HuggingFaceEmbeddings(model_name=embed_model_name)
        except Exception as e:
            log.error("Error loading embedding model", error=str(e))
            raise CustomException("failed to laod embedding model", sys)

    def load_llm(self):
        try:
            llm_block = self.config["llm"]
            provider_key = os.getenv("LLM_PROVIDER", "groq")

            if provider_key not in llm_block:
                log.error("LLM provider not found in config",
                          provider=provider_key)
                return ValueError(f"LLM provider {provider_key} not found in config")

            llm_config = llm_block[provider_key]
            model_name = llm_config.get("model_name")
            temprature = llm_config.get("temprature")
            max_output_tokens = llm_config.get("max_output_tokens")
            provider = llm_config.get("provider")

            log.info("cretaing llm object",
                     provider=provider_key, model_name=model_name)

            if provider == "google":
                return ChatGoogleGenerativeAI(model=model_name, temperature=temprature, max_output_tokens=max_output_tokens)
            elif provider == "groq":
                return ChatGroq(model=model_name, temperature=temprature, max_tokens=max_output_tokens)
            else:
                return ChatOpenAI(model=model_name, temperature=temprature, max_output_tokens=max_output_tokens)

        except Exception as e:
            log.error("error loading llm", error=str(e))
            raise ValueError("error loading llm")


loader = ModelLoader()

# test emebedding
# embeddings = loader.load_embedding()
# embed_result = embeddings.embed_query("hi how are yoy")
# print(embed_result)


# test llm
llm = loader.load_llm()
llm_result = llm.invoke("what is the latest news today")
print(f"LLM result: {llm_result.content}")
