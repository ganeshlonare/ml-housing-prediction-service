# FastAPI-ml-Housing-Prices-predictor
# Housing Price Prediction API

[![Python Version](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![Docker](https://img.shields.io/badge/Docker-Powered-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A robust RESTful API built with FastAPI to predict housing prices using a machine learning model. The application is fully containerized with Docker and features secure user authentication with JWT.

---

## Live Demo

You can access the live, deployed version of this application here:

- **Live API URL**: `[YOUR DEPLOYED APP URL - e.g., https://housing-api.onrender.com]`
- **Interactive Docs (Swagger UI)**: `[YOUR DEPLOYED APP URL]/docs`



---

## Features

-   **User Authentication**: Secure user registration and login using JWT access tokens.
-   **Protected Endpoints**: Prediction endpoint is secured and requires a valid JWT token.
-   **ML Model Integration**: Seamlessly integrated with a Scikit-learn model for real-time price predictions.
-   **On-Demand Model Training**: An endpoint to trigger the training of the machine learning model from a CSV file.
-   **Containerized**: Fully containerized using Docker and Docker Compose for easy setup and deployment.
-   **Interactive API Docs**: Automatic, interactive API documentation powered by Swagger UI.

---

## Tech Stack

| Technology   | Description                                            |
| :----------- | :----------------------------------------------------- |
| **Python** | Core programming language                              |
| **FastAPI** | High-performance web framework for building the API    |
| **PostgreSQL** | Relational database for storing user and prediction data |
| **SQLAlchemy** | Object Relational Mapper (ORM) for database interaction |
| **Scikit-learn** | For building and training the regression model         |
| **Docker** | For containerizing the application and database        |
| **JWT** | For securing API endpoints via token authentication    |
| **Uvicorn** | ASGI server for running the application                |

---

## Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

-   [Git](https://git-scm.com/)
-   [Docker](https://www.docker.com/products/docker-desktop/)
-   [Docker Compose](https://docs.docker.com/compose/install/)

### Local Installation & Setup

1.  **Clone the repository:**
    ```sh
    git clone [YOUR GITHUB REPOSITORY URL]
    cd [YOUR REPOSITORY FOLDER NAME]
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root directory by copying the example file. This file will hold your environment variables.
    ```sh
    cp .env.example .env
    ```
    You can modify the `SECRET_KEY` in the `.env` file if you wish.

3.  **Build and run the application with Docker Compose:**
    This single command will build the Docker images for the API and the database, and then start the containers.
    ```sh
    docker compose up --build
    ```

4.  **Access the application:**
    Once the containers are running, you can access the application:
    -   **API Docs**: Open your browser and go to `http://localhost:8000/docs`

---

## API Endpoints

The best way to test the endpoints is through the interactive `/docs` page.

| Method | Endpoint | Description                                    | Auth Required |
| :----- | :------- | :--------------------------------------------- | :------------ |
| `POST` | `/users` | Register a new user with a username and password. | No            |
| `POST` | `/token` | Log in to get a JWT access token.                | No            |
| `POST` | `/predict` | Predict a house price. Requires a valid JWT token. | **Yes** |

### How to Test the Protected `/predict` Endpoint:
1.  Use the `/users` endpoint to create an account.
2.  Use the `/token` endpoint with your new credentials to get an access token.
3.  On the `/docs` page, click the "Authorize" button and paste your token in the format `Bearer <YOUR_TOKEN>`.
4.  You can now successfully make requests to the `/predict` endpoint.

---

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py        # FastAPI app, endpoints
│   ├── ml_model.py    # Model training and loading
│   ├── crud.py        # Database Create, Read, Update, Delete operations
│   ├── models.py      # SQLAlchemy database models
│   ├── schema.py      # Pydantic data validation schemas
│   └── auth.py        # Authentication logic and JWT handling
├── model/
│   └── model.pkl      # Pre-trained model file (if included)
├── .env.example       # Example environment variables
├── Dockerfile         # Instructions to build the API Docker image
├── docker-compose.yml # Defines the multi-container setup (API + DB)
└── requirements.txt   # Python dependencies
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
