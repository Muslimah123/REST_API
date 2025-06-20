# REST_API
A REST API built with Python and Flask for managing users.

## Technology Stack

- **Language**: Python 3.8+
- **Framework**: Flask 3.0.0
- **Data Storage**: In-memory dictionary (no database needed)

## Features

- Create new users with name and email
- Get user info by ID
- Get all users created
- Auto-generates UUID for user IDs
- Handles errors properly
- Uses JSON for requests/responses
- Validates input

## API Endpoints

### 1. Create User
- **URL**: `/users`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "name": "Idaya Seidu",
    "email": "iseidu@andrew.cmu.edu"
  }
  ```
- **Success Response**: 
  - **Code**: 201 Created
  - **Content**:
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Idaya Seidu",
      "email": "iseidu@andrew.cmu.edu",
      "created_at": "2025-06-20T08:56:04.485483"
    }
    ```
- **Error Response**:
  - **Code**: 400 Bad Request
  - **Content**: `{"error": "Name is required and cannot be empty"}`

### 2. Get User by ID
- **URL**: `/users/:id`
- **Method**: `GET`
- **URL Parameters**: `id` (the user's UUID)
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Idaya Seidu",
      "email": "iseidu@andrew.cmu.edu",
      "created_at": "2025-06-20T08:56:04.485483"
    }
    ```
- **Error Response**:
  - **Code**: 404 Not Found
  - **Content**: `{"error": "User not found"}`

### 3. Get All Users
- **URL**: `/users`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "users": [
        {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Idaya Seidu",
          "email": "iseidu@andrew.cmu.edu",
          "created_at": "2025-06-20T08:56:04.485483"
        }
      ],
      "count": 1
    }
    ```

### 4. Health Check 
- **URL**: `/health`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: `{"status": "healthy", "timestamp": "2025-06-20T08:56:04.485483"}`

## Installation & Setup

### What you need
- Python 3.8 or higher
- pip (Python package manager)

### Steps to run

1. Clone the repo:
   ```
   git clone https://github.com/Muslimah123/REST_API.git
   cd REST_API
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   ```

3. Install what's needed:
   ```
   pip install -r requirements.txt
   ```

4. Run the app:
   ```
   python app.py
   ```

The API will run at `http://172.20.10.3:5000`

## Testing the API

### Using curl

1. **Create a user**:
   ```
   curl -X POST http://172.20.10.3:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "Idaya Seidu", "email": "iseidu@andrew.cmu.edu"}'
   ```

2. **Get a user** (use the ID from the create response):
   ```
   curl http://172.20.10.3:5000/users/<user-id>
   ```

3. **Get all users**:
   ```
   curl http://172.20.10.3:5000/users
   ```

4. **Health check**:
   ```
   curl http://172.20.10.3:5000/health
   ```

### Using Python

```python
import requests

# Create a user
response = requests.post('http://172.20.10.3:5000/users', 
                        json={'name': 'Idaya Seidu', 'email': 'iseidu@andrew.cmu.edu'})
user = response.json()
print(f"Created user: {user}")

# Get the user
response = requests.get(f"http://172.20.10.3:5000/users/{user['id']}")
print(f"Retrieved user: {response.json()}")

# Get all users
response = requests.get('http://172.20.10.3:5000/users')
print(f"All users: {response.json()}")
```

### Using the test script

I included a test script if you want to test everything at once:

```
python test.py http://172.20.10.3:5000
```

This tests all the endpoints and error cases too.

### Using PowerShell (on Windows)

```powershell
# Create a user
Invoke-RestMethod -Uri "http://172.20.10.3:5000/users" -Method Post -ContentType "application/json" -Body '{"name": "Idaya Seidu", "email": "iseidu@andrew.cmu.edu"}'
```

## Error Handling

The API handles these errors:

- **400 Bad Request**: When you send invalid data or miss required fields
- **404 Not Found**: When the user or endpoint doesn't exist
- **405 Method Not Allowed**: When you use the wrong HTTP method
- **500 Internal Server Error**: When something unexpected happens

## Project Structure

```
REST_API/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── test.py        # Test script
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Why I made these choices

1. **Flask**: It's simple and perfect for building REST APIs quickly
2. **UUIDs**: They're guaranteed to be unique without needing a counter
3. **In-memory storage**: Simple dictionary since no database was required
4. **Basic validation**: Checks that name and email are provided and email has @
5. **Clear errors**: Makes debugging easier
6. **Timestamps**: Good to know when users were created

## If you run into issues

- Make sure Flask server is running before testing
- Check that you're using the right URL (http://172.20.10.3:5000)
- If port 5000 is taken, change it in app.py
- The server shows all requests in the terminal which helps with debugging