# 🧠 Unstuck Quiz Generator Backend

AI-powered backend that transforms the content of uploaded PDFs into quizzes.

## 🛠️ Features

- ✅ Upload a PDF file (max 200KB, 2 pages)
- ✅ Extracts text and generates 10 quiz questions via OpenAI
- ✅ Supports encrypted answers for validation
- ✅ Built with FastAPI and designed to scale

## 📦 Tech Stack

```json
  FastAPI
  Pydantic
  Langchain
  OpenAI
  PyPDF2
  Cryptography
```

## 🚀 Getting Started

1. Clone the repository  
   ```bash
   git clone https://github.com/Niltonsf/unstuck-quiz-generator-backend
   cd unstuck-quiz-generator-backend
   ```

2. Create and activate a virtual environment  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

4. Add your `.env` file with the following (or follow .env.example):  
   ```env
   OPENAI_API_KEY=
   PORT=
   SECRET_ENCRYPTION_KEY=
   ```

5. Run the server  
   ```bash
   uvicorn app.main:app --reload
   ```

## 🔍 API Overview

#### Questions
- **POST** `/questions/generate` — Upload a PDF and receive quiz questions  
- **POST** `/questions/decrypt` — Decrypt quiz answers for validation  

#### Quiz
- **POST** `/quiz/create` — Encrypt and create a quiz with questions  
- **POST** `/quiz/validate-answer` — Validate a user’s answer against the correct one  

## 📄 License

This project is licensed under the **Nilton Schumacher F Public License**, which means:

- You can use it.
- You can break it.
- You can improve it.
- If it explodes, it's your fault.
- If it works, it's probably accidental genius.

Made with ❤️ by [Nilton Schumacher F](https://www.linkedin.com/in/nilton-schumacher-filho/). Feel free to connect!
