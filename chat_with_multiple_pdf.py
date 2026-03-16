from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# OpenRouter wrapper
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS


# ---------------- PDF TEXT ----------------

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# ---------------- TEXT CHUNKING ----------------

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )
    chunks = text_splitter.create_documents([text])
    return chunks


# ---------------- VECTOR STORE ----------------

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    vector_store = FAISS.from_documents(text_chunks, embeddings)
    vector_store.save_local("faiss_index")


# ---------------- CONVERSATION CHAIN ----------------

def get_conversation_chain():

    model = ChatOpenAI(
        model="meta-llama/llama-3-8b-instruct",
        temperature=0.3,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    return model


# ---------------- USER INPUT ----------------

def user_input(user_question):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    new_db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = new_db.similarity_search(user_question)

    chain = get_conversation_chain()

    # Manual prompt (LangChain 1.x compatible)
    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Answer the question as detailed as possible from the provided context.
If the answer is not in the context, just say:
"Answer is not available in the context."

Context:
{context}

Question:
{user_question}

Answer:
"""

    response = chain.invoke(prompt)

    st.write("Reply:")
    st.write(response.content)


# ---------------- STREAMLIT UI ----------------

def main():
    st.set_page_config(page_title="Chat with Multiple PDF")
    st.header("Chat with Multiple PDF using GENAI")

    user_question = st.text_input("Ask a question about your PDF:")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu : ")
        pdf_docs = st.file_uploader(
            "Upload your PDF here and click on Process",
            accept_multiple_files=True,
            type=["pdf"]
        )

        if st.button("Submit & Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vectorstore(text_chunks)
                    st.success("PDF processed successfully! You can now ask questions about your PDF.")
            else:
                st.warning("Please upload at least one PDF file.")


if __name__ == "__main__":
    main()