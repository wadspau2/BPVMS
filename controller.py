import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

class controller:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.baudrate = 24000000
        self.spi = board.SPI()
        self.display = st7789.ST7789(self.spi,
                                     height=240,
                                     y_offset=80,
                                     rotation=180,
                                     cs=self.cs_pin,
                                     dc=self.dc_pin,
                                     rst=self.reset_pin,
                                     baudrate=self.baudrate)
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT
        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT
        self.button_Left = DigitalInOut(board.D27)
        self.button_Left.direction = Direction.INPUT
        self.button_Right = DigitalInOut(board.D23)
        self.button_Right.direction = Direction.INPUT
        self.button_Up = DigitalInOut(board.D17)
        self.button_Up.direction = Direction.INPUT
        self.button_Down = DigitalInOut(board.D22)
        self.button_Down.direction = Direction.INPUT
        self.button_Select = DigitalInOut(board.D4)
        self.button_Select.direction = Direction.INPUT
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True
        self.screen = screen(self)

class screen:
    def __init__(self,controller):
        self.controller = controller
        self.width = self.controller.display.width
        self.height = self.controller.display.height
        self.title_location = (5,10)
        self.title_line_location = [(0,45),(self.width,45)]
        self.title_line_width = 4
        self.line_list = [60,90,120,150,180,210,240]
        self.line_start = 5
        self.fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        self.color_black = "#000000"
        self.color_white = "#FFFFFF"
        self.image = Image.new("RGB",(self.width,self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.menu1_line_index = 0
        self.menu2_line_index = 0
        self.menu3_line_index = 0
        self.menu1_options = ['Run Test','Change Units','Reset LPS33','Shutdown']
        self.menu3_options = ['mmHg','PSI','kPa']
        self.clear_screen()

    def clear_screen(self):
        self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=(0,0,0))
        self.controller.display.image(self.image)

    def draw_menu0_screen(self):
        menu0_draw = ImageDraw.Draw(self.image)
        menu0_draw.text(self.title_location,'BPVMS',font=self.fnt,fill=self.color_white)
        menu0_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        if not self.controller.USB_found:
            menu0_draw.text((self.line_start,self.line_list[0]),'Error:',font=self.fnt,fill=self.color_white)
            menu0_draw.text((self.line_start,self.line_list[1]),'  No USB detected',font=self.fnt,fill=self.color_white)
        self.controller.display.image(self.image)

    def draw_menu1_screen(self):
        menu1_draw = ImageDraw.Draw(self.image)
        menu1_draw.text(self.title_location,'MAIN MENU',font=self.fnt,fill=self.color_white)
        menu1_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        menu1_draw.polygon([(0,self.line_list[self.menu1_line_index]),
                            (self.width,self.line_list[self.menu1_line_index]),
                            (self.width,self.line_list[self.menu1_line_index+1]),
                            (0,self.line_list[self.menu1_line_index+1])],
                            fill=self.color_white)
        menu1_draw.text((self.line_start,self.line_list[0]),self.menu1_options[0],font=self.fnt,fill=self.color_white if self.menu1_line_index != 0 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[1]),self.menu1_options[1],font=self.fnt,fill=self.color_white if self.menu1_line_index != 1 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[2]),self.menu1_options[2],font=self.fnt,fill=self.color_white if self.menu1_line_index != 2 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[3]),self.menu1_options[3],font=self.fnt,fill=self.color_white if self.menu1_line_index != 3 else self.color_black)
        self.controller.display.image(self.image)

    # RUN TEST
    def draw_menu2_screen(self):
        menu2_draw = ImageDraw.Draw(self.image)
        menu2_draw.text(self.title_location,'RUN TEST',font=self.fnt,fill=self.color_white)
        menu2_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        self.controller.display.image(self.image)

    # CHANGE UNITS
    def draw_menu3_screen(self):
        menu3_draw = ImageDraw.Draw(self.image)
        menu3_draw.text(self.title_location,'CHANGE UNITS',font=self.fnt,fill=self.color_white)
        menu3_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        menu3_draw.polygon([(0,self.line_list[self.menu3_line_index]),
                            (self.width,self.line_list[self.menu3_line_index]),
                            (self.width,self.line_list[self.menu3_line_index+1]),
                            (0,self.line_list[self.menu3_line_index+1])],
                            fill=self.color_white)
        menu3_draw.text((self.line_start,self.line_list[0]),self.menu3_options[0],font=self.fnt,fill=self.color_white if self.menu3_line_index != 0 else self.color_black)
        menu3_draw.text((self.line_start,self.line_list[1]),self.menu3_options[1],font=self.fnt,fill=self.color_white if self.menu3_line_index != 1 else self.color_black)
        menu3_draw.text((self.line_start,self.line_list[2]),self.menu3_options[2],font=self.fnt,fill=self.color_white if self.menu3_line_index != 2 else self.color_black)
        self.controller.display.image(self.image)

    # RESET LPS33
    def draw_menu4_screen(self):
        menu4_draw = ImageDraw.Draw(self.image)
        menu4_draw.text(self.title_location,'RESET LPS33',font=self.fnt,fill=self.color_white)
        menu4_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        self.controller.display.image(self.image)

    # SHUTDOWN
    def draw_menu5_screen(self):
        menu5_draw = ImageDraw.Draw(self.image)
        menu5_draw.text(self.title_location,'SHUT DOWN',font=self.fnt,fill=self.color_white)
        menu5_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        self.controller.display.image(self.image)
