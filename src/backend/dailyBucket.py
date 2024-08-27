import os
from connection import connectToS3
from backendHelperFunctions import createDirectory,createUniqueFileName, generateDailyBucketParams, saveAndOpenFile
import argparse
import json


def fetchVehicleRawResponse(environmentName, vehicleUrl, date, vehicleUrlBody):
    dailyBucketParams = generateDailyBucketParams(vehicleUrl, vehicleUrlBody, date)
    
    response = connectToS3(environmentName).get_object(Bucket=os.environ["AWS_DAILY_CACHE_BUCKET_NAME"], Key=dailyBucketParams["dailyBucketKeyPrefix"])
    result = json.load(response["Body"])

    dailyBucketPath = createDirectory("dailyBucket")
    outputFileName = createUniqueFileName(dailyBucketPath, dailyBucketParams["vehicleUrlHashed"])

    saveAndOpenFile(outputFileName, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and save vehicle data.")
    parser.add_argument('env', type=str, help='Environment (dev, stage, prod)')
    parser.add_argument('vehicleUrl', type=str, help='The URL of the vehicle to process')
    parser.add_argument('date', type=str, help='date in format YYYYMMDD, example: 20240821')
    parser.add_argument('vehicleUrlBody', type=str, nargs='?', default="_undefined", help='The body of the URL of the vehicle to process (optional)')

    args = parser.parse_args()

    fetchVehicleRawResponse(args.env, args.vehicleUrl, args.date, args.vehicleUrlBody)

