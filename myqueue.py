from celery import Celery
import time

app = Celery('myqueue', broker='redis://localhost')

@app.task
def power(x, y):
    time.sleep(2)
    return x**y

result = power.delay(10, 10)

print(result) 