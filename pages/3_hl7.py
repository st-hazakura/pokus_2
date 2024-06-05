import streamlit as st
import os

st.set_page_config(page_title="HL7 Viewer", initial_sidebar_state="collapsed")
st.title('HL7 Converted Files')

HL7_DIR = "hl7_transformed"

def load_hl7_files():
    hl7_files = {}
    if os.path.exists(HL7_DIR):
        for filename in os.listdir(HL7_DIR):
            if filename.endswith(".hl7"):
                with open(os.path.join(HL7_DIR, filename), "r") as file:
                    hl7_files[filename[:-4]] = file.read()  # Убираем .hl7 при сохранении ключа
    return hl7_files

def display_file(title, content):
    if st.session_state.get(f"edit_{title}", False):
        edited_text = st.text_area("Edit HL7 content", content, key=f"text_{title}")
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

def display_action_buttons(title):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Edit", key=f"edit_button_{title}"):
            st.session_state[f"edit_{title}"] = True
    with col2:
        if st.button(f"Delete", key=f"delete_{title}"):
            delete_hl7_file(title)

def save_changes(title, edited_text):
    with open(os.path.join(HL7_DIR, f"{title}.hl7"), "w") as file:
        file.write(edited_text)
    st.session_state[f"edit_{title}"] = False
    st.experimental_rerun()

def cancel_changes(title):
    st.session_state[f"edit_{title}"] = False
    st.experimental_rerun()

def delete_hl7_file(title):
    os.remove(os.path.join(HL7_DIR, f"{title}.hl7"))
    st.experimental_rerun()

hl7_files = load_hl7_files()
if hl7_files:
    for title, content in hl7_files.items():
        with st.expander(title):
            display_file(title, content)
else:
    st.write("No converted HL7 files found.")

if st.button("Delete All HL7 Files"):
    for filename in os.listdir(HL7_DIR):
        if filename.endswith(".hl7"):
            os.remove(os.path.join(HL7_DIR, filename))
    st.experimental_rerun()
