from fastapi import FastAPI, HTTPException
from service import CourseService
from models import Course
from typing import List

app = FastAPI(title="Course Microservice", version="1.0.0")
course_service = CourseService()

@app.get("/api/courses", response_model=List[Course])
def get_all_courses():
    return course_service.get_all()

@app.get("/api/courses/{course_id}", response_model=Course)
def get_course(course_id: int):
    course = course_service.get_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)