FROM ubuntu:latest

# Author
MAINTAINER "Alireza Km - alireza.karami.m@gmail.com"

# Define Wroking Directory
WORKDIR /opt

# SET YOUR config.json variables here (Required Variables)
ENV TOKEN "PASTE_TOKEN_HERE"

## Optional Variables
# uncomment it , pass `!id` command in group to get group id in log mode.
ENV ENABLE_GET_CHAT_ID true

# features_handler
ENV features_handler.TELEGRAM_LINK_REMOVER true
ENV features_handler.REMOVE_STATUS_MESSAGES true
ENV features_handler.GROUP_LINK_ENABLE true

# PROXY Variables
# ENV PROXY_ON true
# ENV PROXY_URL "http://127.0.0.1:8123/"

# webhook variables
# ENV WEB_HOOK_ON false
# ENV WEB_HOOK_ADDRESS "https://[IP OR DOMAIN]"
# ENV WEB_HOOK_PORT "PORT"
# ENV WEB_HOOK_LISTEN "[IP , Using 0.0.0.0 as default]"

# Admin Group Chat ID
# ENV ADMINS_GROUP_CHAT_ID <ID>

# Register Timer (Minute)
# ENV REGISTER_TIMER_MINUTES 1



# Install Project Requirements
RUN apt-get update
RUN apt-get install python3-pip git -y

# copy to container
ADD . BOT

# Change Working Directory
WORKDIR /opt/BOT

# Install Application Requirements
RUN pip3 install -r requirements.txt

# Run The Bot
ENTRYPOINT ["python3", "Main.py"]