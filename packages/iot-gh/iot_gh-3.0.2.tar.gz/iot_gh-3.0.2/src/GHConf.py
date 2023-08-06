''' Config dictionary used for testing GHService
THIS FILE IS K2 HIDDEN
IoTGreenHouseService reads config file in users directory
'''
CONF = {
        "gh_conf": {
            "version":	"3.0"
            ,"servo_cw_position": 650 
            ,"servo_ccw_position": 1200
            ,"ws_url": "https://api.airtable.com/v0/"
            ,"api_key": "keyD9pfsogQQNbiyL"
            ,"base_key": "appdUQ44rMKJhKcPf"
        }
    }

class GHConf():
    # CONF_FILE = "/home/gh/.gh/gh_conf.json"

    def __init__(self):
        self.json = CONF

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

    # def _get_conf(self) -> dict:
    #     with open(self.CONF_FILE ) as json_data_file:
    #         data = json.load(json_data_file)
    #     return data

    # def _set_conf(self, data:dict):
    #     with open(self.CONF_FILE , "w") as outfile:
    #         json.dump(data, outfile)

