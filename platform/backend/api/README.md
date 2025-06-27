# Backend API Endpoints

This document outlines the key REST API endpoints for the Field Hockey Broadcasting Platform backend. These APIs serve the web, mobile, and training interfaces.

## 📚 API Structure

All API endpoints are prefixed with `/api/v1`.

## 🔑 Authentication

Most endpoints require authentication using JWT (JSON Web Tokens). Include the token in the `Authorization` header as `Bearer <token>`.

## 🚀 Endpoints

### 1. User Management

- **`POST /api/v1/auth/register`**
  - **Description**: Register a new user.
  - **Request Body**: `{ "username": "string", "email": "string", "password": "string" }`
  - **Response**: `{ "message": "User registered successfully" }`

- **`POST /api/v1/auth/login`**
  - **Description**: Authenticate user and get JWT token.
  - **Request Body**: `{ "email": "string", "password": "string" }`
  - **Response**: `{ "access_token": "string", "token_type": "bearer" }`

- **`GET /api/v1/users/me`**
  - **Description**: Get current authenticated user's profile.
  - **Authentication**: Required
  - **Response**: `{ "id": "int", "username": "string", "email": "string" }`

### 2. Video Streaming

- **`GET /api/v1/streams`**
  - **Description**: Get a list of available live streams.
  - **Response**: `[ { "id": "int", "title": "string", "description": "string", "hls_url": "string", "status": "live" | "upcoming" | "finished" } ]`

- **`GET /api/v1/streams/{stream_id}`**
  - **Description**: Get details for a specific stream.
  - **Response**: `{ "id": "int", "title": "string", "description": "string", "hls_url": "string", "status": "live" | "upcoming" | "finished", "events": [...] }`

- **`POST /api/v1/streams/upload`**
  - **Description**: Upload a video file or provide a YouTube link for processing.
  - **Authentication**: Admin Required
  - **Request Body**: `{ "file": "binary" }` or `{ "youtube_url": "string" }`
  - **Response**: `{ "message": "Video uploaded/queued for processing", "stream_id": "int" }`

### 3. Player Profiles & Analytics

- **`GET /api/v1/players`**
  - **Description**: Get a list of all registered players.
  - **Response**: `[ { "id": "int", "name": "string", "team": "string", "jersey_number": "int", "profile_image_url": "string" } ]`

- **`GET /api/v1/players/{player_id}`**
  - **Description**: Get detailed profile and statistics for a specific player.
  - **Response**: `{ "id": "int", "name": "string", "team": "string", "jersey_number": "int", "profile_image_url": "string", "stats": { "goals": "int", "assists": "int", "cards": { "yellow": "int", "red": "int" } } }`

- **`GET /api/v1/matches/{match_id}/stats`**
  - **Description**: Get real-time statistics for a specific match.
  - **Response**: `{ "score": "string", "possession": "float", "shots_on_goal": "int", "player_stats": [...] }`

### 4. Community & Interaction

- **`GET /api/v1/streams/{stream_id}/chat`**
  - **Description**: Get recent chat messages for a stream.
  - **Response**: `[ { "user": "string", "message": "string", "timestamp": "datetime" } ]`

- **`POST /api/v1/streams/{stream_id}/chat`**
  - **Description**: Post a new chat message.
  - **Authentication**: Required
  - **Request Body**: `{ "message": "string" }`
  - **Response**: `{ "message": "Message sent" }`

- **`GET /api/v1/streams/{stream_id}/polls`**
  - **Description**: Get active polls for a stream.
  - **Response**: `[ { "id": "int", "question": "string", "options": ["string"], "results": { "option1": "int" } } ]`

- **`POST /api/v1/streams/{stream_id}/polls/{poll_id}/vote`**
  - **Description**: Cast a vote in a poll.
  - **Authentication**: Required
  - **Request Body**: `{ "option": "string" }`
  - **Response**: `{ "message": "Vote cast successfully" }`

### 5. AI Commentary & Events

- **`GET /api/v1/streams/{stream_id}/commentary`**
  - **Description**: Get real-time AI-generated commentary snippets.
  - **Response**: `[ { "timestamp": "datetime", "text": "string", "event_type": "goal" | "card" | "penalty" | "general" } ]`

- **`GET /api/v1/streams/{stream_id}/events`**
  - **Description**: Get detected game events (goals, cards, etc.).
  - **Response**: `[ { "timestamp": "datetime", "type": "goal" | "card" | "penalty", "description": "string", "player_id": "int" } ]`

## 🛠️ Admin & Training Endpoints (Admin Role Required)

- **`POST /api/v1/admin/models/train`**
  - **Description**: Start a new model training job.
  - **Request Body**: `{ "model_type": "cv" | "nlp" | "audio", "config": { ... } }`
  - **Response**: `{ "job_id": "string", "status": "queued" }`

- **`GET /api/v1/admin/models/training_status/{job_id}`**
  - **Description**: Get the status of a training job.
  - **Response**: `{ "job_id": "string", "status": "queued" | "running" | "completed" | "failed", "progress": "float" }`

- **`POST /api/v1/admin/data/upload`**
  - **Description**: Upload training data (videos, annotations).
  - **Request Body**: `{ "file": "binary", "type": "video" | "annotation" }`
  - **Response**: `{ "message": "Data uploaded successfully" }`

---

**Note**: This is a high-level overview. Detailed request/response schemas and error codes will be available in the OpenAPI (Swagger) documentation at `/docs` when the backend is running.
