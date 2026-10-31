from sfhelpers.sf_logining import hash_password
from pathlib import Path
import json

HOME = Path(__file__).resolve().parent

def load_credentials(path=HOME / "credentials.json"):
    with open(path,"r") as f:
        try:
            credentials = json.load(f)
            return credentials
        except json.decoder.JSONDecodeError:
            raise Exception("Add [] to the file credentials.json")
        except Exception as err:
            print("Please check that credentials.json exists")

def obtain_credentials():
    username = input("Enter username (or email): ")
    password = input("Enter password: ")
    password = hash_password(password)
    
    return {"username":username, "password":password}    

def save_credentials(credentials,path=HOME / "credentials.json"):
     with open(path,"w") as f:
            json.dump(credentials,f,indent=4)