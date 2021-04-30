import random
import sys
import time
import cv2
from celery import Task, exceptions
from task_queue.celery import celery_app
from detection.card_detection import card_detection, darknet


class DetectionError(Exception):
    def __init__(self):
        super().__init__("Faill to detect cards")

class DetectionTask(Task):

    def __init__(self):
        self._network_preloaded = False
        # self._preload_network()
    
    def __call__(self, *args, **kwargs):
        try:
            if not self._network_preloaded:
                self._preload_network()
            result = self.run(*args, **kwargs)
            return result
        except:
            raise 

    def _preload_network(self):
        sys.argv = [sys.argv[0]]
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
        self._network_preloaded = True
    


@celery_app.task(base=DetectionTask)
def detect_cards(a):
    start = time.time()
    image = cv2.imread('./detection/1.jpeg')
    res_dict = card_detection.image2dict(image, detect_cards.args, detect_cards.network, detect_cards.class_names, detect_cards.class_colors)
    end = time.time()
    print(f'Recognition time:{end-start}')
    return res_dict

