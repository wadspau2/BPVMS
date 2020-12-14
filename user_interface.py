import numpy as np
import matplotlib.pyplot as plt
import time,board,csv,os,statistics
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
    def __init__(self,GUI):
        # USB_path = self.get_USB_path()
        self.USB_folder = '/mnt/DATA_USB/data'
        # data_folder = os.getcwd()+'/data'
        data_folder = self.USB_folder
        directory_contents = os.listdir(data_folder)
        max_folder_num = 0
        for folder in directory_contents:
            split_folder = folder.split("_")
            for index,split in enumerate(split_folder):
                if split == 'Test':
                    max_folder_num = max(max_folder_num,int(split_folder[index+1])+1)
        self.test_str = 'Test_'+str(max_folder_num)
        self.test_folder = os.path.join(data_folder,self.test_str)
        print('Test Folder:',self.test_folder)
        os.mkdir(self.test_folder,mode=0o777)
        GUI.test_str = self.test_str
        self.file_path = os.path.join(self.test_folder,'data.csv')
        self.write_file = open(self.file_path,mode='w+')
        self.writer = csv.writer(self.write_file,delimiter=',')
        self.writer.writerow(['time','pressure','units'])


            # os.mkdir(os.path.join(data_folder,timestr))
        # self.writer = csv.writer(csvfile)

    def get_USB_path(self):
        basedir = '/dev/disk/by-path/'
        for d in os.listdir(basedir):
            if 'usb' in d and 'part' not in d:
                path = os.path.join(basedir,d)
                link = os.readlink(path)
                print('/dev/'+os.path.basename(link))
                USB_path = '/dev/'+os.path.basename(link)
                mount_str = "sudo mount " + USB_path + " /USB_MOUNT"
                os.system(mount_str)
        return True

    def analyze_data(self):
        self.write_file.close()
        with open(self.file_path) as csvfile:
            reader = csv.DictReader(csvfile)
            time_list,pressure,units,vacuum = [],[],[],[]
            for row in reader:
                time_list.append(float(row['time']))
                pressure.append(float(row['pressure']))
                vacuum.append(float(row['pressure'])*-1.0)
                units.append(row['units'])
        time_normalized = []
        for t in time_list:
            time_normalized.append(abs(t-time_list[0]))
        fig_vacuum = plt.figure()
        plt.plot(time_normalized,vacuum,color='black')
        plt.xlabel('Time (s)')
        plt.ylabel('Vacuum ('+units[0]+')')
        # fig_vacuum.savefig(os.path.join(self.test_folder,self.test_str + '_Pressure.svg'),bbox_inches="tight")
        # fig_vacuum.savefig(os.path.join(self.test_folder,self.test_str + '_Pressure.pdf'),bbox_inches="tight")
        # fig_vacuum.savefig(os.path.join(self.test_folder,self.test_str + '_Pressure.png'),bbox_inches="tight",dpi=300)
        fig_vacuum.savefig(os.path.join(self.USB_folder,self.test_str + '_Pressure.svg'),bbox_inches="tight")
        fig_vacuum.savefig(os.path.join(self.USB_folder,self.test_str + '_Pressure.pdf'),bbox_inches="tight")
        fig_vacuum.savefig(os.path.join(self.USB_folder,self.test_str + '_Pressure.png'),bbox_inches="tight",dpi=300)
        max_pressure = max(pressure)
        avg_pressure = statistics.mean(pressure)
        max_vacuum = max(vacuum)
        avg_vacuum = statistics.mean(vacuum)
        print('Max Pressure:',max_pressure)
        print('Average Pressure:',avg_pressure)
        print('Max Vacuum:',max_vacuum)
        print('Average Vacuum:',avg_vacuum)
        txt_file = open(os.path.join(self.USB_folder,self.test_str + '_Results.txt'),'w')
        txt_file.write(self.test_str + ' Results\n\n')
        txt_file.write('Time: {} s\n'.format(int(time_list[-1]-time_list[0])))
        txt_file.write('Max Pressure: {:.3f} {}\n'.format(max_pressure,units[0]))
        txt_file.write('Average Pressure: {:.3f} {}\n'.format(avg_pressure,units[0]))
        txt_file.write('Max Vacuum: {:.3f} {}\n'.format(max_vacuum,units[0]))
        txt_file.write('Average Vacuum: {:.3f} {}\n'.format(avg_vacuum,units[0]))
        txt_file.close()
        results = [max_pressure,avg_pressure,max_vacuum,avg_vacuum,units[0]]
        return results


    def write_line(self,time,pressure,units):
        self.writer.writerow([time,pressure,units])
