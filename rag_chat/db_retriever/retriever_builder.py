from langchain_community.vectorstores import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever

from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.document import Document
from config.settings import settings
from utilities.logging import logger
from classes.file_details import CustomFile
 


class CustomHybridRetriever:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL,base_url=settings.BASE_URL,api_key=settings.API_KEY)

    def build(self,fileobj:CustomFile):
        try:
            bm25retriever = BM25Retriever.from_documents(fileobj.chunks)
            logger.info("BM25 retriever created successfully.")

            vectorstore = Chroma(
                                persist_directory=settings.CHROMA_DB_PATH,
                                embedding_function=self.embeddings,
                                collection_name=settings.CHROMA_COLLECTION_NAME
                                )
            logger.info("Vector store created successfully.")

            # Get all document IDs and metadata
            existing_docs = vectorstore.get()

            # Extract metadata (if available)
            existing_hashes = [
                metadata.get("file_hash")
                for metadata in existing_docs["metadatas"]
                if metadata and "file_hash" in metadata
            ]           
            
            # Check if your hash is present
            target_hash = fileobj.hash
            if target_hash in existing_hashes:
                print("✅ File hash already exists in vectorstore.")
            else:
                print("❌ File hash not found. Safe to add.")
                # Wrap each chunk with metadata
                for i, doc in enumerate(fileobj.chunks):
                    doc.metadata.update({
                        "file_name": fileobj.name,
                        "chunk_index": i,
                        "file_hash": fileobj.hash
                    })
                vectorstore.add_documents(fileobj.chunks)
                vectorstore.persist()         

            vectorretriever = vectorstore.as_retriever(search_kwargs={"k": settings.VECTOR_SEARCH_K})
            logger.info("Vector retriever created successfully.")
            
            # Combine retrievers into a hybrid retriever
            hybridretriever = EnsembleRetriever(
                retrievers=[bm25retriever, vectorretriever],
                weights=settings.HYBRID_RETRIEVER_WEIGHTS
            )
            logger.info("Hybrid retriever created successfully.")
            return hybridretriever
        except Exception as e:
            logger.error(f"Failed to build hybrid retriever: {e}")
            raise
        


