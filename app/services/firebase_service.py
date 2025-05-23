import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
firebase_key_path = os.path.join(project_root, "unstuck-firebase-private-key.json")

cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'unstuck-5bac8.firebasestorage.app'
})

db = firestore.client()
bucket = storage.bucket()

def save_document(collection:str, document_id: str, data: dict):
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.set(data)

def find_document(collection:str, document_id: str):
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    
    return None

def update_document(collection: str, document_id: str, data: dict):
    doc_ref = db.collection(collection).document(document_id)
    doc_ref.update(data)

def update_question_in_array(collection: str, document_id: str, question_id: str, updated_data: dict):
    doc_ref = db.collection(collection).document(document_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise ValueError("Document not found")

    data = doc.to_dict()
    questions = data.get("questions", [])
    
    updated_questions = []
    found = False
    for question in questions:
        if question.get("id") == question_id:
            question.update(updated_data)
            found = True
        updated_questions.append(question)

    if not found:
        raise ValueError("Question ID not found in the array")
    
    doc_ref.update({"questions": updated_questions})
