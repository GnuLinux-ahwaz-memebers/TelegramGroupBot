FROM ubuntu:latest

# Author
MAINTAINER "Alireza Km"

# Define Wroking Directory
WORKDIR /opt
# Copy Project Code to Container
COPY . /opt

# Install Project Requirements
RUN apt-get update
RUN apt-get install python3-pip -y

# Install Application Requirements
RUN pip3 install -r requirements.txt

# Run The Bot
ENTRYPOINT ["python3", "Main.py"]