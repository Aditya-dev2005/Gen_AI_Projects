from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PyPDF2 import PdfReader
from openai import OpenAI


# ---------------- OPENROUTER CONFIG ---------------- #

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


# ---------------- PDF TEXT EXTRACTION ---------------- #

def extract_resume_text(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# ---------------- LLM RESPONSE ---------------- #

def get_llm_response(prompt, job_description, resume_text):
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"""
JOB DESCRIPTION:
{job_description}

CANDIDATE RESUME:
{resume_text}
"""
            }
        ]
    )

    return response.choices[0].message.content


def get_chat_response(user_question, resume_text, job_description, chat_history):
    """Generate response for resume-related questions"""
    
    messages = [
        {
            "role": "system",
            "content": """You are a helpful ATS and recruitment expert assistant. 
The user is asking questions about their resume in the context of a job description.
Provide helpful, specific, and actionable advice based on their resume and the job requirements.
Be concise but thorough. Focus on practical improvements and clarifications."""
        }
    ]
    
    # Add conversation history
    for msg in chat_history:
        messages.append({
            "role": "user" if msg["role"] == "user" else "assistant",
            "content": msg["content"]
        })
    
    # Add current question with context
    messages.append({
        "role": "user",
        "content": f"""
RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

USER QUESTION:
{user_question}
"""
    })
    
    response = client.chat.completions.create(
        model="meta-llama/llama-3-70b-instruct",
        temperature=0.7,
        messages=messages
    )
    
    return response.choices[0].message.content


# ---------------- STREAMLIT CONFIG ---------------- #

st.set_page_config(
    page_title="ATS Resume Expert",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Corporate Color Scheme - Green & Gold
PRIMARY_COLOR = "#2D5016"  # Professional Green
SECONDARY_COLOR = "#1F3A0F"  # Dark Green
ACCENT_COLOR = "#D4AF37"  # Gold accent
BG_DARK = "#0F1419"  # Very dark blue-black
BG_LIGHT = "#1A2332"  # Dark blue-gray
TEXT_PRIMARY = "#E8EAED"  # Light gray
TEXT_SECONDARY = "#9CA3AF"  # Medium gray
SUCCESS_COLOR = "#4CAF50"  # Success green
INPUT_BG = "#1A2A3A"  # Dark input background
BORDER_COLOR = "#D4AF37"  # Gold border

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
        background-color: rgba({45}, {80}, {22}, 0.15);
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
        background: linear-gradient(135deg, {BORDER_COLOR} 0%, {PRIMARY_COLOR} 100%);
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

    .tab-container {{
        display: flex;
        gap: 10px;
        margin-bottom: 25px;
        flex-wrap: wrap;
    }}

    .input-section {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({45}, {80}, {22}, 0.1) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba({212}, {175}, {55}, 0.2);
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

    [data-testid="stTextArea"] textarea {{
        background-color: {INPUT_BG} !important;
        border: 1px solid {BORDER_COLOR} !important;
        color: {TEXT_PRIMARY} !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }}

    [data-testid="stTextArea"] textarea:focus {{
        border-color: {PRIMARY_COLOR} !important;
        box-shadow: 0 0 0 2px rgba({45}, {80}, {22}, 0.2) !important;
    }}

    [data-testid="stFileUploader"] {{
        color: {TEXT_PRIMARY};
    }}

    [data-testid="stFileUploader"] label {{
        color: {TEXT_PRIMARY} !important;
    }}

    [data-testid="stButton"] button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%) !important;
        color: {ACCENT_COLOR} !important;
        border: 1px solid {BORDER_COLOR} !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 12px rgba({212}, {175}, {55}, 0.2) !important;
    }}

    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba({212}, {175}, {55}, 0.3) !important;
        background: linear-gradient(135deg, {SECONDARY_COLOR} 0%, {PRIMARY_COLOR} 100%) !important;
    }}

    [data-testid="stButton"] button:active {{
        transform: translateY(0) !important;
    }}

    .success-message {{
        background-color: rgba({76}, {175}, {80}, 0.15);
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

    .result-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({45}, {80}, {22}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid {BORDER_COLOR};
        margin-top: 25px;
        box-shadow: 0 8px 24px rgba({212}, {175}, {55}, 0.1);
    }}

    .result-title {{
        color: {ACCENT_COLOR};
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 0.3px;
    }}

    .result-content {{
        color: {TEXT_PRIMARY};
        line-height: 1.6;
        font-size: 14px;
    }}

    .chat-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({45}, {80}, {22}, 0.08) 100%);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid {BORDER_COLOR};
        margin-top: 25px;
        box-shadow: 0 8px 24px rgba({212}, {175}, {55}, 0.1);
    }}

    .chat-header {{
        color: {ACCENT_COLOR};
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}

    .messages-wrapper {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        margin-bottom: 15px;
        max-height: 400px;
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
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        padding: 12px 16px;
        border-radius: 10px;
        margin-left: 40px;
        margin-right: 0;
        color: {TEXT_PRIMARY};
        word-wrap: break-word;
        border: 1px solid rgba({212}, {175}, {55}, 0.3);
        animation: slideInRight 0.3s ease-out;
        font-size: 13px;
        line-height: 1.5;
    }}

    .assistant-message {{
        background: linear-gradient(135deg, rgba({45}, {80}, {22}, 0.3) 0%, {BG_LIGHT} 100%);
        padding: 12px 16px;
        border-radius: 10px;
        margin-left: 0;
        margin-right: 40px;
        color: {TEXT_PRIMARY};
        word-wrap: break-word;
        border: 1px solid {BORDER_COLOR};
        animation: slideInLeft 0.3s ease-out;
        font-size: 13px;
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
        box-shadow: 0 0 0 2px rgba({45}, {80}, {22}, 0.2) !important;
    }}

    .empty-state {{
        text-align: center;
        padding: 30px 20px;
        color: {TEXT_SECONDARY};
    }}

    .empty-state-icon {{
        font-size: 36px;
        margin-bottom: 12px;
    }}

    .empty-state-text {{
        font-size: 14px;
        color: {TEXT_PRIMARY};
        margin-bottom: 6px;
    }}

</style>
""", unsafe_allow_html=True)

# Initialize session state for chat
if "resume_chat_history" not in st.session_state:
    st.session_state.resume_chat_history = []

if "current_resume_text" not in st.session_state:
    st.session_state.current_resume_text = None

if "current_job_description" not in st.session_state:
    st.session_state.current_job_description = None

# Sidebar
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">📄 ATS Resume Expert</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-subtitle">Professional Resume Analysis</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🎯 Purpose</div>
        <div class="info-value">Optimize resumes for App Developer, SDE, and Generative AI roles</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">⚙️ Model</div>
        <div class="info-value">Llama 3 70B Instruct</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🔌 Provider</div>
        <div class="info-value">OpenRouter</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.resume_chat_history = []
        st.success("Chat history cleared!")

# Main content
st.markdown('<div class="main-header">ATS Resume Expert</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Analyze, optimize, and improve your resume for technical roles with AI-powered insights</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown('<div class="section-title">📝 Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        "",
        height=200,
        placeholder="Paste the job description here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-title">📄 Upload Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "",
        type=["pdf"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.markdown(f'<div class="success-message">✓ Resume uploaded successfully</div>', unsafe_allow_html=True)
        # Store resume text in session state
        st.session_state.current_resume_text = extract_resume_text(uploaded_file)
        st.session_state.current_job_description = job_description

st.markdown('</div>', unsafe_allow_html=True)

# Prompts
analysis_prompt = """
You are a Senior Technical Recruiter and ATS (Applicant Tracking System) expert with extensive experience hiring candidates for:

• App Developer roles  
• Software Development Engineer (SDE) roles  
• Generative AI / AI Engineer roles  

Your task is to analyze a candidate resume in relation to a given job description.

Generate a structured evaluation with the following sections:

1. Candidate Profile Overview
- Brief summary of the candidate
- Education background
- Primary technical specialization

2. Technical Skills Evaluation
Analyze technical skills found in the resume including:
- Programming languages
- App development frameworks
- Backend development technologies
- Databases
- Software engineering fundamentals
- AI / Generative AI technologies
- Development tools and platforms

Explain how these align with the job description.

3. Project Assessment
Evaluate projects mentioned in the resume:
- Technical complexity
- Technologies used
- Relevance to the job role
- Real-world impact or practical implementation

4. Internship / Work Experience
Analyze any professional or internship experience:
- Engineering practices demonstrated
- Responsibilities handled
- Relevance to the job role

5. Candidate Strengths
List the strongest aspects of the candidate relative to the job description.

6. Candidate Weaknesses
Identify gaps such as:
- Missing technologies
- Lack of experience
- Weak project depth
- Missing ATS keywords

7. ATS Optimization
Evaluate whether the resume is optimized for ATS systems and explain any structural improvements needed.

Provide the response clearly with bullet points and structured sections.
"""

improvement_prompt = """
You are a Senior Technical Recruiter specializing in resume optimization for:

• App Developer internships
• Software Development Engineer (SDE) internships
• Generative AI / AI Engineer internships

Based on the job description and candidate resume, provide improvement suggestions.

Structure the response with the following sections:

1. Skills to Learn or Improve
List important skills from the job description that the candidate should learn or strengthen.

2. Recommended Projects
Suggest 3–5 strong projects that would significantly strengthen the resume.
For each project include:
- Project title
- Key technologies
- What the project should demonstrate
- Why it improves the candidate's profile

3. Resume Content Improvements
Suggest how the candidate can improve:
- Project descriptions
- Technical explanations
- Quantification of achievements
- Clarity of technical experience

4. Missing Resume Sections
Recommend sections the candidate should include if missing:
- Open source contributions
- Research or experimentation
- Technical blogs
- Certifications
- Portfolio or GitHub links

5. ATS Keyword Optimization
List important technical keywords from the job description that should be included in the resume.

Provide practical and actionable suggestions suitable for internship applicants.
"""

match_prompt = """
You are an ATS (Applicant Tracking System) evaluator used by technology companies.

Your task is to evaluate how well a candidate resume matches a given job description for roles such as:

• App Developer
• Software Development Engineer (SDE)
• Generative AI / AI Engineer

Perform the following analysis:

1. ATS Match Score
Provide a percentage score between 0% and 100%.

2. Matching Skills
List the technical skills found in the resume that match the job description.

3. Missing Skills
List important skills from the job description that are missing in the resume.

4. Experience Match
Evaluate whether the candidate's projects, internships, or experience align with the job requirements.

5. Keyword Match
Identify important ATS keywords that appear in the resume and those that are missing.

6. Final Hiring Recommendation
Provide a recruiter-style conclusion indicating whether the candidate would likely pass an ATS screening and whether they should be shortlisted for an interview.

Return the result clearly structured with headings and bullet points.
"""

# Analysis Buttons
st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    analyze_btn = st.button("📊 Resume Analysis", use_container_width=True)

with col2:
    improve_btn = st.button("✨ Skill & Resume Improvement", use_container_width=True)

with col3:
    match_btn = st.button("🎯 ATS Match Score", use_container_width=True)

# Button Logic
if analyze_btn:
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        with st.spinner("⏳ Analyzing resume..."):
            result = get_llm_response(
                analysis_prompt,
                job_description,
                resume_text
            )
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">📊 Resume Analysis Report</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-content">{result}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-message">⚠️ Please upload a resume and provide a job description.</div>', unsafe_allow_html=True)

elif improve_btn:
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        with st.spinner("⏳ Generating improvement suggestions..."):
            result = get_llm_response(
                improvement_prompt,
                job_description,
                resume_text
            )
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">✨ Resume Improvement Suggestions</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-content">{result}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-message">⚠️ Please upload a resume and provide a job description.</div>', unsafe_allow_html=True)

elif match_btn:
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        with st.spinner("⏳ Calculating ATS match score..."):
            result = get_llm_response(
                match_prompt,
                job_description,
                resume_text
            )
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">🎯 ATS Match Score and Evaluation</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-content">{result}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="error-message">⚠️ Please upload a resume and provide a job description.</div>', unsafe_allow_html=True)

# Chat Section - Only show if resume and job description are provided
if uploaded_file and job_description:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">💬 Resume Q&A Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #9CA3AF; font-size: 13px; margin-bottom: 15px;">Ask specific questions about your resume and how it aligns with the job description</div>', unsafe_allow_html=True)
    
    # Display chat history
    if st.session_state.resume_chat_history:
        st.markdown('<div class="messages-wrapper">', unsafe_allow_html=True)
        for msg in st.session_state.resume_chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-state-icon">🤔</div>
            <div class="empty-state-text">Ask a question about your resume</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    col_input, col_button = st.columns([5, 1], gap="small")
    
    with col_input:
        chat_input = st.text_input(
            "",
            placeholder="E.g., How can I highlight my AI experience better?",
            label_visibility="collapsed",
            key="resume_chat_input"
        )
    
    with col_button:
        send_chat = st.button("Send", use_container_width=True, key="send_chat_btn")
    
    # Handle chat input
    if send_chat and chat_input:
        # Add user message to history
        st.session_state.resume_chat_history.append({
            "role": "user",
            "content": chat_input
        })
        
        # Get AI response
        with st.spinner("⏳ Thinking..."):
            ai_response = get_chat_response(
                chat_input,
                st.session_state.current_resume_text,
                st.session_state.current_job_description,
                st.session_state.resume_chat_history[:-1]  # Exclude the message we just added
            )
        
        # Add assistant response to history
        st.session_state.resume_chat_history.append({
            "role": "assistant",
            "content": ai_response
        })
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

else:
    if uploaded_file or job_description:
        st.markdown(f'<div class="error-message">⚠️ Please upload both a resume and job description to use the Q&A Assistant.</div>', unsafe_allow_html=True)