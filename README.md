# SaaS Event Management Platform

An industry-level event platform built with FastAPI and SQLite.

## Features
- **Level 1**: JWT Authentication & Event CRUD operations.
- **Level 2**: Team registration with capacity constraints & Sub-event timelines.
- **Level 3**: Multi-tenancy (data isolation per user), Real-time Announcements via WebSockets, and Docker support.

## How to Run
1. Install dependencies: `pip install -r requirements.txt python-multipart`
2. Start the server: `uvicorn main:app --reload`
3. Access Docs: `http://127.0.0.1:8000/docs`