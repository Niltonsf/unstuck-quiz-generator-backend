from fastapi import APIRouter, HTTPException
from app.models import CreateQuizRequest, DecryptQuizRequest
from app.services.encryption import decrypt_answer
from app.services.question import encrypt_question_answer
from app.services.firebase_service import find_document, update_document

router = APIRouter()

@router.post("/create")
async def create_quiz(data: CreateQuizRequest):
    try:
        print(data.quizId, data.data)
        update_document('quizzes', data.quizId, {'questions': data.data})
        
        return
        quiz = find_document('quizzes', data.quizId)
       
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found.")
        
        questions = quiz.get("questions", [])
                
        if not isinstance(questions, list):
            raise HTTPException(status_code=400, detail="Invalid questions format.")
        
        return encrypt_question_answer(questions)
    except Exception:
        raise HTTPException(status_code=400, detail="Error creating quiz.")

@router.post("/decrypt")
async def decrypt_quiz(request: DecryptQuizRequest):
    try:
        decrypted_questions = [
            question.copy(update={"answers": [decrypt_answer(ans) for ans in question.answers]})
            for question in request.data
        ]

        return decrypted_questions
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error.")