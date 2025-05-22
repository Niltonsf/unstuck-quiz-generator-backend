# 🧠 Unstuck Quiz Generator Backend

AI-powered backend that transforms the content of uploaded PDFs into quizzes.

## 🛠️ Features

- ✅ Upload a PDF file (max 500KB, 3 pages)
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

## 🔐 Generating the SECRET_ENCRYPTION_KEY

The `SECRET_ENCRYPTION_KEY` used for encrypting quiz answers must be a valid Fernet key, which is a URL-safe base64-encoded 32-byte key.

To generate a new key, run the following Python snippet (copy this key to use in step 4 of getting started):

```python
from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()

print(key.decode())  # Copy this key and add it as SECRET_ENCRYPTION_KEY in your .env file
```

## 🔑 Getting Your OpenAI API Key

To use the AI features, you need an OpenAI API key. Follow these steps:

1. Go to [OpenAI's API platform](https://platform.openai.com/account/api-keys) and sign in or create an account.

2. Click on **Create new secret key**.

3. Copy the generated key (it starts with `sk-...`)

4. Use on step 4 of getting started

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
   PORT=8000
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
