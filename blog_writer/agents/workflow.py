from langgraph.graph import StateGraph, START, END
from typing import Literal,TypedDict
from agents.blog_content_agent import Blog
from IPython.display import Image, display

class AgentState(TypedDict):
    topic:str
    blog:str

class AgentWorkflow:
    def __init__(self):
        self.compiled_workflow = self.build_flow()
        self.blog_content = Blog()

    def _generate_content(self, state: AgentState)->str: 
        content = self.blog_content.generate(state["topic"])
        return {"blog":content}    

    def build_flow(self):
        """Create and compile the workflow."""
        graph = StateGraph(AgentState)

        graph.add_node("content_creation", self._generate_content)           
        
        graph.add_edge("content_creation", END)

        graph.set_entry_point("content_creation")

        graph1 = graph.compile()
        print(display(Image((graph1.get_graph(xray=True)).draw_mermaid_png())))
        
        return graph.compile()
    
    def build_pipeline(self, topic: str):
        try:
            print("starting the pipeline")

            initial_state = AgentState(
                topic=topic,
                blog=''
            )

            final_state = self.compiled_workflow.invoke(initial_state)
            print("ending pipeline")
            return {
                "blog": final_state["blog"]
            }            
        except Exception as e:
            return f"❌ Error: {str(e)}"

