import json
from flask import Flask, request, jsonify
from flask_cors import CORS # Import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Load data from data.json
# It's good practice to load this once, ideally outside the request handler
# or use a global variable if reloading is not an issue for small data.
try:
    with open('data.json', 'r') as f:
        student_data = json.load(f)
except FileNotFoundError:
    student_data = [] # Handle case where file might not be found

@app.route('/api', methods=['GET'])
def get_marks():
    # Get all 'name' parameters from the URL
    names = request.args.getlist('name')

    # Prepare a dictionary for quick lookup of marks by name
    marks_dict = {student['name']: student['marks'] for student in student_data}

    # Collect marks for the requested names in the specified order
    result_marks = []
    for name in names:
        if name in marks_dict:
            result_marks.append(marks_dict[name])
        # Optional: handle names not found, e.g., append None or skip
        # else:
        #     result_marks.append(None) 

    return jsonify({"marks": result_marks})

# This is typically not needed for Vercel's serverless functions
# as Vercel handles the WSGI server, but useful for local testing.
if __name__ == '__main__':
    app.run(debug=True)
