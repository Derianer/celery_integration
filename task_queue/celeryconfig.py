broker_url = 'redis://localhost'
result_backend = 'redis://localhost'
imports = ('detection.recognition_task')
accept_content = ['pickle', 'json']
worker_concurrency = 1
worker_prefetch_multiplier = 1