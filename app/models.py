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

class AppException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
        }