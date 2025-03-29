import io
from csv_processor import process_csv_file
from query import query_database

# Option 1: Open a test CSV file from the 'static' folder
with open('static/test.csv', 'rb') as file_stream:
    process_csv_file(file_stream)

# Option 2: Alternatively, you can simulate CSV data using a byte stream
# csv_data = b"""goal_title,goal_due_date,task_title,task_due_date
# Complete Project,2025-04-15,Design Mockups,2025-03-29
# Complete Project,2025-04-15,Develop Backend,2025-04-05
# Start Marketing Campaign,2025-05-01,Plan Social Media Strategy,2025-04-01
# Start Marketing Campaign,2025-05-01,Email Newsletter,2025-04-03
# Personal Goals,2025-06-01,Exercise Daily,2025-03-31
# """
# process_csv_file(io.BytesIO(csv_data))

print("Finished processing CSV file.")

# Query the Notion database to see what goals and tasks were created
data = query_database()
print("Queried Notion Data:")
for goal in data:
    print(f"Goal: {goal['goal_title']} (Due: {goal['goal_due_date']})")
    for task in goal['tasks']:
        print(f"  - Task: {task['task_title']} (Due: {task['task_due_date']})")
