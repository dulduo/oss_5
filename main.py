import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
JSON_FILE = "subjects.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

def load_courses():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_courses(data):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/courses")
def get_courses():
    return load_courses()


@app.post("/courses")
def create_course(course: Course):
    courses = load_courses()
    
    courses.append(course.model_dump())
    
    save_courses(courses)
    
    return {"message": "과목이 성공적으로 추가되었습니다.", "added_course": course}