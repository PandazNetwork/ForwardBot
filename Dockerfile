FROM python:3.10.8-slim-buster
WORKDIR /FORWARDBOT

COPY . .
RUN pip install -r requirements.txt

CMD gunicorn app:app & python3 bot.py

EXPOSE 80/tcp
