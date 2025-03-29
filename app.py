from flask import Flask, render_template
import logging
from dotenv import load_dotenv
import os
import google.generativeai as genai


# Initialize Flask app with correct template folder
app = Flask(__name__, 
    template_folder='templates')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

##api key example
# api_key = os.getenv("API_KEY")
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_KEY:
    raise ValueError("Gemini API key not found.")

genai.configure(api_key=GEMINI_KEY)

# # Path to JSON data file
# DATA_FILE = 'full file name'

@app.route('/')
def index():
    logger.info("--- Rendering Index Page ---")
    return render_template('index.html')


@app.route('/generate' , methods = ['POST'])
def generate():
    logger.info("--- Rendering generate Page ---")
    return render_template('generate.html')

@app.route('/notion')
def notion():
    logger.info("--- Rendering notion Page ---")
    return render_template('notion.html')


if __name__ == '__main__':
    logger.info("--- Starting Flask App ---")
    app.run(debug=True, port=8000)