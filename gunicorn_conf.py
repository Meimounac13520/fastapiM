command = '/home/sv-2/Documents/operateurmiddleware/fastapiM/env/bin/gunicorn'
pythonpath = '/home/sv-2/Documents/operateurmiddleware/fastapiM/main'
bind = '0.0.0.0:8000'
workers = 3
worker_class = 'uvicorn.workers.UvicornWorker'
