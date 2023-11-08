#!/usr/bin/env bash

AWS_REGION=us-east-1
VERSION_TAG=1.0

for dist in focal mantic; do
    docker build -t ${dist}_awstoe:${VERSION_TAG} \
        --build-arg UBUNTU_VERSION=${dist} \
        --build-arg AWS_REGION=${AWS_REGION} \
        --target ${dist} \
        .
done
