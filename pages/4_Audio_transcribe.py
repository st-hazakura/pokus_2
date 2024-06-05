import streamlit as st
import assemblyai as aai
import os
import time
from configure import auth_key

st.set_page_config(page_title="Upload Audio")
st.title('Upload Audio File for Transcription')

aai.settings.api_key = auth_key

def save_transcription(text, title):
    directory = "saved_transcriptions"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{title}.txt")
    with open(file_path, "w") as file:
        file.write(text)

def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    return transcript.text

def clear_uploaded_audios():
    directory = "uploaded_audios"
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)

# Инициализация состояния страницы
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
    st.session_state['transcription_text'] = ""
    st.session_state['title'] = ""

uploaded_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    st.session_state['uploaded_file'] = uploaded_file
    audio_directory = "uploaded_audios"
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)

    file_path = os.path.join(audio_directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded {uploaded_file.name}")
    
    st.write("Transcription in progress...")
    transcription_text = transcribe_audio(file_path)
    st.session_state['transcription_text'] = transcription_text
    st.success("Transcription completed!")
    
if st.session_state['transcription_text']:
    st.text_area("Transcription", value=st.session_state['transcription_text'], height=200, key='transcription_text_area')
    
    st.session_state['title'] = st.text_input("Enter a title for your file", value=st.session_state['title'])
    if st.button("Save Text"):
        if st.session_state['title']:
            save_transcription(st.session_state['transcription_text'], st.session_state['title'])
            st.success(f"Text saved successfully in Records!")
            st.session_state['uploaded_file'] = None
            st.session_state['transcription_text'] = ""
            st.session_state['title'] = ""
            # st.experimental_rerun()  # Перезапуск страницы для применения изменений
        else:
            st.error("Please provide a title for the file.")

clear_uploaded_audios()