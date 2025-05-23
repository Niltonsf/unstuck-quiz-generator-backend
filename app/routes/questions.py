import openai
from fastapi import APIRouter, HTTPException, File, UploadFile # type: ignore
from fastapi.responses import StreamingResponse
from app.services.pdf_parser import extract_text_from_pdf
from app.services.question_parser import parse_questions_string
from app.services.openai_service import generate_questions_from_text
from app.models import QuestionExplainRequest, ValidateAnswerRequest
from app.services.question import encrypt_question_answer
from app.services.encryption import decrypt_answer
from app.services.firebase_service import save_document, update_question_in_array, bucket
from uuid import uuid4
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

        title = file.filename.split(".")[0]

        if len(pdf_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large. Maximum size allowed is 500KB.")
        
        text, num_pages = extract_text_from_pdf(pdf_bytes)
        
        if not text:                        
            raise HTTPException(status_code=400, detail="PDF is empty.")
        if num_pages > MAX_ALLOWED_PAGES:            
            raise HTTPException(status_code=400, detail=f"PDF has too many pages. Maximum allowed is {MAX_ALLOWED_PAGES}.")

        quiz_id = str(uuid4())
        # questions = generate_questions_from_text(text)
        questions = [
{
    "id": str(uuid4()),
  "question": "Qual é o objetivo principal do artigo?",
  "options": [
    { "value": "A", "label": "Promover a sustentabilidade usando certificações convencionais." },
    { "value": "B", "label": "Automatizar a verificação de requisitos de sustentabilidade em projetos habitacionais brasileiros usando BIM." },
    { "value": "C", "label": "Diminuir o uso de recursos naturais na construção civil." },
    { "value": "D", "label": "Facilitar o processo construtivo de edifícios." }
  ],
  "questionNumber": 1,
  "answers": ["B"]
},
{
    "id": str(uuid4()),
  "question": "O que é BIM?",
  "options": [
    { "value": "A", "label": "Um processo de certificação sustentável." },
    { "value": "B", "label": "Um software de planejamento de projetos habitacionais." },
    { "value": "C", "label": "Modelagem da Informação da Construção." },
    { "value": "D", "label": "Uma categoria de avaliação de sustentabilidade." }
  ],
  "questionNumber": 2,
  "answers": ["C"]
},
{
    "id": str(uuid4()),
  "question": "Quais são os impactos ambientais associados à indústria da construção civil?",
  "options": [
    { "value": "A", "label": "Emissão de poluentes e geração de empregos." },
    { "value": "B", "label": "Geração de resíduos e consumo intensivo de recursos naturais." },
    { "value": "C", "label": "Produção de energia renovável e reciclagem." },
    { "value": "D", "label": "Educação ambiental e desenvolvimento sustentável." }
  ],
  "questionNumber": 3,
  "answers": ["B"]
},
{
    "id": str(uuid4()),
  "question": "Qual é a porcentagem de recursos naturais consumidos pela construção civil segundo o Green Building Council?",
  "options": [
    { "value": "A", "label": "25%" },
    { "value": "B", "label": "35%" },
    { "value": "C", "label": "45%" },
    { "value": "D", "label": "55%" }
  ],
  "questionNumber": 4,
  "answers": ["B"]
},
{
    "id": str(uuid4()),
  "question": "Qual dos seguintes não é uma certificação de sustentabilidade utilizada no Brasil?",
  "options": [
    { "value": "A", "label": "AQUA" },
    { "value": "B", "label": "Procel Edifica" },
    { "value": "C", "label": "LEED" },
    { "value": "D", "label": "Green Metric" }
  ],
  "questionNumber": 5,
  "answers": ["D"]
},
{
    "id": str(uuid4()),
  "question": "Qual é o papel das certificações de índice de sustentabilidade na engenharia civil?",
  "options": [
    { "value": "A", "label": "Aumentar o custo dos projetos." },
    { "value": "B", "label": "Reduzir o impacto ambiental dos projetos." },
    { "value": "C", "label": "Promover o uso de tecnologias antigas." },
    { "value": "D", "label": "Limitar o uso de BIM em projetos." }
  ],
  "questionNumber": 6,
  "answers": ["B"]
},
{
    "id": str(uuid4()),
  "question": "Quais aspectos dentro da cadeia produtiva da engenharia civil as certificações de sustentabilidade procuram otimizar?",
  "options": [
    { "value": "A", "label": "Redução de custos e aumento de eficiência." },
    { "value": "B", "label": "Gestão de equipe e comunicação." },
    { "value": "C", "label": "Consumo de energia elétrica, água, redução de resíduos e otimização de serviços." },
    { "value": "D", "label": "Marketing e vendas de projetos." }
  ],
  "questionNumber": 7,
  "answers": ["C"]
},
{
    "id": str(uuid4()),
  "question": "O que a ferramenta BIM integra em seus modelos virtuais inteligentes?",
  "options": [
    { "value": "A", "label": "Somente custos financeiros." },
    { "value": "B", "label": "Informações essenciais para planejamento, projeto, construção e manutenção." },
    { "value": "C", "label": "Dados exclusivamente de marketing." },
    { "value": "D", "label": "Análises de risco legal apenas." }
  ],
  "questionNumber": 8,
  "answers": ["B"]
},
{
    "id": str(uuid4()),
  "question": "Quais são os benefícios esperados da abordagem de usar BIM para verificar automaticamente a sustentabilidade dos projetos?",
  "options": [
    { "value": "A", "label": "Redução de tempo e aumento de precisão em conformidade com padrões sustentáveis." },
    { "value": "B", "label": "Eliminação total do impacto ambiental da construção civil." },
    { "value": "C", "label": "Integração de práticas não sustentáveis na construção civil." },
    { "value": "D", "label": "Aumento do custo e complexidade dos projetos." }
  ],
  "answers": ["A"],
  "questionNumber": 9
},
{
    "id": str(uuid4()),
  "question": "Qual certificação sustentável é específica do Brasil mencionada no texto?",
  "options": [
    { "value": "A", "label": "AQUA" },
    { "value": "B", "label": "Procel Edifica" },
    { "value": "C", "label": "LEED" },
    { "value": "D", "label": "Selo Casa Azul Caixa" }
  ],
  "questionNumber": 10,
  "answers": ["D"]
}
]

        if not questions:
            raise HTTPException(status_code=400, detail="No questions generated.")
        
        save_document('quizzes', quiz_id, {            
            "questions": questions
        })

        blob = bucket.blob(f"pdfs/{quiz_id}.pdf")
        blob.upload_from_string(pdf_bytes, content_type="application/pdf")

        return {
            "id": quiz_id,
            # "id": '08bfe3ed-1c19-4bd4-9a05-5a1822ccd32b',
            "title": title,
            # "questions": parse_questions_string(questions) 
            "questions": questions
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{str(e)}")

@router.post("/answer")
async def validate_answer(request: ValidateAnswerRequest):
    try:
        decrypted_answers = [decrypt_answer(answer) for answer in request.question.answers]

        if not decrypted_answers:
            raise HTTPException(status_code=400, detail="No answers found.")
                 
        user_answers = request.userAnswer
        
        is_correct = (
            set(user_answers) == set(decrypted_answers)
        )

        update_question_in_array('quizzes', request.id, request.questionId, {
            "userAnswers": decrypted_answers,
            "isCorrect": is_correct
        })

        return {
            "isCorrect": is_correct,
            "correctAnswersDescrypted": decrypted_answers,
            "userAnswers": decrypted_answers
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to validate answer.")
    
@router.post("/explain")
async def explain_wrong_answer(data: QuestionExplainRequest):
    save_document('random', {"name": "Alice", "age": 30, "city": "New York"})
    # prompt = f"""
    #     You are a knowledgeable teacher. A student was asked this question:

    #     Question: "{data.question}"

    #     They responded with: "{data.user_response}"

    #     Explain in detail and in a constructive, educational way why the response is incorrect.
    #     """

    # def stream_generator():
    #     stream = openai.chat.completions.create(
    #         model="gpt-4",
    #         messages=[{"role": "user", "content": prompt}],
    #         stream=True,
    #     )

    #     for event in stream:            
    #         dumped = event.model_dump()
    #         yield dumped["choices"][0]["de"]["content"]

    # return StreamingResponse(stream_generator(), media_type="text/plain")