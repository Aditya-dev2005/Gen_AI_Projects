from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
from openai import OpenAI

# ---------------- OPENROUTER CLIENT ----------------

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- LLM RESPONSE ----------------

def get_llm_response(question, prompt):

    response = client.chat.completions.create(
        model="meta-llama/llama-3-8b-instruct",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    return response.choices[0].message.content


# ---------------- CLEAN SQL ----------------

def clean_sql_query(query):

    query = query.replace("```sql", "")
    query = query.replace("```", "")
    query = query.strip()

    return query


# ---------------- SQL EXECUTION ----------------

def read_sql_query(sql, db):

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()

    connection.commit()
    connection.close()

    return rows


# ---------------- PROMPT ----------------

prompt = """
You are an expert SQL assistant.

Given a question, generate an SQL query to retrieve the answer from a database.

The database has a table named STUDENT with the following columns:

NAME (VARCHAR)
CLASS (VARCHAR)
SECTION (VARCHAR)
MARKS (INT)

Return ONLY the SQL query.
Do NOT explain anything.
Do NOT use markdown formatting.
Do NOT use ```sql.
"""


# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="OpenRouter SQL Query App")

st.header("OpenRouter App to Retrieve SQL Data")

question = st.text_input("Input :", key="input")

submit = st.button("Ask the question")


# ---------------- MAIN LOGIC ----------------

if submit and question:

    response = get_llm_response(question, prompt)

    print("Raw LLM Response:", response)

    clean_query = clean_sql_query(response)

    print("Clean SQL:", clean_query)

    result = read_sql_query(clean_query, "student.db")

    st.subheader("The retrieved data is :")

    for row in result:
        st.write(row)