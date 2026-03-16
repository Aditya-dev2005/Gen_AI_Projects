from dotenv import load_dotenv
load_dotenv()  # loads variables from .env file into environment

import streamlit as st
import os
from openai import OpenAI   # using OpenAI compatible client for OpenRouter

# configure OpenRouter client using your API key
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),   # we now use OPENROUTER_API_KEY instead of GOOGLE_API_KEY
    base_url="https://openrouter.ai/api/v1"    # OpenRouter base URL
)

##function to load model and get response
# earlier we were loading gemini-pro model
# now we are using a chat model from OpenRouter
model = "meta-llama/llama-3-8b-instruct"  # stable free model we decided to use

# we will not use start_chat like Gemini
# instead we will manage chat history manually using Streamlit session_state

def get_gemini_response(question):
    # this function sends the user question to OpenRouter
    # and returns full response text
    
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state['chat_history'] + [
            {"role": "user", "content": question}
        ],
        max_tokens=300
    )
    
    # returning assistant message content
    return response.choices[0].message.content


#initialise our streamlit app
st.set_page_config(page_title="Q&A demo")  # keeping same title
st.header("Gemini LLM Application")  # keeping same header


#initialise session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    # OpenAI format requires role + content
    st.session_state['chat_history'] = []


input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")


if submit and input:
    response = get_gemini_response(input)
    
    ##add user query and response to session chat history
    st.session_state['chat_history'].append({"role": "user", "content": input})
    
    st.subheader("The response is : ")
    st.write(response)
    
    st.session_state['chat_history'].append({"role": "assistant", "content": response})


st.subheader("Chat History")

# displaying chat history in readable format
for message in st.session_state['chat_history']:
    role = "You" if message["role"] == "user" else "Bot"
    text = message["content"]
    st.write(f"**{role}:** {text}")