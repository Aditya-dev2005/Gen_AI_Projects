import streamlit as st
import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(page_title="Vision AI App")
st.title("AI Vision App (OpenRouter)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
user_input = st.text_input("Ask something about the image:")

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

def get_response(prompt, image_base64):
    completion = client.chat.completions.create(
        model="meta-llama/llama-3.2-11b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return completion.choices[0].message.content

if st.button("Submit"):
    if uploaded_file and user_input:
        with st.spinner("Analyzing image..."):
            image_base64 = encode_image(uploaded_file)
            reply = get_response(user_input, image_base64)
        st.image(uploaded_file, caption="Uploaded Image")
        st.write("### AI Response:")
        st.write(reply)
    else:
        st.warning("Please upload an image and enter a question.")