import hashlib
from curl_cffi import Session,requests
from sfhelpers.defaults import LOGIN_URL,DEFAULT_HEADERS,SERVER_MAP_URL,SERVER_MAP

HASH_CONST = "ahHoj2woo1eeChiech6ohphoB7Aithoh"

def hash_password(password):
    password += HASH_CONST
    password = hashlib.sha1(password.encode()).hexdigest()
    return hashlib.sha1((password + "0").encode()).hexdigest()

def get_session(credentials):
    body = {"username":credentials["username"],"password":credentials["password"],"language":"en"}

    session = Session()
    session.headers.update(DEFAULT_HEADERS)
    
    resp = session.post(LOGIN_URL,data=body,impersonate="chrome").json()
    session.headers.update({"Authorization":"Bearer " + resp["data"]["token"]["access_token"]})

    return session

def fill_server_map():
    resp = requests.get(SERVER_MAP_URL,headers=DEFAULT_HEADERS).json()["servers"]
    SERVER_MAP.server_map = ({str(server["i"]) : server["d"] for server in resp})

