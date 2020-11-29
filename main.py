# Modules
import numpy as np
import matplotlib,time,board
from colorsys import hsv_to_rgb
from PIL import Image,ImageDraw,ImageFont
from user_interface import user_interface

_RUN_ON_PI = False
_RATE = 10

def main():
    GUI = user_interface()
    while GUI.run:
        # Start-up Menu
        if GUI.current_menu == 0:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu0_screen()
            if not GUI.controller.button_Select.value:
                if not GUI.controller.screen.menu0_lockout:
                    GUI.current_menu = 1
                    GUI.controller.screen.menu1_line_index = 0
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
        # Main Menu
        if GUI.current_menu == 1:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu1_screen()
            if not GUI.controller.button_Up.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu1_line_index -= 1
                    if GUI.controller.screen.menu1_line_index < 0:
                        GUI.controller.screen.menu1_line_index = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Down.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu1_line_index += 1
                    if GUI.controller.screen.menu1_line_index >= len(GUI.controller.screen.menu1_options):
                        GUI.controller.screen.menu1_line_index = len(GUI.controller.screen.menu1_options) - 1
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
                    if GUI.controller.screen.menu1_line_index == 0:
                        GUI.current_menu = 2
                    if GUI.controller.screen.menu1_line_index == 1:
                        GUI.current_menu = 3
                    if GUI.controller.screen.menu1_line_index == 2:
                        GUI.current_menu = 4
                    if GUI.controller.screen.menu1_line_index == 3:
                        GUI.current_menu = 5
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_B.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        # Run Test
        if GUI.current_menu == 2:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu2_screen()
            if not GUI.controller.button_Left.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 1
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        # Change Units Menu
        if GUI.current_menu == 3:
            if GUI.previous_menu != GUI.current_menu:
                if GUI.units != GUI.controller.screen.menu3_line_index:
                    GUI.controller.screen.menu3_line_index = GUI.units
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu3_screen()
            if not GUI.controller.button_Up.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu3_line_index -= 1
                    if GUI.controller.screen.menu3_line_index < 0:
                        GUI.controller.screen.menu3_line_index = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Down.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu3_line_index += 1
                    if GUI.controller.screen.menu3_line_index >= len(GUI.controller.screen.menu3_options):
                        GUI.controller.screen.menu3_line_index = len(GUI.controller.screen.menu3_options) - 1
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
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
                GUI.button_pressed = True
            elif not GUI.controller.button_Left.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 1
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        # Reset LPS35 Menu
        if GUI.current_menu == 4:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu4_screen()
            if not GUI.controller.button_Up.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu4_line_index -= 1
                    if GUI.controller.screen.menu4_line_index < 0:
                        GUI.controller.screen.menu4_line_index = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Down.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu4_line_index += 1
                    if GUI.controller.screen.menu4_line_index >= len(GUI.controller.screen.menu4_options):
                        GUI.controller.screen.menu4_line_index = len(GUI.controller.screen.menu4_options) - 1
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            if not GUI.controller.button_Left.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 1
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
                    if GUI.controller.screen.menu4_line_index == 0:
                        GUI.reset_LPS35HW(True)
                        GUI.current_menu = 1
                        GUI.controller.screen.clear_screen()
                    if GUI.controller.screen.menu4_line_index == 1:
                        GUI.reset_LPS35HW()
                        GUI.current_menu = 1
                        GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        # Shutdown Menu
        if GUI.current_menu == 5:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu5_screen()
            if not GUI.controller.button_Left.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 0
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False

if __name__ == "__main__":
    main()
