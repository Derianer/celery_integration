#/bin/bash
celery -A task_queue worker -l INFO
