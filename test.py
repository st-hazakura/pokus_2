from configure import auth_key
import assemblyai as aai

aai.settings.api_key = auth_key
transcriber = aai.Transcriber()
transcript = transcriber.transcribe("./uploaded_audios/audio_test.m4a")

print(transcript.status)

print(transcript.text)