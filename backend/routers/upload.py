from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
from services.pdf_parser import extract_text_from_pdf
from services.medical_extractor import extract_medical_data
from services.kb_services import retrieve_from_kb
from services.llm_service import generate_response
router = APIRouter()

UPLOAD_FOLDER = "uploaded_reports"

# Create folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/api/extract-pdf")
async def upload_report(file: UploadFile = File(...)):
    
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "path": file_path
    }
@router.post("/extract-text/{filename}")
async def extract_text(filename: str):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        text = extract_text_from_pdf(file_path)

        return {
            "message": "Text extracted successfully",
            "filename": filename,
            "text": text[:1000]  # limit for preview (avoid huge response)
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #medical_extract
@router.post("/structure-report/{filename}")
async def structure_report(filename: str):

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        text = extract_text_from_pdf(file_path)

        # Step 1: Extract structured labs
        structured_data = extract_medical_data(text)

        # Step 2: Retrieve knowledge from RAG
        retrieved_chunks = retrieve_from_kb(structured_data)

        # Step 3: Build abnormal lab summary
        lab_summary = ""
        for lab in structured_data:
            if lab["status"] != "Normal":
                lab_summary += (
                    f"{lab['test_name']} is {lab['status']} "
                    f"({lab['value']} {lab['unit']}, normal range {lab['normal_range']}). "
                )

        # Step 4: Combine retrieved context
        context = "\n\n".join(retrieved_chunks)

        # Step 5: Create final prompt
        prompt = f"""
You are a clinical decision support AI.

Patient abnormal lab findings:
{lab_summary}

Relevant medical guidelines:
{context}

Provide:

1. Professional Clinical Summary (for doctors)
2. Simple Explanation (for patient)

Be medically accurate.
"""

        # Step 6: Call Ollama
        final_explanation = generate_response(prompt)

        # Step 7: Return final response
        return {
            "filename": filename,
            "structured_data": structured_data,
            "final_explanation": final_explanation
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))