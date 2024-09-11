import os
import json
from connection import connectToS3
from backendHelperFunctions import getFilePath, createDirectory, createUniqueFileName, saveAndOpenFile
import argparse


def fetchVehicleData(environmentName, storeId):
    convertedStoreId = getFilePath(storeId)
    
    response = connectToS3(environmentName).get_object(Bucket=os.environ["AWS_STORE_BUCKET_NAME"], Key=convertedStoreId)
    result = json.load(response["Body"])

    storeBucketPath = createDirectory("storeBucket")
    outputFileName = createUniqueFileName(storeBucketPath, storeId)

    saveAndOpenFile(outputFileName, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch store data from S3.")
    parser.add_argument('env', type=str, help='Environment (dev, stage, prod)')
    parser.add_argument('storeId', type=str, help='The ID of the vehicle to fetch')

    args = parser.parse_args()

    fetchVehicleData(args.env, args.storeId)