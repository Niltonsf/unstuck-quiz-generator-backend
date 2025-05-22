from pydantic import BaseModel
from typing import List

class PromptRequest(BaseModel):
    prompt: str

class Question(BaseModel):
    id: str
    question: str
    options: List[dict]
    answer: List[str]
    questionNumber: int

class ValidateAnswerRequest(BaseModel):
    question: Question
    userAnswer: str

class CreateQuizRequest(BaseModel):
    data: List[Question]   

class DecryptQuizRequest(BaseModel):
    data: List[Question]    
