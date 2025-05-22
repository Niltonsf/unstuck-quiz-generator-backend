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
        if num_pages > 2:            
            raise HTTPException(status_code=400, detail="Only single-page PDFs are allowed.")

        questions = generate_questions_from_text(text) 
        # questions = "[\n{\n  \"question\": \"Qual é o código da Instrução de Trabalho para locação de obra?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"IT.01\" },\n    { \"value\": \"B\", \"label\": \"IT.02\" },\n    { \"value\": \"C\", \"label\": \"LOC.01\" },\n    { \"value\": \"D\", \"label\": \"LOC.02\" }\n  ],\n  \"answer\": \"A\"\n},\n{\n  \"question\": \"Qual é a versão da Instrução de Trabalho apresentada no texto?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Versão 1.0\" },\n    { \"value\": \"B\", \"label\": \"Versão 1.1\" },\n    { \"value\": \"C\", \"label\": \"Versão 01\" },\n    { \"value\": \"D\", \"label\": \"Versão 02\" }\n  ],\n  \"answer\": \"C\"\n},\n{\n  \"question\": \"Quantas folhas compõem a Instrução de Trabalho para locação de obra?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"1\" },\n    { \"value\": \"B\", \"label\": \"2\" },\n    { \"value\": \"C\", \"label\": \"3\" },\n    { \"value\": \"D\", \"label\": \"4\" }\n  ],\n  \"answer\": \"A\"\n},\n{\n  \"question\": \"Quais são os documentos de referência mencionados na Instrução de Trabalho?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Projeto de prefeitura, levantamento plani-altimétrico e projeto de locação\" },\n    { \"value\": \"B\", \"label\": \"Projeto arquitetônico, levantamento topográfico e projeto estrutural\" },\n    { \"value\": \"C\", \"label\": \"Projeto hidráulico, projeto elétrico e levantamento plani-altimétrico\" },\n    { \"value\": \"D\", \"label\": \"Levantamento geológico, projeto de prefeitura e projeto de locação\" }\n  ],\n  \"answer\": \"A\"\n},\n{\n  \"question\": \"Qual equipamento não é listado como necessário para a locação de obra?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Martelo\" },\n    { \"value\": \"B\", \"label\": \"Betoneira\" },\n    { \"value\": \"C\", \"label\": \"Teodolito\" },\n    { \"value\": \"D\", \"label\": \"Prumo de centro\" }\n  ],\n  \"answer\": \"B\"\n},\n{\n  \"question\": \"Qual condição deve ser verificada antes do início dos serviços de locação?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Aprovação do projeto pelo cliente\" },\n    { \"value\": \"B\", \"label\": \"Conclusão da fundação\" },\n    { \"value\": \"C\", \"label\": \"Condições de segurança no trabalho\" },\n    { \"value\": \"D\", \"label\": \"Previsão do tempo para os próximos dias\" }\n  ],\n  \"answer\": \"C\"\n},\n{\n  \"question\": \"Qual a cor recomendada para pintar o gabarito?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Verde\" },\n    { \"value\": \"B\", \"label\": \"Vermelho\" },\n    { \"value\": \"C\", \"label\": \"Azul\" },\n    { \"value\": \"D\", \"label\": \"Branca\" }\n  ],\n  \"answer\": \"D\"\n},\n{\n  \"question\": \"Que material é utilizado para marcar os eixos X e Y no gabarito?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"Fita métrica\" },\n    { \"value\": \"B\", \"label\": \"Linha de náilon\" },\n    { \"value\": \"C\", \"label\": \"Lápis de carpinteiro\" },\n    { \"value\": \"D\", \"label\": \"Tinta\" }\n  ],\n  \"answer\": \"C\"\n},\n{\n  \"question\": \"Quem elaborou a Instrução de Trabalho?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"César Augusto Prado\" },\n    { \"value\": \"B\", \"label\": \"Fernando Raposo\" },\n    { \"value\": \"C\", \"label\": \"Franco Anselmi\" },\n    { \"value\": \"D\", \"label\": \"Ricardo Montalbán\" }\n  ],\n  \"answer\": \"A\"\n},\n{\n  \"question\": \"Em que data foi realizada a revisão da Instrução de Trabalho?\",\n  \"options\": [\n    { \"value\": \"A\", \"label\": \"01/01/2019\" },\n    { \"value\": \"B\", \"label\": \"01/02/2019\" },\n    { \"value\": \"C\", \"label\": \"01/03/2019\" },\n    { \"value\": \"D\", \"label\": \"01/04/2019\" }\n  ],\n  \"answer\": \"B\"\n}\n]"

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