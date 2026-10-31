import base64
from datetime import datetime,timedelta
import time
from sfhelpers.defaults import ACCEPTED_CHARACTER_LOGIN_KEYS,SERVER_MAP

CHARACTERS_URL = "https://sso.playa-games.com/json/client/characters"

def get_characters(session):
    resp = session.get(CHARACTERS_URL).json()
    characters = [{"name": character["name"], "uuid": resp["uuid"],
                   "server_id": str(character["server_id"]),"character_id": character["id"]
                                        } for character in resp["data"]["characters"]]
    return characters

def get_character_status(session,character_data):
    number = "315000000000" #I didn't know what it represents
    params = "/".join([character_data["uuid"],character_data["character_id"],"unity3d_webglplayer",
                       f"/{number}",character_data["server_id"]])
    params = base64.b64encode(params.encode()).decode()

    url = f"https://{SERVER_MAP.server_map[character_data["server_id"]]}/cmd.php?req=SFAccountCharLogin&params={params}&sid=0-00000000000000"
    
    resp = session.get(url)
    print(resp.text)
    resp_as_list = [tuple(value.split(":")) for value in (resp.text).split("&") if value.strip()]
    resp_dict = {k:ACCEPTED_CHARACTER_LOGIN_KEYS[k](v) for k,v in resp_as_list if k in ACCEPTED_CHARACTER_LOGIN_KEYS.keys()}

    if(not character_data.get("timezone_diff","")): character_data["timezone_diff"] = caluclate_timezone(resp_dict["timestamp"])

    return resp_dict

def caluclate_timezone(server_timestamp):
    return datetime.fromtimestamp(server_timestamp) - datetime.fromtimestamp(time.time())

def calculate_remaining(time_diff,target):
    remaining =  ((datetime.fromtimestamp(target) - time_diff) - datetime.now())
    return str(remaining)[:str(remaining).find(".")] if remaining > timedelta(0) else "Done"

