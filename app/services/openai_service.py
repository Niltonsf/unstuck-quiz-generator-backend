import openai
from app.config import OPEN_API_KEY

client = openai.OpenAI(api_key=OPEN_API_KEY)

def generate_questions_from_text(text: str) -> str:
    prompt = (
        f"From the text below, generate 10 multiple-choice questions, each with 4 alternatives. "
        f"Indicate the correct answer in the object using the `answer` key. "
        f"Return an array of question objects as raw JSON, do not insert ```json at start or n``` at end. Each question object should follow this format:\n"
        f"{{\n"      
        f"  question: 'The question',\n"
        f"  options: [\n"
        f"    {{ value: 'A', label: 'Option A' }},\n"
        f"    {{ value: 'B', label: 'Option B' }},\n"
        f"    {{ value: 'C', label: 'Option C' }},\n"
        f"    {{ value: 'D', label: 'Option D' }}\n"
        f"  ],\n"
        f"  answer: 'B'\n"
        f"}}\n\n"
        f"Text: {text}"
    )

    response = client.chat.completions.create(
        model="gpt-4-1106-preview",        
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,        
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()