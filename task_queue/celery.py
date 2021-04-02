
from celery import Celery
celery_app = Celery('task_queue',\
                    broker='redis://localhost', 
                    backend='redis://localhost',
                    include=['task_queue.detection_task'])