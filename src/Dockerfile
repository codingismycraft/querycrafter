FROM python:3.10

WORKDIR /querycrafter
COPY /src /src
run pip3 install -r requirements.txt
ENV PYTHONPATH="/"
CMD ["python3.10", "/src/server.py"]

