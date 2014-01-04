import multiprocessing

bind = '127.0.0.1:8000'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 200

accesslog = "/srv/moo-site/gunicorn.access.log"
errorlog = "/srv/moo-site/gunicorn.error.log"
