# Library Project

Welcome to the Library Project! This repository contains the code for a library management system designed to help users manage book inventories, track borrowing and returning of books, and maintain user records.

## Features

- **User Management**: Add, update, and delete user information.
- **Book Inventory**: Manage book details including title, author, genre, and availability status.
- **Borrowing and Returning**: Track which user has borrowed which book and when it is due for return.
- **Search Functionality**: Search for books by title, author, or genre.
- **Reports**: Generate reports on book availability, user activity, and overdue books.

## Installation

To get started with the Library Project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Awesome-Ace22/library_project.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd library_project
    ```
3. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    ```
4. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Flask application, use the following commands:

1. **Set the FLASK_APP environment variable**:
    ```bash
    export FLASK_APP=main.py
    ```
2. **Run the application**:
    ```bash
    flask run
    ```
Open your browser and navigate to `http://localhost:5000` to access the library management system.
