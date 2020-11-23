import numpy as np
import matplotlib,time,smbus,threading,board,keyboard

class user_interface:
    def __init__(self,line_ids=[],line_strings=[]):
        self.run = True
        self.current_line = 0
        self.lines = {}
        assert len(line_ids) == len(line_strings), "Number of ids (%r) does not equal number of strings (%r)" % (len(line_ids),len(line_strings))
        for index,line_id in enumerate(line_ids):
            self.lines[line_id] = user_interface_line(id=line_id,
                                                      string=line_strings[index])


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
