# -*- encoding: utf-8 -*-
import multiprocessing

bind = "0.0.0.0:5000"

# The Access log file to write to, same as --access-logfile
# Using default "-" makes gunicorn log to stdout - perfect for Docker.
# The access log records information about incoming HTTP requests,
# including details like the request method, URL, response status,
# and timing information. It's a useful tool for monitoring and debugging web server activity.
# Example 1: 127.0.0.1 - - [20/Nov/2023:12:34:56 +0000] "GET /example" 200 1234
# Example 2: [17/Nov/2023:16:28:10 +0000] "POST /dash/_dash-update-component HTTP/1.1" 204 0 "https://example.com/" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
# accesslog = "-"
accesslog = None

# Same as --log-file or --error-logfile. Default "-" goes to stderr for Docker.
errorlog = "-"

# We overwrite the below loglevel in __init__.py
# loglevel = "info"

# Redirect stdout/stderr to specified file in errorlog.
# By default, Gunicorn separates the application's standard output and standard error.
# Standard output is sent to the access log, and standard error is sent to the error log.
# Using --capture-output combines both output and error messages into the error log.
capture_output = True
enable_stdio_inheritance = True

# gevent setup
worker_class = "gevent"
# Typically Docker handles the number of workers, not Gunicorn
# https://docs.gunicorn.org/en/latest/design.html
# recommend (2 x $num_cores) + 1 as the number of workers to start off with.
# While not overly scientific, the formula is based on the assumption that for a given core,
# one worker will be reading or writing from the socket while the other worker is processing a request.
# workers = 5
workers = multiprocessing.cpu_count() * 2 + 1
# Run each "Gthread" worker with the specified number of threads
# This setting only affects the Gthread worker type
# https://docs.gunicorn.org/en/latest/settings.html#threads
# threads = 4
# The maximum number of simultaneous clients.
# This setting only affects the gthread, eventlet and gevent worker types.
# Default: 1000
worker_connections = 1000
# Timeout in seconds (default is 30)
# Workers silent for more than this many seconds are killed and restarted.
# The larger the value, the more time gunicorn will wait for a worker to finish tasks.
# Apparently larger values will make the the site more reliable under load.
timeout = 300

# Directory to use for the worker heartbeat temporary file.
# Use an in-memory filesystem to avoid hanging.
# In AWS an EBS root instance volume may sometimes hang for half a minute
# and during this time Gunicorn workers may completely block.
# https://docs.gunicorn.org/en/stable/faq.html#blocking-os-fchmod
worker_tmp_dir = "/dev/shm"
