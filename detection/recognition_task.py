import cv2 as cv
from PIL import Image
from task_queue.celery import celery_app
import tesserocr
import io
import sys 



@celery_app.task
def recongition_task(image_data:bytes, *args, **kwargs):
    print(sys.getsizeof(image_data))
    buff = io.BytesIO(image_data)
    # print(sys.getsizeof(buff))
    image = Image.open(buff, 'r', ['jpeg'])
    with open('temp.jpeg', 'wb') as file:
        file.write(buff.getvalue())
    print("Recognition started !!!")
    with tesserocr.PyTessBaseAPI(lang='rus+eng', oem=tesserocr.OEM.LSTM_ONLY,) as api:
            api.SetVariable("preserve_interword_spaces","1")
            api.SetVariable("tessedit_pageseg_mode", "6")
            api.SetImage(image)
            # tic = time.perf_counter()
            recText = api.GetUTF8Text()
            # toc = time.perf_counter()
            # print(f"Tesseract result: {toc - tic:0.4f} seconds\n")
            TSVText = api.GetTSVText(0)                
            return {'text':recText, 'tsv':TSVText}


