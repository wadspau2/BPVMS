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
        self.title_location = (20,10)
        self.line1_location = (20,60)
        self.line2_location = (20,90)
        self.fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        self.color_black = "#000000"
        self.color_white = "#FFFFFF"
        self.image = Image.new("RGB",(self.width,self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.clear_screen()

    def clear_screen(self):
        self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=(0,0,0))
        self.controller.display.image(self.image)

    def draw_menu0_screen(self):
        menu0_draw = ImageDraw.Draw(self.image)
        menu0_draw.text(self.title_location,'TEST_TITLE',font=self.fnt,fill=self.color_white)
        self.controller.display.image(self.image)

    def draw_menu1_screen(self):
        menu1_draw = ImageDraw.Draw(self.image)
        menu1_draw.text(self.line1_location,'TEST LINE1',font=self.fnt,fill=self.color_white)
        menu1_draw.polygon([(20,90),(220,90),(220,120),(20,120)],fill=self.color_white)
        menu1_draw.text(self.line2_location,'TEST LINE2',font=self.fnt,fill=self.color_black)
        self.controller.display.image(self.image)
