FROM ubuntu
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install -y nano
RUN apt-get install -y git 
RUN apt-get install -y python3 
RUN apt-get install -y python3-opencv
RUN apt-get install -y python3-pip
RUN pip3 install Pillow
RUN git clone https://github.com/Askarpour/enforce.git
RUN chmod -R +x /enforce
