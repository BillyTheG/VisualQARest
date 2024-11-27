FROM python:3.10.13-slim-bullseye

RUN mkdir -p /app/
RUN mkdir -p /app/Resources
RUN mkdir -p /app/static
RUN mkdir -p /app/src
WORKDIR /app
COPY requirements.txt .
COPY src /app/src
COPY Resources /app/Resources
COPY static /app/static

RUN apt update
RUN apt-get install -y gcc
RUN apt install -y vim
RUN apt install -y iputils-ping
RUN apt install -y libmariadb-dev
RUN pip3 install mariadb==1.0.11
RUN pip3 install -r requirements.txt
WORKDIR /app/src/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]