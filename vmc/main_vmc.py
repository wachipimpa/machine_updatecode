import sys

sys.path.append('/home/pi/hottub_ma/vmc/')
from mod_vmc import Mod_vmc

mod_vmc = Mod_vmc()
class Main_vmc:
    def vmc_main_start(self, status):
        with open('/home/pi/txt_file/vmc_set_speed.txt','r') as read_speed:
                data_speed = read_speed.readline().strip()
        if str(status) == '1':
            print("start filtration vmc")
            split_data = data_speed.split(',')
            filtration_speed = split_data[0]
            mod_vmc.compute_speed(int(filtration_speed))
        elif str(status) == '2':
            print("start ozone choc vmc")
            split_data = data_speed.split(',')
            filtration_speed = split_data[1]
            mod_vmc.compute_speed(int(filtration_speed))
        elif str(status) == '3':
            print("start backwash vmc")
            split_data = data_speed.split(',')
            filtration_speed = split_data[2]
            mod_vmc.compute_speed(int(filtration_speed))

            


