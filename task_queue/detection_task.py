from .celery import celery_app
from .card_detection import card_detection, darknet
import random
import sys
import time
import cv2
from celery import Task


class DetectionTask(Task):
    def __init__(self):
        self.args = card_detection.parser()
        card_detection.check_arguments_errors(self.args)

        random.seed(3)  # deterministic bbox colors
        self.network, self.class_names, self.class_colors = darknet.load_network(
        self.args.config_file,
        self.args.data_file,
        self.args.weights,
        batch_size=self.args.batch_size
    )
    sys.argv = [sys.argv[0]]
    


@celery_app.task(base=DetectionTask)
def hard_task(a):
    start = time.time()
    image = cv2.imread('./task_queue/1.jpeg')
    res_dict = card_detection.image2dict(image, hard_task.args, hard_task.network, hard_task.class_names, hard_task.class_colors)
    end = time.time()
    print(f'Recognition time:{end-start}')
    return res_dict
