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
url_heatpump = path_url.url_heatpump
mod_heatpump = Modbus_heatpump()
modbus_relay  = Modbus_relay()
plc_mod = Modbus()


class Main_HeatPump:

    def start_heatpump(self,  temperature, plc, relay_8,status_heatpump,response_api,plc_all_out):
        print('Heat pump working')
        if response_api['setting_mode'][0]['sm_filtration']  != "0":
            with open('/home/pi/txt_file/status_besgo.txt','r') as read_status_besgo:
                status_besgo = read_status_besgo.readline().strip()
            if status_besgo == "False":
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%H", named_tuple)
                
                data_heatpump = response_api['heatpump']
                hour_start = data_heatpump[0]['heatpump_start']
                hour_end = data_heatpump[0]['heatpump_end']
                split_hour_start = hour_start.split(':')
                split_hour_end = hour_end.split(':')
                if int(time_string) >= int(split_hour_start[0])  and int(time_string) < int(split_hour_end[0]) :
                    if plc[2] == True:
                        mod_heatpump.stop_chauffage()
                        time.sleep(0.5)
                        mod_heatpump.stop_chauffage2()
                        time.sleep(0.5)
                        self.clear_heater_open_count()

                    data_setting = response_api['data_setting']


                    data_mode = response_api['setting_mode']
                    if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                        if str(data_mode[0]['sm_filtration']) != "0":
                            if str(data_mode[0]['sm_chauffage']) == "1":
                                if plc[0] == False:
                                    plc_mod.start_filtration()
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("True")
                            if status_heatpump == False:
                                mod_heatpump.start_y14()
                    elif float(data_setting[0]['setting_temperature']) <= float(temperature):
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                        if status_heatpump == True:
                            mod_heatpump.stop_y14()


                else:
                    if status_heatpump == True:
                            mod_heatpump.stop_y14()
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

                                # minus = float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff'])
                                if  float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >=  float(temperature):
                                    print("open pump")
                                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                        read_status_auto.write("True")
                                
                                    if plc[2] == False:
                                        mod_heatpump.start_chauffage()
                                    if plc[2] == True:
                                        mod_heatpump.start_chauffage2()
                                elif float(temperature) >= float(data_setting[0]['setting_temperature']): 
                                    print("close pump")
                                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                        read_status_auto.write("False")
                                    if plc[2] == True:
                                        mod_heatpump.stop_chauffage()
                                        time.sleep(0.5)
                                        mod_heatpump.stop_chauffage2()
                                        time.sleep(0.5)
                                        self.clear_heater_open_count()
                                
                            elif str(data_mode[0]['sm_chauffage']) == "1" and plc[0] == False:
                                set_temp = float(data_setting[0]['setting_temperature'])
                                temp_div = float(data_setting[0]['setting_temp_deff'])
                                read = float(temperature)
                                print(set_temp)
                                print(temp_div)
                                print(read)
                                if float(data_setting[0]['setting_temperature']) - float(data_setting[0]['setting_temp_deff']) >  float(temperature):
                                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                        read_status_auto.write("True")
                                    if plc[0] == False:
                                        plc_mod.start_filtration()
                                # else :
                                elif float(temperature) >= float(data_setting[0]['setting_temperature']):
                                    print("close pump")
                                    with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                        read_status_auto.write("False")
                                    if plc[2] == True:
                                        mod_heatpump.stop_chauffage()
                                        time.sleep(0.5)
                                        mod_heatpump.stop_chauffage2()
                                        time.sleep(0.5)
                                        self.clear_heater_open_count()
                                    # if plc[2] == False:
                                    #     if plc[3] == True:
                                    #         mod_heatpump.stop_chauffage2()
                            else:
                                with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                    read_status_auto.write("False")
                                if plc[2] == True:
                                    mod_heatpump.stop_chauffage()
                                    time.sleep(0.5)
                                    mod_heatpump.stop_chauffage2()
                                    time.sleep(0.5)
                                    self.clear_heater_open_count()
                                # if plc[2] == False:
                                #     if plc[3] == True:
                                #         mod_heatpump.stop_chauffage2()
                        else:
                            with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                                read_status_auto.write("False")
                            if plc[2] == True:
                                mod_heatpump.stop_chauffage()
                                time.sleep(0.5)
                                mod_heatpump.stop_chauffage2()
                                time.sleep(0.5)
                                self.clear_heater_open_count()
                            # if plc[2] == False:
                            #     if plc[3] == True:
                            #         mod_heatpump.stop_chauffage2()

                    else:
                        with open('/home/pi/txt_file/status_working_heater.txt','w') as read_status_auto:
                            read_status_auto.write("False")
                        if plc[2] == True:
                            mod_heatpump.stop_chauffage()
                            time.sleep(0.5)
                            mod_heatpump.stop_chauffage2()
                            time.sleep(0.5)
                            self.clear_heater_open_count()
                        # if plc[2] == False:
                        #     if plc[3] == True:
                        #         mod_heatpump.stop_chauffage2()
                            
                        if plc[2] == False:
                            if plc[1] == True:
                                mod_heatpump.stop_pump_ozone()
            else:
                if plc_all_out[14] == True:
                    mod_heatpump.stop_y14()
        else:
            if plc_all_out[14] == True:
                mod_heatpump.stop_y14()

            
    def clear_heater_open_count(self):
        with open('/home/pi/txt_file/counter_open_heater.txt','w') as write_counter_open:
            write_counter_open.write("0")

        
