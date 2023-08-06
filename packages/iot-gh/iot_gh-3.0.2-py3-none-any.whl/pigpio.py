#mock for development

HIGH = True
LOW = False
INPUT = False
OUTPUT = True
PUD_OFF = 0
PUD_UP = 1
PUD_DOWN = 3

def pi():
    return pi_mock()

class pi_mock(object):
    """mock of pigpio"""
    _gpio_dict = None

    def __init__(self):
        self.connected = True
        self._gpio_dict = {}

    def stop(self):
        pass

    def set_pull_up_down(self, gpio, pud):
        pass

    def set_mode(self, gpio, mode):
        if mode == INPUT:
            self._gpio_dict[gpio] = HIGH
        else:
            self._gpio_dict[gpio] = LOW

    def read(self, gpio):
        return self._gpio_dict[gpio]

    def write(self, gpio, level):
        self._gpio_dict[gpio] = level

    def hardware_PWM(self, gpio, freq, dc):
        pass





