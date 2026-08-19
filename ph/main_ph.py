from urllib.request import urlopen
import json
import sys
import time
from setting.path_url import Path_url
from  modbus_ph import Modbus_PH
sys.path.append('/home/pi/hottub_ma/orp/')
from modbus_orp import Modbus_ORP
sys.path.append('/home/pi/hottub_ma/apf/')
from modbus_apf import Modbus_APF

path_url = Path_url()
url_substance = path_url.url_substance
url_ph = path_url.url_ph
url_orp = path_url.url_orp
url_apf = path_url.url_apf

modbus_ph = Modbus_PH()
modbus_orp = Modbus_ORP()
modbus_apf = Modbus_APF()

class Main_PH:
    current_time = ''
    counter_ph = 0 
    counter_orp = 0
    counter_apf = 0
    read_ph_address = 0
    read_orp_address = 0
    set_relay = ''
    current_hour = ''
    response_api = ''
    plc_all_out = ''
    def __init__(self, current_time, set_ph, set_orp, set_relay, current_hour, response_api,plc_all_out):
        self.current_time = current_time
        self.read_ph_address = set_ph
        self.read_orp_address = set_orp
        self.set_relay = set_relay
        self.current_hour = current_hour
        self.response_api = response_api
        self.plc_all_out = plc_all_out

    def start_ph(self):
        print('-------start PH-------')
        if str(self.response_api['machine_option'][0]['ph']) == '1':
            #load setting ph
            ph_json = self.response_api['substance']

            #load time ph
            data_ph = self.response_api['ph']
            
            #read status 8 relay
            relay8 = self.set_relay
            filtration_time_status = self.response_api['filtration_time']
            
            if str(filtration_time_status[int(self.current_hour)]) != "0":
                self.process_woking(data_ph[0]['ph_'+str(int(self.current_hour) + 1)], ph_json, relay8)


    def process_woking(self, data_ph, ph_json, relay8):

        if data_ph == "1":
            self.process_ph(ph_json, relay8)
        else:
            if relay8[5] == True:
                modbus_ph.stop_ph()
       


    def process_ph(self, ph_json, relay8):
        read_ph = self.read_ph_address
        #อ่าน สถานะ relay
        print('xxxxxxxxxxxxxxxx PH COUNTER xxxxxxxxxxxxxxxx'+str(modbus_ph.read_ph_counter()))
        if ph_json[0]['ph_main_status'] == 'top':
            if float(read_ph) >= float(ph_json[0]['ph_set']):
                if int(modbus_ph.read_ph_counter()) == 0  :
                    modbus_ph.start_ph()
                    time.sleep(float(ph_json[0]['ph_inj']))
                    modbus_ph.stop_ph()
                    modbus_ph.write_ph_counter()
                else:
                    if int(modbus_ph.read_ph_counter()) >= (int(ph_json[0]['ph_freq']) * 60)  :
                        modbus_ph.set_ph_counter_zero()
                    else:
                        modbus_ph.write_ph_counter()

            elif float(read_ph) <= float(ph_json[0]['ph_lower']):
                if relay8[5] == True:
                    modbus_ph.stop_ph()
                    modbus_ph.set_ph_counter_zero()
        else:
            if float(read_ph) <= float(ph_json[0]['ph_lower']):
                if int(modbus_ph.read_ph_counter()) == 0 :
                    modbus_ph.start_ph()
                    time.sleep(float(ph_json[0]['ph_inj']))
                    modbus_ph.stop_ph()
                    modbus_ph.write_ph_counter()
                else:
                    if int(modbus_ph.read_ph_counter()) >= (int(ph_json[0]['ph_freq']) * 60)  :
                        modbus_ph.set_ph_counter_zero()
                    else:
                        modbus_ph.write_ph_counter()

                    
            elif float(read_ph) >= float(ph_json[0]['ph_set']):
                if relay8[5] == True:
                    modbus_ph.stop_ph()
                    modbus_ph.set_ph_counter_zero()


   