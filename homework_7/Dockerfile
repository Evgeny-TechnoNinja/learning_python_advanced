FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    python3 \
    python-setuptools \
    python3-pip \
    python-dev \
    build-essential
COPY . /app_flask_hw7
WORKDIR /app_flask_hw7
RUN pip install -r requirements.txt
CMD ["python3", "hw7.py"]
