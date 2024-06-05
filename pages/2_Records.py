import streamlit as st
import os
from converter_hl7 import convert_single_file, convert_all_files

st.set_page_config(page_title="Records")
st.title('Saved Transcriptions')


TRANSCRIPTIONS_DIR = "saved_transcriptions"
HL7_DIR = "hl7_transformed"

def load_transcriptions():
    transcriptions = {}
    if os.path.exists(TRANSCRIPTIONS_DIR):
        for filename in os.listdir(TRANSCRIPTIONS_DIR):
            if filename.endswith(".txt"):
                filepath = os.path.join(TRANSCRIPTIONS_DIR, filename)
                with open(filepath, "r") as file:
                    transcriptions[filename[:-4]] = file.read()  # Убираем .txt при сохранении ключа
    return transcriptions


def display_transcription(title, content):
    if st.session_state.get(f"edit_{title}", False):
        edited_text = st.text_area("Edit transcription", content, key=f"text_{title}")
        display_edit_buttons(title, edited_text)
    else:
        st.write(content)
        display_action_buttons(title)


def display_edit_buttons(title, edited_text):
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("Save Changes", key=f"save_{title}"):
            save_changes(title, edited_text)
    with col2:
        if st.button("Cancel Changes", key=f"cancel_{title}"):
            cancel_changes(title)


# def display_action_buttons(title):
#     col1, col2, col3 = st.columns([1, 6, 1])
#     with col1:
#         if st.button("Edit", key=f"edit_button_{title}"):
#             st.session_state[f"edit_{title}"] = True
#     with col3:
#         if st.button(f"Delete", key=f"delete_{title}"):
#             delete_transcription(title)
def display_action_buttons(title):
    col1, col2, col3 = st.columns([0.4, 1, 1])
    with col1:
        if st.button("Edit", key=f"edit_button_{title}"):
            st.session_state[f"edit_{title}"] = True
    with col2:
        if st.button(f"Convert to HL7", key=f"convert_{title}"):
            convert_single_file(f"{title}.txt")
            st.success(f"{title} converted to HL7 format!")
    with col3:
        if st.button(f"Delete", key=f"delete_{title}"):
            delete_transcription(title)


def save_changes(title, edited_text):
    with open(os.path.join(TRANSCRIPTIONS_DIR, f"{title}.txt"), "w") as file:
        file.write(edited_text)
    st.session_state[f"edit_{title}"] = False
    st.experimental_rerun()


def cancel_changes(title):
    st.session_state[f"edit_{title}"] = False
    st.experimental_rerun()


def delete_transcription(title):
    os.remove(os.path.join(TRANSCRIPTIONS_DIR, f"{title}.txt"))
    st.experimental_rerun()


def display_transcriptions(transcriptions):
    if transcriptions:
        for title, content in transcriptions.items():
            with st.expander(title):
                display_transcription(title, content)
    else:
        st.write("No saved transcriptions found.")


saved_transcriptions = load_transcriptions()
display_transcriptions(saved_transcriptions)


# if st.button("Delete All Transcriptions"):
#     for filename in os.listdir(TRANSCRIPTIONS_DIR):
#         if filename.endswith(".txt"):
#             os.remove(os.path.join(TRANSCRIPTIONS_DIR, filename))
#     st.experimental_rerun()
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Delete All Transcriptions"):
        for filename in os.listdir(TRANSCRIPTIONS_DIR):
            if filename.endswith(".txt"):
                os.remove(os.path.join(TRANSCRIPTIONS_DIR, filename))
        st.experimental_rerun()

with col2:
    if st.button("Convert All to HL7"):
        convert_all_files()
        st.success("All files converted to HL7 format!")