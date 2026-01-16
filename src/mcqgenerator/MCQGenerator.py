import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.stdout import StdOutCallbackHandler

load_dotenv()

key=os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    groq_api_key=key,
    model_name="llama-3.1-8b-instant", 
    temperature=0.5
)

template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choices questions for {subject} students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_generation_prompt=PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template 
)

quiz_chain = quiz_generation_prompt | llm | StrOutputParser()

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity.
if the quiz is not at per with the cognitive and analytical abilities of the students, \
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the students abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)
review_chain = quiz_evaluation_prompt | llm | StrOutputParser()


def generate_evaluate_chain(inputs: dict):
    quiz = quiz_chain.invoke({
        "text": inputs["text"],
        "number": inputs["number"],
        "subject": inputs["subject"],
        "tone": inputs["tone"],
        "response_json": inputs["response_json"]
    })

    review = review_chain.invoke({
        "quiz": quiz,
        "subject": inputs["subject"]
    })

    return {
        "quiz": quiz,
        "review": review
    }


