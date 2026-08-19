from modbus_chlorine import Modbus_chlorine
import time


modbus_chlorine = Modbus_chlorine()

class Main_chlorine:
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

    def start_chlorine(self):
        print('-------start Chlorine -------')
        if str(self.response_api['machine_option'][0]['chlorine']) == '1':
        #load setting ph
            ph_json = self.response_api['substance']

            #load time ph
            data_chlorine = self.response_api['chlorine']
        
            #read status 8 relay
            relay8 = self.set_relay
            filtration_time_status = self.response_api['filtration_time']
            
            if str(filtration_time_status[int(self.current_hour)]) != "0":
                self.process_woking(data_chlorine[0]['chlorine_'+str(int(self.current_hour) + 1)], ph_json)

    def process_woking(self,data_chlorine ,ph_json):
        if data_chlorine == '1':
            self.process_chlorine(ph_json)
        else:
            if self.plc_all_out[8] == True:
                modbus_chlorine.process_inj(8,0)


    def process_chlorine(self, chlorine_json):
        print('xxxxxxxxxxxxxxxx COUNTER Chlorine xxxxxxxxxxxxxxxx'+str(modbus_chlorine.read_chlorine_counter()))
        
        if int(modbus_chlorine.read_chlorine_counter()) == 0:
            modbus_chlorine.process_inj(8,1)
            time.sleep(float(chlorine_json[0]['chlorine_inj']))
            modbus_chlorine.process_inj(8,0)
            modbus_chlorine.write_chlorine_counter()
        else:
            if modbus_chlorine.read_chlorine_counter() >= (float(chlorine_json[0]['chlorine_freq']) * 60) :
                modbus_chlorine.set_chlorine_counter_zero()
            else:
                modbus_chlorine.write_chlorine_counter()