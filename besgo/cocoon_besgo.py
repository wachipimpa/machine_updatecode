import sys
from setting.path_url import Path_url
import datetime
from modbus_besgo import Modbus_besgo
sys.path.append('/home/pi/hottub_ma/plc/')
from modbus import Modbus

path_url = Path_url()
url_besgo = path_url.url_besgo
url_besgo_setting= path_url.url_besgo_setting
mod_besgo = Modbus_besgo()
mod_plc = Modbus()


class Cocoon_besgo:
    status_working_besgo = False
    counter_besgo_working = 0
    current_time = ''
    set_relay8 = ''
    set_plc_out = ''
    status_working = ""
    set_time_working = ''


    def start_besgo(self, current_time, set_relay8, set_plc_out, setting_mode, setting_selection, response_api, plc_all_in):
        if response_api['setting_mode'][0]['sm_filtration']  != "0":
            if int(setting_selection[0]['backwash']) == 1:
                system_time = datetime.datetime.now()
                day = system_time.strftime("%a")
                
                besgo_json = response_api['get_besgo']
            
                besgo_setting_json = response_api['besgo_setting']
                #read array 8 chanel
                relay8 = set_relay8
                plc_read = set_plc_out
                print("--------Besgo-------"+str(besgo_setting_json[0]['backwash_mode']))
                if str(besgo_setting_json[0]['backwash_mode']) == "1":
                    with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                        write_status_besgo.write("True")
                    with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                        write_loading_in_tank.write("True")

                    with open("/home/pi/txt_file/counter_start_before_backwash.txt","r") as read_counter_before_backwash:
                        number_counter_before_backwash = read_counter_before_backwash.readline().strip()
                    print("xxxxxxxxxxxxx backwash read : "+str(number_counter_before_backwash))

                    if int(number_counter_before_backwash) <= (int(besgo_setting_json[0]['backwash_countdown']) * 60):
                        if plc_read[0] == True:
                            mod_plc.stop_filtration()
                        if plc_read[0] == False:
                            mod_besgo.close_all_working(relay8,set_plc_out)

                    else:
                        #เปิดการทำงาน อ่านค่า Sensor ปกติ
                        with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                            write_loading_in_tank.write("False")
                        #ตั้งสถานะให้อ่าน counter backwash กำลังทำงานจาก Thread 
                        if plc_all_in[6] == True: 
                            if plc_all_in[7] == True:
                                if plc_read[0] == False:
                                    mod_plc.start_filtration()
                                if relay8[4] == False and plc_read[0] == True:
                                    mod_besgo.open_besgo()
                                    
                              
                        else:
                            if relay8[4] == True:
                                mod_besgo.close_besgo()

                    
                elif str(besgo_setting_json[0]['backwash_mode']) == "2":
                    print("backwash AUTO")
                    with open('/home/pi/txt_file/status_besgo.txt','r') as read_status_besgo:
                        status_backwash = read_status_besgo.readline().strip()
                    split_curlen_time = current_time.split(":")
                    time_machine = split_curlen_time[0]+':'+split_curlen_time[1]
                    if status_backwash == "False":
                        for i in range(len(besgo_json)):
                            time_split = besgo_json[i].split('-')  
                            split_time_api = time_split[0].split(":")
                            time_setting = split_time_api[0]+':'+split_time_api[1]              
                            if time_setting == time_machine : 
                                with open('/home/pi/txt_file/status_besgo.txt','w')  as write_status_besgo:
                                    write_status_besgo.write("True")
                        
                                #ปิดการทำงาน อ่านค่า Sensor 
                                with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                                    write_loading_in_tank.write("True")
                                        
                                
                    else:
                        with open("/home/pi/txt_file/counter_start_before_backwash.txt","r") as read_counter_before_backwash:
                            number_counter_before_backwash = read_counter_before_backwash.readline().strip()
                        print("xxxxxxxxxxxxx backwash read : "+str(number_counter_before_backwash))
                        if int(number_counter_before_backwash) <= (int(besgo_setting_json[0]['backwash_countdown']) * 60):
                            if plc_read[0] == True:
                                mod_plc.stop_filtration()
                            if plc_read[0] == False:
                                mod_besgo.close_all_working(relay8,set_plc_out)
                        else:
                            #เปิดการทำงาน อ่านค่า Sensor ปกติ
                            with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                                write_loading_in_tank.write("False")
                                
                            with open('/home/pi/txt_file/status_besgo_start_counter.txt','w') as status_besgo_start_counter:
                                status_besgo_start_counter.write("True")
                            with open('/home/pi/txt_file/counter_backwash_working.txt','r')  as read_counter_backwash:
                                number_counter_backwash = read_counter_backwash.readline().strip()
                            if int(number_counter_backwash) <= int(besgo_setting_json[0]['backwash_time']):
                            #ตั้งสถานะให้อ่าน counter backwash กำลังทำงานจาก Thread 
                                if plc_all_in[6] == True: 
                                    if plc_all_in[7] == True:
                                        if plc_read[0] == False:
                                                mod_plc.start_filtration()
                                        if relay8[4] == False and plc_read[0] == True:
                                            mod_besgo.open_besgo()
            
                                else:
                                    if relay8[4] == True:
                                        mod_besgo.close_besgo()
                            else:
                                if relay8[4] == True:
                                    mod_besgo.close_besgo()
                                with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                                    write_status_besgo.write("False")
                                
                                with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter_in_tank:
                                    write_counter_in_tank.write(str(0))
                                    
                                with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                                    write_counter.write(str(0))
                                
                                with open('/home/pi/txt_file/status_besgo_start_counter.txt','w')  as status_open_backwash:
                                        status_open_backwash.write("False")
                                        
                                with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                                        write_loading_in_tank.write("False")
                
                                        
                else:
                    if relay8[4] == True:
                        mod_besgo.close_besgo()
                    if int(setting_mode[0]['sm_filtration']) == 0:
                        if relay8[4] == False:
                            mod_plc.stop_filtration()
                    with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                        write_status_besgo.write("False")
                    
                    with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter_in_tank:
                        write_counter_in_tank.write(str(0))
                        
                    with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                        write_counter.write(str(0))
                    
                    with open('/home/pi/txt_file/status_besgo_start_counter.txt','w')  as status_open_backwash:
                        status_open_backwash.write("False")
                            
                    with open('/home/pi/txt_file/stop_loading_in_tank.txt','w')  as write_loading_in_tank:
                        write_loading_in_tank.write("False")
    

       