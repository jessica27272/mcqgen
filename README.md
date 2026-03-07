# MCQs Creator Application

An AI-based MCQ generator built using LangChain, Groq LLM, and Streamlit.  
The application generates multiple-choice questions from uploaded PDF or TXT documents.

---

## Features

- Upload PDF or TXT files
- Generate MCQs using Groq LLM (LLaMA 3.1)
- Select number of questions
- Subject-specific question generation
- Adjustable difficulty level
- Tabular output display

---

## Tech Stack

- Python
- Streamlit
- LangChain
- Groq LLM (llama-3.1-8b-instant)
- PyPDF2
- Pandas

---

## Project Workflow

1. User uploads a PDF or TXT file.
2. The system extracts text from the file.
3. Extracted content is processed using LangChain.
4. The Groq LLM generates multiple-choice questions.
5. Generated MCQs are displayed in a structured table using Streamlit.

---

## How to Run

1. Clone the repository
2. Install dependencies

pip install -r requirements.txt

3. Run the Streamlit application

streamlit run streamlitAPP.py

---

## Example Output

The system generates MCQs with:
- Question
- Four options
- Correct answer

---

## Future Improvements

- Export MCQs to PDF/CSV
- Add explanation for answers
- Support more file formats
- Deploy the application online





