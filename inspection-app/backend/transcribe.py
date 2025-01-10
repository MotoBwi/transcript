import whisper

def transcribe_audio(file_path):
    # Load the model without the weights_only argument
    model = whisper.load_model("base")  # Remove weights_only=True
    result = model.transcribe(file_path)  # Transcribe the audio file
    return result['text']
