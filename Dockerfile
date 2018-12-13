FROM ubuntu:latest

# Author
MAINTAINER "Alireza Km - alitm28@gmail.com"

# Define Wroking Directory
WORKDIR /opt

# Install Project Requirements
RUN apt-get update
RUN apt-get install python3-pip git -y

# fetch from repo
RUN git clone https://github.com/GnuLinux-ahwaz-memebers/TelegramGroupBot BOT

# Change Working Directory
WORKDIR /opt/BOT

# Install Application Requirements
RUN pip3 install -r requirements.txt

# Run The Bot
ENTRYPOINT ["python3", "Main.py"]