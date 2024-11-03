import os
from fastapi import FastAPI, File, UploadFile, Form, Header, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import whisper
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Retrieve the expected bearer token from the environment variable
EXPECTED_BEARER_TOKEN = os.environ.get('ENV_BEARER')

if not EXPECTED_BEARER_TOKEN:
    raise Exception("The ENV_BEARER environment variable is not set.")

# Load the Whisper model when the server starts
whisper_model = whisper.load_model("small")

@app.post("/audio/transcriptions")
async def transcribe_audio(
    authorization: Optional[str] = Header(None),
    file: UploadFile = File(...),
    model: str = Form(...)
):
    # Validate the Authorization header
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing.")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format.")
    
    token = authorization[7:]  # Extract the token after 'Bearer '
    if token != EXPECTED_BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid bearer token.")

    # Validate the model parameter
    if model != 'whisper-1':
        raise HTTPException(status_code=400, detail="Invalid model parameter.")

    # Read the uploaded file content
    audio_content = await file.read()

    # Create a temporary file to store the audio content
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        temp_audio_file.write(audio_content)
        temp_audio_path = temp_audio_file.name

    try:
        # Transcribe the audio using the Whisper model
        transcription_result = whisper_model.transcribe(temp_audio_path)
    finally:
        # Clean up the temporary file
        os.remove(temp_audio_path)

    # Return the transcription as JSON
    return JSONResponse(content={"text": transcription_result['text']})
