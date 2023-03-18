# iwd
iwd repo
# FreeCovery

This is the back-end of a website built using **Django 4**.



## Table of Contents 
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Run the application](#run-the-application)
- [View the application](#view-the-application)
- [Copyright and License](#copyright-and-license)


## Prerequisites

Install the following prerequisites:

1. [Python 3.10.4 or higher](https://www.python.org/downloads/)
2. [Visual Studio Code](https://code.visualstudio.com/download), or any code editor.


## Installation
### 1. Clone the repository in root directory:
```bash
git clone https://github.com/hiba247/iwd
```

### 2. Create a virtual environment

From the **root** directory run:

```bash
python -m venv venv
```

### 3. Activate the virtual environment

From the **root** directory run:

On macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\scripts\activate
```

### 4. Install required dependencies

From the **root** directory run:

```bash
pip install -r requirements.txt
```

### 5. Run migrations

From the **root** directory run:

```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
### 6. Run the development server
```bash
python manage.py runserver
```

## View the application

Go to http://127.0.0.1:8000/ to view the application.
Preferably, since it's only a back-end, you should use it with postman or django's browsable API.

## Order of routes

The database is empty as of now, so I advise you to start with the following endpoits so you can populate the database, and then access the other endpoints:
http://127.0.0.1:8000/register/    # To create user instances
http://127.0.0.1:8000/create_post/   # To create post instance, requires an authenticated user session
http://127.0.0.1:8000/post/<int:id>/add_comment/   # To create a comment, requires an authenticated user session and a post
http://127.0.0.1:8000/psychologist/register/   # To create a psychologist instance
http://127.0.0.1:8000/create_post/add_article/    # To create an article instance, requires an authenticated user
http://127.0.0.1:8000/create_post/add_event/    # To create an event instance, requires an authenticated user
