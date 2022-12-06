FROM python:3.7

WORKDIR /app/

COPY ./main.py /app/
COPY ./requirements.txt /app/
COPY ./train.h5 /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 main:app