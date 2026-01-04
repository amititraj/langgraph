import gradio as gr
from typing import Dict
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

            var text = 'Welcome to Blog creation';
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

    with gr.Blocks(theme=gr.themes.Citrus(), title="Blog writer", css=css, js=js) as demo:        

        session_state = gr.State()
        #     {                
        #         "blog": ''
        #     }
        # )
        
        with gr.Row():
            with gr.Column():
                topic = gr.Textbox(label="Provide the topic to generate Blog")

        with gr.Row():
            with gr.Column():
                blog = gr.Textbox(label="Generated Blog", lines=18, max_lines=18, interactive=False) 

        with gr.Row():
            with gr.Column():
                submit_btn = gr.Button("Submit 🚀")               

                def generate_blog(topic:str,state: Dict):
                    try:
                        workflow = AgentWorkflow()
                        result = workflow.build_pipeline(topic)
                        return result["blog"],state
                    except Exception as e:
                        return f"❌ Error: {str(e)}"

                submit_btn.click(fn=generate_blog, inputs=[topic,session_state], outputs=[blog, session_state])

    demo.launch()
                


if __name__ == "__main__":
    main()