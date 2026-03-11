from groq import Groq

# Put your API key here
client = Groq(api_key="YOUR_GROQ_API_KEY")

def transcribe_audio(file_path):

    with open(file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,
            model="whisper-large-v3",
            response_format="text"
        )

    return transcription