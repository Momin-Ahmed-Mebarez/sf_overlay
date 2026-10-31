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