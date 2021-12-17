FROM python:3.8-slim


RUN pip3 install --upgrade pip

WORKDIR /app

ENV program addition.py
ENV config config.json

COPY . ./

RUN pip3 install numpy
RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "flasktest.py"]
