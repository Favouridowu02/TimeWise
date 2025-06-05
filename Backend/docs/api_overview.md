# TimeWise API Documentation

This document provides an overview of the main API endpoints for the TimeWise backend. For detailed request/response schemas and examples, see the Swagger UI (`/apidocs`) or the individual endpoint docs in this directory.

---

## Authentication

### POST `/api/v1/auth/register`
Register a new user.
- **Body:** `{ "email": str, "password": str, "name": str, "username": str }`
- **Responses:**
  - `201`: User registered successfully
  - `400`: Missing required field
  - `409`: User already exists
  - `500`: Registration failed

### POST `/api/v1/auth/login`
Login and receive a JWT token.
- **Body:** `{ "email" or "username": str, "password": str }`
- **Responses:**
  - `200`: Login successful
  - `400`: Missing credentials
  - `401`: Invalid credentials
  - `500`: Login failed

### GET `/api/v1/auth/profile`
Get the authenticated user's profile.
- **Auth:** JWT required
- **Responses:**
  - `200`: User profile
  - `404`: User not found

### PUT `/api/v1/auth/profile`
Update the authenticated user's profile.
- **Auth:** JWT required
- **Body:** `{ "name", "timezone", "language", "profile_image", "bio", ... }`
- **Responses:**
  - `200`: Profile updated
  - `400`: Invalid input
  - `404`: User not found

---

## Tasks

### GET `/api/v1/task/tasks`
Get all tasks for the current user.
- **Auth:** JWT required
- **Responses:**
  - `200`: List of tasks
  - `404`: User not found

### POST `/api/v1/task/tasks`
Create a new task.
- **Auth:** JWT required
- **Body:** `{ "title": str, "description": str }`
- **Responses:**
  - `201`: Task created
  - `400`: Missing required field
  - `404`: User not found

### GET `/api/v1/task/tasks/<task_id>`
Get a specific task by ID.
- **Auth:** JWT required
- **Responses:**
  - `200`: Task found
  - `404`: Task or user not found

### PUT `/api/v1/task/tasks/<task_id>`
Update a specific task by ID.
- **Auth:** JWT required
- **Body:** `{ "title", "description", ... }`
- **Responses:**
  - `200`: Task updated
  - `404`: Task or user not found

---

## Progress

### POST `/api/v1/progress/`
Create a new progress entry for the authenticated user.
- **Auth:** JWT required
- **Body:** `{ "description": str, "status": str }`
- **Responses:**
  - `201`: Progress entry created
  - `400`: Invalid input
  - `500`: Server error

### GET `/api/v1/progress/`
Get all progress entries for the authenticated user.
- **Auth:** JWT required
- **Responses:**
  - `200`: List of progress entries
  - `500`: Server error

---

## Analytics

See `analytics_api.md` for full details.

### GET `/api/v1/analytics`
Get analytics for the current user.
- **Auth:** JWT required
- **Responses:**
  - `200`: Analytics data
  - `404`: User not found
  - `500`: Failed to calculate analytics

### POST `/api/v1/analytics`
Create a new analytics entry for a task.
- **Auth:** JWT required
- **Body:** `{ "task_id": str, "time_spent": int (seconds) }`
- **Responses:**
  - `201`: Analytics entry created
  - `400`: Invalid input
  - `404`: User or task not found
  - `500`: Failed to create analytics entry

---

## Admin (User Management)

### GET `/api/v1/admin/users`
List all users (admin only).
- **Auth:** JWT (admin role)
- **Responses:**
  - `200`: List of users
  - `500`: Failed to retrieve users

### GET `/api/v1/admin/users/<user_id>`
Get a user by ID (admin only).
- **Auth:** JWT (admin role)
- **Responses:**
  - `200`: User found
  - `404`: User not found

### PUT `/api/v1/admin/users/<user_id>`
Update a user by ID (admin only).
- **Auth:** JWT (admin role)
- **Body:** `{ "name", "username", "email", ... }`
- **Responses:**
  - `200`: User updated
  - `400`: Invalid input
  - `404`: User not found
  - `500`: Failed to update user

### DELETE `/api/v1/admin/users/<user_id>`
Delete a user by ID (admin only).
- **Auth:** JWT (admin role)
- **Responses:**
  - `200`: User deleted
  - `404`: User not found
  - `500`: Failed to delete user

---

## Notes
- All endpoints require a valid JWT token in the `Authorization` header: `Bearer <token>` unless otherwise noted.
- For detailed schemas and live testing, use the Swagger UI (`/apidocs`) when the backend is running.
- See `analytics_api.md` for analytics endpoint details.
