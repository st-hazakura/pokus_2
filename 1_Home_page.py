import streamlit as st
import websockets
import asyncio
import base64
import json
from configure import auth_key
import os
import pyaudio

st.set_page_config(page_title="Bibup", initial_sidebar_state="collapsed")

if 'text' not in st.session_state: # 1. инициализация сессии, если нет переменных то создаст
    st.session_state['text'] = ''  # To store the final transcription
    st.session_state['run'] = False
    st.session_state['temp_text'] = ''  # To store interim text during recording

# параметры для пиаудио
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# запуск аудио
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

#  функции для управления записью
def start_listening(): # отчищает переменные для новой записи
    st.session_state['run'] = True
    st.session_state['text'] = ''  # Clear text field when starting a new recording
    st.session_state['temp_text'] = ''  # Reset interim text

def stop_listening():
    st.session_state['run'] = False
    st.session_state['text'] += st.session_state['temp_text']  # Save final transcription
    st.session_state['temp_text'] = ''  # Clear interim text after saving

#  заголовок и кнопки записи
st.title('Get real-time transcription')
start, stop = st.columns(2)
start.button('Start listening', on_click=start_listening)
stop.button('Stop listening', on_click=stop_listening)


# Устанавливает URL WebSocket-сервера и содержит функции send и receive для отправки аудио и получения текста.
URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
    print(f'Connecting websocket to url {URL}')

    async with websockets.connect(
        URL,
        extra_headers=(("Authorization", auth_key),), 
        # extra_headers=(("Authorization", auth_key), ("Content-Language", "ru")),
        ping_interval=5,
        ping_timeout=20
    ) as _ws:

        await asyncio.sleep(0.1)
        print("Receiving SessionBegins ...")

        session_begins = await _ws.recv()
        print(session_begins)
        print("Sending messages ...")

        async def send():
            while st.session_state['run']:
                try:
                    data = stream.read(FRAMES_PER_BUFFER)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio_data": str(data)})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    break
                except Exception as e:
                    print(e)
                    break
                await asyncio.sleep(0.01)

        async def receive():
            while st.session_state['run']:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    if result['message_type'] == 'FinalTranscript':
                        transcript = result['text']
                        st.session_state['temp_text'] += ' ' + transcript  # Append to interim text \n
                        st.markdown(transcript)  # Display in real-time without accumulating
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    break
                except Exception as e:
                    print(e)
                    break

        await asyncio.gather(send(), receive())

if st.session_state['run']:
    asyncio.run(send_receive())

# Обновляем st.session_state['text'] при каждом изменении текста в st.text_area
st.session_state['text'] = st.text_area('Transcript', value=st.session_state['text'], height=400)


title = st.text_input("Enter a title for your file")
if st.button("Save Text"):
    if title != '' and st.session_state['text'] != '':
        directory = "saved_transcriptions"
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_path = os.path.join(directory, f"{title}.txt")
        with open(file_path, "w") as file:
            file.write(st.session_state['text'])
        st.success(f"Text saved successfully at Records!")
    else:
        st.error("Please provide both a title and text.")
