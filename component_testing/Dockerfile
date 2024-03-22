ARG UBUNTU_VERSION=22.04
FROM ubuntu:${UBUNTU_VERSION} as base
ARG AWS_REGION=us-east-1
ARG NO_USER=yes
ENV AWS_REGION=$AWS_REGION
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
WORKDIR /usr/local/bin

FROM base as mantic
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/America select UTC" | debconf-set-selections && \
    apt-get update && \
    apt-get install -y \
    tzdata \
    ca-certificates \
    wget \
    sudo \
    git \
    apt-utils && \
    wget https://awstoe-${AWS_REGION}.s3.${AWS_REGION}.amazonaws.com/latest/linux/amd64/awstoe && \
    chmod +x /usr/local/bin/awstoe
VOLUME /root/components
WORKDIR /root/components
CMD ["/bin/bash"]

FROM base as kinetic
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/America select UTC" | debconf-set-selections && \
    sed -i -e 's/archive/old-releases/g' -e 's/security/old-releases/' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y \
    tzdata \
    ca-certificates \
    wget \
    sudo \
    git \
    apt-utils && \
    wget https://awstoe-${AWS_REGION}.s3.${AWS_REGION}.amazonaws.com/latest/linux/amd64/awstoe && \
    chmod +x /usr/local/bin/awstoe
VOLUME /root/components
WORKDIR /root/components
CMD ["/bin/bash"]

FROM base as jammy
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/America select UTC" | debconf-set-selections && \
    apt-get update && \
    apt-get install -y \
    tzdata \
    ca-certificates \
    wget \
    sudo \
    git \
    apt-utils && \
    wget https://awstoe-${AWS_REGION}.s3.${AWS_REGION}.amazonaws.com/latest/linux/amd64/awstoe && \
    chmod +x /usr/local/bin/awstoe
VOLUME /root/components
WORKDIR /root/components
CMD ["/bin/bash"]

FROM base as focal
RUN echo "tzdata tzdata/Areas select Etc" | debconf-set-selections && \
    echo "tzdata tzdata/Zones/America select UTC" | debconf-set-selections && \
    apt-get update && \
    apt-get install -y \
    tzdata \
    ca-certificates \
    wget \
    sudo \
    git \
    apt-utils && \
    wget https://awstoe-${AWS_REGION}.s3.${AWS_REGION}.amazonaws.com/latest/linux/amd64/awstoe && \
    chmod +x /usr/local/bin/awstoe
VOLUME /root/components
WORKDIR /root/components
RUN adduser --disabled-password --gecos "" ubuntu
CMD ["/bin/bash"]
