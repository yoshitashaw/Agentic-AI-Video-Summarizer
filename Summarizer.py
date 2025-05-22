import streamlit as st 
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai
import time
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
from streamlit_lottie import st_lottie
import json

# Set up page
st.set_page_config(
    page_title="Multimodal AI Agent - Video Summarizer",
    page_icon="🎥",
    layout="wide"
)

# Global CSS styling
st.markdown(
    """
    <style>
    .block-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding-top: 2rem;
    }
    .stTextArea textarea {
        height: 100px;
        text-align: center;
    }
    .stButton > button {
        display: block;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("❌ Google API Key not found. Please set it in a .env file as GOOGLE_API_KEY.")
    st.stop()

# Load Lottie animation
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

lottie_animation = load_lottie_file("animations/ai.json")

# Display animation centered
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st_lottie(lottie_animation, speed=1, loop=True, quality="high", height=300)

# Headers
st.markdown("<h1 style='text-align: center; color: white;'>PHIDATA VIDEO SUMMARIZER AGENT 🎥🎤🖬</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #f9f9f9;'>Powered by Gemini 2.0 Flash Exp</h3>", unsafe_allow_html=True)

# Initialize the agent
@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

multimodal_Agent = initialize_agent()

# File uploader
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    video_file = st.file_uploader("📤 Upload a video file", type=['mp4', 'mov', 'avi'])

# User query input
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_query = st.text_area(
        "🔎 What insights are you seeking from the video?",
        placeholder="Ask anything about the video content.",
        help="Provide specific questions or topics of interest."
    )

video_path = None
if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

if video_path:
    st.video(video_path)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔍 Analyze Video"):
            if not user_query:
                st.warning("⚠️ Please enter a question or insight to analyze the video.")
            else:
                try:
                    with st.spinner("⏳ Processing video and gathering insights..."):
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)

                        analysis_prompt = f"""
                        Analyze the uploaded video for visual and contextual insights.
                        Respond to the following user query using detailed reasoning, key observations,
                        and additional knowledge as needed:\n\n{user_query}

                        Output a comprehensive, user-friendly, and informative response.
                        """

                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

                    st.subheader("📊 Analysis Result")
                    st.markdown(response.content)

                except Exception as error:
                    st.error(f"❌ An error occurred during analysis: {error}")
                finally:
                    Path(video_path).unlink(missing_ok=True)
else:
    st.info("📁 Upload a video file to begin analysis.")











# import streamlit as st 
# from phi.agent import Agent
# from phi.model.google import Gemini
# from phi.tools.duckduckgo import DuckDuckGo
# from google.generativeai import upload_file,get_file
# import google.generativeai as genai
# import time
# from pathlib import Path
# import tempfile

# # Page configuration
# st.set_page_config(
#     page_title="Multimodal AI Agent- Video Summarizer",
#     page_icon="🎥",
#     layout="wide"
# )

# from dotenv import load_dotenv
# load_dotenv()

# import os
# from streamlit_lottie import st_lottie
# import requests
# import json

# def load_lottie_file(filepath: str):
#     with open(filepath, "r", encoding="utf-8") as f:
#         return json.load(f)

# # Load animation
# lottie_animation = load_lottie_file("animations/ai.json")

# st_lottie(
#     lottie_animation,
#     speed=1,
#     reverse=False,
#     loop=True,
#     quality="high",
#     height=300,
#     key="video_ai_anim"
# )


# # Load the Google API key from Google AI Studio
# API_KEY=os.getenv("GOOGLE_API_KEY")
# if API_KEY:
#     genai.configure(api_key=API_KEY)


# st.markdown("<h1 style='text-align: center; color: white;'>PHIDATA VIDEO SUMMARIZER AGENT 🎥🎤🖬</h1>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: #f9f9f9;'>Powered by Gemini 2.0 Flash Exp</h3>", unsafe_allow_html=True)

# @st.cache_resource
# def initialize_agent():
#     return Agent(
#         name="Video AI Summarizer",
#         model=Gemini(id="gemini-2.0-flash-exp"),
#         tools=[DuckDuckGo()],
#         markdown=True,
#     )

# ## Initialize the agent
# multimodal_Agent=initialize_agent()

# # File uploader
# # video_file = st.file_uploader(
# #     "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
# # )
# col1, col2, col3 = st.columns([1, 2, 1])  # Creates a 3-column layout

# with col2:
#     video_file = st.file_uploader(
#         "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
#     )


# if video_file:
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
#         temp_video.write(video_file.read())
#         video_path = temp_video.name

#     st.video(video_path, format="video/mp4", start_time=0)

#     user_query = st.text_area(
#         "What insights are you seeking from the video?",
#         placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
#         help="Provide specific questions or insights you want from the video."
#     )

#     if st.button("🔍 Analyze Video", key="analyze_video_button"):
#         if not user_query:
#             st.warning("Please enter a question or insight to analyze the video.")
#         else:
#             try:
#                 with st.spinner("Processing video and gathering insights..."):
#                     # Upload and process video file
#                     processed_video = upload_file(video_path)
#                     while processed_video.state.name == "PROCESSING":
#                         time.sleep(1)
#                         processed_video = get_file(processed_video.name)

#                     # Prompt generation for analysis
#                     analysis_prompt = (
#                         f"""
#                         You are a multimodal AI assistant designed to summarize and analyze video content.

#                         ### Instructions:
#                         1. Watch the uploaded video carefully.
#                         2. Identify and summarize the key scenes, visual elements, and events.
#                         3. Extract any spoken or displayed text, dialogues, or relevant audio cues.
#                         4. Combine all insights to answer the user query below.
#                         5. Perform supplementary web research if needed (e.g., identifying known places, people, or terms).
#                         6. Provide your answer in this structured format:
#                         - **Key Events Timeline**
#                         - **Main Characters or Subjects**
#                         - **Summary of Visual & Audio Content**
#                         - **Insights Related to the User Query**
#                         - **Relevant External Information or Context**
#                         - **Actionable Takeaways or Suggestions**

#                         ### User Query:
#                         {user_query}

#                         Please ensure the response is comprehensive, easy to read, and well-organized.
#                         """
#                     )

#                     # AI agent processing
#                     response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

#                 # Display the result
#                 st.subheader("Analysis Result")
#                 st.markdown(response.content)

#             except Exception as error:
#                 st.error(f"An error occurred during analysis: {error}")
#             finally:
#                 # Clean up temporary video file
#                 Path(video_path).unlink(missing_ok=True)
# else:
#     st.info("Upload a video file to begin analysis.")

# # Customize text area height
# st.markdown(
#     """
#     <style>
#     .stTextArea textarea {
#         height: 80px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )