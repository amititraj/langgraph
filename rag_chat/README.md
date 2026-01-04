# RAG Chat

RAG Chat is a small retrieval-augmented generation (RAG) application that demonstrates
how to build a question-answering/chat system backed by a local vector store and
document processing pipeline.

Demo: See the `demo` folder for a short video showing how the application works.

## Project layout

- `askrag.py`: Main entry script (example runner) to start a simple QA flow.
- `requirements.txt`: Python dependencies.
- `agents/`: High-level agent workflows and task orchestrators (question answering,
	document summarization, relevance workflows).
- `chroma_db/`: Local Chroma vector DB files (SQLite and data blobs). This folder
	contains the local database and should not be committed to source control.
- `classes/`: Small helper classes and domain models (e.g., `file_details.py`).
- `config/`: Configuration constants and settings used across the app.
- `db_retriever/`: Builder for the retrieval layer that talks to the vector store.
- `demo/`: Short demo video(s) and assets showing the application in action.
- `document_processor/`: Code that ingests and processes documents for indexing.
- `upload/`: (Local) file upload storage used by demo or local runs.
- `utilities/`: Logging and miscellaneous helper utilities.
- `log/`: Runtime logs (ignored by `.gitignore`).

## Quick start

1. Create and activate a virtual environment:

```bash
python -m venv .venv
.
# Windows
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add secrets/config to a local `.env` file as below.
EMBEDDING_MODEL = openai/text-embedding-3-small
BASE_MODEL = openai/gpt-4.1-mini
VERIFICATION_MODEL = openai/gpt-4o
BASE_URL = 
API_KEY = 

4. Run the example script:

```bash
python askrag.py
```



