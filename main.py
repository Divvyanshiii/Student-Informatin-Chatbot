import os
import time
import google.generativeai as genai
import csv

# Replace with your API key directly or through environment variable
GENAI_API_KEY = "AIzaSyDAj7MfChlMgtQg1N2TGUd9I0AJu73IJx8"
genai.configure(api_key=GENAI_API_KEY)

# Store uploaded file URIs to prevent re-uploading
uploaded_files = {}

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini, only if it has not been uploaded before."""
    if path in uploaded_files:
        print(f"File '{path}' already uploaded: {uploaded_files[path]}")
        return uploaded_files[path]

    file = genai.upload_file(path, mime_type=mime_type)
    uploaded_files[path] = file.uri
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready\n")

# Upload files only once
files = [
    upload_to_gemini("B.Tech Semester 6 Publish Result File.csv", mime_type="text/csv"),
    upload_to_gemini("B.Tech CS Semester 6 Publish Result File.csv", mime_type="text/csv"),
    upload_to_gemini("B.Tech FS Semester 6 Publish Result File.csv", mime_type="text/csv"),
]

# Wait for files to be processed
wait_for_files_active(files)

# Start chat session with initial context
chat_session = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config={"temperature": 1, "top_p": 0.95, "top_k": 40, "max_output_tokens": 8192}
).start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                files[0],
                files[1],
                files[2],
                "explain the content",
            ],
        },
        {
            "role": "model",
            "parts": [
                "These three CSV files contain student result data for B.Tech students in different specializations (or branches) during their sixth semester. Let's break down the content of each..."
            ],
        },
    ]
)

# Continuously ask the user for input and send it to the model
while True:
    user_input = input("Ask the model your question: ")
    if user_input.lower() == "exit":
        print("Exiting the chatbot.")
        break
    
    # Send the user's input to the model and get the response
    response = chat_session.send_message(user_input)
    print("Model's response:", response.text)
