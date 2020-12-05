import numpy as np
import matplotlib,time,board,csv,os
from controller import controller
import adafruit_lps35hw

class user_interface:
    def __init__(self):
        self.run = True
        self.current_line = 0
        self.current_menu = 0
        self.previous_menu = 0
        self.units = 0  # 0:mmHg, 1:psi, 2:kPa
        self.button_pressed = False
        self.i2c = board.I2C()
        self.LPS35HW = adafruit_lps35hw.LPS35HW(self.i2c)
        self.LPS35HW.zero_pressure()
        self.test_lengths = [10,20,30]
        self.test_start_time = None
        self.test_end_time = None
        self.test_rate = 10 # hz
        self.last_test_screen_draw = None
        self.run_test = False
        self.controller = controller(self)
        self.controller.screen.clear_screen()

    def reset_LPS35HW(self,zero=False):
        if zero:
            self.LPS35HW.zero_pressure()
        if not zero:
            self.LPS35HW.reset_pressure()

    def get_LPS35HW_measurement(self):
        pressure = self.LPS35HW.pressure
        temperature = self.LPS35HW.temperature
        if self.units == 0:
            pressure = self.hPa_to_mmHg(self.LPS35HW.pressure)
            unit = 'mmHg'
        elif self.units == 1:
            pressure = self.hPa_to_PSI(self.LPS35HW.pressure)
            unit = 'PSI'
        elif self.units == 2:
            pressure = self.hPa_to_kPa(self.LPS35HW.pressure)
            unit = 'kPa'
        else:
            pressure = self.controller.user_interface.LPS35HW.pressure
            unit = 'hPa'
        return pressure,temperature,unit

    def hPa_to_mmHg(self,pressure):
        mmHg = pressure*100*0.00750062
        return mmHg

    def hPa_to_PSI(self,pressure):
        PSI = pressure*100*0.000145038
        return PSI

    def hPa_to_kPa(self,pressure):
        kPa = pressure*0.1
        return kPa

class csv_writer:
    def __init__(self):
        USB_path = self.get_USB_path()
        print(os.getcwd())
        # self.writer = csv.writer(csvfile)

    def get_USB_path(self):
        basedir = '/dev/disk/by-path/'
        for d in os.listdir(basedir):
            if 'usb' in d and 'part' not in d:
                path = os.path.join(basedir,d)
                link = os.readlink(path)
                print('/dev/',os.path.basename(link))
        return True

    def start_csv(self):
        pass

    def write_line(self,time,pressure,temperature,unit):
        pass
