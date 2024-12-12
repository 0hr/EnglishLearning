import os
import re

from fastapi import APIRouter, UploadFile, File, HTTPException
import whisper
from openai import OpenAI
from pathlib import Path
import uuid

speaking_router = APIRouter()

# Load the smallest Whisper model
whisper_model = whisper.load_model("base")

# Load the smallest LLaMA model
client = OpenAI(
    api_key=os.getenv('OPENAPI_KEY'),
)


@speaking_router.post("/chat")
async def generate(file: UploadFile = File(...)):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Invalid file type. Only M4A files are supported.")

    # Save the uploaded file
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio file using Whisper
    result = whisper_model.transcribe(file_location)
    text = result["text"]

    prompt = """
    Act as a fluent English speaker. Engage in a natural, conversational exchange with me, responding thoughtfully to my questions or comments. Use everyday vocabulary, idiomatic expressions, and proper grammar to make the conversation immersive and realistic. Adapt your tone and style based on the topic or context, and feel free to ask me questions to keep the conversation going.

    If I make any mistakes, politely correct them and offer a short explanation to help me learn.

    Here’s an example interaction:

    User: 'Hi, how are you?' Assistant: 'I’m doing great, thanks for asking! How about you?'

    Only give conversation response.

    Let’s begin! My first message is:
    """

    conversation_history = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history,
    )
    assistant_reply = response.choices[0].message.content

    unique_id = uuid.uuid4()
    speech_file_path = Path(f"temp/{unique_id}.mp3")
    with client.with_streaming_response.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=assistant_reply
    ) as audio_response:
        audio_response.stream_to_file(speech_file_path)

    os.remove(file_location)

    return {
        "transcription": text,
        "response": assistant_reply,
        "audio_file_url": f"/audio/{unique_id}.mp3"
    }

@speaking_router.post("/pronunciation")
async def generate(file: UploadFile = File(...)):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Invalid file type. Only M4A files are supported.")

    # Save the uploaded file
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Transcribe the audio file using Whisper
    result = whisper_model.transcribe(file_location)
    text = result["text"].strip().split(' ')

    if len(text) > 0:
        text = text[0]
        text = re.sub(r'[^a-zA-Z]', '', text)
    else:
        text = ''

    return {
        "transcription": text,
    }



