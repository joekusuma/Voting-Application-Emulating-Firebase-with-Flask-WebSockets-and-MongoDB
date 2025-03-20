# Voting Application

## Overview

The **Voting Application** is a prototype system designed to emulate Firebase's RESTful API using **Flask**, **WebSockets**, and **MongoDB**. This application demonstrates real-time data synchronization, CRUD operations, and a user-friendly interface for creating and managing polls. It serves as an alternative to Firebase for applications requiring real-time interactions and data management.

## Features

- **Real-Time Polling:** Create, view, and vote on polls with instant updates across all connected clients.
- **CRUD Operations:** Full support for creating, reading, updating, and deleting polls and user data.
- **WebSockets Integration:** Ensures real-time data synchronization without the need for manual page refreshes.
- **User Management:** Create and manage user accounts with basic authentication (future implementation).
- **Database Querying:** Advanced querying capabilities to filter and sort user data.
- **Responsive UI:** User-friendly web interface built with Flask and Jinja2 templates.
- **Command-Line Interface:** Interact with the database using curl-like commands for flexibility.

## Technologies Used

### Backend

- **Flask:** Web framework for Python
- **MongoDB:** NoSQL database
- **PyMongo:** MongoDB driver for Python

### Frontend

- **HTML, CSS, JavaScript**
- **Jinja2:** Templating engine for Flask

## Installation

### Prerequisites

- **Python 3.7+**
- **MongoDB Atlas account**
- **Git**

### Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/joekusuma/dsci551-project.git
    cd voting-app
    ```

2. **Create a Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables:**

    - Create a `.env` file in the root directory.
    - Add your MongoDB URI:

    ```env
    MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
    ```

5. **Run the Application:**

    ```bash
    python main.py
    ```

    - Open your browser and navigate to `http://localhost:5000`

## Usage

- **Create Poll:**
  - Navigate to `/create-poll` to create a new poll by providing a title, description, options, author name, and age.

- **View Polls:**
  - Visit `/view-polls` to see all existing polls. You can vote on any poll by selecting an option.

- **Vote on Polls:**
  - Select your preferred option in a poll and submit your vote. The results update in real-time.

- **Query Database:**
  - Go to `/query` to perform custom queries on the user database, such as ordering and limiting results.

- **User Management:**
  - Create new users via `/create-user` and manage user accounts.
