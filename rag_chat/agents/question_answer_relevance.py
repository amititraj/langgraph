from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import settings
from utilities.logging import logger

class AnswerRelevance:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.VERIFICATION_MODEL,            
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL 
        )
        self.prompt = ChatPromptTemplate.from_template(
            """you need to validate the answer generated for the question in reference to the context provided. Your response 
            should be either Valid or Invalid. Also generate a confidence score for the answer generated
            between 0 to 100. Output should return Valid/Invalid and confidence score between 0 to 100 as comma separated.
            provide the output as comma separated with only the fields requested and don't include additional details.please 
            refer the format for output Valid,80.            
            question:{question}  
            answer:{answer}
            context:{context}        
            """
        )

    def validate_answer(self, question:str, answer:str, context: str):
        """validate the answer generated."""       
        
        chain = self.prompt | self.llm | StrOutputParser()
        try:
            result = chain.invoke({ 
                "question":question,
                "answer": answer,               
                "context": context
            })  
            return result           
        except Exception as e:
            logger.error(f"Error validating summary: {e}")
            raise        
        