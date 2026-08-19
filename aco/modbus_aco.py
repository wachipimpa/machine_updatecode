import serial
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url
import minimalmodbus

path_url = Path_url()
class Modbus_aco:
        
    def read_aco_counter(self):
        read_ph = open('/home/pi/txt_file/counter_aco.txt','r')
        return int(read_ph.read())
    
    def write_aco_counter(self):
        counter_ph = self.read_aco_counter()
        counter_ph += 1
        write_ph = open('/home/pi/txt_file/counter_aco.txt','w')
        write_ph.write(str(counter_ph))

    def set_aco_counter_zero(self):
        write_ph = open('/home/pi/txt_file/counter_aco.txt','w')
        write_ph.write("0")

    def process_inj(self,addres,status):
        instrument = minimalmodbus.Instrument(path_url.modbus_port,path_url.plc_address)
        instrument.serial.port                     # this is the serial port name
        instrument.serial.baudrate = 9600         # Baud        instrument.serial.bytesize = 8
        instrument.serial.parity   = serial.PARITY_NONE
        instrument.serial.stopbits = 1
        instrument.serial.timeout  = 1
        instrument.write_bit(addres,status,5)