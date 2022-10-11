# FROM continuumio/miniconda3:master
FROM continuumio/miniconda3:master-alpine

ENV LANG C.UTF-8 
ENV TZ Asia/Shanghai

COPY ./conf/pip.conf /etc/pip.conf
RUN python3 -m pip install --upgrade pip
COPY ./conf/requirements.txt /usr/src/conf/requirements.txt
RUN pip3 install -r /usr/src/conf/requirements.txt

COPY app /usr/src/app
RUN chmod +x /usr/src/app

WORKDIR /usr/src/app

EXPOSE 5016