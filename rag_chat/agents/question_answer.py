from utilities.logging import logger
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_classic.retrievers import EnsembleRetriever
from config.settings import settings
from langchain_core.documents import Document
from typing import List

class AnswerCreator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.BASE_MODEL,            
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL 
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Generate a proper answer in string format for the provided question in 2 t0 3 lines based on the context provided.
            Be precise and include important points only.The answer should not exceed 3 lines. If you are unable to answer  
            the question return the answer as I can't answer this question as it is not related to the document provided.
            question:
            {question}   
            context:
            {context}         
            """
        )

    def generateanswer(self, question: str, retriever:EnsembleRetriever) -> str:
        """Generate an answer for the question."""            
        try:
            documents = retriever.invoke(question)  
            if len(documents) > 0: 
                context = "\n\n".join([doc.page_content for doc in documents])
                chain = self.prompt | self.llm | StrOutputParser()
                answer = chain.invoke({                
                    "question": question,
                    "context":context
                })  
                if len(answer.strip())>0:
                    return {"answer":answer, "context":context}
                else:
                    return {"answer":"I can't answer this question as it is not related to the document provided.","context":""}         
            else:
                return {"answer":"I can't answer this question as it is not related to the document provided.","context":""}
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise
        
        