from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the Gemini API key from the environment
GEMINI_KEY = os.getenv("GEMINI_KEY")

if not GEMINI_KEY:
    raise ValueError("Gemini API key not found. Please check your .env file.")

# Initialize the Gemini client
try:
    client = genai.Client(api_key = GEMINI_KEY)
    # model = genai.GenerativeModel('gemini-2.0-flash')
    print("Gemini client initialized successfully.")
    
    # Test the API by generating a simple text
    prompt = "Can you summarize University Physics kinematics for me?"
    response = client.models.generate_content(model = 'gemini-2.0-flash', contents = prompt)
    print("API Response:")
    print(response.text)
except Exception as e:
    print(f"Error testing Gemini API key: {e}")