# 📚 Stud Assistant

## 🚀 Project Overview

**Stud Assistant** is a modern student assistant web application built on **FastAPI** (for the backend) and **Vue.js 3** (for the frontend). The project integrates with **Large Language Models (LLM)** via the **LangChain** library to provide intelligent, conversational responses in a chat interface.

The project is architecturally divided into two main components:
1.  **Backend (`backend/`):** The API server handling business logic, database interaction (SQLAlchemy), and LLM processing.
2.  **Frontend (`frontend/`):** The client interface, developed using Vue.js, which manages the user experience.

### Key Features
* **LLM-Powered Chatbot:** Integration with **LangChain** for response generation.
* **Conversation Management:** Functionality to create, retrieve, update, and delete chats.
* **Authentication:** Use of JWT tokens to secure routes (indicated by `Depends(get_current_user)`).
* **ORM and Database:** Utilizes **SQLAlchemy 2.0** for database operations, likely with PostgreSQL (indicated by `psycopg2-binary`).

***

## ⚙️ Technology Stack

| Category | Technology | Details (Versions from `pyproject.toml` and `package.json`) |
| :--- | :--- | :--- |
| **Backend (API)** | **Python** | `>=3.13` (Minimum requirement) |
| | **FastAPI** | `0.117.1` |
| | **ORM** | **SQLAlchemy** `2.0.43`, `fastapi-users-db-sqlalchemy` |
| | **Database** | **PostgreSQL** (uses `psycopg2-binary`, `asyncpg`) |
| | **AI/LLM** | **LangChain**, `langchain-google-genai` |
| **Frontend (UI)** | **JavaScript/TypeScript** | `type: "module"` |
| | **Framework** | **Vue.js** `^3.5.18` |
| | **Routing** | **Vue Router** `^4.5.1` |
| | **HTTP Client** | **Axios** `^1.13.2` |
| | **Bundler** | **Vite** |
| **Deployment** | **Containerization** | **Docker**, **Docker Compose** |

***

## 🛠️ Installation and Setup

The project is configured for execution using **Docker Compose**, which is the recommended method.

### 1. Prerequisites
* **Docker**
* **Docker Compose**

### 2. Configuration (Mandatory)

Create a configuration file named `.env` in the root directory of the project. This file must contain the environment variables required for database connection, LLM settings, and secrets (e.g., `SECRET_KEY`, `DATABASE_URL`, `GOOGLE_API_KEY`, etc.).

### 3. Running with Docker Compose

Execute this command in the root directory:

```
docker-compose up --build
```

**--build** ensures that the images are rebuilt from the latest code.

#### - The Backend (FastAPI) will be available on the port specified in docker-compose.yml.
#### - The Frontend (VueJS) is typically available at http://localhost:7153 .

### 4. Local Run (For Development)
#### A. Backend (FastAPI)

1. Install Python Dependencies:
```
    cd backend
    pip install -r requirements.txt # or poetry install, if using Poetry
```
2. Database Setup:

    - Ensure your database (e.g., PostgreSQL) is running.

3.  Run migrations (if Alembic is used):
```
    - alembic upgrade head
```
4.  Run Server:

```
    uvicorn app.main:app --reload
```
*The API documentation will be available at /docs (Swagger UI)*.

#### B. Frontend (Vue.js)

1. Install Node.js Dependencies:
```
    cd frontend/stud_assistant
    npm install

    # or yarn install / pnpm install
```

2. Run in Development Mode:

```
    npm run dev
```
*The application will be available on the port specified by Vite (usually http://localhost:5173).*

# 🌐 API Endpoints (Backend: FastAPI)

- All routes are protected by the Depends(get_current_user) dependency, which requires a valid JWT token in the header.
- Router: /conversations (Chat Management)

| Method | Route | Description |
| :--- | :--- | :--- |
| **POST** | `/conversations/new-conversation` | Creates a **new conversation** (chat). The initial title is set to "New chat". |
| **GET** | `/conversations` | Retrieves a list of all conversations owned by the current user. The list is ordered by the **last change date** (`date_changed`). |
| **DELETE** | `/conversations/{conversation_id}/delete` | **Deletes a conversation** specified by its unique `{conversation_id}`. |
| **GET** | `/conversations/{conversation_id}` | Retrieves the **full details of a specific conversation**, including the complete list of all messages within it. |
| **PUT** | `/conversations/{conversation_id}` | **Updates the conversation**. It is used to change the conversation's **title** (`title`) and automatically updates the `date_changed` timestamp. |
| **POST** | `/conversations/{conversation_id}/sendmessage` | **Sends a new user message** to the specified conversation and retrieves the AI's immediate response. |

## 📬 Details of POST /conversations/{conversation_id}/sendmessage

This endpoint is the core of the chat functionality.

* **Endpoint:** `/conversations/{conversation_id}/sendmessage`
* **Method:** `POST`
* **Purpose:** To send a user's input to the conversation and receive the corresponding AI-generated reply.
* **Request Body (Expected Data):** Typically requires the **message content** (e.g., a JSON body with a `message` or `text` field).
* **Path Parameter:**
    * `{conversation_id}`: The unique identifier of the chat session to which the message belongs.
* **Response:** The response will usually contain the **AI's generated message**, which is then added to the conversation's message history.


    