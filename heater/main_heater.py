import sys
import time
from modbus_heater import Modbus_heatpump
sys.path.append('/home/pi/hottub_ma/relay/')
from modbus_relay import Modbus_relay
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_ma/plc/')
from modbus import Modbus


path_url = Path_url()
url_setting = path_url.url_setting
url = path_url.url_setting_mode
mod_heatpump = Modbus_heatpump()
modbus_relay  = Modbus_relay()
plc_mod = Modbus()


class Main_Heater:

    def start_heater(self,  temperature, plc, relay_8,response_api):
        if relay_8[4] == False:
            data_setting = response_api['data_setting']
            data_mode = response_api['setting_mode']

            if str(data_mode[0]['sm_filtration']) != "0":
                if str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == True:
                    set_temp = float(data_setting[0]['setting_temperature'])
                    temp_div = float(data_setting[0]['setting_temp_deff'])
                    read = float(temperature)
                    print(set_temp)
                    print(temp_div)
                    print(read)

                    if  float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                        print('step heater 1')
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("True")
                   
                        if plc[2] == False:
                            mod_heatpump.write_modbus(2,1)
                        if plc[3] == False:
                            mod_heatpump.write_modbus(3,1)
       
                    elif float(temperature) >= float(data_setting[0]['setting_temperature']): 
                        print('step heater 2')
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                        if plc[2] == True:
                            mod_heatpump.write_modbus(2,0)
                        if plc[3] == True:
                            mod_heatpump.write_modbus(3,0)
                        self.clear_heater_open_count()
              
                elif str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == False:
                    print('step heater 3')
                    set_temp = float(data_setting[0]['setting_temperature'])
                    temp_div = float(data_setting[0]['setting_temp_deff'])
                    read = float(temperature)
                    print(set_temp)
                    print(temp_div)
                    print(read)
                    if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                        print('step heater 4')
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("True")
                        if plc[0] == False:
                            plc_mod.start_filtration()
                    else :
                        print('step heater 5')
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                        if plc[2] == True:
                            mod_heatpump.write_modbus(2,0)
                        if plc[3] == True:
                            mod_heatpump.write_modbus(3,0)
                        self.clear_heater_open_count()
    
                else:
                    print('step heater 6')
                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                        read_status_auto.write("False")
                    if plc[2] == True:
                        mod_heatpump.write_modbus(2,0)
                    if plc[3] == True:
                        mod_heatpump.write_modbus(3,0)
          
                    self.clear_heater_open_count()
           
            else:
                print('step heater 7')
                with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                    read_status_auto.write("False")
                if plc[2] == True:
                    mod_heatpump.write_modbus(2,0)
                if plc[3] == True:
                    mod_heatpump.write_modbus(3,0)
   
                self.clear_heater_open_count()
      

        else:
            print('step heater 8')
            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                read_status_auto.write("False")
            if plc[2] == True:
                mod_heatpump.write_modbus(2,0)
            if plc[3] == True:
                mod_heatpump.write_modbus(3,0)
   
            self.clear_heater_open_count()
    

            if plc[2] == False:
                if plc[1] == True:
                    mod_heatpump.stop_pump_ozone()
    def clear_heater_open_count(self):
        with open('/home/pi/txt_file/counter_open_heater.txt','w') as write_counter_open:
            write_counter_open.write("0")

        
