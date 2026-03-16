from dotenv import load_dotenv
load_dotenv()  # load environment variables

import streamlit as st
import os
import base64
from PIL import Image
from openai import OpenAI  # OpenRouter uses OpenAI compatible client

## Configure OpenRouter API key
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),  # get API key from .env
    base_url="https://openrouter.ai/api/v1"   # OpenRouter base URL
)

## Function to load model and get response
model = "meta-llama/llama-3.2-11b-vision-instruct"  # vision capable model

def get_gemini_response(input, image, prompt):
    """Send text + image to vision model for invoice analysis"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": input},   # user question
                    {"type": "text", "text": prompt},  # system instruction
                    {
                        "type": "image_url",           # image input
                        "image_url": {
                            "url": image[0]["data"]    # base64 image
                        },
                    },
                ],
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content


def input_image_setup(uploaded_file):
    """Convert uploaded image to base64 format"""
    if uploaded_file is not None:
        # read file into bytes
        bytes_data = uploaded_file.getvalue()
        
        # convert image to base64
        base64_image = base64.b64encode(bytes_data).decode("utf-8")
        
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # detect image type
                "data": f"data:{uploaded_file.type};base64,{base64_image}"
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Professional Corporate Color Scheme - Purple & Indigo for Documents/Business
PRIMARY_COLOR = "#6366F1"  # Professional Indigo
SECONDARY_COLOR = "#4F46E5"  # Deep Indigo
ACCENT_COLOR = "#A78BFA"  # Light Purple accent
BG_DARK = "#0F1419"  # Very dark blue-black
BG_LIGHT = "#1F2937"  # Dark gray
TEXT_PRIMARY = "#E8EAED"  # Light gray
TEXT_SECONDARY = "#9CA3AF"  # Medium gray
SUCCESS_COLOR = "#10B981"  # Success green
INPUT_BG = "#1A2332"  # Dark input background
BORDER_COLOR = "#A78BFA"  # Light purple border

# Initialize Streamlit app
st.set_page_config(
    page_title="Multi Language Invoice Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {BG_DARK};
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, {SECONDARY_COLOR}22 100%);
        border-right: 2px solid {BORDER_COLOR};
    }}

    [data-testid="stSidebarContent"] {{
        padding-top: 20px;
    }}

    .sidebar-header {{
        font-size: 22px;
        font-weight: 700;
        color: {ACCENT_COLOR};
        margin-bottom: 5px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }}

    .sidebar-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 13px;
        margin-bottom: 20px;
        letter-spacing: 0.3px;
    }}

    .sidebar-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {BORDER_COLOR}, transparent);
        margin: 20px 0;
    }}

    .info-box {{
        background-color: rgba({99}, {102}, {241}, 0.1);
        border-left: 4px solid {BORDER_COLOR};
        padding: 12px 15px;
        border-radius: 6px;
        margin: 10px 0;
        color: {TEXT_PRIMARY};
        font-size: 13px;
    }}

    .info-label {{
        color: {ACCENT_COLOR};
        font-weight: 600;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
    }}

    .info-value {{
        color: {TEXT_PRIMARY};
        font-size: 13px;
    }}

    .main-header {{
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, {ACCENT_COLOR} 0%, {PRIMARY_COLOR} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }}

    .main-subtitle {{
        color: {TEXT_SECONDARY};
        font-size: 16px;
        margin-bottom: 30px;
        font-weight: 400;
        letter-spacing: 0.3px;
    }}

    .input-section {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({99}, {102}, {241}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba({167}, {139}, {250}, 0.2);
        margin-bottom: 25px;
    }}

    .section-title {{
        color: {ACCENT_COLOR};
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    [data-testid="stFileUploader"] {{
        color: {TEXT_PRIMARY};
    }}

    [data-testid="stFileUploader"] label {{
        color: {TEXT_PRIMARY} !important;
    }}

    [data-testid="stTextInput"] input {{
        background-color: {INPUT_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
        color: {TEXT_PRIMARY} !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }}

    [data-testid="stTextInput"] input::placeholder {{
        color: {TEXT_SECONDARY} !important;
    }}

    [data-testid="stTextInput"] input:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px rgba({99}, {102}, {241}, 0.2) !important;
    }}

    [data-testid="stButton"] button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%) !important;
        color: white !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 12px rgba({99}, {102}, {241}, 0.25) !important;
    }}

    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba({99}, {102}, {241}, 0.35) !important;
        background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, {PRIMARY_COLOR} 100%) !important;
    }}

    [data-testid="stButton"] button:active {{
        transform: translateY(0) !important;
    }}

    .success-message {{
        background-color: rgba({16}, {185}, {129}, 0.15);
        border-left: 4px solid {SUCCESS_COLOR};
        padding: 12px 15px;
        border-radius: 6px;
        color: {SUCCESS_COLOR};
        margin-bottom: 15px;
    }}

    .error-message {{
        background-color: rgba({244}, {67}, {54}, 0.15);
        border-left: 4px solid #f44336;
        padding: 12px 15px;
        border-radius: 6px;
        color: #ffcdd2;
        margin-bottom: 15px;
    }}

    .document-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({99}, {102}, {241}, 0.08) 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid {BORDER_COLOR};
        box-shadow: 0 8px 24px rgba({99}, {102}, {241}, 0.1);
        overflow: hidden;
    }}

    .document-label {{
        color: {ACCENT_COLOR};
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .result-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({99}, {102}, {241}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid {BORDER_COLOR};
        margin-top: 25px;
        box-shadow: 0 8px 24px rgba({99}, {102}, {241}, 0.1);
    }}

    .result-title {{
        color: {ACCENT_COLOR};
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 20px;
        letter-spacing: 0.3px;
    }}

    .result-content {{
        color: {TEXT_PRIMARY};
        line-height: 1.7;
        font-size: 14px;
    }}

    .divider {{
        height: 2px;
        background: linear-gradient(90deg, transparent, {BORDER_COLOR}, transparent);
        margin: 25px 0;
    }}

    .empty-state {{
        text-align: center;
        padding: 40px 20px;
        color: {TEXT_SECONDARY};
    }}

    .empty-state-icon {{
        font-size: 48px;
        margin-bottom: 16px;
    }}

    .empty-state-text {{
        font-size: 16px;
        color: {TEXT_PRIMARY};
        margin-bottom: 8px;
    }}

    .feature-list {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }}

    .feature-item {{
        background: rgba({99}, {102}, {241}, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid {BORDER_COLOR};
    }}

    .feature-icon {{
        color: {ACCENT_COLOR};
        font-size: 20px;
        margin-bottom: 8px;
    }}

    .feature-text {{
        color: {TEXT_PRIMARY};
        font-size: 13px;
        font-weight: 500;
    }}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">📄 Invoice Extractor</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-subtitle">Multi-Language Document Analysis</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🎯 Purpose</div>
        <div class="info-value">Extract and analyze invoice information in multiple languages</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🤖 Model</div>
        <div class="info-value">Llama 3.2 11B Vision</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🌍 Languages</div>
        <div class="info-value">All major languages supported</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🔌 Provider</div>
        <div class="info-value">OpenRouter</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-list">
        <div class="feature-item">
            <div class="feature-icon">📋</div>
            <div class="feature-text">Invoice Details</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">💰</div>
            <div class="feature-text">Amount Extraction</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🌐</div>
            <div class="feature-text">Multi-Language</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">✔️</div>
            <div class="feature-text">Data Validation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">📄 Multi Language Invoice Extractor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Upload invoice documents and extract information intelligently with AI-powered vision analysis</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

# Left Column - Input
with col1:
    st.markdown('<div class="section-title">🤔 Ask About Invoice</div>', unsafe_allow_html=True)
    
    input_prompt_user = st.text_input(
        "",
        placeholder="e.g., What is the total amount? Who is the vendor? What's the invoice date?",
        label_visibility="collapsed"
    )

# Right Column - Upload
with col2:
    st.markdown('<div class="section-title">📤 Upload Invoice</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f'<div class="success-message">✓ Invoice uploaded successfully</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Document Preview
st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)

if uploaded_file is not None:
    st.markdown('<div class="document-container">', unsafe_allow_html=True)
    st.markdown('<div class="document-label">📸 Invoice Preview</div>', unsafe_allow_html=True)
    
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# System Prompt
input_prompt = """You are an expert in understanding invoices from around the world. 
We will upload an image of invoices and you will have to answer any questions based on 
the uploaded image of invoices. Provide accurate, structured, and detailed information 
about the invoice contents. Support multi-language documents and extract key information 
such as invoice number, date, vendor, customer, amounts, taxes, and line items."""

# Submit Button
st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)

col_button = st.columns([1, 4, 1])
with col_button[0]:
    submit = st.button("🔍 Analyze Invoice", use_container_width=True)

# Analysis Logic
if submit:
    if uploaded_file is not None:
        if input_prompt_user.strip():
            try:
                image_data = input_image_setup(uploaded_file)
                
                with st.spinner("⏳ Analyzing invoice..."):
                    response = get_gemini_response(
                        input_prompt_user,
                        image_data,
                        input_prompt
                    )
                
                # Display Result
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown('<div class="result-title">📋 Invoice Analysis Result</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-content">{response}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
            except FileNotFoundError:
                st.markdown(f'<div class="error-message">⚠️ Error: Could not process the image. Please try again.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">⚠️ Please ask a question about the invoice.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-message">⚠️ Please upload an invoice image first.</div>', unsafe_allow_html=True)