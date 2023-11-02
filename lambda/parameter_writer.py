"""Use an SNS message fired by ImageBuilder to write an AMI id to an SSM
parameter."""
import os
import json
import logging
import boto3

PARAMETER_PREFIX = os.environ.get("PARAMETER_PREFIX", "/images/ami")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "info")
TESTING = os.environ.get("TESTING", None)

loglevels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "error": logging.ERROR
        }
logger = logging.getLogger("ImageBuilderParamWriter")
logger.setLevel(loglevels[LOG_LEVEL])
if TESTING:
    logger.addHandler(logging.StreamHandler())

def handler(event, context):
    """Write an ami-id to a parameter at PARAMETER_PREFIX."""
    # pylint: disable=unused-argument
    message = json.loads(
            event["Records"][0]["Sns"]["Message"])
    recipe = message.get("versionlessArn", None).split("/")[-1]
    if not recipe:
        logger.info("Recipe name not found.")
        return {
                "status": "OK",
                "statusCode": 200,
                "message": "Recipe not found."
                }
    outputs = message.get("outputResources", None)
    if not outputs["amis"]:
        logger.info("No output resources found.")
        logger.info("%s", str(message["state"]))
        return {
                "status": "OK",
                "statusCode": 200,
                "message": message["state"]
                }
    ami = outputs["amis"][0]["image"]
    if TESTING:
        sess = boto3.Session(profile_name="sandbox")
        ssm = sess.client("ssm")
    else:
        ssm = boto3.client("ssm")
    func_args = {
            "Name": f"{PARAMETER_PREFIX}/{recipe}",
            "Description": f"Latest AMI for {recipe}",
            "DataType": "text",
            "Overwrite": True,
            "Value": ami,
            "Type": "String",
            "AllowedPattern": "^ami-[0-9a-f]{17}$"
            }
    logger.info("Writing parameter for %s/%s", PARAMETER_PREFIX, recipe)
    logger.info("Value is %s", ami)
    ssm.put_parameter(**func_args)
    tags = [
            {"Key": "lib:env", "Value": "any"},
            {"Key": "lib:created-by", "Value": "automation"},
            {"Key": "lib:app", "Value": "any"}
            ]
    ssm.add_tags_to_resource(
            ResourceType="Parameter",
            ResourceId=f"{PARAMETER_PREFIX}/{recipe}",
            Tags=tags)
    return {
            "status": "OK",
            "statusCode": 200,
            "message": "Parameter written."
            }
