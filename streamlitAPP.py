import os
import json
import traceback
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

load_dotenv()

# -------- Load RESPONSE JSON --------
with open("Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

st.title("MCQs Creator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")

    mcq_count = st.number_input(
        "No. of MCQs",
        min_value=3,
        max_value=50
    )

    subject = st.text_input("Insert Subject", max_chars=20)

    tone = st.text_input(
        "Complexity level of questions",
        max_chars=20,
        placeholder="Simple"
    )

    button = st.form_submit_button("Create MCQs")

# ---------------- MAIN LOGIC ----------------
if button:
    if not uploaded_file:
        st.error("Please upload a file")
    elif not subject or not tone:
        st.error("Please fill subject and complexity")
    else:
        with st.spinner("Generating MCQs..."):
            try:
                # 1️⃣ Read file
                text = read_file(uploaded_file)

                # 🔥 IMPORTANT FIX: limit text size (Groq context issue)
                MAX_CHARS = 6000
                text = text[:MAX_CHARS]

                # 2️⃣ Generate MCQs
                response = generate_evaluate_chain(
                    {
                        "text": text,
                        "number": mcq_count,
                        "subject": subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                    }
                )

                if not response or "quiz" not in response:
                    st.error("No MCQs could be generated ❌")
                    st.stop()

                quiz = response["quiz"]

                # 3️⃣ Convert quiz → table
                table_data = get_table_data(quiz)

                if not table_data or len(table_data) == 0:
                    st.error("No MCQs could be generated ❌")
                    st.stop()

                df = pd.DataFrame(table_data)
                df.index = df.index + 1

                st.success("MCQs Generated Successfully ✅")
                st.table(df)

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                logging.error(e)
                st.error("Something went wrong ❌")
