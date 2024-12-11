import os
from fastapi import APIRouter, UploadFile, File, HTTPException
import whisper
from openai import OpenAI
from pathlib import Path

router = APIRouter()

# Load the smallest Whisper model
whisper_model = whisper.load_model("base")

# Load the smallest LLaMA model
client = OpenAI(
    api_key='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',
)


@router.post("/speak")
async def generate(file: UploadFile = File(...)):
    if file.content_type != "audio/m4a":
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

    # Generate audio response using OpenAI
    import uuid

    unique_id = uuid.uuid4()
    speech_file_path = Path(f"temp/{unique_id}.mp3")
    with client.with_streaming_response.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=assistant_reply
    ) as audio_response:
        audio_response.stream_to_file(speech_file_path)

    # Clean up the temporary file
    os.remove(file_location)

    return {
        "transcription": text,
        "response": assistant_reply,
        "audio_file_url": f"/audio/{unique_id}.mp3"
    }

