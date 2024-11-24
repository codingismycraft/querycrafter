FROM python:3.10

WORKDIR /querycrafter
COPY src /querycrafter/src
COPY requirements.txt /querycrafter
RUN pip3 install -r /querycrafter/requirements.txt
EXPOSE 15959
ENV PYTHONPATH="/"
CMD ["python3.10", "/querycrafter/src/server.py"]

