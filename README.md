SaaS Event Management Platform
A robust, multi-tenant backend system designed for managing large-scale events and technology festivals. This platform features secure authentication, data isolation for different organizers, and real-time announcement broadcasting.

🚀 Features
Level 1: Secure User Authentication using JWT tokens and Argon2 password hashing.

Level 2: Hierarchical event timelines (Parent/Sub-events) and business logic for team registrations (size limits 2-5).

Level 3: SaaS Multi-tenancy (data isolation per user), real-time WebSocket announcements, and Docker containerization.

🏗️ Architecture Explanation
This project follows a Modular Monolith architecture built with FastAPI for high performance and SQLAlchemy for database management.

Security: Implements OAuth2 with Password Grant flow. Access is controlled via stateless JWT (JSON Web Tokens).

Multi-Tenancy: The database schema uses an owner_id foreign key on the Events table. The application logic automatically filters data based on the current_user extracted from the JWT, ensuring one organizer cannot see another's data.

Real-Time Layer: A ConnectionManager class handles WebSocket lifecycles, allowing the server to broadcast announcements to all connected clients instantly without page refreshes.

Infrastructure: Containerized using a Dockerfile and Docker Compose to ensure the development environment matches the production environment exactly.

📖 API Documentation
The API is interactive and self-documenting:

Swagger UI: Once the server is running locally, visit http://127.0.0.1:8000/docs. This allows you to test endpoints like /signup, /login, and /events directly.

Redoc: Alternative documentation available at http://127.0.0.1:8000/redoc.

🛠️ Setup Instructions
Local Setup
Clone the repository:

Bash

git clone <your-github-repo-url>
cd SaaS-Event-Platform
Install Dependencies:

Bash

pip install -r requirements.txt python-multipart
Run the Server:

Bash

uvicorn main:app --reload
Docker Setup
If you have Docker installed, you can run the entire stack with one command:

Bash

docker-compose up --build
📹 Demo Walkthrough
Please refer to the submission link for the video demo. The demo covers:

Authentication Flow: Signing up and using the "Authorize" button.

Business Logic: Validation errors when team sizes exceed limits.

Multi-Tenancy: Showing that /my-events only displays events owned by the logged-in user.

WebSockets: Real-time terminal logs showing broadcasted announcements.
