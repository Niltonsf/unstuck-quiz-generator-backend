import json
import uuid

def parse_questions_string(questions_str: str):
    try:
        questions_obj = json.loads(questions_str)

        for i, question in enumerate(questions_obj, start=1):
            question["questionNumber"] = i

            question["id"] = str(uuid.uuid4())
            
            if "answer" in question:                
                question["answer"] = [question["answer"]]
                
        return questions_obj
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON")
