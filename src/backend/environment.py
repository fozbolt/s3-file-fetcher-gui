import os
from dotenv import load_dotenv

def loadEnvironmentKeys(environmentName):
    for var in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_LOCALSTACK_PORT"]:
        os.environ.pop(var, None)  # remove if it exists

    envFile = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../", f".env.{environmentName}"))
    
    if not os.path.exists(envFile):
        raise FileNotFoundError(f"Environment file {envFile} does not exist.")
    
    load_dotenv(envFile, override=True)
    awsAccesKeyId = os.getenv("AWS_ACCESS_KEY_ID")
    awsSecretKey = os.getenv("AWS_SECRET_ACCESS_KEY")
    awsLocalstackPort = os.getenv("AWS_LOCALSTACK_PORT")

    return {
        "awsAccesKeyId": awsAccesKeyId,
        "awsSecretKey": awsSecretKey,
        "awsLocalstackPort": awsLocalstackPort,
    }


def loadEnvironmentName(environmentName, bucketAlias):
    envFile = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../", f".env.{environmentName}"))
    if not os.path.exists(envFile):
        raise FileNotFoundError(f"Environment file {envFile} does not exist.")
    
    load_dotenv(envFile, override=True)
    dailyBucketName = os.getenv("AWS_DAILY_CACHE_BUCKET_NAME")
    storeBucketName = os.getenv("AWS_STORE_BUCKET_NAME")

    return dailyBucketName if bucketAlias == 'dailyBucket' else storeBucketName