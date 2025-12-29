# Social Media API

## Setup
- Install dependencies
- Run migrations
- Start server

## Authentication
- POST /register → returns token
- POST /login → returns token
- GET /profile → requires token

## Posts and Comments API

### Endpoints
- GET /api/posts/
- POST /api/posts/
- GET /api/comments/
- POST /api/comments/

Authentication is required for creating, updating, and deleting posts or comments.
Follow System:
POST /follow/<user_id>/
POST /unfollow/<user_id>/

Feed:
GET /feed/
Returns posts from followed users ordered by newest first.

