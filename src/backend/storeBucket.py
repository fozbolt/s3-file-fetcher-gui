import os
import json
import subprocess
from datetime import datetime
from connect import s3Client
from backendHelperFunctions import getFilePath
import argparse


def fetchVehicleData(storeId): 
    print(storeId)
    convertedStoreId = getFilePath(storeId)
    response = s3Client.get_object(Bucket=os.environ["AWS_STORE_BUCKET_NAME"], Key=convertedStoreId)
    result = json.load(response["Body"])

    project_root = os.path.dirname(os.path.abspath(__file__))
    storeBucketPath = os.path.join(project_root, "storeBucket")  # if changing this, also change it in .gitignore
    os.makedirs(storeBucketPath, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    outputFileName = os.path.join(storeBucketPath, f"{storeId}_{timestamp}")

    with open(outputFileName, "w") as file:
        json.dump(result, file, indent=4)  # Use json.dump to write the result in JSON format

    # Automatically open the file (macOS)
    subprocess.Popen(['open', outputFileName])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch store data from S3.")
    parser.add_argument('storeId', type=str, help='The ID of the vehicle to fetch')
    args = parser.parse_args()

    fetchVehicleData(args.storeId)