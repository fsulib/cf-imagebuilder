"""Forwards an SNS message to an event bus."""
import os
import json
import logging
from pathlib import Path
import boto3
import botocore

EVENT_BUS_NAME = os.environ.get("EVENT_BUS_NAME", None)
EVENT_SOURCE = os.environ.get("EVENT_SOURCE", "edu.fsu.lib")
TESTING = os.environ.get("TESTING", None)
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")

loglevels = {
        "error": logging.ERROR,
        "info": logging.INFO,
        "debug": logging.DEBUG
        }
logger = logging.getLogger("SNSForwarder")
logger.setLevel(
        loglevels[LOG_LEVEL])
if TESTING:
    logger.addHandler(logging.StreamHandler())

detail_types = {
        "AVAILABLE": "ImageBuilder Job Completion",
        "FAILED": "ImageBuilder Job Failure"
        }

def handler(event, context):
    """Handle incoming SNS; send to Events."""
    logger.info("Received message.")
    message_map = json.loads(event["Records"][0]["Sns"]["Message"])
    logger.info("Message is of type %s", message_map["state"]["status"])
    entry = {
            "Source": EVENT_SOURCE,
            "Detail": message_string,
            "Resources": [
                message_map["sourcePipelineArn"]
                ],
            "DetailType": detail_types[message_map["state"]["status"]],
            "EventBusName": EVENT_BUS_NAME
            }
    if TESTING:
        # Send to default bus if testing.
        entry.pop("EventBusName", None)
    logger.debug("%s", json.dumps(entry))
    if TESTING:
        # Testing using sandbox
        session = boto3.Session(profile_name="sandbox")
        eventbridge = session.client("events")
    else:
        eventbridge = boto3.client("events")
    try:
        response = eventbridge.put_events(Entries=[entry])
        logger.debug("put_events response: %s", json.dumps(response, indent=2))
    except botocore.exceptions.ClientError as error:
        logger.error("%s", error)
    except botocore.exceptions.ParamValidationError as error:
        logger.error("An entry's parameters are invalid.")
    except eventbridge.exceptions.InternalException as error:
        logger.error("%s", error)

if __name__ == "__main__":
    for example in ("example_success.json", "example_failure.json"):
        with Path(f"../test_data/{example}").open(mode="r", encoding="utf8") as eventinput:
            eventmap = json.load(eventinput)
        handler(eventmap, None)
