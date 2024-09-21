import os
import json
from connection import connectToS3
from backendHelperFunctions import getFilePath, createDirectory, createUniqueFileName, saveAndOpenFile
import argparse


def fetchVehicleData(environmentName, storeId):
    try: 
        convertedStoreId = getFilePath(storeId)
        response = connectToS3(environmentName).get_object(Bucket=os.environ["AWS_STORE_BUCKET_NAME"], Key=convertedStoreId)
        result = json.load(response["Body"])

        storeBucketPath = createDirectory("storeBucket")
        outputFileName = createUniqueFileName(storeBucketPath, storeId)

        saveAndOpenFile(outputFileName, result)

        return {
            "message": f"Success: Data for store ID {storeId} fetched and saved successfully.", 
            "status": "success"
        }


    except Exception as e:
        # TODO separate aws boto errors, json errors and other erros
        return {
            "message": f"Error: An unexpected error occurred. {str(e)}", 
            "status": "error"
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch store data from S3.")
    parser.add_argument('env', type=str, help='Environment (dev, stage, prod)')
    parser.add_argument('storeId', type=str, help='The ID of the vehicle to fetch')

    args = parser.parse_args()

    fetchVehicleData(args.env, args.storeId)