# Todo App API

This Todo App API provides functionalities to manage tasks and user authentication using Django and Django REST Framework.

## Overview

The Todo App API allows users to perform CRUD operations on tasks and includes user authentication features like signup and login.

### Features

- **Tasks:**
  - Create, Read, Update, and Delete tasks
  - Retrieve all tasks or a specific task
- **User Authentication:**
  - User signup
  - User login

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

- Python 3.x
- Git

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Alok-jaiswal-075/todolist
   ```
2. **Create and activate a virtual environment:**

   ```bash
   python -m virtualenv myenv
   # On Windows
   myenv\Scripts\activate
   # On macOS/Linux
   source myenv/bin/activate
   ```
3. **Install dependencies:**

   ```bash
   cd todolist
   pip install -r requirements.txt
   ```
4. **Set up the database:**

   ```bash
   python manage.py migrate
   ```

### Usage

1. **Run the development server:**

   ```bash
   python manage.py runserver
   ```
2. **Access the API:**

   Visit `http://127.0.0.1:8000/` in your web browser.

## Handling Forbidden (CSRF) Errors

During API testing, if you encounter a Forbidden (CSRF) error, follow these steps to include the CSRF token in the request header:

1. **Retrieve the CSRF Token:**

   - When accessing the API endpoints that require CSRF protection, the server generates a CSRF token.
   - To retrieve the CSRF token, make a request to any endpoint that requires authentication (e.g., `/login/`, `/signup/`).
2. **Copy the CSRF Token:**

   - Once the request is made, the CSRF token will be included in the response headers. Look for the `CSRF-Token` or `X-CSRFToken` header.
   - Copy the CSRF token value.
3. **Include CSRF Token in Header:**

   - For subsequent requests that trigger Forbidden errors, add the CSRF token to the request header.
   - Include the token in the header with the key `X-CSRFToken`.
   - Set the `X-CSRFToken` header value to the copied CSRF token.

### API Endpoints

#### Tasks

-`GET /`: Home
-`POST /login/`: User login
-`POST /signup/`: User signup
-`POST /add-todo/`: Add a new task
-`DELETE /delete-todo/<int:id>/`: Delete a task by ID
-`PUT /change-status/<int:id>/<str:status>/`: Change status of a task by ID
-`POST /logout/`: User logout
-`GET /all-tasks/`: Retrieve all tasks
-`GET /specific-task/<int:task_id>/`: Retrieve a specific task by ID

### Additional Notes

- To access the admin panel, create a superuser:

  ```bash
  python manage.py createsuperuser
  ```
- Configure environment variables for settings if specified in the project.

## Tech Stack

- Django
- Django REST Framework
- SQLite (or your preferred database)
