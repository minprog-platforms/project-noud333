FROM python:3.8-slim


RUN pip3 install --upgrade pip

WORKDIR /app

COPY . ./

RUN pip3 install numpy
RUN pip3 install -r requirements.txt

EXPOSE 5000

RUN mkdir json
RUN mkdir output
RUN rm -rf run
RUN mkdir run

ENTRYPOINT ["python3", "simulationrunner.py"]
