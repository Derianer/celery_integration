broker_url = 'redis://localhost'
result_backend = 'redis://localhost'
imports = ('detection.detection_task')
worker_concurrency = 1
worker_prefetch_multiplier = 1