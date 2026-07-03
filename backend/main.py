from fastapi import FastAPI
from pydantic import BaseModel
class Student(BaseModel):
    name:str
    cgpa:float
    college:str
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
@app.post("/student")
def add_student(student:Student):
    return {
        "message":"student added successfully",
        "student":student
        
    }