import os
from datetime import datetime
import hashlib
import subprocess
import json
from .environment import loadBucketName, loadEnvironmentKeys

# ee315ac12567a2b44ae03fc30b093334 -> e/e/3/ee315ac12567a2b44ae03fc30b093334
# returns string alert if string doesn't look like storeId (dummy way of checking with length)
# in try because of gui crashing when writing incorrect storeId: tring index out of range 
def getFilePath(storeId):
    try:
        if (len(storeId) == 32):
            return f"{storeId[0]}/{storeId[1]}/{storeId[2]}/{storeId}"
        elif len(storeId) == 0: 
            return ''
        else:
            return 'invalid storeId'
    except Exception as e:
        return ''


def createDirectory(dirName):
    project_root = os.path.dirname(os.path.abspath(__file__))
    storeBucketPath = os.path.join(project_root, dirName)  # if changing this, also change it in .gitignore
    os.makedirs(storeBucketPath, exist_ok=True)

    return storeBucketPath

def createUniqueFileName(storeBucketPath, storeId):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return os.path.join(storeBucketPath, f"{storeId}_{timestamp}")

def generateDailyBucketParams(vehicleUrl, vehicleUrlBody, date):
    vehicleUrlWithBody = f"{vehicleUrl}_{vehicleUrlBody}" if vehicleUrlBody else f"{vehicleUrl}_undefined" #TODO should be handled by fetchVehicleRawResponse default
   
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


def getSortedBucketFileNames(bucketName):
    bucketPath = os.path.join(os.path.dirname(__file__), bucketName)

    try:
        return sorted(
            [name for name in os.listdir(bucketPath) if os.path.isfile(os.path.join(bucketPath, name))],
            key=getDateFromFileName,
            reverse=True,
        )

    except FileNotFoundError:
        print(f"Directory {bucketPath} not found")
        return []
    

def getDateFromFileName(name):
    return int(name.split('_')[-1])


def addRawResponseMapping(vehicleUrl, hash, date, jsonFileName):
    new_entry = {
        "hash": hash,
        "vehicleUrl": vehicleUrl,
        "date": date
    }
    
    if os.path.exists(jsonFileName):
        with open(jsonFileName, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    data.append(new_entry)
    
    with open(jsonFileName, "w") as file:
        json.dump(data, file, indent=4)


def getMappingByHash(hash, jsonFileName):
    if os.path.exists(jsonFileName):
        with open(jsonFileName, "r") as file:
            data = json.load(file)
        
        for entry in data:
            if entry['hash'] == hash:
                return entry['vehicleUrl'], entry['date']
    
    return None, None


def deleteBucketHistory(self, folderName):
    bucketFileNames = getSortedBucketFileNames(folderName)
    deletedFiles = []
    errorFiles = []

    if (len(bucketFileNames) == 0):
        return {
            "message": "Found 0 files for deletion",
            "status": "error"
        }
    
    for fileName in bucketFileNames:
        filePath = f"{os.getcwd()}/src/backend/{folderName}/{fileName}"
        try:
            os.remove(filePath)
            deletedFiles.append(fileName)
        except OSError as e:
            errorFiles.append(f"{fileName}: {e}")
    
    if errorFiles:
        return {
            "message": f"Errors occurred with deletion of: {', '.join(errorFiles)}",
            "status": "error"
        }
    else:
        return {
            "message": f"Successfully deleted all files in {folderName}",
            "status": "success"
        }
    
    
def createReverseCheckBucketCmd(environmentName, filePath, bucketName):
    bucketName = loadBucketName(environmentName, bucketName)
    envKeys = loadEnvironmentKeys(environmentName)
    localStackPort = envKeys["awsLocalstackPort"];

    if environmentName == "dev" and localStackPort:
        return f"aws --endpoint-url=http://localhost:{localStackPort} s3 cp s3://{bucketName}/{filePath} ./"
    else:
        return f"aws s3 cp s3://{bucketName}/{filePath} ./"