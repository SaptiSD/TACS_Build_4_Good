from flask import Flask, render_template, request, send_file
import csv
from io import StringIO
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os
from google import genai


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

client = genai.Client(api_key = GEMINI_KEY)

# # Path to JSON data file
# DATA_FILE = 'full file name'

@app.route('/')
def index():
    logger.info("--- Rendering Index Page ---")
    return render_template('index.html')


@app.route('/generate' , methods = ['POST'])
def generate():
    logger.info("--- Rendering generate Page ---")

    # gets form data from generate.html
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    subject = request.form.get('subject')
    frequency = request.form.get('frequency')

    # validating the dates
    try:
        start_date = datetime.strptime(start_date, '%y-%m-%d')
        end_date = datetime.strptime(end_date, '%y-%m-%d')

        if start_date > end_date:
            raise ValueError("Whoops! The start date needs to be after the end date.")
    except ValueError as e:
        logger.error(f"Date validation error: {e}")
        return "Invalid date range provided.", 400
    
    # generate actual study plan using AI
    prompt = f"Pretend that you are a high-paid tutor who is internationally renowned for their amazing tutoring services. Your latest client is a billionaire with a lot of money and influence who would like you to generate a study plan for their favorite only child. Because of how high-profile this client is, you want to do everything you can not to let them down or else your reputation and career will be at stake. Create a day-by-day study plan for the subject {subject} from {start_date.date()} to {end_date.date()} with a frequency of '{frequency}'."
    response = client.generate_text(prompt = prompt)
    study_plan = response.result.split("\n")

    # creating .csv file to be later integrated with Notion
    csv_output = StringIO()
    csvWriter = csv.writer(csv_output)
    csvWriter.writerow(['Date', 'Task'])

    current_date = start_date
    for task in study_plan:
        if current_date > end_date:
            break
        csvWriter.writerow([current_date.strftime('%Y-%m-%d'), task])
        current_date += timedelta(days = 1) # increments date based on frequency logic (currently increments daily)
    
    csv_output.seek(0)

    return send_file(
        StringIO(csv_output.getvalue()),
        mimetype = 'text/csv',
        as_attachment = True,
        download_name = 'study_plan.csv'
    )

    #return render_template('generate.html')

@app.route('/notion')
def notion():
    logger.info("--- Rendering notion Page ---")
    return render_template('notion.html')


if __name__ == '__main__':
    logger.info("--- Starting Flask App ---")
    app.run(debug=True, port=8000)