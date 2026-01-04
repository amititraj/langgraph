from utilities.logging import logger
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings
from langchain_core.documents import Document
from typing import List

class DocumentSumary:
    def __init__(self):
        
        self.llm = ChatOpenAI(
            model=settings.BASE_MODEL,            
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL 
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Generate a summary for the provided context in 10 t0 15 lines. Be precise and include important points only.
            The summary should not exceed 15 lines.
            Context:
            {context}            
            """
        )

    def generate(self, documents: str) -> str:
        """Generate a summary using the provided documents."""
        #context = "\n\n".join([doc.page_content for doc in documents])
        
        chain = self.prompt | self.llm | StrOutputParser()
        try:
            summary = chain.invoke({                
                "context": documents
            })            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
        
        return summary            