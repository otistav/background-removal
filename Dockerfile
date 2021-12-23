FROM python:3.9

WORKDIR /python_server

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 5000

CMD ["python3", "server.py"]