import time

from celery import Celery

# app = Celery("celery_config.tasks", broker="redis://localhost:6379")
app = Celery("celery_config.tasks", broker="redis://redis:6379")
app.config_from_object("celery_config.celeryconfig")


@app.task
def test_func():
    time.sleep(5)
    print("CEELRY WORKS")
    time.sleep(3)
    print("CEELRY FINISHED")
