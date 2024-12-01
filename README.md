# CSV Data Chatbot

This project implements a chatbot using Google's Gemini API that answers questions related to CSV data, specifically B.Tech Semester 6 result files. The chatbot can help users query student performance across various subjects and generate insights based on the uploaded CSV data.

**Features**

Upload CSV files to Gemini.
Query information from the uploaded data using natural language.
Answers questions about student marks, subject-wise performance, and more.
Technologies Used
Python
Google Gemini API (Generative AI)
CSV for storing student result data
Virtual Environment for dependency management

**Requirements**

Python 3.x
Gemini API Key
Required Python libraries:
google-generativeai
os
csv

**Installation**

Clone this repository or download the project files.
Create a virtual environment:
python -m venv venv
Activate the virtual environment:
For Windows:
venv\Scripts\activate
For macOS/Linux:
source venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt
Set up your Gemini API key. Create an .env file and add your API key:
GENAI_API_KEY="your-api-key-here"

**Usage**

Upload your CSV result files to Gemini using the upload_to_gemini function.
Run the script and interact with the chatbot by sending queries related to the student results data.
The chatbot will process the data and respond with relevant insights.

**Example**

# Example query:
response = chat_session.send_message("Who scored the highest in Compiler Design?")
print(response.text)
Contributing
Feel free to fork this repository, submit issues, or make pull requests. Contributions are welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.
