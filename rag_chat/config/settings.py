from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Database settings
    CHROMA_DB_PATH: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "rag_documents"

    # Retrieval settings
    VECTOR_SEARCH_K: int = 5
    HYBRID_RETRIEVER_WEIGHTS: list = [0.4, 0.6]

    BASE_MODEL :str
    VERIFICATION_MODEL : str
    BASE_URL : str
    API_KEY : str
    EMBEDDING_MODEL:str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()