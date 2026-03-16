import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
import re

load_dotenv()

# ---------------- OPENROUTER CONFIG ---------------- #

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="YouTube Notes Generator",
    page_icon="🎥",
    layout="wide"
)

st.markdown(
"""
# 🎥 YouTube Video Notes Generator

Convert any **YouTube video transcript into structured notes using AI**.
Paste a video link and generate **clear study notes instantly.**
"""
)

st.divider()

# ---------------- PROMPT ---------------- #

prompt = """
You are an expert AI assistant specialized in summarizing educational YouTube videos.

You will receive a transcript from a video.

Your task:

Create structured study notes summarizing the key information.

Rules:
• Summary must be between **200–250 words**
• Use **bullet points**
• Focus only on **important concepts**
• Avoid filler sentences
• Highlight important insights and takeaways

Output should look like **clean study notes** someone could revise quickly.
"""

# ---------------- TRANSCRIPT EXTRACTION ---------------- #

def extract_video_id(youtube_url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([^&]+)',
        r'(?:youtu\.be\/)([^?]+)',
        r'(?:youtube\.com\/embed\/)([^?]+)',
        r'(?:youtube\.com\/v\/)([^?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

def extract_transcript_details(youtube_video_url):
    try:
        # Extract video ID
        video_id = extract_video_id(youtube_video_url)
        
        if not video_id:
            st.error("Could not extract video ID from the URL")
            return None
        
        # For version 1.2.4, we need to use this approach
        try:
            # Try to get transcript in English first
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to find a manually created English transcript
            try:
                transcript = transcript_list.find_manually_created_transcript(['en'])
            except:
                # If no manual transcript, try automatically generated one
                try:
                    transcript = transcript_list.find_generated_transcript(['en'])
                except:
                    # If no English, get any available transcript and translate it
                    transcript = transcript_list.find_transcript(['en'])
            
            # Fetch the actual transcript
            transcript_data = transcript.fetch()
            
            # Combine all text
            transcript_text = ""
            for item in transcript_data:
                transcript_text += " " + item['text']
            
            return transcript_text.strip()
            
        except NoTranscriptFound:
            st.error("No transcript found for this video in English")
            return None
        except TranscriptsDisabled:
            st.error("Transcripts are disabled for this video")
            return None
        except VideoUnavailable:
            st.error("This video is unavailable")
            return None
        except Exception as e:
            # Fallback method - try direct get_transcript
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                transcript_text = ""
                for item in transcript:
                    transcript_text += " " + item['text']
                return transcript_text.strip()
            except Exception as inner_e:
                st.error(f"Could not fetch transcript: {str(inner_e)}")
                return None

    except Exception as e:
        st.error(f"Transcript Error: {str(e)}")
        return None

# ---------------- SUMMARY GENERATION ---------------- #

def generate_summary(transcript_text):
    try:
        if not transcript_text or len(transcript_text.strip()) < 50:
            st.error("Transcript is too short to generate meaningful notes")
            return None
            
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": transcript_text[:10000]}  # Limit transcript length
            ]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None

# ---------------- INPUT ---------------- #

st.subheader("🔗 Enter YouTube Video Link")

youtube_link = st.text_input("Paste the YouTube video URL here", placeholder="https://www.youtube.com/watch?v=...")

# ---------------- VIDEO PREVIEW ---------------- #

if youtube_link:
    video_id = extract_video_id(youtube_link)
    
    if video_id:
        # Create embed URL for better compatibility
        embed_url = f"https://www.youtube.com/watch?v={video_id}"
        st.video(embed_url)
    else:
        st.warning("Please enter a valid YouTube link.")

st.divider()

# Create columns for button layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate_button = st.button("📝 Generate Detailed Notes", use_container_width=True)

# ---------------- BUTTON LOGIC ---------------- #

if generate_button:
    if youtube_link:
        with st.spinner("🔄 Extracting transcript and generating notes..."):
            
            transcript_text = extract_transcript_details(youtube_link)
            
            if transcript_text:
                # Show transcript preview
                with st.expander("📝 View extracted transcript (preview)"):
                    st.text(transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text)
                
                # Show transcript stats
                st.info(f"📊 Transcript length: {len(transcript_text.split())} words")
                
                # Generate summary
                summary = generate_summary(transcript_text)
                
                if summary:
                    st.subheader("📚 Video Summary Notes")
                    
                    # Create a nice container for the summary
                    with st.container():
                        st.markdown("---")
                        st.markdown(summary)
                        st.markdown("---")
                    
                    # Add download button for notes
                    st.download_button(
                        label="📥 Download Notes",
                        data=summary,
                        file_name=f"video_notes_{video_id}.txt",
                        mime="text/plain"
                    )
            else:
                st.error(
                    "❌ Could not fetch transcript for this video.\n\n"
                    "**Possible reasons:**\n"
                    "• The video doesn't have captions/subtitles enabled\n"
                    "• The video is age-restricted or private\n"
                    "• The video is a live stream or premiere\n"
                    "• The transcript language is not supported"
                )
    else:
        st.warning("⚠️ Please enter a YouTube video link.")

# ---------------- SIDEBAR WITH INFO ---------------- #

with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app uses:
    - **YouTube Transcript API** (v1.2.4)
    - **OpenRouter AI** (GPT-4o-mini)
    
    **How it works:**
    1. Extract video ID from URL
    2. Fetch video transcript
    3. Generate AI summary
    4. Download your notes
    """)
    
    st.divider()
    
    st.header("💡 Tips")
    st.markdown("""
    **Best results with:**
    - Educational videos
    - Lectures & tutorials
    - Videos with clear English captions
    
    **Test Videos:**
    - `bO7FQsCcbD8` - CrashCourse (US History)
    - `3ez10ADR_gM` - Khan Academy (Economics)
    - `iCvmsMzlF7o` - TED Talk
    """)
    
    # Show current video ID if available
    if youtube_link and 'video_id' in locals() and video_id:
        st.divider()
        st.success(f"📌 **Current Video ID:** `{video_id}`")
        
        # Test the transcript availability
        if st.button("🔍 Test Transcript Availability"):
            with st.spinner("Checking..."):
                try:
                    # Just check if transcript exists without fetching full text
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                    st.success("✅ Transcript is available!")
                except Exception as e:
                    st.error(f"❌ No transcript available: {str(e)}")