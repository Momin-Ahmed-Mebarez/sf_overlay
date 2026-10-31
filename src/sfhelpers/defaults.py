LOGIN_URL = "https://sso.playa-games.com/json/login?client_id=i43nwwnmfc5tced4jtuk4auuygqghud2yopx&auth_type=access_token"
SERVER_MAP_URL = "https://sfgame.net/config.json"
HASH_CONST = "ahHoj2woo1eeChiech6ohphoB7Aithoh"
ACCEPTED_CHARACTER_LOGIN_KEYS = {"timestamp":lambda x: int(x)
                                 ,"arena":lambda x: int(x.split("/")[0]),
                                 "characterstatus": lambda x: int(x.split("/")[21])}
DEFAULT_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded'}

class SERVER_MAP():
    server_map = {}