import os
from dotenv import load_dotenv
import sys

def getEnvFilePath(environmentName):
    projectRoot = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../"))

    envFile = os.path.join(projectRoot, f".env.{environmentName}")

    if not os.path.exists(envFile):
        raise FileNotFoundError(f"Environment file {envFile} does not exist.")
    
    return envFile

def loadEnvFile(envFile):
    load_dotenv(envFile, override=True)

def loadEnvironmentKeys(environmentName):
    for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_LOCALSTACK_PORT"]:
        os.environ.pop(var, None)

    envFile = getEnvFilePath(environmentName)
    loadEnvFile(envFile)

    awsAccessKeyId = os.getenv("AWS_ACCESS_KEY_ID")
    awsSecretKey = os.getenv("AWS_SECRET_ACCESS_KEY")
    
    awsLocalstackPort = None
    if environmentName == "dev":
        awsLocalstackPort = os.getenv("AWS_LOCALSTACK_PORT")

    if not awsAccessKeyId or not awsSecretKey:
        raise ValueError(f"Missing required AWS environment variables in {envFile}")

    return {
        "awsAccessKeyId": awsAccessKeyId,
        "awsSecretKey": awsSecretKey,
        "awsLocalstackPort": awsLocalstackPort,
    }

def loadBucketName(environmentName, bucketAlias):
    envFile = getEnvFilePath(environmentName)
    loadEnvFile(envFile)

    dailyBucketName = os.getenv("AWS_DAILY_CACHE_BUCKET_NAME")
    storeBucketName = os.getenv("AWS_STORE_BUCKET_NAME")

    if not dailyBucketName or not storeBucketName:
        raise ValueError(f"Missing bucket names in {envFile}")

    if bucketAlias == 'dailyBucket':
        return dailyBucketName
    elif bucketAlias == 'storeBucket':
        return storeBucketName
    else:
        raise ValueError(f"Invalid bucket alias '{bucketAlias}'. Must be 'dailyBucket' or 'storeBucket'.")