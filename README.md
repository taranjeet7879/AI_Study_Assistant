# 🤖 AI Study Assistant

An AI-powered study assistant built with **Flask** and the **Groq API**. The application allows students to upload PDF study material and use AI to generate summaries, exam questions, multiple-choice questions, revision notes, and answers based on the uploaded material.

## ✨ Features

### 📄 PDF Upload

Upload a PDF containing your study material.

The application:

* Extracts text from the PDF using PyPDF2
* Stores the extracted text in memory
* Splits the text into chunks
* Uses the chunks to provide relevant context when answering questions

### 📝 AI Study Summary

Generates a structured study summary containing:

1. Overview
2. Important Concepts
3. Key Definitions
4. Exam Notes

The summary is generated from the uploaded study material.

### ❓ Exam Questions

Generates **10 important university-level exam questions** based on the uploaded study material.

### 🧠 MCQ Generator

Generates **10 multiple-choice questions**.

Each question includes:

* A)
* B)
* C)
* D)
* Correct answer

### 📚 One-Day Revision Notes

Generates concise revision notes containing the most important concepts for quick revision.

### 💬 Ask Questions

Users can ask questions about the uploaded study material.

The application uses a simple keyword-based retrieval system to identify the most relevant text chunks before sending the context to the AI model.

If the requested information cannot be found in the selected study material, the AI is instructed to respond that the information is not present in the notes.

---

## 🛠️ Technologies Used

### Backend

* Python
* Flask
* Groq API

### AI

The application uses the following Groq model:

```text
openai/gpt-oss-120b
```

The model is called through the Groq Python SDK.

The application uses a temperature of `0.3` for AI responses.

### PDF Processing

* PyPDF2

PyPDF2 is used to extract text from uploaded PDF files.

### Environment Configuration

* python-dotenv

Environment variables are loaded from a `.env` file.

### Frontend

The frontend uses:

* HTML
* CSS
* JavaScript

---

## 📁 Project Structure

```text
AI_Study_Assistant/
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── .env
└── venv/
```

> `.env` and `venv/` should not be uploaded to GitHub.

---

## ⚙️ How It Works

The application follows this general workflow:

```text
             ┌─────────────────┐
             │   Upload PDF    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Extract PDF Text│
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Create Chunks   │
             └────────┬────────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
      Summary      Questions     MCQs
          │           │           │
          └───────────┼───────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   Groq LLM      │
             │ gpt-oss-120b    │
             └─────────────────┘
```

For questions asked about the uploaded material:

```text
User Question
      │
      ▼
Keyword Matching
      │
      ▼
Top Relevant Chunks
      │
      ▼
Study Material + Question
      │
      ▼
Groq AI Model
      │
      ▼
Answer
```

---

## 🔍 Question Retrieval

The application does not use a vector database or embedding model.

Instead, it uses a simple keyword-based retrieval approach.

The question and each document chunk are converted into sets of words. The application calculates the number of matching words and selects the top three most relevant chunks.

This provides contextual information to the AI model before generating the answer.

---

## 🤖 AI Configuration

The AI client is initialized using the Groq API:

```python
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
```

The application expects the following environment variable:

```text
GROQ_API_KEY
```

The AI model currently configured in the application is:

```text
openai/gpt-oss-120b
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory of the project:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

### ⚠️ Security

**Never upload your `.env` file to GitHub.**

Your `.gitignore` should contain:

```gitignore
venv/
.env
__pycache__/
*.pyc
.vscode/
.idea/
```

Never put API keys directly inside `app.py`.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AI_Study_Assistant.git
```

Replace `YOUR-USERNAME` with your GitHub username.

Then enter the project directory:

```bash
cd AI_Study_Assistant
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

macOS/Linux:

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

The required packages are:

```text
Flask
groq
python-dotenv
PyPDF2
```

### 5. Configure the API key

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 6. Start the application

```bash
python app.py
```

The Flask development server runs on:

```text
http://127.0.0.1:5000/
```

Open the address in your browser.

---

## 📌 API Routes

The Flask application currently provides the following routes:

| Route        | Method | Purpose                                         |
| ------------ | ------ | ----------------------------------------------- |
| `/`          | GET    | Displays the main application                   |
| `/upload`    | POST   | Uploads and processes a PDF                     |
| `/summary`   | POST   | Generates a study summary                       |
| `/questions` | POST   | Generates 10 exam questions                     |
| `/mcqs`      | POST   | Generates 10 MCQs                               |
| `/revision`  | POST   | Generates one-day revision notes                |
| `/ask`       | POST   | Answers questions using relevant study material |

---

## 💾 Data Storage

The current application uses **in-memory storage**.

Uploaded document data is stored in a Python dictionary:

```python
document_data = {
    "raw_text": "",
    "chunks": [],
    "summary": None
}
```

This means:

* Data is stored only while the application is running.
* There is currently no database.
* Uploaded documents are not permanently stored.
* Restarting the application clears the uploaded document and generated summary.

---

## ⚠️ Current Limitations

The current version has some limitations:

* PDF content is stored only in memory.
* There is no user authentication.
* There is no database.
* Uploaded documents are not permanently saved.
* The retrieval system uses keyword matching rather than embeddings/vector search.
* Only selected portions of the document are sent to the AI for some operations.
* The application is currently configured to use Flask's development server.
* The application does not currently provide persistent chat history.
* The application depends on the Groq API for AI-generated responses.

---

## 🔮 Possible Future Improvements

Future versions could include:

* 🔐 User authentication
* 💾 Database support
* 📖 Multiple PDF/document support
* 🧠 Vector embeddings and semantic search
* 🔎 Vector database integration
* 💬 Persistent chat history
* 📊 Student progress tracking
* 📝 Interactive quizzes
* 🎯 Personalized study plans
* 🗂️ Document management
* 📱 Improved mobile interface
* ☁️ Production deployment
* ⚡ Streaming AI responses

---

## 👨‍💻 Author

**Your Name**

GitHub: `https://github.com/YOUR-USERNAME`

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.
