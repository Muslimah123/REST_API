from flask import Flask, request, jsonify
import uuid
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# In-memory storage for users
users_db = {}

# function to validate user data
def validate_user_data(data):
    """Validate that required fields are present and valid"""
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"
    
    if 'name' not in data or not data['name'].strip():
        return False, "Name is required and cannot be empty"
    
    if 'email' not in data or not data['email'].strip():
        return False, "Email is required and cannot be empty"
    
    #  email validation
    if '@' not in data['email']:
        return False, "Invalid email format"
    
    return True, None

@app.route('/users', methods=['GET'])
def list_users():
    """List all users"""
    try:
        # Convert dict values to list for JSON serialization
        users_list = list(users_db.values())
        return jsonify({
            'users': users_list,
            'count': len(users_list)
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if data is None:
            return jsonify({
                'error': 'Invalid JSON or Content-Type header missing'
            }), 400
        
        # Validate user data
        is_valid, error_message = validate_user_data(data)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Generate unique ID for the user
        user_id = str(uuid.uuid4())
        
        # Create user object
        user = {
            'id': user_id,
            'name': data['name'].strip(),
            'email': data['email'].strip(),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store user in memory
        users_db[user_id] = user
        
        # Return created user
        return jsonify(user), 201
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a user by ID"""
    try:
        # Check if user exists
        if user_id not in users_db:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user data
        return jsonify(users_db[user_id]), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Error handler for 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

# Error handler for 405 
@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)