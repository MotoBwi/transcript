# transcribe.py
import whisper

# Load the Whisper model
model = whisper.load_model("base")

def transcribe_audio(audio_file_path):
    result = model.transcribe(audio_file_path)
    return result['text']
