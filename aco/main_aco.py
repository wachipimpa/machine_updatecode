from modbus_aco import Modbus_aco
import time


modbus_aco = Modbus_aco()

class Main_aco:
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

    def start_aco(self):
        print('-------Start ACO -------')
        #load setting ph
        ph_json = self.response_api['substance']

        #load time ph
        data_aco = self.response_api['acos']
    
        #read status 8 relay
        relay8 = self.set_relay
        filtration_time_status = self.response_api['filtration_time']
        
        if str(filtration_time_status[int(self.current_hour)]) != "0":
            self.process_woking(data_aco[0]['aco_'+str(int(self.current_hour) + 1)], ph_json)

    def process_woking(self,data_aco ,ph_json):
        if data_aco == '1':
            self.process_aco(ph_json)
        else:
            if self.plc_all_out[9] == True:
                modbus_aco.process_inj(9,0)


    def process_aco(self, aco_json):
        print('xxxxxxxxxxxxxxxx COUNTER ACO xxxxxxxxxxxxxxxx'+str(modbus_aco.read_aco_counter()))
        
        if int(modbus_aco.read_aco_counter()) == 0:
            modbus_aco.process_inj(9,1)
            time.sleep(float(aco_json[0]['aco_inj']))
            modbus_aco.process_inj(9,0)
            modbus_aco.write_aco_counter()
        else:
            if modbus_aco.read_aco_counter() >= (float(aco_json[0]['aco_freq']) * 60) :
                modbus_aco.set_aco_counter_zero()
            else:
                modbus_aco.write_aco_counter()