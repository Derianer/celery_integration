from celery import Celery
celery_app = Celery('task_queue')
celery_app.config_from_object('task_queue.celeryconfig')

