from fastapi import APIRouter, HTTPException
from app.models import ValidateAnswerRequest, CreateQuizRequest, DecryptQuizRequest
from app.services.encryption import decrypt_answer
from app.services.question import encrypt_question_answer

router = APIRouter()

@router.post("/create")
async def create_quiz(data: CreateQuizRequest):
    try:
        return encrypt_question_answer(data.data)
    except Exception:
        raise HTTPException(status_code=400, detail="Error creating quiz.")

@router.post("/validate-answer")
async def validate_answer(request: ValidateAnswerRequest):
    try:
        decrypted_answers = [decrypt_answer(answer) for answer in request.question.answer]
        if not decrypted_answers:
            raise HTTPException(status_code=400, detail="No answers found.")
        
        is_correct = request.userAnswer in decrypted_answers

        return {
            "isCorrect": is_correct,
            "correctAnswers": decrypted_answers
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to validate answer.")
