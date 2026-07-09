from fastapi import FastAPI
from pydantic import BaseModel
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