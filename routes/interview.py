from fastapi import APIRouter
from pydantic import BaseModel
from services.openai_service import ask_ai
from dependencies import get_current_user
from fastapi import Depends

router = APIRouter()

class ResumeInput(BaseModel):
    text: str
    role: str = "General"

class QuestionInput(BaseModel):
    level: str
    role: str = "General"
    category: str = "Technical"

class AnswerInput(BaseModel):
    answer: str
    role: str = "General"

class ExpertAnswerInput(BaseModel):
    question: str
    role: str = "General"


# ✅ Resume Analysis
@router.post("/analyze-resume")
def analyze_resume(data: ResumeInput, current_user = Depends(get_current_user)):
    prompt = f"Analyze this resume for a {data.role} position and give strengths, weaknesses and suggestions:\n{data.text}"
    return {"analysis": ask_ai(prompt)}


# ✅ Generate Question
@router.post("/generate-question")
def generate_question(data: QuestionInput, current_user = Depends(get_current_user)):
    prompt = f"Generate exactly 10 {data.level}-level {data.category} interview questions for a {data.role} role. Important: Do not make them only Data Structures and Algorithms (DSA). Include practical scenarios, architecture, framework-specific, or behavioral elements where appropriate. Provide the output as a clean, numbered markdown list."
    return {"question": ask_ai(prompt)}


# ✅ Evaluate Answer
@router.post("/evaluate")
def evaluate_answer(data: AnswerInput, current_user = Depends(get_current_user)):
    prompt = f"Evaluate this answer for a {data.role} interview and give score out of 10 with feedback in specific sections 'Score: X/10', 'Strengths:', 'Feedback:'. Format beautifully:\n{data.answer}"
    return {"feedback": ask_ai(prompt)}

# ✅ Generate Expert Answer
@router.post("/expert-answer")
def generate_expert_answer(data: ExpertAnswerInput, current_user = Depends(get_current_user)):
    prompt = f"Provide a concise, expert-level answer to the following {data.role} interview question:\n{data.question}"
    return {"answer": ask_ai(prompt)}