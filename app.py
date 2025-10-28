from flask import Flask, jsonify, request, url_for, redirect

# Initialize the Flask application
app = Flask(__name__)

# --- MODIFIED DATABASE TO TRIGGER ALL PII DETECTION ---
USER_DATABASE = {
    "101": {
        "full_name": "Jane Doe",
        "email_address": "jane.doe@example.com",
        "status": "Active",
        "date_of_birth": "1991-07-25",  # Added DOB
        "ssn": "999-00-1234",          # High-Confidence PII Pattern
        "card_last_4": "4111-XXXX",     # Financial/PCI Pattern
        "ip_address": "192.168.1.10"   # Network PII Pattern
    },
    "102": {
        "full_name": "Alex Smith",
        "email_address": "alex.smith@example.com",
        "status": "Inactive",
        "date_of_birth": "1985-03-10",
        "ssn": "999-00-5678",
        "card_last_4": "4222-XXXX",
        "ip_address": "172.16.0.5"
    },
    "103": {
        "full_name": "Test User",
        "email_address": "test.user@example.com",
        "status": "Pending",
        "date_of_birth": "1978-12-01",
        "ssn": "999-00-9012",
        "card_last_4": "4333-XXXX",
        "ip_address": "10.0.0.2"
    }
}
# -------------------------------------------------


# Route to retrieve user data by ID (REST REMAINS UNCHANGED)
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
