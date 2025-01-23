# Celery

- Celery is a task queue.
- Celery Beat is used to schedule tasks.
- The process is:
  - There is a *task producer* (Django application) which communicates with the *broker* (e.g., RabbitMQ, Redis), which acts like a *task queue* for performing tasks asynchronously, based on the *task consumer* (worker).
  - If we need to add task scheduling, we can use *Celery Beat* (task scheduler), which will send the task to the broker based on the schedule for operation.

- Celery requires a "message transport" to send and receive messages.
- *django-celery-results*: used to store results in Django DB and we can view tasks in the Django admin panel.

## Why use Celery?

- Third-party API calls.
- For high CPU intensive tasks.
- Periodic/scheduled tasks.
- For improving the user experience (using async tasks).

## Steps

1. Install the required package: Celery

    ```bash
      pip install celery
    ```

2. Add the following lines in the `settings.py` of your django project:

    ```python
    CELERY_BROKER_URL = "redis://localhost:6379"  # for this, you need to install the Redis server [redis-cli.exe]
    accept_content = ["application/json"]  # Replace CELERY_ACCEPT_CONTENT
    result_serializer = "json"  # Replace CELERY_RESULT_SERIALIZER
    task_serializer = "json"  # Replace CELERY_TASK_SERIALIZER
    timezone = "UTC"  # Replace CELERY_TIMEZONE
    result_backend = "django-db"  # Replace CELERY_RESULT_BACKEND

    # Celery Beat settings
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
    ```

Note:

- for redis, need to download redis (for windows - <https://github.com/tporadowski/redis/releases>) and then install using pip:

  ```bash
    pip install redis
  ```

- for storing these tasks into the DB, need to install *django-celery-results*, following are the steps:

  ```bash
    pip install django-celery-results
  ```

  In settings.py, need to add this:

  ```python
    INSTALLED_APPS = [
    ....
    ....
    "django_celery_results", # for django celery
  ]
  ```

- for scheduling tasks, need to install *django-celery-beat*, following are the steps:

  ```bash
    pip install django-celery-beat
  ```

  In settings.py need to add this:

  ```python
    INSTALLED_APPS = [
    ....
    ....
    "django_celery_beat", # for django beat
  ]
  ```

- If you use celery-results or celery-beat, you need to run this command:

  ```bash
    python manage.py migrate
  ```

3. Create *celery.py* in main project for adding the configuration of celery

4. Add initialization part of celery in *__init__.py* file of main project:

  ```python
  from .celery import app as celery_app

  __all__ = ("celery_app",)
  ```

5. Create a *tasks.py* file for adding all the task, it should be present in the app in which you need to use this task.

6. Now, write the function in *views.py* and need to include the url of the app in which you need to define the task, and add the url of the function (task).

7. After running all the migrate and migrations, we can run the django server:

  ```bash
    python manage.py runserver
  ```

8. Now, in the separate terminal, we can run the following command for starting the celery server:

  ```bash
    celery -A <project>.celery worker -l info
  ```

Note: Windows lacks native support for fork, which is why billiard (or any prefork-based model) can cause permission issues.
Solution

- Switch to a Threaded Worker Model
The simplest fix is to switch from prefork (default) to solo or threads for concurrency. Add the --pool option when starting the Celery worker:

  ```bash
    celery -A celery_project.celery worker -l info --pool=solo
  ```

Or, if you want multithreading:

  ```bash
    celery -A celery_project.celery worker -l info --pool=threads
  ```

9. Now, all set and your celery should works fine.
