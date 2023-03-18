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
