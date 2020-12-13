import time
import random
from colorsys import hsv_to_rgb
import board,os,time
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

class controller:
    def __init__(self,user_interface):
        self.user_interface = user_interface
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
        self.USB_last_time = time.time()
        self.USB_refresh_time = 5.0
        self.USB_previous = False
        self.USB_found = False
        self.screen = screen(self,self.user_interface)

    def get_USB_status(self):
        basedir = '/dev/disk/by-path/'
        temp_found = False
        for d in os.listdir(basedir):
            if 'usb' in d and 'part' not in d:
                path = os.path.join(basedir,d)
                link = os.readlink(path)
                print('/dev/',os.path.basename(link))
                temp_found = True
                self.mount_USB(self,os.path.basename(link))
        self.USB_found = temp_found
        self.USB_last_time = time.time()
        return temp_found

    def mount_USB(self,USB_name,mount_location='/mnt/DATA_USB'):
        if not os.path.ismount(mount_location):
            mount_str = '/dev/' + str(USB_name)
            cmd_str = 'mount ' + mount_str + ' ' + mount_location
            print(cmd_str)
            os.system(cmd_str)

class screen:
    def __init__(self,controller,user_interface):
        self.controller = controller
        self.user_interface = user_interface
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
        self.menu4_line_index = 0
        self.menu6_line_index = 0
        self.menu0_lockout = True
        self.menu1_options = ['Run Test','Change Units','Reset LPS35','Shutdown']
        self.menu2_options = [str(self.user_interface.test_lengths[0])+'s',str(self.user_interface.test_lengths[1])+'s',str(self.user_interface.test_lengths[2])+'s','Manual']
        self.menu3_options = ['mmHg','PSI','kPa']
        self.menu4_options = ['Zero_LPS35','Abs_LPS35']
        self.menu6_options = ['Stop Test']
        self.clear_screen()

    def clear_screen(self):
        self.draw.rectangle((0,0,self.width,self.height),outline=0,fill=(0,0,0))
        self.controller.display.image(self.image)

    def draw_menu0_screen(self):
        menu0_draw = ImageDraw.Draw(self.image)
        menu0_draw.text(self.title_location,'BPVMS',font=self.fnt,fill=self.color_white)
        menu0_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        if (time.time()-self.controller.USB_last_time)>self.controller.USB_refresh_time:
            self.controller.get_USB_status()
        if not self.controller.USB_found:
            menu0_draw.text((self.line_start,self.line_list[0]),'Error:',font=self.fnt,fill=self.color_white)
            menu0_draw.text((self.line_start,self.line_list[1]),'  Insert USB',font=self.fnt,fill=self.color_white)
            if self.controller.USB_previous:
                self.controller.USB_previous = False
                self.clear_screen()
            self.menu0_lockout = True
        else:
            menu0_draw.text((self.line_start,self.line_list[0]),'USB Found',font=self.fnt,fill=self.color_white)
            menu0_draw.polygon([(0,self.line_list[2]),
                                (self.width,self.line_list[2]),
                                (self.width,self.line_list[3]),
                                (0,self.line_list[3])],
                                fill=self.color_white)
            menu0_draw.text((self.line_start,self.line_list[2]),'Continue',font=self.fnt,fill=self.color_black)
            if not self.controller.USB_previous:
                self.controller.USB_previous = True
                self.clear_screen()
            self.menu0_lockout = False
        self.controller.display.image(self.image)

    def draw_menu1_screen(self):
        menu1_draw = ImageDraw.Draw(self.image)
        menu1_draw.text(self.title_location,'MAIN MENU',font=self.fnt,fill=self.color_white)
        menu1_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        for i in range(0,5):
            menu1_draw.polygon([(0,self.line_list[i]),
                                (self.width,self.line_list[i]),
                                (self.width,self.line_list[i+1]),
                                (0,self.line_list[i+1])],
                                fill=self.color_black)
        menu1_draw.polygon([(0,self.line_list[self.menu1_line_index]),
                            (self.width,self.line_list[self.menu1_line_index]),
                            (self.width,self.line_list[self.menu1_line_index+1]),
                            (0,self.line_list[self.menu1_line_index+1])],
                            fill=self.color_white)
        menu1_draw.text((self.line_start,self.line_list[0]),self.menu1_options[0],font=self.fnt,fill=self.color_white if self.menu1_line_index != 0 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[1]),self.menu1_options[1],font=self.fnt,fill=self.color_white if self.menu1_line_index != 1 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[2]),self.menu1_options[2],font=self.fnt,fill=self.color_white if self.menu1_line_index != 2 else self.color_black)
        menu1_draw.text((self.line_start,self.line_list[3]),self.menu1_options[3],font=self.fnt,fill=self.color_white if self.menu1_line_index != 3 else self.color_black)
        menu1_draw.polygon([(0,self.line_list[5]),
                            (self.width,self.line_list[5]),
                            (self.width,self.line_list[6]),
                            (0,self.line_list[6])],
                            fill=self.color_black)
        if self.controller.user_interface.units == 0:
            pressure_str = "P: {:.1f} {}".format(self.controller.user_interface.hPa_to_mmHg(self.controller.user_interface.LPS35HW.pressure),"mmHg")
        elif self.controller.user_interface.units == 1:
            pressure_str = "P: {:.3f} {}".format(self.controller.user_interface.hPa_to_PSI(self.controller.user_interface.LPS35HW.pressure),"PSI")
        elif self.controller.user_interface.units == 2:
            pressure_str = "P: {:.2f} {}".format(self.controller.user_interface.hPa_to_kPa(self.controller.user_interface.LPS35HW.pressure),"kPa")
        else:
            pressure_str = "P: {:.3f} {}".format(self.controller.user_interface.LPS35HW.pressure,"hPa")

        menu1_draw.text((self.line_start,self.line_list[5]),pressure_str,font=self.fnt,fill=self.color_white)
        self.controller.display.image(self.image)

    # RUN TEST
    def draw_menu2_screen(self):
        menu2_draw = ImageDraw.Draw(self.image)
        menu2_draw.text(self.title_location,'RUN TEST',font=self.fnt,fill=self.color_white)
        menu2_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        for i in range(0,5):
            menu2_draw.polygon([(0,self.line_list[i]),
                                (self.width,self.line_list[i]),
                                (self.width,self.line_list[i+1]),
                                (0,self.line_list[i+1])],
                                fill=self.color_black)
        menu2_draw.polygon([(0,self.line_list[self.menu2_line_index+1]),
                            (self.width,self.line_list[self.menu2_line_index+1]),
                            (self.width,self.line_list[self.menu2_line_index+2]),
                            (0,self.line_list[self.menu2_line_index+2])],
                            fill=self.color_white)
        menu2_draw.text((self.line_start,self.line_list[0]),'Test Length:',font=self.fnt,fill=self.color_white)
        menu2_draw.text((self.line_start+10,self.line_list[1]),self.menu2_options[0],font=self.fnt,fill=self.color_white if self.menu2_line_index != 0 else self.color_black)
        menu2_draw.text((self.line_start+10,self.line_list[2]),self.menu2_options[1],font=self.fnt,fill=self.color_white if self.menu2_line_index != 1 else self.color_black)
        menu2_draw.text((self.line_start+10,self.line_list[3]),self.menu2_options[2],font=self.fnt,fill=self.color_white if self.menu2_line_index != 2 else self.color_black)
        menu2_draw.text((self.line_start+10,self.line_list[4]),self.menu2_options[3],font=self.fnt,fill=self.color_white if self.menu2_line_index != 3 else self.color_black)
        self.controller.display.image(self.image)

    # CHANGE UNITS
    def draw_menu3_screen(self):
        menu3_draw = ImageDraw.Draw(self.image)
        menu3_draw.text(self.title_location,'CHANGE UNITS',font=self.fnt,fill=self.color_white)
        menu3_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        for i in range(0,5):
            menu3_draw.polygon([(0,self.line_list[i]),
                                (self.width,self.line_list[i]),
                                (self.width,self.line_list[i+1]),
                                (0,self.line_list[i+1])],
                                fill=self.color_black)
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
        menu4_draw.text(self.title_location,'RESET LPS35',font=self.fnt,fill=self.color_white)
        menu4_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        for i in range(0,5):
            menu4_draw.polygon([(0,self.line_list[i]),
                                (self.width,self.line_list[i]),
                                (self.width,self.line_list[i+1]),
                                (0,self.line_list[i+1])],
                                fill=self.color_black)
        menu4_draw.polygon([(0,self.line_list[self.menu4_line_index]),
                            (self.width,self.line_list[self.menu4_line_index]),
                            (self.width,self.line_list[self.menu4_line_index+1]),
                            (0,self.line_list[self.menu4_line_index+1])],
                            fill=self.color_white)
        menu4_draw.text((self.line_start,self.line_list[0]),self.menu4_options[0],font=self.fnt,fill=self.color_white if self.menu4_line_index != 0 else self.color_black)
        menu4_draw.text((self.line_start,self.line_list[1]),self.menu4_options[1],font=self.fnt,fill=self.color_white if self.menu4_line_index != 1 else self.color_black)
        self.controller.display.image(self.image)

    # SHUTDOWN
    def draw_menu5_screen(self):
        menu5_draw = ImageDraw.Draw(self.image)
        menu5_draw.text(self.title_location,'SHUT DOWN',font=self.fnt,fill=self.color_white)
        menu5_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        self.controller.display.image(self.image)

    def draw_menu6_screen(self):
        menu6_draw = ImageDraw.Draw(self.image)
        menu6_draw.text(self.title_location,self.user_interface.test_str,font=self.fnt,fill=self.color_white)
        menu6_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        for i in range(0,5):
            menu6_draw.polygon([(0,self.line_list[i]),
                                (self.width,self.line_list[i]),
                                (self.width,self.line_list[i+1]),
                                (0,self.line_list[i+1])],
                                fill=self.color_black)
        menu6_draw.polygon([(0,self.line_list[self.menu6_line_index]),
                            (self.width,self.line_list[self.menu6_line_index]),
                            (self.width,self.line_list[self.menu6_line_index+1]),
                            (0,self.line_list[self.menu6_line_index+1])],
                            fill=self.color_white)
        menu6_draw.text((self.line_start,self.line_list[0]),self.menu6_options[0],font=self.fnt,fill=self.color_white if self.menu6_line_index != 0 else self.color_black)
        if self.user_interface.test_end_time is not None:
            menu6_draw.text((self.line_start,self.line_list[3]),'Time Left:',font=self.fnt,fill=self.color_white)
            menu6_draw.text((self.line_start,self.line_list[4]),"{:.1f}s".format(self.user_interface.test_end_time-time.time()),font=self.fnt,fill=self.color_white)
        self.controller.display.image(self.image)

    def draw_menu7_screen(self,results):
        menu7_draw = ImageDraw.Draw(self.image)
        menu7_draw.text(self.title_location,self.user_interface.test_str + " Results",font=self.fnt,fill=self.color_white)
        menu7_draw.line(self.title_line_location,fill=self.color_white,width=self.title_line_width)
        menu7_draw.text((self.line_start,self.line_list[0]),'Max Vacuum:',font=self.fnt,fill=self.color_white)
        menu7_draw.text((self.line_start+10,self.line_list[1]),'{:.3f} {}'.format(results[2],results[4]),font=self.fnt,fill=self.color_white)
        menu7_draw.text((self.line_start,self.line_list[2]),'Avg Vacuum:',font=self.fnt,fill=self.color_white)
        menu7_draw.text((self.line_start+10,self.line_list[3]),'{:.3f} {}'.format(results[3],results[4]),font=self.fnt,fill=self.color_white)
        menu7_draw.polygon([(0,self.line_list[4]),
                            (self.width,self.line_list[4]),
                            (self.width,self.line_list[5]),
                            (0,self.line_list[5])],
                            fill=self.color_white)
        menu7_draw.text((self.line_start,self.line_list[4]),'Continue',font=self.fnt,fill=self.color_black)
        self.controller.display.image(self.image)
