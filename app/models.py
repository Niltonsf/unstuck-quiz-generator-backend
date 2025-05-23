from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    prompt: str

class Question(BaseModel):
    id: str
    question: str
    options: List[dict]
    answers: List[str]
    questionNumber: int

class QuestionExplainRequest(BaseModel):
    question: str
    user_response: str
    
class ValidateAnswerRequest(BaseModel):
    id: str
    questionId: str
    question: Question
    userAnswer: List[str]

class CreateQuizRequest(BaseModel):
    quizId: str
    data: List[Question]   

class DecryptQuizRequest(BaseModel):
    data: List[Question]    
