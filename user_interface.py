import numpy as np
import matplotlib,time,board
from controller import controller

class user_interface:
    def __init__(self,line_ids=[],line_strings=[]):
        self.run = True
        self.current_line = 0
        self.current_menu = 0
        self.previous_menu = 0
        self.lines = {}
        assert len(line_ids) == len(line_strings), "Number of ids (%r) does not equal number of strings (%r)" % (len(line_ids),len(line_strings))
        for index,line_id in enumerate(line_ids):
            self.lines[line_id] = user_interface_line(id=line_id,
                                                      string=line_strings[index])
        self.controller = controller()
        self.controller.screen.clear_screen()
        self.units = 0  # 0:mmHg, 1:psi, 2:kPa
        self.button_pressed = False

    def draw_menu_screen(self):
        # Clear screen
        # Draw black box for screen
        # Draw white box on line number (self.selected_option)
        # Draw text lines
        pass

class user_interface_line:
    def __init__(self,id='default_id',string='default_string'):
        self.id = id
        self.string = string


def main():
    line_ids = ['line1','line2','line3']
    line_strings = ['line1_string','line2_string','line3_string']
    user_interface(line_ids,line_strings)



if __name__ == "__main__":
    main()
