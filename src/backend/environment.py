import os
from dotenv import load_dotenv

def loadEnvironment(environmentName):
    envFile = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../", f".env.{environmentName}"))
    
    if not os.path.exists(envFile):
        raise FileNotFoundError(f"Environment file {envFile} does not exist.")
    
    load_dotenv(envFile)

    awsAccesKeyId = os.getenv("AWS_ACCESS_KEY_ID")
    awsSecretKey = os.getenv("AWS_SECRET_ACCESS_KEY")

    return {
        "awsAccesKeyId": awsAccesKeyId,
        "awsSecretKey": awsSecretKey
    }
