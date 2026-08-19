import time
import sys
import datetime
from restart import *
from write_file import Write_file
from modbus_read import Modbus_read
from urllib.request import urlopen
import json
from close_all import Close_All
import threading

sys.path.append('/home/pi/hottub_ma/besgo/')
from main_besgo import Main_Besgo
from cocoon_besgo import Cocoon_besgo
sys.path.append('/home/pi/hottub_ma/plc/')
from main_plc import Main_PLC
from modbus import Modbus
sys.path.append('/home/pi/hottub_ma/relay/')
from main_relay import Main_relay
from modbus_relay import Modbus_relay
sys.path.append('/home/pi/hottub_ma/ph/')
from main_ph import Main_PH
sys.path.append('/home/pi/hottub_ma/volttag/')
from main_volt_tag import Main_volt_tag
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
sys.path.append('/home/pi/hottub_ma/heater/')
from main_heater import Main_Heater
from main_heatpump import Main_HeatPump
from modbus_heater import Modbus_heatpump
sys.path.append('/home/pi/hottub_ma/vmc/')
from main_vmc import Main_vmc
sys.path.append('/home/pi/hottub_ma/orp/')
from main_orp import Main_orp
sys.path.append('/home/pi/hottub_ma/apf/')
from main_apf import Main_apf
sys.path.append('/home/pi/hottub_ma/chlorine/')
from main_chlorine import Main_chlorine




modbus_read = Modbus_read()
path_url = Path_url()
besgo = Main_Besgo()
close_all  = Close_All()
volt = Main_volt_tag()
heater  = Main_Heater()
main_pump = Main_HeatPump()
plc_mod = Modbus()
write_file = Write_file()
main_vmc = Main_vmc()
mod_relay = Modbus_relay()
cocoon_besgo = Cocoon_besgo()
modbus_heater= Modbus_heatpump()

counter_pressure = 0
url_setting = path_url.url_setting
url_setting_mode = path_url.url_setting_mode
url_selection = path_url.url_selection
url_night_time = path_url.url_night_time
url_all_api = path_url.url_all_api
type_machine = ""
plc_7_trict = ""


#เทรด นับเวลา หยุดปั้ม backwash
def counter_before_backwash():
    while True:
        try:
            with open('/home/pi/txt_file/status_besgo.txt','r') as read_status_backwash:
                status_backwash = read_status_backwash.readline().strip()
                print('before chcek status counter backwash : '+str(status_backwash))
            if status_backwash == "True":
                with open('/home/pi/txt_file/counter_start_before_backwash.txt','r')  as read_counter_backwash:
                    check_counter_first = read_counter_backwash.readline().strip()
                if check_counter_first != '':
                    number_counter_backwash = int(check_counter_first) + 1
                    with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter:
                        write_counter.write(str(number_counter_backwash))
                else:
                     with open('/home/pi/txt_file/counter_start_before_backwash.txt','w') as write_counter:
                        write_counter.write("0")
            time.sleep(1)
        except:
            pass
               
def counter_start_backwash_time():
    while True:
        try:
            with open('/home/pi/txt_file/status_besgo_start_counter.txt','r') as read_status_backwash:
                status_backwash = read_status_backwash.readline().strip()
            if status_backwash == "True":
                with open('/home/pi/txt_file/counter_backwash_working.txt','r')  as read_counter_backwash:
                    number_counter_backwash = int(read_counter_backwash.readline().strip()) + 1
                with open('/home/pi/txt_file/counter_backwash_working.txt','w') as write_counter:
                    write_counter.write(str(number_counter_backwash))   
            time.sleep(1)
        except:
            pass

def counter_start_heater():
    while True:
        try:
            with open('/home/pi/txt_file/status_working_heater.txt','r') as read_status_auto:
                status_working = read_status_auto.readline().strip()
            if status_working == "True":
                with open('/home/pi/txt_file/counter_open_heater.txt','r') as read_counter_open:
                    counter_open_heater = int(read_counter_open.readline().strip()) + 1
                if counter_open_heater <= 60:
                    with open('/home/pi/txt_file/counter_open_heater.txt','w') as write_counter_open:
                        write_counter_open.write(str(counter_open_heater))
            time.sleep(1)
        except:
            pass

        

before_backwash = threading.Thread(target=counter_before_backwash, args=())
before_backwash.start()
start_counter_backwash =  threading.Thread(target=counter_start_backwash_time, args=())
start_counter_backwash.start()
start_counter_heater =  threading.Thread(target=counter_start_heater, args=())
start_counter_heater.start()

try:
    while True:
        with open('/home/pi/machine_code/type_machine.txt','r') as read_machine_type:
                type_machine = read_machine_type.read().strip()
        print("type machine : "+str(type_machine))
        print("WORKING HOTTUB")
        system_time = datetime.datetime.now()
        current_time = system_time.strftime("%H:%M")
        current_time_sec = system_time.strftime("%H:%M:%S")
        current_hour =  system_time.strftime("%H")
        current_minute =  system_time.strftime("%M")
        sec_time =  system_time.strftime("%S")
        #all api one generate
        res_api = urlopen(url_all_api)
        response_api = json.loads(res_api.read())

        #counter pump ja start
        with open('/home/pi/txt_file/set_minute_ja.txt','r') as read_minute_counter_ja:
            minute_ja_reading = read_minute_counter_ja.readline().strip()
            if str(minute_ja_reading) != str(current_minute):
                with open('/home/pi/txt_file/set_minute_ja.txt','w') as write_minute_ja:
                    write_minute_ja.write(str(current_minute))
                with open('/home/pi/txt_file/counter_ja.txt','r') as read_counter_ja:
                    counter_ja = read_counter_ja.readline().strip()
                    sum_counter_ja = int(counter_ja) + 1
                with open('/home/pi/txt_file/counter_ja.txt','w') as write_counter_ja:
                    write_counter_ja.write(str(sum_counter_ja))
        #counter pump ja end

        setting_night_time = response_api['night_time']
        hour_start_night_time = setting_night_time[0]['night_time_start']
        hour_end_night_time = setting_night_time[0]['night_time_end']
        night_time_split_start = hour_start_night_time.split(':')
        night_time_split_end = hour_end_night_time.split(':')

        read_pressure =  modbus_read.read_pressure(response_api['data_setting'])


        relay_8 = modbus_read.read_status_relay()

        # #read plc
        plc = modbus_read.read_status_plc_out()
        
        plc_in = modbus_read.read_status_plc_in()  
        plc_all_in = modbus_read.read_all_plc_in()
        print(plc_all_in)
        plc_all_out = modbus_read.read_all_plc_out()   
        
        #vmc
        if response_api['machine_option'][0]['vmc'] == 1:
            write_file.write_speed_vmc(response_api['vmc_speed'])
            if relay_8[7] == True :
                main_vmc.vmc_main_start('3')
            else:
                if relay_8[2] == True:
                    main_vmc.vmc_main_start('2')
                else:
                    main_vmc.vmc_main_start('1')
         
        # #read temperature
        temperature = modbus_read.read_temperature(response_api['data_setting'])
        # read ph
        ph = 0
        if int(response_api['machine_option'][0]['ph']) == 1:
            ph = modbus_read.read_ph()
            # ph = 7.9
        print("PH"+str(ph))
        #read orp
        orp = 0
        if int(response_api['machine_option'][0]['orp']) == 1:
            orp = modbus_read.read_orp()
            # orp = 400
        print("ORP"+str(orp))
        #write file 
        heatpump = False
        if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
            heatpump = modbus_read.read_heatpump()

        write_file.start_write(relay_8, plc, temperature, ph, orp, read_pressure, plc_in,plc_all_in)

        read_status_besgo = open('/home/pi/txt_file/status_besgo.txt','r')
        status_bes = read_status_besgo.read().rstrip('\n')

        #อ่านค่า set pressure จาก front
        read_set_pressure = open('/home/pi/txt_file/set_pressure.txt','r')
        set_pressure_text = read_set_pressure.read().rstrip('\n')
        split_set_pressure = set_pressure_text.split(",")

        # check nighttime swicth
        # lock_machine = open('/home/pi/txt_file/count_down_close_system.txt','r')
        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
        with open(myFile, "r") as file:
            lock_machine = file.read().rstrip("\n")
        print('file counter'+lock_machine)
        if lock_machine != "":
            sum_counter_lock = write_file.counter_locking(response_api['data_setting'])
            
            if str(response_api['setting_mode'][0]['sm_bypass']) == "1":
               write_file.set_zero_locking_counter()
        
        read_loading_in_tank = open('/home/pi/txt_file/stop_loading_in_tank.txt','r')
        status_loading_in_tank = read_loading_in_tank.read().rstrip('\n')
        

        if type_machine == "1":
            if status_loading_in_tank == "False":
                if str(plc_all_in[6]) == "False" : 
                    if plc[0] == True:
                        plc_mod.stop_filtration()
                
                if str(plc_all_in[7]) =='False':
                
                    if plc_all_out[15] == False:
                        mod_relay.open_solenoid()
                else:
                
                    if plc[0] == False and response_api['setting_mode'][0]['sm_filtration'] == 1: 
                        plc_mod.start_filtration()
                
                if plc_all_in[8] == True:
                
                    if plc_all_out[15] == True:
                        mod_relay.close_solenoid()
        #เงื่อนไข coocon
        if type_machine == "1":
            plc_7_trict = str(plc_all_in[7])
        else:
            plc_7_trict = True

        if str(plc_7_trict) == "True":
            if str(setting_night_time[0]['night_time_enable']) == "0":
                print("night time plc")
                if plc_in[2] == False:
                    print('use night time plc')
                    if int(current_hour) < 21 and int(current_hour) > 7 : 
                        print("in of time")
                        #check bypass mode
                        if str(response_api['setting_mode'][0]['sm_bypass']) == "0":
                            print('NO BY PASS')
                            myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                            with open(myFile, "r") as file:
                                check_close = file.read().rstrip("\n")

                            if check_close == '':  
                                if type_machine == '0':  
                                    besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                                else:
                                    cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                                
                                if status_bes == "True":
                                    if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                        main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                    else:
                                        if int(response_api['machine_option'][0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8,response_api)
                                else :
                                    main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour, response_api,plc_all_out)
                                    main_plc.start_plc()

                                    main_relay = Main_relay(relay_8, plc[0], response_api)
                                    main_relay.start_relay()
                                    
                                    main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                    main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                    main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                    main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                  
                                    if plc[0] == True:
                                        main_ph.start_ph()
                                        main_orp.start_orp()
                                        main_apf.start_apf()
                                        main_chlorine.start_chlorine()
                                      
                                    if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                        main_pump.start_heatpump(temperature, plc, relay_8, heatpump, response_api,plc_all_out)
                                    else:
                                        if int(response_api['machine_option'][0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8,response_api)
                                    #นับเวลาตรวจสอบ pressure ไม่มีแรงดัน
                                    if plc[0] == True and relay_8[4] == False:
                                        if float(split_set_pressure[0]) > float(read_pressure):
                                            counter_pressure = counter_pressure + 1
                                            print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                            if counter_pressure == int(split_set_pressure[1]) :
                                                minus_hour = int(current_hour) + int(split_set_pressure[2])
                                                set_new_time = str(minus_hour)+':'+str(sec_time)
                                                write_file.write_over_presssure(set_new_time)
                                        

                                        
                            else:
                                print("close Anoter Time")
                                close_all.start_close_all(plc_all_out)
                            

                                
                            time.sleep(0.5)
                            volt.start_volt(response_api['machine_option'])
                                
                        else:
                            counter_pressure = 0
                            print('YES BY PASS')
                            myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                            with open(myFile, "r") as file:
                                check_close = file.read().rstrip("\n")
                            if check_close != '':
                                write_file.clear_pressure_time()
                                
                            if type_machine == '0':  
                                besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                            else:
                                cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)

                            if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api, plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)

                            else:
                                print('working machine')
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour,response_api,plc_all_out)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0],response_api)
                                main_relay.start_relay()

                                main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                               
                                if plc[0] == True:
                                    main_ph.start_ph()
                                    main_orp.start_orp()
                                    main_apf.start_apf()
                                    main_chlorine.start_chlorine()
                                  
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                        
                                
                            time.sleep(0.5)
                            volt.start_volt(response_api['machine_option'])
                    else:
                        print("out of time")
                        close_all.start_close_all(plc_all_out)
                            
                        time.sleep(0.5)
                else:
                    print('use night time plc 2')
                    #check bypass mode
                    if str(response_api['setting_mode'][0]['sm_bypass']) == "0":
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close == '':
                            if type_machine == '0':  
                                besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                            else:
                                cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                            if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                            
                            else:
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour,response_api,plc_all_out)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0],response_api)
                                main_relay.start_relay()

                                main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                              
                                if plc[0] == True:
                                    main_ph.start_ph()
                                    main_orp.start_orp()
                                    main_apf.start_apf()
                                    main_chlorine.start_chlorine()
                                  
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)

                                if plc[0] == True and relay_8[4] == False:
                                    if float(split_set_pressure[0]) > float(read_pressure):
                                        counter_pressure = counter_pressure + 1
                                        print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)
                            
                        else:
                            print('CLOSE ALL PLC')
                            close_all.start_close_all(plc_all_out)
                                

                            
                        time.sleep(0.5)
                        volt.start_volt(response_api['machine_option'])
                                
                            
                    else:
                        counter_pressure = 0
                        print("by pass counter pressure stop xxxxxxxxxxx : "+str(counter_pressure))
                        print("by pass night time plc")
                        print("status besgo main : "+status_bes)
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close != '':
                            write_file.clear_pressure_time()
                           

                        if type_machine == '0':  
                            besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                        else:
                            cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                
                        if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                        else:
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour,response_api,plc_all_out)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0],response_api)
                            main_relay.start_relay()

                            main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                            main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                            main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                            main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                           
                            if plc[0] == True:
                                main_ph.start_ph()
                                main_orp.start_orp()
                                main_apf.start_apf()
                                main_chlorine.start_chlorine()
                             
                            if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                            else:
                                if int(response_api['machine_option'][0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8,response_api)
                            
                        time.sleep(0.5)
                        volt.start_volt(response_api['machine_option'])
            else:
                print("night time config api")
                if str(setting_night_time[0]['night_time_status']) == "0":
                    if int(current_hour) < 21 and int(current_hour) > 7 : 
                        print("in of time 2")
                        #check bypass mode
                        if str(response_api['setting_mode'][0]['sm_bypass']) == "0":
                            myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                            with open(myFile, "r") as file:
                                check_close = file.read().rstrip("\n")
                            if check_close == '':    
                                if type_machine == '0':  
                                    besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                                else:
                                    cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                                
                                if status_bes == "True":
                                    if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                        main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                    else:
                                        if int(response_api['machine_option'][0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8,response_api)
                                else:
                                    main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour,response_api,plc_all_out)
                                    main_plc.start_plc()

                                    main_relay = Main_relay(relay_8, plc[0],response_api)
                                    main_relay.start_relay()
                                    
                                    main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                    main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                    main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                    main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                   
                                    if plc[0] == True:
                                        main_ph.start_ph()
                                        main_orp.start_orp()
                                        main_apf.start_apf()
                                        main_chlorine.start_chlorine()
                                      
                                    if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                        main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                    else:
                                        if int(response_api['machine_option'][0]['heater_1']) == 1:
                                            heater.start_heater(temperature, plc, relay_8,response_api)
                                    #นับเวลาตรวจสอบ pressure ไม่มีแรงดัน
                                    if plc[0] == True and relay_8[4] == False:
                                        if float(split_set_pressure[0]) > float(read_pressure):
                                            counter_pressure = counter_pressure + 1
                                            print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                            if counter_pressure == int(split_set_pressure[1]) :
                                                minus_hour = int(current_hour) + int(split_set_pressure[2])
                                                set_new_time = str(minus_hour)+':'+str(sec_time)
                                                write_file.write_over_presssure(set_new_time)
                                        

                                        
                            else:
                                print("close Anoter Time")
                                close_all.start_close_all(plc_all_out)
                                    

                                
                            time.sleep(0.5)
                            volt.start_volt(response_api['machine_option'])
                                
                            
                        else:
                            counter_pressure = 0
                            myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                            with open(myFile, "r") as file:
                                check_close = file.read().rstrip("\n")
                            if check_close != '':
                                write_file.clear_pressure_time()
                                
                            if type_machine == '0':  
                                besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                            else:
                                cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                            
                            if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                        main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)

                            else:
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour,response_api,plc_all_out)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0],response_api)
                                main_relay.start_relay()

                                main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                               
                                if plc[0] == True:
                                    main_ph.start_ph()
                                    main_orp.start_orp()
                                    main_apf.start_apf()
                                    main_chlorine.start_chlorine()
                                
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                        
                                
                            time.sleep(0.5)
                            volt.start_volt(response_api['machine_option'])
                    else:
                        print("out of time")
                        close_all.start_close_all(plc_all_out)
                           
                        time.sleep(0.5)
                else:
                    print("PLC NOT FALSE"+str(relay_8[4]))
                    #check bypass mode
                    if str(response_api['setting_mode'][0]['sm_bypass']) == "0":
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close == '':
                            if type_machine == '0':  
                                besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                            else:
                                cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                            
                            if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                            
                            else:
                                main_plc = Main_PLC(current_time, temperature, plc, relay_8,current_hour,response_api,plc_all_out)
                                main_plc.start_plc()

                                main_relay = Main_relay(relay_8, plc[0],response_api)
                                main_relay.start_relay()

                                main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                                main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                                
                                if plc[0] == True:
                                    main_ph.start_ph()
                                    main_orp.start_orp()
                                    main_apf.start_apf()
                                    main_chlorine.start_chlorine()
                                 
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)

                                if plc[0] == True and relay_8[4] == False:
                                    if float(split_set_pressure[0]) > float(read_pressure):
                                        counter_pressure = counter_pressure + 1
                                        print('xxxxxxxpressure counterxxxxxxxx'+str(counter_pressure))
                                        if counter_pressure == int(split_set_pressure[1]) :
                                            minus_hour = int(current_hour) + int(split_set_pressure[2])
                                            set_new_time = str(minus_hour)+':'+str(sec_time)
                                            write_file.write_over_presssure(set_new_time)
                            
                        else:
                            close_all.start_close_all(plc_all_out)
                                

                            
                        time.sleep(0.5)
                        volt.start_volt(response_api['machine_option'])
                                
                            
                    else:
                        counter_pressure = 0
                        myFile = os.path.abspath("/home/pi/txt_file/count_down_close_system.txt")
                        with open(myFile, "r") as file:
                            check_close = file.read().rstrip("\n")
                        if check_close != '':
                            write_file.clear_pressure_time()
                            

                        if type_machine == '0':  
                            besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api)
                        else:
                            cocoon_besgo.start_besgo(current_time_sec, relay_8, plc, response_api['setting_mode'], response_api['machine_option'],response_api,plc_all_in)
                    
                        if status_bes == "True":
                                if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                    main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                                else:
                                    if int(response_api['machine_option'][0]['heater_1']) == 1:
                                        heater.start_heater(temperature, plc, relay_8,response_api)
                        else:
                            main_plc = Main_PLC(current_time, temperature, plc, relay_8, current_hour,response_api,plc_all_out)
                            main_plc.start_plc()

                            main_relay = Main_relay(relay_8, plc[0],response_api)
                            main_relay.start_relay()

                            main_ph = Main_PH(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                            main_orp = Main_orp(current_time, ph, orp, relay_8,current_hour, response_api,plc_all_out)
                            main_apf = Main_apf(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                            main_chlorine = Main_chlorine(current_time, ph, orp, relay_8,current_hour,response_api,plc_all_out)
                           
                            if plc[0] == True:
                                main_ph.start_ph()
                                main_orp.start_orp()
                                main_apf.start_apf()
                                main_chlorine.start_chlorine()
                             
                            if int(response_api['machine_option'][0]['heat_pump_heater']) == 1 or int(response_api['machine_option'][0]['heat_pump_cooling']) == 1 or  int(response_api['machine_option'][0]['heat_pump_all']) == 1:
                                main_pump.start_heatpump(temperature, plc, relay_8, heatpump,response_api,plc_all_out)
                            else:
                                if int(response_api['machine_option'][0]['heater_1']) == 1:
                                    heater.start_heater(temperature, plc, relay_8,response_api)
                            
                        time.sleep(0.5)
                        volt.start_volt(response_api['machine_option'])
        else:
            if plc[0] == False:
                main_relay = Main_relay(relay_8, plc[0])
                main_relay.start_relay()


except:
    restart_programs()


