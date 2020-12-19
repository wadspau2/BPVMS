# Modules
import numpy as np
import matplotlib,time,board
from colorsys import hsv_to_rgb
from PIL import Image,ImageDraw,ImageFont
from user_interface import user_interface,csv_writer

_RUN_ON_PI = False
_RATE = 10 # hz

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
                    if GUI.controller.screen.menu1_line_index == 4:
                        GUI.current_menu = 5
                    if GUI.controller.screen.menu1_line_index == 3:
                        GUI.current_menu = 8
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
            if not GUI.controller.button_Up.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu2_line_index -= 1
                    if GUI.controller.screen.menu2_line_index < 0:
                        GUI.controller.screen.menu2_line_index = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Down.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu2_line_index += 1
                    if GUI.controller.screen.menu2_line_index >= len(GUI.controller.screen.menu2_options):
                        GUI.controller.screen.menu2_line_index = len(GUI.controller.screen.menu2_options) - 1
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
                    if GUI.controller.screen.menu2_line_index == 0:
                        GUI.run_test = True
                        GUI.test_start_time = time.time()
                        GUI.test_end_time = GUI.test_start_time + GUI.test_lengths[0]
                        GUI.current_menu = 6
                        GUI.last_test_screen_draw = time.time()
                    elif GUI.controller.screen.menu2_line_index == 1:
                        GUI.run_test = True
                        GUI.test_start_time = time.time()
                        GUI.test_end_time = GUI.test_start_time + GUI.test_lengths[1]
                        GUI.current_menu = 6
                        GUI.last_test_screen_draw = time.time()
                    elif GUI.controller.screen.menu2_line_index == 2:
                        GUI.run_test = True
                        GUI.test_start_time = time.time()
                        GUI.test_end_time = GUI.test_start_time + GUI.test_lengths[2]
                        GUI.current_menu = 6
                        GUI.last_test_screen_draw = time.time()
                    elif GUI.controller.screen.menu2_line_index == 3:
                        GUI.run_test = True
                        GUI.test_start_time = time.time()
                        GUI.test_end_time = None
                        GUI.current_menu = 6
                        GUI.last_test_screen_draw = time.time()
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Left.value:
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
                GUI.controller.screen.menu4_line_index = 0
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
                GUI.shutdown_start_time = time.time()
                GUI.shutdown_end_time = GUI.shutdown_start_time + 3.0
            GUI.controller.screen.draw_menu5_screen()
            if not GUI.controller.button_Left.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 0
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        # Running Test Menu
        if GUI.current_menu == 6:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
                GUI.csv_writer = csv_writer(GUI)
            if (time.time()-GUI.last_test_screen_draw) > (1/GUI.test_rate):
                GUI.last_test_screen_draw = time.time()
                GUI.controller.screen.draw_menu6_screen()
                if GUI.run_test:
                    pressure,temperature,unit = GUI.get_LPS35HW_measurement()
                    GUI.csv_writer.write_line(time.time(),
                                              pressure,
                                              unit)
                if GUI.test_end_time is not None:
                    if time.time() >= GUI.test_end_time:
                        GUI.run_test = False
                        results = GUI.csv_writer.analyze_data()
                        GUI.current_menu = 7
                        GUI.controller.screen.clear_screen()
            if not GUI.controller.button_Up.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu6_line_index -= 1
                    if GUI.controller.screen.menu6_line_index < 0:
                        GUI.controller.screen.menu6_line_index = 0
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Down.value:
                if not GUI.button_pressed:
                    GUI.controller.screen.menu6_line_index += 1
                    if GUI.controller.screen.menu6_line_index >= len(GUI.controller.screen.menu6_options):
                        GUI.controller.screen.menu6_line_index = len(GUI.controller.screen.menu6_options) - 1
                    # GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            elif not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
                    GUI.run_test = False
                    GUI.csv_writer.analyze_data()
                    GUI.current_menu = 2
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        if GUI.current_menu == 7:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
            GUI.controller.screen.draw_menu7_screen(results)
            if not GUI.controller.button_Select.value:
                if not GUI.button_pressed:
                    GUI.current_menu = 1
                    GUI.controller.screen.clear_screen()
                GUI.button_pressed = True
            else:
                GUI.button_pressed = False
        if GUI.current_menu == 8:
            if GUI.previous_menu != GUI.current_menu:
                GUI.previous_menu = GUI.current_menu
                lock = GUI.controller.screen.draw_menu8_screen(True)
            else:
                lock = GUI.controller.screen.draw_menu8_screen()
            if not lock:
                if not GUI.controller.button_Select.value:
                    if not GUI.button_pressed:
                        GUI.current_menu = 0
                        GUI.controller.screen.clear_screen()
                    GUI.button_pressed = True
                else:
                    GUI.button_pressed = False

if __name__ == "__main__":
    main()
