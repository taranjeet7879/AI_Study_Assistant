from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import PyPDF2
import re

# -------------------------
# CONFIG
# -------------------------

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = Flask(__name__)

# -------------------------
# IN-MEMORY STORAGE
# -------------------------

document_data = {
    "raw_text": "",
    "chunks": [],
    "summary": None
}

# -------------------------
# HELPERS
# -------------------------

def extract_pdf_text(pdf_file):

    reader = PyPDF2.PdfReader(pdf_file)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def create_chunks(text, chunk_size=1500):

    words = text.split()

    chunks = []

    for i in range(0, len(words), chunk_size):

        chunk = " ".join(words[i:i + chunk_size])

        chunks.append(chunk)

    return chunks


def call_llm(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI Study Assistant. "
                    "Provide clear, educational answers."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def keyword_score(question, chunk):

    q_words = set(
        re.findall(r"\w+", question.lower())
    )

    c_words = set(
        re.findall(r"\w+", chunk.lower())
    )

    return len(q_words.intersection(c_words))


def get_relevant_chunks(question, top_k=3):

    scored = []

    for chunk in document_data["chunks"]:

        score = keyword_score(
            question,
            chunk
        )

        scored.append((score, chunk))

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [
        item[1]
        for item in scored[:top_k]
    ]

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# PDF UPLOAD
# -------------------------

@app.route("/upload", methods=["POST"])
def upload():

    try:

        pdf = request.files.get("pdf")

        if not pdf:

            return jsonify({
                "success": False,
                "message": "No PDF uploaded"
            })

        text = extract_pdf_text(pdf)

        if len(text.strip()) == 0:

            return jsonify({
                "success": False,
                "message": "Could not extract text"
            })

        document_data["raw_text"] = text

        document_data["chunks"] = create_chunks(
            text
        )

        document_data["summary"] = None

        return jsonify({
            "success": True,
            "message": "PDF uploaded successfully",
            "pages_processed":
                len(document_data["chunks"]),
            "characters":
                len(text)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        })

# -------------------------
# SUMMARY
# -------------------------

@app.route("/summary", methods=["POST"])
def summary():

    try:

        if not document_data["raw_text"]:

            return jsonify({
                "success": False,
                "result":
                "Upload a PDF first"
            })

        if document_data["summary"]:

            return jsonify({
                "success": True,
                "result":
                document_data["summary"]
            })

        text = document_data["raw_text"][:12000]

        prompt = f"""
        Create a structured study summary.

        Include:

        1. Overview
        2. Important Concepts
        3. Key Definitions
        4. Exam Notes

        Notes:

        {text}
        """

        result = call_llm(prompt)

        document_data["summary"] = result

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "result": str(e)
        })

# -------------------------
# QUESTIONS
# -------------------------

@app.route("/questions", methods=["POST"])
def questions():

    try:

        text = document_data["raw_text"][:10000]

        prompt = f"""
        Generate 10 important
        university-level exam questions.

        Notes:

        {text}
        """

        result = call_llm(prompt)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "result": str(e)
        })

# -------------------------
# MCQ
# -------------------------

@app.route("/mcqs", methods=["POST"])
def mcqs():

    try:

        text = document_data["raw_text"][:10000]

        prompt = f"""
        Generate 10 MCQs.

        Each MCQ should have:

        A)
        B)
        C)
        D)

        Also provide answer.

        Notes:

        {text}
        """

        result = call_llm(prompt)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "result": str(e)
        })

# -------------------------
# REVISION NOTES
# -------------------------

@app.route("/revision", methods=["POST"])
def revision():

    try:

        text = document_data["raw_text"][:10000]

        prompt = f"""
        Create one-day revision notes.

        Include only the most
        important concepts.

        Notes:

        {text}
        """

        result = call_llm(prompt)

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "result": str(e)
        })

# -------------------------
# ASK QUESTIONS
# -------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:

        question = request.json.get(
            "question",
            ""
        )

        if not question:

            return jsonify({
                "success": False,
                "answer":
                "Question missing"
            })

        chunks = get_relevant_chunks(
            question
        )

        context = "\n\n".join(chunks)

        prompt = f"""
        Answer ONLY from the
        provided study material.

        Study Material:

        {context}

        Question:

        {question}

        If the answer is not found,
        say:
        "This information is not
        present in the notes."
        """

        answer = call_llm(prompt)

        return jsonify({
            "success": True,
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "answer": str(e)
        })

# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )