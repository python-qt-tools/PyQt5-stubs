FROM ubuntu
MAINTAINER Stefan Lehmann "stlm@posteo.de"
RUN apt-get update
RUN apt-get install -y build-essential wget qt5-default python3 python3-pip dos2unix
COPY ./build_pyqt5.sh .
RUN dos2unix build_pyqt5.sh
CMD bash build_pyqt5.sh
