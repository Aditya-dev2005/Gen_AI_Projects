from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3

from langchain_openai import ChatOpenAI


# Professional Corporate Color Scheme - Teal & Cyan for Database/Tech
PRIMARY_COLOR = "#0D9488"  # Professional Teal
SECONDARY_COLOR = "#0F766E"  # Deep Teal
ACCENT_COLOR = "#06B6D4"  # Cyan accent
BG_DARK = "#0F1419"  # Very dark blue-black
BG_LIGHT = "#1F2937"  # Dark gray
TEXT_PRIMARY = "#E8EAED"  # Light gray
TEXT_SECONDARY = "#9CA3AF"  # Medium gray
SUCCESS_COLOR = "#10B981"  # Success green
INPUT_BG = "#1A2332"  # Dark input background
BORDER_COLOR = "#06B6D4"  # Cyan border
WARNING_COLOR = "#F59E0B"  # Warning orange
ERROR_COLOR = "#EF4444"  # Error red


# ---------------- LLM FUNCTION ----------------

def get_llm_response(question, prompt):
    """Get SQL query from LLM based on natural language question"""
    model = ChatOpenAI(
        model="meta-llama/llama-3-8b-instruct",
        temperature=0,
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    full_prompt = prompt + "\nQuestion:\n" + question

    response = model.invoke(full_prompt)

    return response.content


# ---------------- SQL EXECUTION ----------------

def read_sql_query(sql, db):
    """Execute SQL query and return results"""
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()

        connection.commit()
        connection.close()

        return rows
    except Exception as e:
        st.error(f"Database Error: {str(e)}")
        return None


# Get table schema for display
def get_table_schema(db):
    """Get column information from STUDENT table"""
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        
        cursor.execute("PRAGMA table_info(STUDENT)")
        columns = cursor.fetchall()
        
        connection.close()
        return columns
    except:
        return None


# Get column names for table display
def get_column_names(db):
    """Get column names from STUDENT table"""
    try:
        connection = sqlite3.connect(db)
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM STUDENT LIMIT 0")
        columns = [description[0] for description in cursor.description]
        
        connection.close()
        return columns
    except:
        return ["NAME", "CLASS", "SECTION", "MARKS"]


# ---------------- PROMPT ----------------

prompt = """
You are an expert SQL assistant.

Given a question, generate an SQL query to retrieve the answer from a database.

The database has a table named STUDENT with the following columns:

NAME (VARCHAR)
CLASS (VARCHAR)
SECTION (VARCHAR)
MARKS (INT)

Only generate the SQL query.
Do not include explanation.
Return only the SQL query.
Do not include markdown formatting or backticks.
"""


# Initialize Streamlit app
st.set_page_config(
    page_title="SQL Query App",
    page_icon="🗄️",
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
        background-color: rgba({13}, {148}, {136}, 0.1);
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
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({13}, {148}, {136}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid rgba({6}, {182}, {212}, 0.2);
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
        box-shadow: 0 0 0 2px rgba({13}, {148}, {136}, 0.2) !important;
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
        box-shadow: 0 4px 12px rgba({13}, {148}, {136}, 0.25) !important;
    }}

    [data-testid="stButton"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba({13}, {148}, {136}, 0.35) !important;
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
        font-weight: 500;
    }}

    .error-message {{
        background-color: rgba({239}, {68}, {68}, 0.15);
        border-left: 4px solid {ERROR_COLOR};
        padding: 12px 15px;
        border-radius: 6px;
        color: #ffcdd2;
        margin-bottom: 15px;
        font-weight: 500;
    }}

    .warning-message {{
        background-color: rgba({245}, {158}, {11}, 0.15);
        border-left: 4px solid {WARNING_COLOR};
        padding: 12px 15px;
        border-radius: 6px;
        color: {WARNING_COLOR};
        margin-bottom: 15px;
        font-weight: 500;
    }}

    .result-container {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, rgba({13}, {148}, {136}, 0.08) 100%);
        padding: 25px;
        border-radius: 12px;
        border: 1px solid {BORDER_COLOR};
        margin-top: 25px;
        box-shadow: 0 8px 24px rgba({13}, {148}, {136}, 0.1);
    }}

    .result-title {{
        color: {ACCENT_COLOR};
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 15px;
        letter-spacing: 0.3px;
    }}

    .query-box {{
        background-color: {INPUT_BG};
        padding: 15px;
        border-radius: 8px;
        border: 1px solid {BORDER_COLOR};
        margin-bottom: 20px;
        font-family: 'Courier New', monospace;
        color: {ACCENT_COLOR};
        font-size: 12px;
        line-height: 1.5;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }}

    .query-label {{
        color: {TEXT_SECONDARY};
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}

    .data-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
    }}

    .data-table thead {{
        background-color: rgba({13}, {148}, {136}, 0.2);
    }}

    .data-table th {{
        color: {ACCENT_COLOR};
        padding: 12px;
        text-align: left;
        font-weight: 700;
        border-bottom: 2px solid {BORDER_COLOR};
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}

    .data-table td {{
        color: {TEXT_PRIMARY};
        padding: 10px 12px;
        border-bottom: 1px solid rgba({6}, {182}, {212}, 0.1);
        font-size: 13px;
    }}

    .data-table tbody tr:hover {{
        background-color: rgba({13}, {148}, {136}, 0.05);
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

    .schema-box {{
        background-color: rgba({13}, {148}, {136}, 0.1);
        padding: 15px;
        border-radius: 8px;
        border-left: 3px solid {BORDER_COLOR};
        margin-top: 10px;
    }}

    .schema-title {{
        color: {ACCENT_COLOR};
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }}

    .schema-item {{
        color: {TEXT_PRIMARY};
        font-size: 12px;
        padding: 5px 0;
        font-family: 'Courier New', monospace;
    }}

    .feature-list {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }}

    .feature-item {{
        background: rgba({13}, {148}, {136}, 0.1);
        padding: 12px;
        border-radius: 8px;
        border-left: 3px solid {BORDER_COLOR};
    }}

    .feature-icon {{
        color: {ACCENT_COLOR};
        font-size: 18px;
        margin-bottom: 6px;
    }}

    .feature-text {{
        color: {TEXT_PRIMARY};
        font-size: 12px;
        font-weight: 500;
    }}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">🗄️ SQL Query App</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-subtitle">Natural Language to SQL</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🎯 Purpose</div>
        <div class="info-value">Convert natural language questions to SQL queries</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🤖 Model</div>
        <div class="info-value">Llama 3 8B Instruct</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">💾 Database</div>
        <div class="info-value">SQLite (student.db)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <div class="info-label">🔌 Provider</div>
        <div class="info-value">OpenRouter</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-header" style="font-size: 14px; margin-bottom: 15px;">📊 Database Schema</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="schema-box">
        <div class="schema-title">STUDENT Table</div>
        <div class="schema-item">• NAME (VARCHAR)</div>
        <div class="schema-item">• CLASS (VARCHAR)</div>
        <div class="schema-item">• SECTION (VARCHAR)</div>
        <div class="schema-item">• MARKS (INT)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-list">
        <div class="feature-item">
            <div class="feature-icon">💬</div>
            <div class="feature-text">Natural Language</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🔄</div>
            <div class="feature-text">SQL Generation</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <div class="feature-text">Query Execution</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📈</div>
            <div class="feature-text">Data Display</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">🗄️ SQL Query Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Ask questions in natural language and get intelligent SQL queries with instant results</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)

st.markdown('<div class="section-title">🤔 Ask a Question</div>', unsafe_allow_html=True)

question = st.text_input(
    "",
    placeholder="e.g., Show all students who scored more than 80 marks in class 10",
    label_visibility="collapsed",
    key="input"
)

st.markdown('</div>', unsafe_allow_html=True)

# Submit Button
st.markdown('<div style="margin: 25px 0;"></div>', unsafe_allow_html=True)

col_button = st.columns([1, 4, 1])
with col_button[0]:
    submit = st.button("🚀 Execute Query", use_container_width=True)

# Query Execution Logic
if submit:
    if question.strip():
        try:
            # Get LLM response (SQL query)
            with st.spinner("⏳ Generating SQL query..."):
                sql_query = get_llm_response(question, prompt)
            
            # Display Result Container
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            
            # Display Generated Query
            st.markdown(f'<div class="result-title">📝 Generated SQL Query</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="query-label">Query:</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="query-box">{sql_query.strip()}</div>', unsafe_allow_html=True)
            
            # Execute Query
            with st.spinner("⏳ Executing query..."):
                result = read_sql_query(sql_query, "student.db")
            
            if result is not None and len(result) > 0:
                # Get column names
                columns = get_column_names("student.db")
                
                # Display Results
                st.markdown(f'<div class="result-title" style="margin-top: 20px;">📊 Query Results</div>', unsafe_allow_html=True)
                
                # Create table HTML
                table_html = '<table class="data-table"><thead><tr>'
                for col in columns:
                    table_html += f'<th>{col}</th>'
                table_html += '</tr></thead><tbody>'
                
                for row in result:
                    table_html += '<tr>'
                    for cell in row:
                        table_html += f'<td>{cell}</td>'
                    table_html += '</tr>'
                
                table_html += '</tbody></table>'
                
                st.markdown(table_html, unsafe_allow_html=True)
                
                # Display row count
                st.markdown(f'<div class="success-message">✓ Found {len(result)} row(s)</div>', unsafe_allow_html=True)
                
            elif result is not None and len(result) == 0:
                st.markdown(f'<div class="warning-message">ℹ️ Query executed successfully but no results found</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f'<div class="error-message">⚠️ Error: {str(e)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warning-message">ℹ️ Please enter a question to generate a SQL query</div>', unsafe_allow_html=True)