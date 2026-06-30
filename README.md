# RunbookGen AI

## AI-Based Intelligent IT Troubleshooting Runbook Generator

RunbookGen AI is an AI-powered web application that automatically generates structured IT troubleshooting runbooks from user-provided issue descriptions. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant documentation and combines it with Large Language Models (LLMs) through Ollama to produce accurate, step-by-step troubleshooting guides.

---

## Features

- AI-powered runbook generation
- Retrieval-Augmented Generation (RAG)
- Semantic document retrieval using FAISS
- Ollama LLM integration
- User authentication (Login & Signup)
- Forgot Password module
- Runbook history management
- Export generated runbooks as TXT
- Responsive and modern web interface

---

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
- RAG (Retrieval-Augmented Generation)
- Sentence Transformers
- FAISS

---

## Project Structure

```
RunbookGen-AI/
│── app.py
│── generator.py
│── retriever.py
│── models.py
│── requirements.txt
│── runbooks.db
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
│
├── docs/
│
└── README.md
```

---

## Workflow

1. User logs into the application.
2. User enters an IT issue.
3. The query is converted into embeddings.
4. FAISS retrieves relevant documentation.
5. Ollama generates a structured troubleshooting runbook.
6. The generated runbook is displayed.
7. The runbook is stored in SQLite history.
8. Users can export the runbook as a text file.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/RunbookGen-AI.git
cd RunbookGen-AI
```

### Create Virtual Environment

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

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Ollama

Download and install Ollama from:

https://ollama.com

Pull a language model (example):

```bash
ollama pull llama3
```

### Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## Modules

### app.py
- Flask application
- Routing
- Authentication
- Database management
- Runbook generation

### retriever.py
- Converts queries into embeddings
- Retrieves relevant documents using FAISS

### generator.py
- Generates runbooks using Ollama
- Uses retrieved context for better accuracy

### models.py
- Database models
- User management
- Runbook history storage

---

## Technologies Used

- Python
- Flask
- HTML5
- CSS3
- JavaScript
- SQLite
- SQLAlchemy
- Ollama
- FAISS
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

---

## Project Domain

- Artificial Intelligence (AI)
- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Intelligent Document Retrieval
- Knowledge Management Systems

---

## Future Enhancements

- PDF and DOCX export
- Cloud database integration
- Multi-user authentication
- Voice-based issue input
- Multi-language support
- Advanced analytics dashboard

---


**Project Title:**  
**RunbookGen AI – AI-Based Intelligent IT Troubleshooting Runbook Generator**

---

## License

This project is developed for educational and academic purposes.
