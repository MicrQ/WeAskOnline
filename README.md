# WeAsk.Online

WeAsk.Online is a question-and-answer platform that allows users to ask, answer, and engage in discussions on various topics. This API facilitates user registration, login, posting questions, answering questions, and more. It provides full CRUD functionality for managing questions and answers in a secure environment using Flask, SQLAlchemy, and Redis.

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Running the Application](#running-the-application)
4. [Usage Guidelines](#usage-guidelines)
5. [API Documentation](#api-documentation)
    - [Registration](#registration)
    - [Email Verification](#email-verification)
    - [Login](#login)
    - [Create/Post Question](#createpost-question)
    - [Update/Put a Question](#updateput-a-question)
    - [Delete a Question](#delete-a-question)
    - [Get Questions](#get-questions)
    - [Get a Single Question](#get-a-single-question)
6. [Contribution](#contribution)
7. [License](#license)

---

## Overview

WeAsk.Online is designed to provide a seamless experience for users looking to engage in a Q&A community. The application is built using Flask for the web framework, SQLAlchemy for database interactions, and Redis for caching. The architecture is designed for scalability and efficiency, handling user management, question posting, and interactions securely and effectively.

## Installation

To get started with the project, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/MicrQ/WeAskOnline.git
    cd WeAskOnline
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the necessary dependencies from the `requirements.txt` file:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

After installing the necessary dependencies, follow these steps to run the application:

1. Set up your environment variables (for example, using `python-dotenv`):
   - Create a `.env` file and include your configurations like the secret key, database URL, and email SMTP configurations.

    ```bash
    FLASK_APP=app.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    REDIS_URL=your_redis_url
    SMTP_EMAIL=your_email
    SMTP_PASSWORD=your_password
    ```

2. Run the Flask server:

    ```bash
    flask run
    ```

   The API will be available at `http://localhost:5000/`.

## Usage Guidelines

Once the application is running, you can interact with the API to manage questions and answers. Below are some basic usage guidelines:

1. **Authentication**: To access protected endpoints, you need to include an `api-token` in the request headers. This token is obtained after logging in.

2. **Making Requests**: Use tools like `curl`, Postman, or similar to interact with the API. Ensure that you include the necessary headers and payload in your requests.

3. **Handling Responses**: The API responds with JSON objects. Check the status codes and message fields to ensure that your requests were successful.

4. **Error Handling**: If a request fails, review the error message and status code provided in the response. Common errors include invalid credentials, missing parameters, and unauthorized access.

5. **Data Validation**: Ensure that all required fields are provided and valid. For instance, when posting a question, include fields such as `title`, `body`, and optionally `tags`.


## For Contribution

We welcome contributions to `WeAsk.Online!` If you would like to contribute, please follow these steps:

-  Fork the repository.
- Create a feature branch (git checkout -b feature/your-feature).
- Commit your changes (git commit -am 'Add new feature').
- Push to the branch (git push origin feature/your-feature).
- Open a Pull Request on GitHub.

`Please ensure that your code adheres to our coding standards and includes appropriate tests.`

## WeAsk.Online API Documentation
[WeAsk.Online](https://github.com/MicrQ/WeAskOnline/blob/main/docs/v1/v1_docs.md)
## Authors
[Authors](https://github.com/MicrQ/WeAskOnline/blob/main/AUTHORS)
