from flask import Flask, jsonify, request

# Initialize the Flask application
app = Flask(__name__)

# --- SIMULATED IN-MEMORY DATA STORE ---
# Stores data submitted by the client (simulating a database)
CUSTOMER_RECORDS = {}
NEXT_USER_ID = 1001 

# Route to create a new user record (POST request)
@app.route('/api/user', methods=['POST'])
def create_user():
    """
    Accepts sensitive user data via JSON POST request and stores it.
    """
    global NEXT_USER_ID

    # Ensure the request contains JSON data
    if not request.json:
        return jsonify({"status": "error", "message": "Missing JSON data"}), 400

    # Extract required and sensitive data elements
    data = request.json
    
    # 1. Core PII/Identity
    full_name = data.get('full_name')
    date_of_birth = data.get('date_of_birth')
    
    # 2. Financial/Sensitive Data
    card_number = data.get('card_number')
    
    # Simple validation (ensure name is present)
    if not full_name:
        return jsonify({"status": "error", "message": "Missing required field: full_name"}), 400

    # Structure the new record
    new_record = {
        "user_id": NEXT_USER_ID,
        "name": full_name,
        "age": data.get('age'),
        "date_of_birth": date_of_birth,
        "credit_card": card_number,
        "detection_flag": True
    }

    # Store and increment ID
    CUSTOMER_RECORDS[str(NEXT_USER_ID)] = new_record
    NEXT_USER_ID += 1

    return jsonify({
        "status": "success",
        "message": "User record created successfully and data elements exchanged.",
        "user_id": new_record['user_id']
    }), 201 # 201 Created


# Route to retrieve a user record (GET request)
@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a single user record by ID and returns all stored data.
    """
    record = CUSTOMER_RECORDS.get(str(user_id))

    if record:
        # Success: Data is returned, including sensitive fields
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
        "name": "Initial Test Subject",
        "age": 30,
        "date_of_birth": "1995-01-01",
        "credit_card": "4111-XXXX-XXXX-1111",
        "detection_flag": True
    }
    NEXT_USER_ID = 1001
    
    app.run(debug=True)
