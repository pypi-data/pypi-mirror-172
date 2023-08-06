from GHConf import GHConf

class Greenhouse(object):
    """IoT Greenhouse data object"""
    def __init__(self, id=0, conf:GHConf=None): 
        self.id = id
        if conf:
            self.name = conf.name
            self.group = conf.group
            self.number = conf.number
        else:
            self.name = "GreenhouseFFFF"
            self.group = "FF"
            self.number = "FF"
        #house state
        self.led_red_state = None
        self.led_red_status = None
        self.led_white_state = None
        self.led_white_status = None
        self.led_dual_state = None
        self.led_dual_status = None
        self.switch_pb_state = None
        self.switch_pb_status = None
        self.switch_toggle_state = None
        self.switch_toggle_status = None
        self.fan_state = None
        self.fan_status = None
        self.servo_position = None
        self.servo_status = None
        self.heater_state = None
        self.heater_status = None
        self.buzzer_state = None
        self.buzzer_status = None
        self.ain_pot_raw = None
        self.ain_light_raw = None
        self.ain_aux_raw = None
        self.temp_inside_C = None
        self.temp_inside_F = None
        self.temp_outside_C = None
        self.temp_outside_F = None
        self.last_update = None
        self.message = None

    
