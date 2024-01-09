# Choosing an image for you container.
FROM python:3.9.7
# Setting your working directory
WORKDIR /EXAMPLE
# This command would copy EVERY FILE from your project folder into your container, so be careful.
COPY . .
# Installing needed packages and dependencies.**
RUN pip install -r requirements.txt
# This command basically executes your main file with Python.
CMD ["python", "bot.py"]
# Setting a port for your app communications with Telegram servers.
EXPOSE 80/tcp
