import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import PyPDF2
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load the secret API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("System Error: GEMINI_API_KEY is missing from the .env file.")

# 2. Configure the new Unified GenAI Client
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="AI Resume Summarizer", version="2.0.0")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/extract-text")
async def extract_pdf_text(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    try:
        # Step A: Extract Text 
        pdf_reader = PyPDF2.PdfReader(file.file)
        extracted_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
        if not extracted_text.strip():
             raise HTTPException(status_code=400, detail="Empty or image-based PDF.")

        # Step B: The AI Prompt Engineering 
        system_instruction = (
            "You are an expert technical recruiting manager. Analyze the following resume text. "
            "Extract the candidate's name, core technical skills (as a comma-separated list), "
            "total years of experience, and write a 2-sentence summary verdict on their profile. "
            "Return the output STRICTLY as a JSON object with keys: name, skills, experience, summary."
        )

        # Step C: Call the new Gemini 3.5 Engine with Structured Output
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=f"{system_instruction}\n\nResume Data:\n{extracted_text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        clean_json_output = response.text
             
        return JSONResponse(content={
            "status": "success", 
            "filename": file.filename,
            "ai_analysis": clean_json_output
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backend Generation Error: {str(e)}")