FROM ubuntu
MAINTAINER Stefan Lehmann "stlm@posteo.de"
RUN apt-get update
RUN apt-get install -y build-essential wget qt5-default python3 python3-pip
COPY ./build_pyqt5.sh /root/
COPY ./build_sip.sh /root/
