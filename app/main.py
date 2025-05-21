from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import questions
from app.models import AppException
from app.services.app_exception import app_exception_handler

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppException, app_exception_handler)
app.include_router(questions.router)