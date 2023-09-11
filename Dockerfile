FROM python:3.10-slim
 
RUN apt-get update

RUN mkdir -p /home/app
WORKDIR /home/app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv==2023.9.8
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv sync
ENV PATH=/home/app/.venv/bin:${PATH}

COPY app.py ./

CMD gunicorn --workers=5 --threads=1 -b 0.0.0.0:80 app:server
