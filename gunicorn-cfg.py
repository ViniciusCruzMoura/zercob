#from multiprocessing import cpu_count
bind = '0.0.0.0:8000'
# workers = cpu_count()
# worker_class = "gthread"
# threads = cpu_count()
workers = 1
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
timeout = 120
