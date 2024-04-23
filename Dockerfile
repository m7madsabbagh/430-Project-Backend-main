FROM python:3.8

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3","manage.py","runserver", "0.0.0.0:8000"]