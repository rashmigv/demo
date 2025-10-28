from flask import Flask, jsonify, request, url_for, redirect

# Initialize the Flask application
app = Flask(__name__)

# --- SIMULATED DATABASE (REPLACES SQLAlchemy) ---
# In a real app, this data would come from Airtable, SQL, etc.
USER_DATABASE = {
    "101": {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "status": "Active"
    },
    "102": {
        "name": "Alex Smith",
        "email": "alex.smith@example.com",
        "status": "Inactive"
    },
    "103": {
        "name": "Test User",
        "email": "test.user@example.com",
        "status": "Pending"
    }
}
# -------------------------------------------------


# Route to retrieve user data by ID
@app.route('/api/user/<user_id>', methods=['GET'])
def get_user_data(user_id):
    """
    Retrieves user data based on the ID provided in the URL path.
    """
    
    user_data = USER_DATABASE.get(user_id)
    
    if user_data:
        # Success: Return the data as a JSON object with a 200 status code
        return jsonify({
            "status": "success",
            "user_id": user_id,
            "data": user_data
        }), 200
    else:
        # Failure: Return a JSON error message with a 404 status code
        return jsonify({
            "status": "error",
            "message": f"User ID '{user_id}' not found in database."
        }), 404


# Route for the main URL (optional redirect/info page)
@app.route('/')
def home():
    return "Welcome to the Simple Data API. Try accessing /api/user/101"


# Run the application
if __name__ == '__main__':
    # Running on port 5000 by default
    app.run(debug=True)
