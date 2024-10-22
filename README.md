# Task Management API

A Django REST Framework-based API for managing tasks and user assignments.

## Features

- Create and manage tasks
- Assign tasks to multiple users
- Retrieve tasks for specific users
- User authentication and authorization
- RESTful API endpoints

## Tech Stack

- Python 3.8+
- Django 5.0.1
- Django REST Framework 3.14.0
- SQLite (default database)

## Project Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd task-management
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Database setup
```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 5. Create superuser
```bash
python manage.py createsuperuser
```
Test Credentials:
- Username: admin
- Email: admin@example.com
- Password: admin123

### 6. Run the development server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/api/`

## API Endpoints

### Authentication

All API endpoints require authentication. Include the following header in your requests:
```
Authorization: Basic <base64-encoded-credentials>
```

### 1. Create Task
```http
POST /api/tasks/

Request:
{
    "name": "Implement Login Feature",
    "description": "Create login functionality with email and password",
    "task_type": "FEATURE",
    "assigned_user_ids": [1, 2]
}

Response:
{
    "id": 1,
    "name": "Implement Login Feature",
    "description": "Create login functionality with email and password",
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-20T10:00:00Z",
    "completed_at": null,
    "task_type": "FEATURE",
    "status": "PENDING",
    "assigned_users": [
        {
            "id": 1,
            "username": "user1",
            "email": "user1@example.com",
            "mobile": "1234567890"
        },
        {
            "id": 2,
            "username": "user2",
            "email": "user2@example.com",
            "mobile": "0987654321"
        }
    ]
}
```

### 2. Assign Task to Users
```http
POST /api/tasks/{task_id}/assign_users/

Request:
{
    "user_ids": [1, 2, 3]
}

Response:
{
    "status": "success",
    "message": "Users assigned successfully"
}
```

### 3. Get Tasks for Specific User
```http
GET /api/tasks/?user_id=1

Response:
[
    {
        "id": 1,
        "name": "Implement Login Feature",
        "description": "Create login functionality with email and password",
        "created_at": "2024-01-20T10:00:00Z",
        "updated_at": "2024-01-20T10:00:00Z",
        "completed_at": null,
        "task_type": "FEATURE",
        "status": "PENDING",
        "assigned_users": [
            {
                "id": 1,
                "username": "user1",
                "email": "user1@example.com",
                "mobile": "1234567890"
            }
        ]
    }
]
```

### 4. Get Current User's Tasks
```http
GET /api/tasks/my_tasks/

Response:
[
    {
        "id": 1,
        "name": "Implement Login Feature",
        "description": "Create login functionality with email and password",
        "created_at": "2024-01-20T10:00:00Z",
        "status": "PENDING",
        ...
    }
]
```

## Data Models

### User Model
```python
Fields:
- id: Integer (Primary Key)
- username: String
- email: String
- mobile: String
- first_name: String
- last_name: String
- created_at: DateTime
- updated_at: DateTime
```

### Task Model
```python
Fields:
- id: Integer (Primary Key)
- name: String
- description: Text
- created_at: DateTime
- updated_at: DateTime
- completed_at: DateTime (nullable)
- task_type: String (choices: FEATURE, BUG, ENHANCEMENT)
- status: String (choices: PENDING, IN_PROGRESS, COMPLETED, CANCELLED)
- assigned_users: Many-to-Many relationship with User
- created_by: Foreign Key to User
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- 200: Successful request
- 201: Resource created successfully
- 400: Bad request / Invalid data
- 401: Unauthorized
- 403: Forbidden
- 404: Resource not found
- 500: Server error

Example error response:
```json
{
    "status": "error",
    "message": "Invalid task data provided",
    "errors": {
        "name": ["This field is required."],
        "assigned_user_ids": ["Invalid user ID provided."]
    }
}
```

## Testing

Run the test suite:
```bash
python manage.py test
```

## Additional Notes

1. All timestamps are returned in UTC format
2. Task types and statuses are predefined and cannot be modified through the API
3. Users can only view and modify tasks they have access to
4. The API uses token-based authentication for secure access

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
