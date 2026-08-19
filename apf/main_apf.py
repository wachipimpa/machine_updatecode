from modbus_apf import Modbus_APF
import time


modbus_apf = Modbus_APF()

class Main_apf:
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

    def start_apf(self):
        print('-------start APF -------')
        #load setting ph
        if str(self.response_api['machine_option'][0]['apf']) == '1':
            ph_json = self.response_api['substance']

            #load time ph
            data_apf = self.response_api['apf']

            #read status 8 relay
            relay8 = self.set_relay
            filtration_time_status = self.response_api['filtration_time']
            
            if str(filtration_time_status[int(self.current_hour)]) != "0":
                self.process_woking(data_apf[0]['apf_'+str(int(self.current_hour) + 1)], ph_json, relay8)

    def process_woking(self,data_apf ,ph_json, relay8):
        if data_apf == "1":
            self.process_apf(ph_json)
        else:
            if relay8[7] == True:
                modbus_apf.process_inj(7,0)


    def process_apf(self, apf_json):
        print('xxxxxxxxxxxxxxxx COUNTER APF xxxxxxxxxxxxxxxx'+str(modbus_apf.read_apf_counter()))
        print(apf_json[0]['apf_inj'])
        print(apf_json[0]['apf_freq'])

        if int(modbus_apf.read_apf_counter()) == 0:
            modbus_apf.process_inj(7,1)
            time.sleep(float(apf_json[0]['apf_inj']))
            modbus_apf.process_inj(7,0)
            modbus_apf.write_apf_counter()
        else:
            if modbus_apf.read_apf_counter() >= (float(apf_json[0]['apf_freq']) * 60) :
                modbus_apf.set_apf_counter_zero()
            else:
                modbus_apf.write_apf_counter()