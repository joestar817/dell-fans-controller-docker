FROM ubuntu:22.04
LABEL maintainer="joestar817@foxmail.com"


RUN apt update && apt install -y \
    ipmitool \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY . /dell-fans-controller-docker
WORKDIR /dell-fans-controller-docker

ENV TZ=Asia/Shanghai
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' >/etc/timezone

CMD ["python3","start.py"]

