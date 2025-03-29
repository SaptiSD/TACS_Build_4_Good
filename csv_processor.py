import csv
import io
from create import create_goal, create_task

def process_csv_file(file_stream):
    """
    Reads CSV data from a file stream and creates goals and tasks in the Notion database.
    
    The CSV is expected to have the following columns:
      - goal_title
      - goal_due_date
      - task_title
      - task_due_date
      
    Each unique goal is created only once, and tasks are added as child blocks to the corresponding goal.
    """
    # Convert the binary stream to a text stream (assuming UTF-8 encoding)
    stream = io.StringIO(file_stream.read().decode("utf-8"), newline=None)
    reader = csv.DictReader(stream)
    
    # Dictionary to track created goals to avoid duplicates
    goals = {}
    
    for row in reader:
        goal_title = row["goal_title"].strip()
        goal_due_date = row["goal_due_date"].strip()
        task_title = row["task_title"].strip()
        task_due_date = row["task_due_date"].strip()
        
        # Create the goal if not already created
        if goal_title not in goals:
            goal_id = create_goal(goal_title, goal_due_date)
            goals[goal_title] = goal_id
        else:
            goal_id = goals[goal_title]
        
        # Create the task as a child block under the goal
        create_task(goal_id, task_title, task_due_date)
