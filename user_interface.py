import numpy as np
import matplotlib,time,board
from controller import controller
import adafruit_lps35hw

class user_interface:
    def __init__(self):
        self.run = True
        self.current_line = 0
        self.current_menu = 0
        self.previous_menu = 0
        self.controller = controller(self)
        self.controller.screen.clear_screen()
        self.units = 0  # 0:mmHg, 1:psi, 2:kPa
        self.button_pressed = False
        self.i2c = board.I2C()
        self.LPS35HW = adafruit_lps35hw.LPS35HW(self.i2c)
        self.LPS35HW.zero_pressure()

    def reset_LPS35HW(self):
        self.LPS35HW.zero_pressure()

    def hPa_to_mmHg(self,pressure):
        mmHg = pressure*100*0.00750062
        return mmHg

    def hPa_to_PSI(self,pressure):
        PSI = pressure*100*0.000145038
        return PSI

    def hPa_to_kPa(self,pressure):
        kPa = pressure*10
        return kPa
