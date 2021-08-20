FROM python:3.7-slim-buster

RUN apt-get update
RUN apt-get upgrade -y

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "/usr/src/app/app.py"]
