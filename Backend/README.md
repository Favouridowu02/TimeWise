⏳ TimeWise Backend
This is the Flask-powered backend for TimeWise, a productivity app designed to help users manage tasks, schedule events, and analyze their productivity. It provides a RESTful API for task management, scheduling, user authentication, and analytics.

🚀 Features
✅ User Authentication – Secure login & registration with JWT
✅ Task Management – Create, update, delete, and track tasks
✅ Scheduling System – Set reminders and due dates for tasks
✅ Real-time Notifications – Firebase integration for alerts
✅ Data Caching – Redis-powered performance boost
✅ PostgreSQL Database – Scalable and efficient data storage

🛠 Tech Stack
Framework: Flask
Database: PostgreSQL
Caching: Redis
Authentication: JWT (JSON Web Token)
Notifications: Firebase
Environment Management: dotenv

This the API for TimeWise
│── api/
│   ├── v1/
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── task_routes.py
│   │   │   ├── progress_routes.py
│   │   │   ├── analytics_routes.py
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── config.py
│
│── models/                         # Database models
│   ├── __init__.py
│   ├── base_model.py               # Base models
│   ├── user.py
│   ├── task.py
│   ├── progress.py
│   ├── analytics.py
│
|
│── migrations/ (Flask-Migrate directory)
│── .env
│── requirements.txt
│── run.py


Authentication
POST /api/auth/register – Register a new user
POST /api/auth/login – Login and receive JWT token
GET /api/auth/user – Get authenticated user details
Tasks
POST /api/tasks – Create a new task
GET /api/tasks – Retrieve all tasks
GET /api/tasks/:id – Get a specific task
PUT /api/tasks/:id – Update a task
DELETE /api/tasks/:id – Delete a task
Scheduling & Notifications
POST /api/notifications – Send scheduled notifications
GET /api/notifications – Retrieve notification history
Full API documentation will be available via Postman collection or Swagger UI.