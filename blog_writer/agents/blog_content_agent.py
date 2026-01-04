from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.google_serper import GoogleSerperResults
from config.settings import settings
import os

class Blog:
    def __init__(self):
        
        self.llm = ChatOpenAI(
            model=settings.MODEL,            
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.BASE_URL 
        )

        self.prompt = ChatPromptTemplate.from_template(
            """
            You are a blog writing assistant. Your task is to generate high-quality, informative, and 
            engaging blog content based on a topic provided by the user. Follow these instructions:

            Use Markdown formatting to structure the blog post. Include:
            A compelling title using a level-1 heading (#)
            An engaging introduction
            Several relevant sections with level-2 headings (##) that logically organize the content
            Use bullet points, numbered lists to enhance readability
            A conclusion that summarizes key points or offers a call to action
            Use web search tools to gather accurate, up-to-date, and relevant information about the topic. 
            You may use web search to gather current information about {topic}.
            Limit the search results to top 3.
            Incorporate insights, facts, or examples from reliable sources to enrich the content.
            Ensure the tone is clear, informative, and engaging, suitable for a general audience. 
            topic:
            {topic}            
            """
        )

    def generate(self, topic: str) -> str:
        # os.environ["SERPER_API_KEY"] = settings.SERPER_API_KEY
        # search_tool = GoogleSerperResults()
        # llm_tools = self.llm.bind_tools([search_tool])
        chain = self.prompt | self.llm | StrOutputParser()
        try:
            content = chain.invoke({                
                "topic": topic
            })                       
        except Exception as e:  
            print(f"Error:{e}")              
            raise e
        
        return content  