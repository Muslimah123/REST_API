import requests
import json
import sys
import os


BASE_URL = os.environ.get('API_URL', 'http://localhost:5000')


if len(sys.argv) > 1:
    BASE_URL = sys.argv[1]

def print_response(response, description):
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except json.JSONDecodeError:
        print(f"Response (raw): {response.text}")

def test_api():
    """Testing all API endpoints"""
    
    # Test 1: Health check
    print("\n Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    
    # Test 2: List users
    print("\n Testing list users ")
    response = requests.get(f"{BASE_URL}/users")
    print_response(response, "List Users ")
    
    # Test 3: Create a valid user
    print("\n Testing user creation with valid data")
    user_data = {
        "name": "Idaya Seidu",
        "email": "iseiduu@andrew.cmu.edu"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    print_response(response, "Creating valid user data User")
    
    if response.status_code == 201:
        created_user = response.json()
        user_id = created_user.get('id')
        
        # Test 4: Get the created user
        print("\n Testing get user by ID.")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print_response(response, "Get valid User")
        
        # Test 5: List users 
        print("\n Testing list users (with data).")
        response = requests.get(f"{BASE_URL}/users")
        print_response(response, "List Users with data")
    
    # Test 6: Create user with missing name
    print("\n Testing user creation with missing name.")
    invalid_data = {"email": "rest.api@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=invalid_data)
    print_response(response, "Create missing username ")
    
    # Test 7: Create user with invalid email
    print("\n Testing user creation with invalid email.")
    invalid_data = {"name": "Test User", "email": "invalid-email"}
    response = requests.post(f"{BASE_URL}/users", json=invalid_data)
    print_response(response, "Create invalid user email")
    
    # Test 8: Get non-existent user
    print("\n Testing get user with invalid ID.")
    response = requests.get(f"{BASE_URL}/users/non-existent-id")
    print_response(response, "Get invalid user ")
    
    # Test 9: Invalid JSON
    print("\n Testing with invalid JSON.")
    response = requests.post(f"{BASE_URL}/users", 
                           data="not json", 
                           headers={"Content-Type": "application/json"})
    print_response(response, "Create invalid json User ")
    
    # Test 10: Create multiple users
    print("\n Creating multiple users.")
    users = [
        {"name": "Ahmed Issah Tahiru", "email": "aissah@andrew.cmu.edu"},
        {"name": "Mariam Suleiman", "email": "msuleiman@andrew.cmu.edu"},
        {"name": "Ayisha Nuhu", "email": "anhuhu@andrew.cmu.edu"}
    ]
    
    for user_data in users:
        response = requests.post(f"{BASE_URL}/users", json=user_data)
        if response.status_code == 201:
            print(f" Created user: {user_data['name']}")
        else:
            print(f" Failed to create user: {user_data['name']}")
    
    # Test 11: List all users 
    print("\n Testing list users")
    response = requests.get(f"{BASE_URL}/users")
    print_response(response, "list all users")

if __name__ == "__main__":
    try:
        print("Starting API testing")
        print(f"Testing API at: {BASE_URL}")
        
        test_api()
        print("\n All tests completed")
    except requests.exceptions.ConnectionError:
        print(f"\n Error: Could not connect to API at {BASE_URL}")
        print("\nPossible issues:")
        print("1. Make sure the API server is running: python app.py")
        print("2. Check if the server is running on a different address")
        print("3. Try: python test.py http://172.20.10.3:5000")
       
        sys.exit(1)
    except Exception as e:
        print(f"\n Unexpected error: {e}")
        sys.exit(1)