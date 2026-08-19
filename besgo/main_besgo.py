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


class Main_Besgo:
    status_working_besgo = False
    counter_besgo_working = 0
    current_time = ''
    set_relay8 = ''
    set_plc_out = ''
    status_working = ""
    set_time_working = ''


    def start_besgo(self, current_time, set_relay8, set_plc_out, setting_mode, setting_selection, response_api):
        try:
            if response_api['setting_mode'][0]['sm_filtration']  != "0":
                if int(setting_selection[0]['backwash']) == 1:
                    system_time = datetime.datetime.now()
                    day = system_time.strftime("%a")
                    
                    besgo_json = response_api['get_besgo']
                    print(besgo_json)
                
                    besgo_setting_json = response_api['besgo_setting']
                    #read array 8 chanel
                    relay8 = set_relay8
                    plc_read = set_plc_out
                    print("--------Besgo-------"+str(besgo_setting_json[0]['backwash_mode']))
                    if str(besgo_setting_json[0]['backwash_mode']) == "1":
                        with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                            write_status_besgo.write("True")
                        if plc_read[0] == False:
                            mod_plc.start_filtration()
                        if relay8[4] == False and plc_read[0] == True:
                            mod_besgo.open_besgo()
                            
                        if relay8[4] == True:
                            mod_besgo.close_all_working(relay8, plc_read)
                        
                    elif str(besgo_setting_json[0]['backwash_mode']) == "2":
                        print("backwash AUTO")
                        if relay8[4] == True:
                            print("WORKING XXXXXXXXXXXXXXXXXXXXXXXXX WORKING")
                            mod_besgo.close_all_working(relay8, plc_read)
                        for item in besgo_json:
                            print("backwash step 1")
                            time_set = item.split('-')
                            print("backwash step : "+str(current_time)+' - '+time_set[0]+' - '+ time_set[0])
                            timeset_start = datetime.datetime.strptime(time_set[0], '%H:%M:%S').time()
                            timeset_end =  datetime.datetime.strptime(time_set[1], '%H:%M:%S').time()
                            time_machine =  datetime.datetime.strptime(current_time, '%H:%M:%S').time()
                            print(timeset_start)
                            print(timeset_end)
                            if time_machine >= timeset_start and time_machine <= timeset_end:
                                print("backwash step 2")
                                if plc_read[0] == False:
                                    print("backwash step start filtration")
                                    mod_plc.start_filtration()
                                else:
                                    print("backwash step 3")
                                    if relay8[4] == False and plc_read[0] == True:
                                        print("backwash step 4")
                                        if self.status_working != "complete" or self.set_time_working != current_time:
                                            print("backwash step 5")
                                            print("open bessgo working")
                                            mod_besgo.open_besgo()
                                            self.counter_besgo_working = self.counter_besgo_working + 1
                                            self.set_time_working = current_time
                                            with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                                                write_status_besgo.write("True")
                                                write_status_besgo.close()
                                            self.status_working = "working"
                                
                            elif current_time >= time_set[1]:
                                print("backwash step 6")
                                if relay8[4] == True:
                                    print('-------- close besgo 1 ------')
                                    mod_besgo.close_besgo()
                                with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                                    write_status_besgo.write("False")
                                    print('-------- close besgo 2 ------')
                                self.counter_besgo_working = 0
                                self.status_working = ""
                                self.set_time_working  = ""
                                print('-------- close besgo 3 ------')
                                            
                    else:
                        if relay8[4] == True:
                            mod_besgo.close_besgo()
                        if int(setting_mode[0]['sm_filtration']) == 0:
                            if relay8[4] == False:
                                mod_plc.stop_filtration()
                        with open('/home/pi/txt_file/status_besgo.txt','w') as write_status_besgo:
                            write_status_besgo.write("False")
        except:
            pass
        

        