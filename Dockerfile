# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8083

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

RUN apt-get update

# telegram bot @HomeCam001_bot
ENV BOT_TOKEN='' 

# chat id of group telegram MyHomeMonitor
ENV CHAT_ID='' 

# MJPEG Stream URL
ENV MJPEG_URL=""

WORKDIR /app
ADD . /app

# Switching to a non-root user, please refer to https://aka.ms/vscode-docker-python-user-rights
RUN useradd appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "app.py"]
