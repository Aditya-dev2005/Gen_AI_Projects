import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Corporate Color Scheme
PRIMARY_COLOR = "#0066CC"  # Professional Blue
SECONDARY_COLOR = "#003D99"  # Darker Blue
ACCENT_COLOR = "#00D9FF"  # Cyan accent
BG_DARK = "#0A0E27"  # Very dark blue-black
BG_LIGHT = "#1A2847"  # Dark blue
TEXT_PRIMARY = "#E8EAED"  # Light gray
TEXT_SECONDARY = "#9CA3AF"  # Medium gray
USER_MSG_BG = "#0D47A1"  # Deep blue for user
BOT_MSG_BG = "#1565C0"  # Lighter blue for bot
BORDER_COLOR = "#00D9FF"  # Cyan border

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
        background: linear-gradient(135deg, {BG_LIGHT} 0%, {SECONDARY_COLOR} 100%);
        border-right: 2px solid {BORDER_COLOR};
    }}

    [data-testid="stSidebarContent"] {{
        padding-top: 20px;
    }}

    .sidebar-header {{
        font-size: 24px;
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
        background-color: rgba({0}, {102}, {204}, 0.1);
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

    .chat-container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 0 20px;
    }}

    .messages-wrapper {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 30px;
        max-height: 600px;
        overflow-y: auto;
        padding-right: 10px;
    }}

    .messages-wrapper::-webkit-scrollbar {{
        width: 6px;
    }}

    .messages-wrapper::-webkit-scrollbar-track {{
        background: {BG_LIGHT};
        border-radius: 10px;
    }}

    .messages-wrapper::-webkit-scrollbar-thumb {{
        background: {BORDER_COLOR};
        border-radius: 10px;
    }}

    .user-message {{
        background: linear-gradient(135deg, {USER_MSG_BG} 0%, {PRIMARY_COLOR} 100%);
        padding: 14px 18px;
        border-radius: 12px;
        margin-left: 60px;
        margin-right: 0;
        color: {TEXT_PRIMARY};
        word-wrap: break-word;
        border: 1px solid rgba({0}, {217}, {255}, 0.2);
        box-shadow: 0 4px 12px rgba({0}, {102}, {204}, 0.15);
        animation: slideInRight 0.3s ease-out;
        font-size: 14px;
        line-height: 1.5;
    }}

    .bot-message {{
        background: linear-gradient(135deg, {BOT_MSG_BG} 0%, {BG_LIGHT} 100%);
        padding: 14px 18px;
        border-radius: 12px;
        margin-left: 0;
        margin-right: 60px;
        color: {TEXT_PRIMARY};
        word-wrap: break-word;
        border: 1px solid {BORDER_COLOR};
        box-shadow: 0 4px 12px rgba({0}, {217}, {255}, 0.1);
        animation: slideInLeft 0.3s ease-out;
        font-size: 14px;
        line-height: 1.5;
    }}

    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    @keyframes slideInLeft {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}

    .input-container {{
        display: flex;
        gap: 10px;
        margin-top: 20px;
        margin-bottom: 20px;
    }}

    [data-testid="stTextInput"] {{
        flex: 1;
    }}

    [data-testid="stTextInput"] input {{
        background-color: {BG_LIGHT} !important;
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
        box-shadow: 0 0 0 2px rgba({0}, {102}, {204}, 0.2) !important;
    }}

    [data-testid="stButton"] button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 12px rgba({0}, {102}, {204}, 0.3) !important;
    }}

    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba({0}, {102}, {204}, 0.4) !important;
    }}

    [data-testid="stButton"] button:active {{
        transform: translateY(0) !important;
    }}

    [data-testid="stSpinner"] {{
        color: {ACCENT_COLOR} !important;
    }}

    .stSpinner {{
        color: {ACCENT_COLOR} !important;
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

    .timestamp {{
        font-size: 11px;
        color: {TEXT_SECONDARY};
        margin-top: 6px;
        opacity: 0.7;
    }}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">🤖 AI Assistant</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-subtitle">Powered by Advanced AI</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">📊 Model</div>
        <div class="info-value">Llama 3 8B Instruct</div>
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
        <div class="info-label">⚙️ Max Tokens</div>
        <div class="info-value">200 per response</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main content
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

st.markdown('<div class="main-header">Chat with AI</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Ask anything and get intelligent, instant responses</div>', unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
if st.session_state.messages:
    st.markdown('<div class="messages-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-state-icon">💬</div>
        <div class="empty-state-text">Start a conversation</div>
        <div style="color: {TEXT_SECONDARY}; font-size: 13px;">Ask me anything and I'll help you out</div>
    </div>
    """, unsafe_allow_html=True)

# Get response function
def get_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return completion.choices[0].message.content or "No response generated."
    except Exception as e:
        return f"Error: {str(e)}"

# Input section
user_input = st.text_input("", placeholder="Type your message here...", label_visibility="collapsed")

# Handle send - only when button is clicked
if st.button("Send", use_container_width=True):
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("⏳ Generating response..."):
            reply = get_response(user_input)

        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)