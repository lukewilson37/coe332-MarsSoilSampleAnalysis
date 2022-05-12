FROM python:3.9

RUN mkdir /app
WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app


ENTRYPOINT ["python3"]