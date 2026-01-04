# Blog Writer

Blog Writer is an AI-powered application for generating high-quality, informative, and engaging blog content based on user-provided topics. It uses LangChain, OpenAI, and web search tools to create well-structured blog posts in Markdown format.

## Features
- **Automated Blog Generation:** Enter a topic and receive a complete blog post with title,  
   introduction, sections, lists, and conclusion.
- **Markdown Formatting:** Output is structured for easy publishing.
- **Customizable Workflow:** Modular agent-based design for extensibility.

## How It Works
- The main workflow (`AgentWorkflow`) orchestrates blog creation using a content agent (`Blog`).
- The content agent uses OpenAI's language model and web search to gather information and generate content.
- Configuration is managed via environment variables in `config/settings.py`.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with required API keys (OpenAI).
      MODEL = openai/gpt-4.1-mini
      BASE_URL = 
      OPENAI_API_KEY = 
      SERPER_API_KEY = 

## Usage
Run the application:
```cmd
python app.py
```
A Gradio interface will launch for interactive blog generation.

## Demo
The `demo/` folder contains a short walkthrough video demonstrating the application in action.




