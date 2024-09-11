import os
from datetime import datetime
import hashlib
import subprocess
import json

# ee315ac12567a2b44ae03fc30b093334 -> e/e/3/ee315ac12567a2b44ae03fc30b093334
def getFilePath(storeId):
    return f"{storeId[0]}/{storeId[1]}/{storeId[2]}/{storeId}"

def createDirectory(dirName):
    project_root = os.path.dirname(os.path.abspath(__file__))
    storeBucketPath = os.path.join(project_root, dirName)  # if changing this, also change it in .gitignore
    os.makedirs(storeBucketPath, exist_ok=True)

    return storeBucketPath

def createUniqueFileName(storeBucketPath, storeId):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return os.path.join(storeBucketPath, f"{storeId}_{timestamp}")

def generateDailyBucketParams(vehicleUrl, vehicleUrlBody, date):
    vehicleUrlWithBody = f"{vehicleUrl}{vehicleUrlBody}" 

    md5_hash = hashlib.md5()
    md5_hash.update(vehicleUrlWithBody.encode())
    vehicleUrlHashed = md5_hash.hexdigest()

    convertedDate = date # TODO: add different input format if needed

    return {
        "vehicleUrlHashed": vehicleUrlHashed,
        "dailyBucketKeyPrefix": f"{convertedDate}/{vehicleUrlHashed}"
    }

def saveAndOpenFile(fileName, fileContent):
    with open(fileName, "w") as file:
        json.dump(fileContent, file, indent=4)  # Use json.dump to write the result in JSON format

    # Automatically open the file (macOS)
    subprocess.Popen(['open', fileName])