from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import questions, quiz

app = FastAPI()

origins = [
    "https://www.unstuck-quiz.com",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
async def root():
    return {"message": "API Health OK"}

app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])