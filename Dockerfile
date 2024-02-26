FROM ubuntu:22.04

# set a directory for the app
WORKDIR /usr/src/

# copy all the files to the container
COPY . .

# install dependencies
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip install --no-cache-dir -r requirements.txt
