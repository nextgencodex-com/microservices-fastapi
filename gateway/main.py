from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import httpx
import time
from typing import Any

app = FastAPI(title="API Gateway", version="2.0.0")

SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}

# Activity 2: Auth Setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # සරලව ඕනෑම login එකකට 'secret-token' ලබා දේ
    if form_data.password == "secret-token":
        return {"access_token": "secret-token", "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Incorrect password (use 'secret-token')")

async def verify_token(token: str = Depends(oauth2_scheme)):
    if token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

# Activity 3: Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    print(f"LOG: {request.method} {request.url.path} | Status: {response.status_code} | Time: {duration:.2f}ms")
    return response

# Activity 4: Enhanced Forwarding & Error Handling
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not configured")

    url = f"{SERVICES[service]}{path}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, timeout=5.0, **kwargs)
            if response.is_error:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": f"{service.upper()} error", "details": response.text}
                )
            return JSONResponse(content=response.json() if response.text else {}, status_code=response.status_code)
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Service {service} is OFFLINE")

# Routes
@app.get("/gateway/students")
async def get_students(token: str = Depends(verify_token)):
    return await forward_request("student", "/api/students", "GET")

@app.get("/gateway/courses")
async def get_courses(token: str = Depends(verify_token)):
    return await forward_request("course", "/api/courses", "GET")