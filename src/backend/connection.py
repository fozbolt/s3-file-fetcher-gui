import boto3
from environment import loadEnvironmentKeys

class S3ConnectionManager:
    _instance = None
    _cachedEnv = None
    _s3Client = None
    
    @classmethod
    def connect(cls, environmentName):
        # If the environmentName is different from the cached one, reconnect
        if cls._cachedEnv != environmentName:
            try:
                environmentVars = loadEnvironmentKeys(environmentName)
                
                cls._s3Client = boto3.client(
                    's3',
                    aws_access_key_id=environmentVars["awsAccesKeyId"],
                    aws_secret_access_key=environmentVars["awsSecretKey"],
                    endpoint_url=f"http://localhost:{environmentVars['awsLocalstackPort']}" if environmentVars.get("awsLocalstackPort") else None
                )
                
                cls._cachedEnv = environmentName
            
            except Exception as e:
                print(f"Error: Failed to connect to S3 using {environmentName} environment. {e}")
                raise e
            
        return cls._s3Client

def s3GetClient(environmentName):
    return S3ConnectionManager.connect(environmentName)