from typing import List,TypedDict,Literal
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from langgraph.graph import StateGraph, START, END
from utilities.logging import logger
from agents.document_summary import DocumentSumary
from agents.document_summary_relevance import SummaryRelevance
from agents.question_answer import AnswerCreator
from agents.question_answer_relevance import AnswerRelevance

class AgentState(TypedDict):
    user_question: str
    generate_summary:bool
    user_document: str   
    document_summary:str
    question_document:str
    question_answer: str
    confidence_score: str
    is_valid: bool
    retriever: EnsembleRetriever

class AgentWorkflow:
    def __init__(self):                
        self.document_summary = DocumentSumary()
        self.validate_summary = SummaryRelevance()
        self.answer_creator = AnswerCreator()
        self.validate_answer = AnswerRelevance()
        self.compiled_workflow = self.build_flow()


    def _generate_document_summary(self, state: AgentState)->str:
        summary = self.document_summary.generate(state["user_document"]) if state["generate_summary"] else ""
        return {
            "document_summary": summary            
        } 

    def _generate_answer(self, state: AgentState)->str:
        result = self.answer_creator.generateanswer(state["user_question"],state["retriever"])
        
        answer = result.get("answer")
        content = result.get("context")
        return {
            "question_answer": answer,
            "question_document": content           
        }   

    def _validate_document_summary(self, state: AgentState):
        summary = state["document_summary"]
        if len(summary.strip())>0:
            result = self.validate_summary.validate_summary(state["document_summary"],state["user_document"]) 
            values = result.split(',')  
            status = values[0]     
            score = f"Document Summary:{values[1]}"
            if status == "Valid":
                return {"status":True,"con_score":values[1],"confidence_score":score}
            else:
                return {"status":False,"con_score":values[1]}
        else:
            return {"status":True,"con_score":"75"}
        
    def _validate_question_answer(self, state: AgentState):
        answer = state["question_answer"]
        content = state["question_document"]
        if answer == "I can't answer this question as it is not related to the document provided.":
            return {"status":True,"con_score":"75"}
        else:
            result = self.validate_answer.validate_answer(state["user_question"],state["question_answer"],state["question_document"]) 
            values = result.split(',')  
            status = values[0]     
            score = state["confidence_score"] + "\n" + f"Answer to Question:{values[1]}"
            if status == "Valid":
                return {"status":True,"con_score":values[1],"confidence_score":score}
            else:
                return {"status":False,"con_score":values[1]}
        
        
    def edge_status(self,output):
        print(f"Output:{output.get("status")}")
        if output.get("status") is True:      
            if int(output.get("con_score"))>70:      
                return "valid"
            else:
                return "invalid"
        else:            
            return "invalid" 
    
    def build_flow(self):
        """Create and compile the workflow."""
        graph = StateGraph(AgentState)
        
        # Add nodes        
        graph.add_node("document_summary", self._generate_document_summary)   
        graph.add_node("validate_summary",self._validate_document_summary)     
        graph.add_node("question_answer",self._generate_answer)  
        graph.add_node("validate_answer",self._validate_question_answer)      
        
        # Define edges                     
        graph.add_edge("document_summary", "validate_summary")          
        graph.add_conditional_edges("validate_summary",
                self.edge_status,
                {
                    "valid": "question_answer",
                    "invalid": "document_summary"
                })
        graph.add_edge("question_answer", "validate_answer")
        graph.add_conditional_edges("validate_answer",
                self.edge_status,
                {
                    "valid": END,
                    "invalid": "question_answer"
                })

        # Define entry point
        graph.set_entry_point("document_summary")              
        
        return graph.compile()
    
    def build_pipeline(self, user_question: str, generate_summary:bool, user_document:str, retriever: EnsembleRetriever):
        try:
            print(f"Starting pipeline")
            #documents = retriever.invoke(user_question)
            #logger.info(f"Retrieved {len(documents)} relevant documents from retriever.")

            initial_state = AgentState(
                user_question=user_question,
                generate_summary=generate_summary,
                user_document=user_document,                
                document_summary="",
                question_document = "",
                question_answer="",
                confidence_score="",
                is_valid=False,
                retriever=retriever
                )
            print(f"Graph:{self.compiled_workflow.get_graph()}")
            #print(self.compiled_workflow)
            final_state = self.compiled_workflow.invoke(initial_state)
            
            return {
                "document_summary": final_state["document_summary"],
                "question_answer": final_state["question_answer"],
                "confidence_score":final_state["confidence_score"],
            }
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            raise