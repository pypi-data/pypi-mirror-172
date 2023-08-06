#mock for development

def SpiDev():
    return spidev_mock()

class spidev_mock(object):
    """description of class"""

    max_speed = 0
    def __init__(self):
        pass

    def open(self, num1, num2):
        pass

    def xfer2(self, foo):
        return [1, 0, 512]

