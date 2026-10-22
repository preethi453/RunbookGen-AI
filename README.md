
# RunbookGen AI

## AI-Based Intelligent IT Troubleshooting Runbook Generator

RunbookGen AI is an AI-powered web application that automatically generates structured IT troubleshooting runbooks from user-provided issue descriptions. It uses Retrieval-Augmented Generation (RAG), FAISS, Sentence Transformers, and Large Language Models (LLMs) through Ollama to generate context-aware, step-by-step troubleshooting guides.

## Features

- AI-powered runbook generation
- Retrieval-Augmented Generation (RAG)
- Semantic document retrieval using FAISS
- Ollama LLM integration
- User authentication (Login & Signup)
- Forgot Password module
- Runbook history management
- Export generated runbooks as TXT
- Responsive web interface

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Flask

### Database
- SQLite
- SQLAlchemy

### AI Technologies
- Ollama
- Retrieval-Augmented Generation (RAG)
- Sentence Transformers
- FAISS

## Project Structure

```text
RunbookGen-AI/
│
├── app.py
├── generator.py
├── retriever.py
├── models.py
├── requirements.txt
├── runbooks.db
├── README.md
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── forgot.html
│   ├── result.html
│   └── history.html
│
├── static/
├── docs/
└── reports/
    └── RunbookGen_AI_Report.pdf
```

## Workflow

1. The user logs into the application.
2. The user enters an IT issue description.
3. The query is converted into an embedding.
4. FAISS retrieves relevant documentation.
5. The retrieved context is passed to Ollama.
6. Ollama generates a structured troubleshooting runbook.
7. The generated runbook is displayed to the user.
8. The runbook is stored in SQLite history.
9. The user can export the runbook as a text file.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/RunbookGen-AI.git
cd RunbookGen-AI
```

Replace `your-username` with your GitHub username.

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

Download Ollama from:

https://ollama.com

Pull the required language model:

```bash
ollama pull llama3
```

Ensure the model name matches your application configuration.

### 5. Run the Application

```bash
python app.py
```

Open the application in your browser:

http://127.0.0.1:5000

## Core Modules

### `app.py`
- Flask application and routing
- User authentication
- Database operations
- Runbook generation workflow

### `retriever.py`
- Converts queries into embeddings
- Retrieves relevant documents using FAISS

### `generator.py`
- Integrates with Ollama
- Uses retrieved context to generate troubleshooting runbooks

### `models.py`
- Defines database models
- Manages user data and runbook history

## Technologies Used

- Python
- Flask
- HTML5, CSS3, JavaScript
- SQLite and SQLAlchemy
- Ollama
- FAISS
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

## Project Domain

- Artificial Intelligence (AI)
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Retrieval-Augmented Generation (RAG)
- Semantic Search and Document Retrieval
- IT Troubleshooting and Knowledge Management

## Future Enhancements

- PDF and DOCX export
- Cloud database integration
- Enhanced user access control
- Voice-based issue input
- Multilingual support
- Advanced analytics dashboard
- Improved command validation and rollback guidance

## Project Report

The complete project report provides details about the objectives, system architecture, implementation, technologies, workflow, and future enhancements.

**[View / Download RunbookGen AI Project Report (PDF)](https://drive.google.com/file/d/1J7YIxJHFr6PtYYBFdZf5JNf5ETzeeK4C/view?usp=drivesdk)**

## License

This project is developed for educational and academic purposes.

---

**Project Title:** RunbookGen AI – AI-Based Intelligent IT Troubleshooting Runbook Generator
