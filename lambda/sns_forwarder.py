"""Subscribes to a topic, forward to a bus."""
import os
import json
import logging
import boto3

logger = logging.getLogger("SNSForwarder")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

with open("example_success.json", "r", encoding="utf8") as snsinput:
    sns = json.load(snsinput)


