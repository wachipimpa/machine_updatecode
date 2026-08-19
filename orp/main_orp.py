from modbus_orp import Modbus_ORP
import time


modbus_orp = Modbus_ORP()
class Main_orp:
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

    def start_orp(self):
        print('-------start ORP -------')
        #load setting ph
        if str(self.response_api['machine_option'][0]['orp']) == '1':
            ph_json = self.response_api['substance']

            #load time ph
            data_orp = self.response_api['orp']
        
            #read status 8 relay
            relay8 = self.set_relay
            filtration_time_status = self.response_api['filtration_time']
            
            if str(filtration_time_status[int(self.current_hour)]) != "0":
                self.process_woking(data_orp[0]['orp_'+str(int(self.current_hour) + 1)], ph_json, relay8)

    def process_woking(self,data_orp ,ph_json, relay8):
        if data_orp == "1":
            self.process_orp(ph_json, relay8)
        else:
            if relay8[6] == True:
                modbus_orp.stop_orp()


    def process_orp(self, orp_json,relay8):
        read_orp = self.read_orp_address
        #อ่าน สถานะ relay
        print('xxxxxxxxxxxxxxxx ORP COUNTER xxxxxxxxxxxxxxxx'+str(modbus_orp.read_orp_counter()))
        print(read_orp)
        print(orp_json[0]['orp_set'])

        if float(read_orp) <= float(orp_json[0]['orp_set']):
            if int(modbus_orp.read_orp_counter()) == 0 :
                modbus_orp.start_orp()
                time.sleep(float(orp_json[0]['orp_inj']))
                modbus_orp.stop_orp()
                modbus_orp.write_orp_counter()
            else:
                if int(modbus_orp.read_orp_counter()) >= (int(orp_json[0]['orp_freq']) * 60) :
                    modbus_orp.set_orp_counter_zero()
                else :
                    modbus_orp.write_orp_counter()
            

        elif float(read_orp) >= float(orp_json[0]['orp_lower']):
            if relay8[6] == True:
                modbus_orp.stop_orp()
                modbus_orp.set_orp_counter_zero()