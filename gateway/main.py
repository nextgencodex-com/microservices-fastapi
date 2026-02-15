# gateway/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import httpx
from typing import Any

app = FastAPI(title="API Gateway", version="1.0.0")

# Student Service එක 8001 port එකේ run වන බව තහවුරු කරගන්න
SERVICES = {
    "student": "http://localhost:8001"
}

async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            # Request එක අදාළ microservice එකට යැවීම
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            
            # Response එකේ දත්ත තිබේදැයි පරීක්ෂා කර JSON ලෙස ලබා දීම
            # හිස් දත්ත ලැබුණහොත් (JSONDecodeError) එය මගහැරවීමට try/except භාවිතා කර ඇත
            try:
                response_data = response.json() if response.text else None
            except Exception:
                response_data = {"detail": "Response is not a valid JSON", "content": response.text}

            return JSONResponse(
                content=response_data,
                status_code=response.status_code
            )
            
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail="Student Service is not running on port 8001")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}

# --- Student Service Routes ---

@app.get("/gateway/students")
async def get_all_students():
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "GET")

@app.post("/gateway/students")
async def create_student(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = None
    return await forward_request("student", "/api/students", "POST", json=body)

@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, request: Request):
    try:
        body = await request.json()
    except Exception:
        body = None
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)

@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")