from fastapi import APIRouter, HTTPException, File, UploadFile # type: ignore
from app.services.pdf_parser import extract_text_from_pdf
from app.services.question_parser import parse_questions_string
from app.services.openai_service import generate_questions_from_text
from app.services.encryption import decrypt_answer
from app.models import DecryptQuizRequest
from app.services.question import encrypt_question_answer
# from app.services.count_tokens import count_tokens

router = APIRouter()

MAX_FILE_SIZE_KB = 500
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_KB * 1024
MAX_ALLOWED_PAGES = 3

@router.post("/generate")
async def upload_pdf(file: UploadFile = File(...)):
    try:        
        if file.content_type != "application/pdf":            
            raise HTTPException(status_code=400, detail= "Invalid file type. Only PDF allowed.")
        
        pdf_bytes = await file.read()

        if len(pdf_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large. Maximum size allowed is 500KB.")
        
        text, num_pages = extract_text_from_pdf(pdf_bytes)
        
        if not text:                        
            raise HTTPException(status_code=400, detail="PDF is empty.")
        if num_pages > MAX_ALLOWED_PAGES:            
            raise HTTPException(status_code=400, detail="Only single-page PDFs are allowed.")

        questions = generate_questions_from_text(text) 

        title = file.filename.split(".")[0]

        if not questions:
            raise HTTPException(status_code=400, detail="No questions generated.")

        return {
            "title": title,
            "questions": parse_questions_string(questions) 
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Error generating questions.")
    
@router.post("/decrypt")
async def decrypt_quiz(request: DecryptQuizRequest):
    try:
        decrypted_questions = [
            question.copy(update={"answer": [decrypt_answer(ans) for ans in question.answer]})
            for question in request.data
        ]
        return decrypted_questions
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")