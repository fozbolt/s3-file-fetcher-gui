import os
import json
import hashlib
import subprocess
from datetime import datetime
from connect import s3Client
import argparse


def fetchVehicleRawResponse(vehicleUrl, date, vehicleUrlBody):
    vehicleUrlWithBody = f"{vehicleUrl}{vehicleUrlBody}" 

    md5_hash = hashlib.md5()
    md5_hash.update(vehicleUrlWithBody.encode())
    vehicleUrlHashed = md5_hash.hexdigest()
    convertedDate = date

    dailyCacheBucketPrefix = f"{convertedDate}/{vehicleUrlHashed}" 

    response = s3Client.get_object(Bucket=os.environ["AWS_DAILY_CACHE_BUCKET_NAME"], Key=dailyCacheBucketPrefix)
    result = json.load(response["Body"])

    project_root = os.path.dirname(os.path.abspath(__file__))
    dailyBucketPath = os.path.join(project_root, "dailyBucket")  # if changing this, also change it in .gitignore
    os.makedirs(dailyBucketPath, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    outputFileName = os.path.join(dailyBucketPath, f"{vehicleUrlHashed}_{timestamp}")

    with open(outputFileName, "w") as file:
        json.dump(result, file, indent=4)  # Use json.dump to write the result in JSON format

    # Automatically open the file (macOS)
    subprocess.Popen(['open', outputFileName])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and save vehicle data.")
    parser.add_argument('vehicleUrl', type=str, help='The URL of the vehicle to process')
    parser.add_argument('date', type=str, help='date in format YYYYMMDD, example: 20240821')
    parser.add_argument('vehicleUrlBody', type=str, nargs='?', default="_undefined", help='The body of the URL of the vehicle to process (optional)')

    args = parser.parse_args()

    fetchVehicleRawResponse(args.vehicleUrl, args.date, args.vehicleUrlBody)

