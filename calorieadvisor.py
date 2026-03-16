import streamlit as st
import os
import base64
from dotenv import load_dotenv
from PIL import Image
from openai import OpenAI

load_dotenv()

# ---------------- OPENROUTER CONFIG ---------------- #

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Calories Advisor",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Corporate Color Scheme - Orange & Red for Nutrition
PRIMARY_COLOR = "#D97706"  # Professional Orange
SECONDARY_COLOR = "#B91C1C"  # Deep Red
ACCENT_COLOR = "#FBBF24"  # Amber accent
BG_DARK = "#0F1419"  # Very dark blue-black
BG_LIGHT = "#1F2937"  # Dark gray
TEXT_PRIMARY = "#E8EAED"  # Light gray
TEXT_SECONDARY = "#9CA3AF"  # Medium gray
SUCCESS_COLOR = "#10B981"  # Success green
INPUT_BG = "#1A2332"  # Dark input background
BORDER_COLOR = "#FBBF24"  # Amber border

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
        background-color: rgba({217}, {119}, {6}, 0.1);
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
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({217}, {119}, {6}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba({251}, {191}, {36}, 0.2);
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
        box-shadow: 0 4px 12px rgba({217}, {119}, {6}, 0.25) !important;
    }}

    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba({217}, {119}, {6}, 0.35) !important;
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

    .image-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({217}, {119}, {6}, 0.08) 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid {BORDER_COLOR};
        box-shadow: 0 8px 24px rgba({217}, {119}, {6}, 0.1);
        overflow: hidden;
    }}

    .image-label {{
        color: {ACCENT_COLOR};
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .result-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({217}, {119}, {6}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid {BORDER_COLOR};
        margin-top: 25px;
        box-shadow: 0 8px 24px rgba({217}, {119}, {6}, 0.1);
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

    .result-section {{
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba({251}, {191}, {36}, 0.1);
    }}

    .result-section:last-child {{
        border-bottom: none;
    }}

    .result-section h3 {{
        color: {ACCENT_COLOR};
        margin-bottom: 10px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}

    .nutrition-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }}

    .nutrition-card {{
        background: linear-gradient(135deg, rgba({217}, {119}, {6}, 0.1) 0%, rgba({185}, {28}, {28}, 0.05) 100%);
        padding: 15px;
        border-radius: 8px;
        border: 1px solid rgba({251}, {191}, {36}, 0.2);
        text-align: center;
    }}

    .nutrition-label {{
        color: {TEXT_SECONDARY};
        font-size: 12px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}

    .nutrition-value {{
        color: {ACCENT_COLOR};
        font-size: 18px;
        font-weight: 700;
    }}

    .loading-spinner {{
        color: {ACCENT_COLOR} !important;
    }}

    .stSpinner {{
        color: {ACCENT_COLOR} !important;
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

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">🥗 AI Calories Advisor</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-subtitle">Professional Nutrition Analysis</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🎯 Purpose</div>
        <div class="info-value">AI-powered calorie estimation and comprehensive nutrition analysis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">📊 Model</div>
        <div class="info-value">GPT-4o Mini Vision</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🔌 Provider</div>
        <div class="info-value">OpenRouter</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🌡️ Temperature</div>
        <div class="info-value">0.3 (Precise)</div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">🥗 AI Calories Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Upload a food image and get AI-powered calorie estimation with comprehensive nutrition analysis</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Image Processing Function
def input_image_setup(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    base64_image = base64.b64encode(bytes_data).decode("utf-8")
    image_url = f"data:{uploaded_file.type};base64,{base64_image}"
    return image_url

# LLM Response Function
def get_openrouter_response(prompt, image):
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        temperature=0.3,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Analyze the food items in this image and estimate calories."},
                    {"type": "image_url", "image_url": {"url": image}}
                ]
            }
        ]
    )
    return response.choices[0].message.content

# Nutrition Analysis Prompt
input_prompt = """
You are a professional nutritionist and diet analysis expert.

Analyze the uploaded food image and provide a complete nutritional breakdown.

Your analysis should include:

1. Food Identification
Identify all food items present in the image.

2. Portion Size Estimation
Estimate approximate portion sizes.

3. Calorie Estimation
Provide estimated calories for each food item.

4. Total Calories
Calculate total calories for the entire meal.

5. Macronutrient Breakdown
Estimate:
- Protein
- Carbohydrates
- Fats
- Fiber

6. Health Evaluation
Explain whether the meal is balanced or unhealthy.

7. Diet Advice
Suggest healthier alternatives or improvements.

8. Fitness Recommendation
Explain whether the meal is suitable for:
- Weight loss
- Muscle gain
- Maintenance diet

Structure the response clearly with headings and bullet points.
"""

# Main Layout
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="medium")

# Left Column - Upload
with col1:
    st.markdown('<div class="section-title">📤 Upload Food Image</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f'<div class="success-message">✓ Image uploaded successfully</div>', unsafe_allow_html=True)

# Right Column - Preview
with col2:
    st.markdown('<div class="section-title">📷 Image Preview</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(image, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">📷</div>
            <div class="empty-state-text">No image uploaded yet</div>
            <div style="color: {TEXT_SECONDARY}; font-size: 13px;">Upload an image to see preview</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Analyze Button
st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)

col_button = st.columns([1, 4, 1])
with col_button[0]:
    analyze_button = st.button("🔍 Analyze Calories", use_container_width=True)

# Analysis Logic
if analyze_button:
    if uploaded_file is not None:
        image_data = input_image_setup(uploaded_file)
        
        with st.spinner("⏳ Analyzing nutrition and calories..."):
            response = get_openrouter_response(input_prompt, image_data)
        
        # Display Result
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">📊 Nutrition Analysis Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-content">{response}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        st.markdown(f'<div class="error-message">⚠️ Please upload a food image first.</div>', unsafe_allow_html=True)