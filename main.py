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

    while GUI.run:
        if GUI.current_menu == 0:
            GUI.controller.screen.draw_menu0_screen()
            if not GUI.controller.button_Select.value:
                GUI.current_menu = 1
                GUI.controller.screen.clear_screen()
        if GUI.current_menu == 1:
            GUI.controller.screen.draw_menu1_screen()
            if not GUI.controller.button_Up.value:
                GUI.controller.screen.menu1_line_index -= 1
                if GUI.controller.screen.menu1_line_index < 0:
                    GUI.controller.screen.menu1_line_index = 0
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Down.value:
                GUI.controller.screen.menu1_line_index += 1
                if GUI.controller.screen.menu1_line_index >= len(GUI.controller.screen.menu1_options):
                    GUI.controller.screen.menu1_line_index = len(GUI.controller.screen.menu1_options) - 1
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Select.value:
                if GUI.controller.screen.menu1_line_index == 0:
                    GUI.current_menu = 2
                if GUI.controller.screen.menu1_line_index == 1:
                    GUI.current_menu = 3
                if GUI.controller.screen.menu1_line_index == 2:
                    GUI.current_menu = 4
                if GUI.controller.screen.menu1_line_index == 3:
                    GUI.current_menu = 5
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_B.value:
                GUI.current_menu = 0
                GUI.controller.screen.clear_screen()
        if GUI.current_menu == 2:
            GUI.controller.screen.draw_menu2_screen()
            if not GUI.controller.button_Left.value:
                GUI.current_menu = 1
                GUI.controller.screen.clear_screen()
        if GUI.current_menu == 3:
            GUI.controller.screen.draw_menu3_screen()
            if not GUI.controller.button_Up.value:
                GUI.controller.screen.menu3_line_index -= 1
                if GUI.controller.screen.menu3_line_index < 0:
                    GUI.controller.screen.menu3_line_index = 0
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Down.value:
                GUI.controller.screen.menu3_line_index += 1
                if GUI.controller.screen.menu3_line_index >= len(GUI.controller.screen.menu3_options):
                    GUI.controller.screen.menu3_line_index = len(GUI.controller.screen.menu3_options) - 1
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Select.value:
                if GUI.controller.screen.menu3_line_index == 0:
                    GUI.units = 0
                    GUI.current_menu = 1
                if GUI.controller.screen.menu3_line_index == 1:
                    GUI.units = 1
                    GUI.current_menu = 1
                if GUI.controller.screen.menu3_line_index == 2:
                    GUI.units = 2
                    GUI.current_menu = 1
                GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Left.value:
                GUI.current_menu = 1
                GUI.controller.screen.clear_screen()
        if GUI.current_menu == 4:
            GUI.controller.screen.draw_menu4_screen()
            if not GUI.controller.button_Left.value:
                GUI.current_menu = 1
                GUI.controller.screen.clear_screen()
        if GUI.current_menu == 5:
            GUI.controller.screen.draw_menu5_screen()
            if not GUI.controller.button_Left.value:
                GUI.current_menu = 0
                GUI.controller.screen.clear_screen



if __name__ == "__main__":
    main()
