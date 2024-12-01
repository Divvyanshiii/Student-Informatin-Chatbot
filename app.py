import os
import time
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Page config and styling
st.set_page_config(
    page_title="Student Results Analysis Bot",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .stChat {
        border-radius: 10px;
        padding: 10px;
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .user-message {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 15px;
        margin: 5px 0;
        color: #ffffff;
    }
    .bot-message {
        background-color: #363636;
        padding: 15px;
        border-radius: 15px;
        margin: 5px 0;
        color: #ffffff;
    }
    .upload-section {
        padding: 20px;
        border-radius: 10px;
        background-color: #2d2d2d;
        margin: 10px 0;
        color: #ffffff;
    }
    /* Make all text white for better visibility */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

def initialize_gemini():
    """Initialize Gemini API with error handling"""
    load_dotenv()
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        st.error("⚠️ GENAI_API_KEY not found in environment variables!")
        st.stop()
    genai.configure(api_key=api_key)

def upload_to_gemini(file, mime_type="text/csv"):
    """Upload file to Gemini with progress tracking"""
    try:
        with st.spinner(f"Uploading {file.name}..."):
            if file.name in st.session_state.uploaded_files:
                return st.session_state.uploaded_files[file.name]
            
            uploaded_file = genai.upload_file(file, mime_type=mime_type)
            st.session_state.uploaded_files[file.name] = uploaded_file
            return uploaded_file
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return None

def wait_for_files_active(files):
    """Wait for files to be processed with progress bar"""
    progress_bar = st.progress(0)
    for idx, file in enumerate(files):
        file_obj = genai.get_file(file.name)
        while file_obj.state.name == "PROCESSING":
            progress_bar.progress((idx + 0.5) / len(files))
            time.sleep(2)
            file_obj = genai.get_file(file.name)
        if file_obj.state.name != "ACTIVE":
            st.error(f"File {file.name} failed to process")
            return False
        progress_bar.progress((idx + 1) / len(files))
    return True

def initialize_chat(files):
    """Initialize chat session with uploaded files"""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.9,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192
            }
        )
        
        history = [
            {
                "role": "user",
                "parts": [*files, "explain the content"],
            },
            {
                "role": "model",
                "parts": ["These CSV files contain student result data for B.Tech students. Let me analyze the content..."]
            }
        ]
        
        st.session_state.chat_session = model.start_chat(history=history)
        st.success("✅ Chat session initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing chat: {str(e)}")

def main():
    st.title("🎓 Student Results Analysis Bot")
    
    # Initialize Gemini
    initialize_gemini()
    
    # File upload section
    st.header("📁 Upload Result Files")
    with st.container(border=True):
        uploaded_files = st.file_uploader(
            "Upload CSV result files",
            type=["csv"],
            accept_multiple_files=True,
            help="Upload one or more CSV files containing student results"
        )
        
        if uploaded_files and st.button("Process Files", type="primary"):
            files = [upload_to_gemini(file) for file in uploaded_files]
            if all(files) and wait_for_files_active(files):
                initialize_chat(files)

    # Chat interface
    st.header("💬 Chat Interface")
    
    # Display chat history
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f'<div class="user-message">👤 You: {content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 Bot: {content}</div>', unsafe_allow_html=True)

    # Chat input
    if st.session_state.chat_session:
        user_input = st.chat_input("Ask about the results...")
        if user_input:
            # Add user message to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.spinner("Thinking..."):
                response = st.session_state.chat_session.send_message(user_input)
                st.session_state.chat_history.append({"role": "bot", "content": response.text})
            
            # Rerun to update chat display
            st.rerun()
    else:
        st.info("👆 Please upload files first to start the conversation")

    # Sidebar with additional information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("This bot analyzes student result data and answers questions about performance, trends, and statistics.")
        
        st.header("🔍 Features")
        st.write("- Upload multiple CSV result files")
        st.write("- Interactive chat interface")
        st.write("- Detailed analysis of student performance")
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main() 