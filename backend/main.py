from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import fitz
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

LATEST_RESUME = ""

class Student(BaseModel):
    name:str
    college:str
    cgpa:float
    skills:list[str]

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to AI Placement Mentor"}
    
@app.get("/profile")
def profile():
    return {
        "name": "Aditi",
        "college": "BIT Patna",
        "cgpa": 8.92
    }
    
@app.get("/skills")
def skills():
    return {
        "skills" : ["Python",
                    "DSA",
                    "SQL",
                    "AI"
                    ]
    }
    
@app.post("/profile")
def create_profile(student:Student):
    if student.cgpa>=8.5:
        level = "Excellent"
    elif student.cgpa>=7:
        level = "Good"
    else:
        level = "Needs Improvement"
    required=["Python","SQL","DSA"]
    missing=[]
    for skill in required:
        if skill not in student.skills:
            missing.append(skill)

    roadmap = []

    for skill in missing:
        if skill == "Python":
            roadmap.append("Complete Python Fundamentals")

        elif skill == "SQL":
            roadmap.append("Learn SQL Joins and Queries")

        elif skill == "DSA":
            roadmap.append("Practice Striver A2Z Sheet")
            
    return {
        "name" : student.name,
        "college" : student.college,
        "cgpa" : student.cgpa,
        "skills" : student.skills,
        "level" : level,
        "missing_skill" : missing,
        "roadmap" : roadmap
    }
    
@app.get("/student/{name}/{cgpa}")
def get_student(name: str,cgpa:float):
    return {
        "student_name": name,
        "cgpa":cgpa
    }
    
@app.get("/search")
def search(skill:str):
    return {
        "search_skill":skill
    }
    
@app.get("/filter")
def filter_students(skill:str,cgpa:float):
    return {
        "skill":skill,
        "cgpa":cgpa
    }
    
@app.post("/upload-resume")

async def upload_resume(
    file: UploadFile = File(...)
):

    contents = await file.read()

    with open(
        f"uploads/{file.filename}",
        "wb"
    ) as f:

        f.write(contents)
    global LATEST_RESUME
    LATEST_RESUME = file.filename

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename
    }
    
@app.get("/extract-resume")
def extract_resume():

    if LATEST_RESUME == "":
        return {
            "message": "No resume uploaded yet"
        }

    doc = fitz.open(
        f"uploads/{LATEST_RESUME}"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    return {
        "resume_text": text
    }
<<<<<<< HEAD
=======

@app.get("/test-gemini")
def test_gemini():

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents="Say hello to Aditi"
        )

        return {
            "response": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }
@app.get("/analyze-resume")
def analyze_resume():

    if LATEST_RESUME == "":
        return {
            "message": "No resume uploaded yet"
        }

    doc = fitz.open(
        f"uploads/{LATEST_RESUME}"
    )

    text = ""

    for page in doc:
        text += page.get_text()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        Analyze this resume.

        Return ONLY in this format:

        Placement Score: <score>/100

        Strengths:
        - ...

        Weaknesses:
        - ...

        Missing Skills:
        - ...

        Learning Roadmap:
        Week 1:
        ...

        Week 2:
        ...

        Week 3:
        ...

        Week 4:
        ...

        Resume:

        {text}
        """
        
    )

    return {
        "analysis": response.text
    }
>>>>>>> 92e4359 (Added Gemini resume analysis)
