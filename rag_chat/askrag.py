import gradio as gr
from config import constants
from typing import List, Dict
from utilities.logging import logger
from document_processor.document_handler import DocumentProcessor
from db_retriever.retriever_builder import CustomHybridRetriever
import os
import hashlib
from agents.workflow import AgentWorkflow

def main():    
    
    css = """
        .title {
            font-size: 1em !important; 
            text-align: center !important;
            color: #FFD700; 
        }

        .subtitle {
            font-size: 0.5em !important; 
            text-align: center !important;
            color: #FFD700; 
        }

        .text {
            text-align: center;
        }
        """

    js = """
        function createGradioAnimation() {
            var container = document.createElement('div');
            container.id = 'gradio-animation';
            container.style.fontSize = '2em';
            container.style.fontWeight = 'bold';
            container.style.textAlign = 'center';
            container.style.marginBottom = '20px';
            container.style.color = '#eba93f';

            var text = '💬📄🤖 Welcome to Ask RAG - chat with your document! 💬📄🤖';
            for (var i = 0; i < text.length; i++) {
                (function(i){
                    setTimeout(function(){
                        var letter = document.createElement('span');
                        letter.style.opacity = '0';
                        letter.style.transition = 'opacity 0.1s';
                        letter.innerText = text[i];

                        container.appendChild(letter);

                        setTimeout(function() {
                            letter.style.opacity = '0.9';
                        }, 50);
                    }, i * 250);
                })(i);
            }

            var gradioContainer = document.querySelector('.gradio-container');
            gradioContainer.insertBefore(container, gradioContainer.firstChild);

            return 'Animation created';
        }
        """

    with gr.Blocks(theme=gr.themes.Citrus(), title="Ask RAG 💬📄🤖", css=css, js=js) as demo:
        gr.Markdown("## Ask RAG created using Docling and LangGraph", elem_classes="subtitle")
        gr.Markdown("# How it works:", elem_classes="title")
        gr.Markdown("📤 Upload your document and get your questions answered along with document summary", elem_classes="text")
        gr.Markdown("⚠️ **Note:** Supported file types: '.pdf', '.docx', '.txt', '.md'", elem_classes="text")

        session_state = gr.State({            
            "retriever": None
        })

        with gr.Row():
            with gr.Column():
                uploaded_file = gr.Files(label="📄 Upload Documents", height=125, scale=1,file_count="single" , file_types=constants.SUPPORTED_FILE_TYPES)                          
                
        with gr.Row():
            with gr.Column():
                generate_summary = gr.Radio(["Yes", "No"], label="Generate document summary", value="No")
                document_summary = gr.Textbox(label="Document Summary", interactive=False, visible=False, lines=4)

                def process(choice):                    
                    return gr.update(visible=(choice == "Yes"))                    
                
                generate_summary.change(fn=process, inputs=[generate_summary], outputs=[document_summary])  
                        
        with gr.Row():
            with gr.Column():
                user_question = gr.Textbox(label="Ask your Question:", lines=2)  
                question_answer =  gr.Textbox(label="Answer:", lines=2, interactive=False, visible=False)  
                confidence_score = gr.Textbox(label="Confidence score in %:", lines=2, interactive=False, visible=False)  

        with gr.Row():
            with gr.Column():
                submit_btn = gr.Button("Submit 🚀")

                def process_question(uploaded_file, generate_summary, user_question, state: Dict):                    
                    try:
                        if not user_question.strip():
                            raise ValueError("Question cannot be empty")
                        if not uploaded_file:
                            raise ValueError("No documents uploaded")   
                        if(os.path.getsize(uploaded_file.name) > constants.MAXIMUM_FILE_SIZE):    
                            raise ValueError(f"Total size exceeds {constants.MAXIMUM_FILE_SIZE//1024//1024}MB limit")  
                        if not uploaded_file.name.endswith(('.pdf', '.docx', '.txt', '.md')):
                            raise ValueError("File type not supported.")   
                        
                        documentprocessor = DocumentProcessor()
                        fileobj = documentprocessor.process(uploaded_file)
                        customretriever = CustomHybridRetriever()
                        retriever = customretriever.build(fileobj)

                        document = "\n\n".join([doc.page_content for doc in fileobj.chunks])
                        #print(f"My document:{context}")
                        #document = fileobj.chunks
                        result = generate_summary == "Yes"

                        state.update({                        
                        "retriever": retriever
                        })                        

                        worklow = AgentWorkflow()
                        result = worklow.build_pipeline(user_question=user_question,generate_summary=result,user_document=document,retriever=state["retriever"])                        
                        return result["document_summary"], gr.update(visible=True,value=result["question_answer"]), gr.update(visible=True,value=result["confidence_score"]),state
                            
                    except Exception as e:
                        logger.error(f"Processing error: {str(e)}")
                        return f"❌ Error: {str(e)}", "" #, state
                
                submit_btn.click(fn=process_question, inputs=[uploaded_file, generate_summary, user_question,session_state], outputs=[document_summary, question_answer, confidence_score, session_state])
    
    demo.launch()


if __name__ == "__main__":
    main()