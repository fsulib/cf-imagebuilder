#!/usr/bin/env bash

AWS_REGION=${AWS_REGION:-us-east-1}
VERSION_TAG=${VERSION_TAG:-1.0}
dist=${DIST:-focal}

docker build -t ${dist}_awstoe:${VERSION_TAG} \
    --build-arg UBUNTU_VERSION=${dist} \
    --build-arg AWS_REGION=${AWS_REGION} \
    --target ${dist} \
    .
