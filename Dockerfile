FROM ubuntu:16.04
MAINTAINER wangxinsheng "wangx_0102@126.com"
# 换uestc的源
COPY ./config/sources.list /etc/apt/
COPY ./config/get-pip.py .
RUN apt-get update
# 安装允许环境
RUN apt-get install -y python python3.5  gcc g++ $buildDeps && \
    apt-get install -y openjdk-8-jdk curl python3-pip
RUN cp /usr/bin/python /usr/bin/python_bak &&\
    rm /usr/bin/python &&\
    ln -s /usr/bin/python3.5 /usr/bin/python
ADD . /code
WORKDIR /code
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r  requirements.txt
RUN python run.py
EXPOSE 5000


