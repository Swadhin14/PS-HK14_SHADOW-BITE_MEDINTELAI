from fastapi import FastAPI
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles 
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Form
from starlette.middleware.sessions import SessionMiddleware


import io
import os
from datetime import datetime
from routers import upload

UPLOAD_FOLDER = "uploaded_pdfs"
app = FastAPI(
    title="Medical AI Backend",
    version="1.0.0"
)
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key-change-this"
)
app.mount("/static", StaticFiles(directory="D:\HACKKKK\Frontend\static"), name="Frontend")
templates = Jinja2Templates(directory="D:\HACKKKK\Frontend")
app.include_router(upload.router)
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "main.html", 
        {"request": request, "title": "Medical Report AI"}  
    )

# 2. Upload Report page (upload.html)
@app.get("/upload", response_class=HTMLResponse)
async def upload_page(request: Request):
    return templates.TemplateResponse(
        "upload.html", 
        {"request": request, "title": "Upload Medical Report"}
    )

# 3. Patient Context page (patient-context.html)
@app.get("/patient-context", response_class=HTMLResponse)
async def patient_context_page(request: Request):
    return templates.TemplateResponse(
        "patient-context.html", 
        {"request": request, "title": "Patient Context"}
    )

@app.get("/result", response_class=HTMLResponse)
async def patient_context_page(request: Request):
    return templates.TemplateResponse(
        "result.html", 
        {"request": request, "title": "result"}
    )
@app.get("/doctor-interface", response_class=HTMLResponse)
async def patient_context_page(request: Request):
    return templates.TemplateResponse(
        "doctor.html", 
        {"request": request, "title": "doctor-interface"}
    )
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)



