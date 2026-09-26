from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import fitz
from google import genai
from dotenv import load_dotenv
import os
import joblib

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

LATEST_RESUME = ""
placement_model = joblib.load(
    "models/placement_model.pkl"
)
class ScoreInput(BaseModel):
    cgpa: float
    projects: int
    dsa: int
    internship: int
class ProfileInput(BaseModel):
    cgpa: float
    projects: int
    dsa: int
    internship: int

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to AI Placement Mentor"}


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
@app.post("/predict-score")
def predict_score(data: ScoreInput):

    score = placement_model.predict([
        [
            data.cgpa,
            data.projects,
            data.dsa,
            data.internship
        ]
    ])[0]

    return {
        "placement_score": round(score, 2)
    }
@app.post("/analyze-profile")
def analyze_profile(data: ProfileInput):

    score = placement_model.predict([
        [
            data.cgpa,
            data.projects,
            data.dsa,
            data.internship
        ]
    ])[0]

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"""
        Student Profile:

        CGPA: {data.cgpa}
        Projects: {data.projects}
        DSA: {data.dsa}
        Internship: {data.internship}

        ML Placement Score: {round(score,2)}

        Give:

        1. Placement Readiness
        2. Strengths
        3. Weaknesses
        4. Missing Skills
        5. 4 Week Learning Roadmap
        """
    )

    return {
        "placement_score": round(score, 2),
        "analysis": response.text
    }