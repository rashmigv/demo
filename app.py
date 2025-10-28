from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# --- SIMULATED IN-MEMORY DATA STORE ---
# Used to demonstrate the successful exchange of data
CUSTOMER_RECORDS = {}
NEXT_USER_ID = 1001 
# -------------------------------------------------


# Route to handle creation and exchange of sensitive user data
@app.route('/api/user', methods=['POST'])
def handle_data_exchange():
    """
    Accepts, stores, and confirms exchange of sensitive user data (POST).
    """
    global NEXT_USER_ID

    # 1. Input Validation and Extraction
    if not request.json:
        return jsonify({"status": "error", "message": "Missing JSON data in request."}), 400

    data = request.json
    
    # Extract all requested sensitive data elements
    new_record = {
        "user_id": NEXT_USER_ID,
        "full_name": data.get('full_name', 'N/A'),
        "age": data.get('age', 'N/A'),
        "date_of_birth": data.get('date_of_birth', 'N/A'),
        "credit_card_details": data.get('credit_card_details', 'N/A'),
        "is_sensitive_record": True 
    }

    # 2. Store and increment ID
    # Simulates storing the complete PII and financial record securely
    CUSTOMER_RECORDS[str(NEXT_USER_ID)] = new_record
    NEXT_USER_ID += 1

    return jsonify({
        "status": "success",
        "message": "Sensitive user data received and stored.",
        "user_id": new_record['user_id']
    }), 201 # 201 Created


# Route to retrieve the exchanged user data (GET request)
@app.route('/api/user/<int:user_id>', methods=['GET'])
def retrieve_user_data(user_id):
    """
    Retrieves a single user record by ID, returning all exchanged data types.
    """
    record = CUSTOMER_RECORDS.get(str(user_id))

    if record:
        # Success: All sensitive data elements are returned to the client
        return jsonify({
            "status": "success",
            "data": record
        }), 200
    else:
        # Failure: Resource not found
        return jsonify({
            "status": "error",
            "message": f"User ID {user_id} not found."
        }), 404


# Run the application
if __name__ == '__main__':
    # Initialize the first record for easy testing
    CUSTOMER_RECORDS["1000"] = {
        "user_id": 1000,
        "full_name": "Test Subject PII",
        "age": 45,
        "date_of_birth": "1980-06-15",
        "credit_card_details": "5432-xxxx-xxxx-9012",
        "is_sensitive_record": True
    }
    global NEXT_USER_ID
    NEXT_USER_ID = 1001
    
    # Note: Install Flask using 'pip install Flask' before running.
    app.run(debug=True)
