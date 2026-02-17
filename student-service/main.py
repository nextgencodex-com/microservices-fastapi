from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from models import Student, StudentCreate, StudentUpdate
from service import StudentService
from typing import List

app = FastAPI(title="Student Microservice", version="1.1.0")
student_service = StudentService()

# Global Error Handler for unexpected errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred in Student Service", "error": str(exc)},
    )

@app.get("/api/students", response_model=List[Student])
def get_all_students():
    data = student_service.get_all()
    if data is None:
        return []
    return data

@app.get("/api/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    student = student_service.get_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Student with ID {student_id} not found"
        )
    return student

@app.post("/api/students", response_model=Student, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    try:
        return student_service.create(student)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create student: {str(e)}")

@app.delete("/api/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    success = student_service.delete(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cannot delete. Student not found.")
    return None