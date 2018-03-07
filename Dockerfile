# Instructions copied from - https://hub.docker.com/_/python/
FROM python:3.6.4

# Required to view docker's log
# Force the binary layer of the stdout and stderr streams (which is available as their buffer attribute) to be unbuffered. The text I/O layer will still be line-buffered if writing to the console, or block-buffered if redirected to a non-interactive file.
# https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

# tell the port number the container should expose
EXPOSE 8000

# Specify work directory
WORKDIR /usr/src/app

# Copy requirements to the docker Images
COPY requirements requirements

# Install the requirements
RUN pip install -r requirements

COPY . /usr/src/app

# Uncomment if you want to start the app after you start the container
# run the command (app)
CMD ["python", "./app.py"]
CMD ["./start.sh"]
