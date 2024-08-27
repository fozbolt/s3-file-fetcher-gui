import boto3
from environment import loadEnvironment

def connectToS3(environmentName):
    environmentVars = loadEnvironment(environmentName)

    return boto3.client(
        's3',
        aws_access_key_id=environmentVars["awsAccesKeyId"],
        aws_secret_access_key=environmentVars["awsSecretKey"]
    )