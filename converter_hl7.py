import os
from datetime import datetime

def convert_to_hl7(text):
    # hl7_message = f"MSH|^~\\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|{datetime.now().strftime('%Y%m%d%H%M%S')}||ORU^R01|123|P|2.4\r"
    # hl7_message += f"PID|||123456||Doe^John||19800101|M|||\r"
    # hl7_message += f"OBR|1|||Test^Description\r"
    hl7_message = f"OBX|1|TX|Report||{text}\r"
    return hl7_message

def convert_single_file(filename):
    source_dir = "saved_transcriptions"
    target_dir = "hl7_transformed"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    filepath = os.path.join(source_dir, filename)
    with open(filepath, "r") as file:
        text = file.read()
        hl7_text = convert_to_hl7(text)
        hl7_filename = filename.replace(".txt", ".hl7")
        with open(os.path.join(target_dir, hl7_filename), "w") as hl7_file:
            hl7_file.write(hl7_text)

def convert_all_files():
    source_dir = "saved_transcriptions"

    for filename in os.listdir(source_dir):
        if filename.endswith(".txt"):
            convert_single_file(filename)
