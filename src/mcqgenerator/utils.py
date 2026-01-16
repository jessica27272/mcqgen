import json
import traceback
from PyPDF2 import PdfReader

def read_file(file):
    try:
        if file.name.endswith(".pdf"):
            file.seek(0)
            reader = PdfReader(file)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

            if text.strip() == "":
                raise Exception("PDF has no readable text.")

            return text

        elif file.name.endswith(".txt"):
            file.seek(0)
            return file.read().decode("utf-8")

        else:
            raise Exception("Unsupported file format. Only PDF and TXT allowed.")

    except Exception as e:
        raise Exception("Error reading the file.")


import json
import re
import traceback

def get_table_data(quiz_str):
    try:
        
        json_match = re.search(r"\{[\s\S]*\}", quiz_str)

        if not json_match:
            return None

        quiz_dict = json.loads(json_match.group())

        quiz_table_data = []

        for key, value in quiz_dict.items():
            mcq = value.get("mcq", "")
            options = " | ".join(
                [f"{k}: {v}" for k, v in value.get("options", {}).items()]
            )
            correct = value.get("correct", "")

            quiz_table_data.append({
                "MCQ": mcq,
                "Choices": options,
                "Correct": correct
            })

        return quiz_table_data

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return None


def split_text(text, chunk_size=3000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks
