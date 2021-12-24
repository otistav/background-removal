FROM python:3.9

WORKDIR /python_server

COPY requirements.txt ./
RUN pip3 install scikit_image
RUN pip3 install scipy
RUN pip3 install torch
RUN pip3 install opencv-python

RUN pip3 install -r requirements.txt
COPY . .
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN ./setup.sh

EXPOSE 5000

CMD ["python3", "server.py"]