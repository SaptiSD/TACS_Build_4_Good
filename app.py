from flask import Flask, render_template, request, send_file
import csv
from io import BytesIO, StringIO
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv
import os
from google import genai
from test_notion import testNotion


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

# genai.configure(api_key=GEMINI_KEY)
client = genai.Client(api_key = GEMINI_KEY)

# # Path to JSON data file
# DATA_FILE = 'full file name'

@app.route('/')
def index():
    logger.info("--- Rendering Index Page ---")
    return render_template('index.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'GET':
        logger.info("--- Rendering Generate Page (GET) ---")
        return render_template('generate.html')
    
    logger.info("--- Processing Generate Request (POST) ---")

    # gets form data from generate.html
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    subject = request.form.get('subject')
    frequency = request.form.get('frequency')

    # validating the dates
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        if start_date > end_date:
            raise ValueError("Whoops! The start date needs to be after the end date.")
    except ValueError as e:
        logger.error(f"Date validation error: {e}")
        return "Invalid date range provided.", 400
    
    # generate actual study plan using AI
    try:
        prompt = f"Pretend that you are a tutor who has been tasked to generate a study plan for student. All you need to do is make a plan where each line is a task for the student to complete in order to achieve their goal of mastering {subject} within the timeframe from {start_date.date()} to {end_date.date()} with a frequency of {frequency}. Remember, do not return ANY other text other than a line-by-line string of the task the student should complete each day. Additionally, each line need not include the date that the task needs to be completed."
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        study_plan = response.text.split("\n")
        if not study_plan:
            raise ValueError("Empty response from Gemini API")
    except Exception as e:
        logger.error(f"Error accessing Gemini: {e}")
        return f"Error generating study plan: {str(e)}", 500

    # creating .csv file to be later integrated with Notion
    """try:
        csv_output = StringIO()
        csvWriter = csv.writer(csv_output)
        csvWriter.writerow(['goal_title', 'goal_due_date', 'task', 'due_date'])

        current_date = start_date
        for task in study_plan:
            if current_date > end_date:
                break
            if task.strip():  # Only write non-empty tasks
                csvWriter.writerow([subject, end_date.date(), task, current_date.strftime('%Y-%m-%d')])
            current_date += timedelta(days=1)

        # convert to bytes for send_file
        csv_bytes = BytesIO()
        csv_bytes.write(csv_output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)

        return send_file(
            csv_bytes,
            mimetype='text/csv',
            as_attachment=True,
            download_name='study_plan.csv'
        )
    except Exception as e:
        logger.error(f"Error creating CSV: {e}")
        return f"Error creating study plan CSV: {str(e)}", 500"""

    try:
        # Define the path to your static data folder
        csv_file_path = os.path.join('Folder', 'static', 'data', 'test.csv')
        
        if not os.path.exists(os.path.dirname(csv_file_path)):
            try:
                os.makedirs(os.path.dirname(csv_file_path))
            except Exception as e:
                logger.error(f"Error creating directory: {e}")
                return "Error creating directory for CSV file", 500

        # Write to the CSV file
        with open(csv_file_path, 'w', newline='') as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(['goal_title', 'goal_due_date', 'task_title', 'task_due_date'])
            
            current_date = start_date
            for task in study_plan:
                if current_date > end_date:
                    break
                if task.strip():  # Only write non-empty tasks
                    csvWriter.writerow([subject, end_date.strftime('%Y-%m-%d'), task.strip(), current_date.strftime('%Y-%m-%d')])
                current_date += timedelta(days=1)

        testNotion()

        # Redirect to notion page or return success message
        return render_template('notion.html')
        
    except Exception as e:
        logger.error(f"Error creating CSV: {e}")
        return f"Error creating study plan CSV: {str(e)}", 500


@app.route('/notion')
def notion():
    logger.info("--- Rendering notion Page ---")
    return render_template('notion.html')


if __name__ == '__main__':
    logger.info("--- Starting Flask App ---")
    app.run(debug=True, port=8000)