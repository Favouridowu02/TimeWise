# Analytics API Endpoint Documentation

This document describes the `/api/v1/analytics` endpoints for the TimeWise backend. These endpoints allow authenticated users to retrieve and create analytics data related to their tasks.

## Endpoints

### 1. GET `/api/v1/analytics`
Retrieve analytics for the current user, including total tasks, completed tasks, and total time spent.

**Authentication:** JWT required (Bearer token)

**Responses:**
- `200 OK`: Analytics data retrieved successfully
    ```json
    {
      "total_tasks": 5,
      "completed_tasks": 3,
      "total_time_spent": "3:30:00"
    }
    ```
- `404 Not Found`: User not found
    ```json
    {"error": "User not found"}
    ```
- `500 Internal Server Error`: Failed to calculate analytics
    ```json
    {"error": "Failed to calculate analytics"}
    ```

---

### 2. POST `/api/v1/analytics`
Create a new analytics entry for the current user for a specific task.

**Authentication:** JWT required (Bearer token)

**Request Body:**
```json
{
  "task_id": "string (UUID)",
  "time_spent": 3600  // Time spent in seconds (integer)
}
```

**Responses:**
- `201 Created`: Analytics entry created successfully
    ```json
    {
      "message": "Analytics entry created successfully",
      "analytics": {
        "user_id": "user-uuid",
        "task_id": "task-uuid",
        "total_time_spent": "1:00:00"
      }
    }
    ```
- `400 Bad Request`: Invalid input
    ```json
    {"error": "Invalid input"}
    ```
- `404 Not Found`: User or Task not found
    ```json
    {"error": "User not found"}
    // or
    {"error": "Task not found"}
    ```
- `500 Internal Server Error`: Failed to create analytics entry
    ```json
    {"error": "Failed to create analytics entry"}
    ```

---

## Notes
- All endpoints require a valid JWT token in the `Authorization` header: `Bearer <token>`
- The `time_spent` field in POST requests should be provided in seconds (integer).
- The `total_time_spent` field in responses is formatted as a string (e.g., `"1:00:00"` for one hour).
- Proper error logging and validation are implemented for all endpoints.

---

For more details, see the Swagger UI at `/apidocs` when running the backend.
