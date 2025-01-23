
# Celery Guide

Celery is a powerful task queue that allows for asynchronous task processing. This guide provides step-by-step instructions for setting up Celery with Django and includes details about scheduling tasks with Celery Beat.

## What is Celery?

- **Celery**: A distributed task queue for asynchronous processing.
- **Celery Beat**: An extension for scheduling tasks.
- **Process Overview**:
  - A **task producer** (e.g., Django application) sends tasks to a **broker** (e.g., RabbitMQ, Redis).
  - The broker acts as a **task queue** and forwards tasks to a **task consumer** (worker) for execution.
  - **Celery Beat** enables task scheduling and communicates with the broker to trigger tasks at specified intervals.

## Why Use Celery?

- Handling third-party API calls.
- Managing high CPU-intensive tasks.
- Executing periodic or scheduled tasks.
- Improving user experience with asynchronous task handling.

---

## Setting Up Celery

### 1. Install Celery

Install Celery using pip:

```bash
pip install celery
```

### 2. Configure Celery in `settings.py`

Add the following configuration in your Django project's `settings.py`:

```python
CELERY_BROKER_URL = "redis://localhost:6379"  # Requires Redis server
accept_content = ["application/json"]
result_serializer = "json"
task_serializer = "json"
timezone = "UTC"
result_backend = "django-db"

# Celery Beat settings
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
```

#### Install Redis

Download and install Redis (for Windows, use [this release](https://github.com/tporadowski/redis/releases)) and install the Redis Python client:

```bash
pip install redis
```

---

### 3. Install and Configure `django-celery-results` (fo storing results in DB)

Install the package:

```bash
pip install django-celery-results
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_celery_results",
]
```

Run migrations to set up the database:

```bash
python manage.py migrate
```

---

### 4. Install and Configure `django-celery-beat` (for task scheduling)

Install the package:

```bash
pip install django-celery-beat
```

Add it to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    "django_celery_beat",
]
```

Run migrations:

```bash
python manage.py migrate
```

---

### 5. Create `celery.py` for Configuration

Create a `celery.py` file in your project's main directory and configure Celery.

---

### 6. Initialize Celery in `__init__.py`

Add the following code to the `__init__.py` file in your main project directory:

```python
from .celery import app as celery_app

__all__ = ("celery_app",)
```

---

### 7. Add Task Definitions

Create a `tasks.py` file in your app directory and define your Celery tasks.

---

### 8. Set Up URLs and Views

Define the views for your tasks and include the corresponding URLs in your app's `urls.py`.

---

### 9. Start the Django Server

Run the Django development server:

```bash
python manage.py runserver
```

---

### 10. Start the Celery Worker

Run the Celery worker in a separate terminal:

```bash
celery -A <project>.celery worker -l info
```

#### Note for Windows Users

Windows lacks native support for the prefork model. Use one of the following solutions:

- **Run Celery with the Solo Pool**:

  ```bash
  celery -A <project>.celery worker -l info --pool=solo
  ```

- **Run Celery with Multithreading**:

  ```bash
  celery -A <project>.celery worker -l info --pool=threads
  ```

---

## Verifying the Setup

After completing the steps above, your Celery configuration should be ready. Test your tasks to ensure everything is functioning as expected.
