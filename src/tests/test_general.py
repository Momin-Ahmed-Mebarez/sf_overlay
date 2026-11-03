import pytest
from src.credential_manager import load_credentials
from pathlib import Path
HOME = Path(__file__).resolve().parent


class TestCredentials:
    '''
        These are created for me to learn unittesting.
        Since I don't believe json dumps will suddenly start failing.
    '''
    @pytest.mark.parametrize("file,expected",[("files/valid_cred.json",{
    "username": "me@me.com",
    "password": "123"
    }), ("gibbresh",None)])

    def test_load_credentials(self,file,expected):
        if(file == "gibbresh"):
            with pytest.raises(FileNotFoundError):
                load_credentials(HOME / file)
            return
        
        cred = load_credentials(HOME / file)
        
        assert cred == expected


def test_config_equal_backup():
    with open(HOME.parent / "config.txt") as f:
        config = f.readlines()
    with open(HOME.parent / "backup" / "config_backup.txt") as f:
        backup = f.readlines()
    
    assert config[0].strip() == "0:0", "Coordinations aren't 0:0"
    assert config == backup, "Forgot to update backup"
