# Modules
import numpy as np
import matplotlib,time,board
from colorsys import hsv_to_rgb
from PIL import Image,ImageDraw,ImageFont
from user_interface import user_interface

_RUN_ON_PI = False
_RATE = 10

if _RUN_ON_PI:
    import lps33hw_main
    from digitalio import DigitalInOut,Direction
    import adafruit_rgb_display.st7789 as st7789

    # def get_wait_time(self,start_time):
    #     elapsed_time = time.time() - start_time
    #     sleep_time = (1/self.rate) - elapsed_time
    #     return sleep_time

def get_pressure():
    if _RUN_ON_PI:
        t_data,p_data = lps33hw_main.read()
        return p_data
    else:
        return 0.0

def main():
    # Check if MS can communicate with SL
    if _RUN_ON_PI:
        if lps33hw_main.init() == False:
            print('Sensor LPS33HW counld not be initialized')
            exit(1)
        else:
            print('Sensor LPS33HW initialized')
    GUI = user_interface()

    # while GUI.run:
    #     time_start = time.time()
    #     time.sleep(GUI.get_wait_time(time_start))
    #     if GUI.mode == 0:
    #         GUI.draw_menu_screen()
    #         if keyboard.is_pressed('up'):
    #             GUI.get_new_option('U')
    #         elif keyboard.is_pressed('D'):
    #             GUI.get_new_option('D')
    #         print('Mode:',GUI.mode)
    #     elif GUI.mode == 1:
    #         GUI.draw_testing_screen()
    #     pass
    #     # if GUI.mode == 0:
    #     #     print('Menu')
    #     # time.sleep(1)
    if GUI.run:
        GUI.controller.screen.draw_menu1_screen()



if __name__ == "__main__":
    main()
