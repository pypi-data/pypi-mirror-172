''' Read config file to provide GHConf object
'''
import socket
import json

class GHConf():
    CONF_FILE = "/home/gh/.gh/gh_conf.json"

    def __init__(self, gh_name:str=None, json:str=None):
        if gh_name:
            self.gh_name = gh_name
        else:
            hostname = socket.gethostname()
            if "Greenhouse" in hostname:
                self.gh_name = hostname 
            else:
                self.gh_name = "GreenHouseTestingFFFF"

        if json:
            self.json = json
        else:
            self.json = self._get_conf()

    @property
    def name(self) -> str:
        return self.gh_name

    @property
    def group(self) -> str:
        return self.gh_name[-4:-2]

    @property
    def number(self) -> str:
        return self.gh_name[-2:]

    @property
    def version(self) -> str:
        return self.json["gh_conf"]["version"]

    @property
    def servo_cw_position(self) -> str:
        return self.json["gh_conf"]["servo_cw_position"]

    @property
    def servo_ccw_position(self) -> str:
        return self.json["gh_conf"]["servo_ccw_position"]

    @property
    def ws_url(self) -> str:
        return self.json["gh_conf"]["ws_url"]

    @property
    def api_key(self) -> str:
        return self.json["gh_conf"]["api_key"]

    @property
    def base_key(self) -> str:
        return self.json["gh_conf"]["base_key"]

    def _get_conf(self) -> dict:
        with open(self.CONF_FILE ) as json_data_file:
            data = json.load(json_data_file)
        return data

    def _set_conf(self, data:dict):
        with open(self.CONF_FILE , "w") as outfile:
            json.dump(data, outfile)

