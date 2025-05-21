import json
from app.services.encryption import encrypt_answer
from app.models import Question
from typing import List

def encrypt_question_answer(questions: List[Question]):
  for question in questions:
    question.answer = [
        encrypt_answer(answer) for answer in question.answer
    ]

  return questions
    
