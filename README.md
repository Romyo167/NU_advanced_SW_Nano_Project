# Django Channels Real-Time Chat Application

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Overview

This project is a real-time chat application built using Django, Django Channels, and WebSockets. It allows multiple users to join different chat rooms and send messages to each other in real-time.

## Features

*   **Real-Time Messaging:** Users can send and receive messages instantly.
*   **Multiple Chat Rooms:** Users can join different chat rooms.
*   **Usernames:** Users can choose a username to identify themselves.
*   **Simple and Clean UI:** The user interface is designed to be intuitive and easy to use.
* **Room selection**: Users can select a room to join.

## Technologies Used

*   **Django:** A high-level Python web framework.
*   **Django Channels:** Extends Django to handle WebSockets, HTTP2, and other asynchronous protocols.
*   **WebSockets:** Provides full-duplex communication channels over a single TCP connection.
*   **HTML, CSS, JavaScript:** For the front-end user interface.
* **Git**: For version control.
* **Github**: For hosting the code.

## Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
    cd YOUR_REPOSITORY_NAME
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Run the Daphne ASGI Server:**
    ```bash
    daphne chatApp.asgi:application -p 8000 -b 0.0.0.0
    ```

7.  **Open Your Browser:**
    *   Go to `http://127.0.0.1:8000/` in your web browser.

## Usage

1.  **Enter a Room Name:** On the home page, enter a name for the chat room you want to join.
2. **Enter a username**: Enter a username to identify yourself.
3.  **Send Messages:** Type your message in the input box and click "Send."
4.  **View Messages:** Messages from other users in the same room will appear in the chat box.

## Project Structure

```` NU_advanced_SW_Nano_Project/ ├── chatApp/ │ ├── init.py │ ├── asgi.py # ASGI application configuration │ ├── settings.py # Django project settings │ ├── urls.py # Project-level URL configuration │ └── wsgi.py # WSGI application configuration ├── myapp/ │ ├── init.py │ ├── consumers.py # WebSocket consumers │ ├── migrations/ # Database migrations │ ├── routing.py # WebSocket URL routing │ ├── templates/ │ │ └── home.html # Chat room template │ ├── urls.py # App-level URL configuration │ ├── views.py # Django views │ └── tests.py # Tests ├── manage.py # Django management script ├── requirements.txt # Project dependencies ├── venv/ # Virtual environment └── db.sqlite3 # Database file ```
