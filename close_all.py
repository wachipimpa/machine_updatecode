import sys
import serial
import minimalmodbus
import time
sys.path.append('/home/pi/hottub_ma/plc/')
from modbus import Modbus
sys.path.append('/home/pi/hottub_ma/relay/')
from modbus_relay import Modbus_relay
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url


plc_mod = Modbus()
relay_mod = Modbus_relay()
path_url = Path_url()

class Close_All:
    def start_close_plc(self, plc):
        if plc[0] == True:
            try:
                send = serial.Serial(
                    port=path_url.modbus_port,
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1)
                data_bytes = bytes([path_url.plc_address,0x05,0x00,0x00,0x00,0x00,0xCD,0xCA])
                send.write(data_bytes)
                # send.write(b"\x01\x05\x26\x00\x00\x00\xC6\x82")
                send.close()
            except:
                pass
        if plc[0] == False:
            if plc[1] == True:
                try:
                    ozone = serial.Serial(
                        port=path_url.modbus_port,
                        baudrate = 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
                    data_bytes = bytes([path_url.plc_address,0x05,0x00,0x01,0x00,0x00,0x9C,0x0A])
                    ozone.write(data_bytes)
                    # ozone.write(b"\x01\x05\x26\x01\x00\x00\x97\x42")
                    # ozone.close()
                except:
                    pass
        if plc[1] == False:
            if plc[2] == True:
                try:
                    send = serial.Serial(
                        port=path_url.modbus_port,
                        baudrate = 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=1)
                    data_bytes = bytes([path_url.plc_address,0x05,0x00,0x02,0xFF,0x00,0x2D,0xFA])
                    send.write(data_bytes)
                    # send.write(b"\x01\x05\x26\x02\x00\x00\x67\x42")
                except:
                    pass

    def start_close_relay(self, relay):
        if relay[1] == False:
            relay_mod.close_pompe_air()
        if relay[0] == True:
            relay_mod.close_lamp_ozone()
        if relay[0] == False:
            relay_mod.close_lamp_uv()
        if relay[2] == False:
            relay_mod.close_besgo()
        if relay[3] == False:
            relay_mod.close_ph()
        if relay[4] == False:
            relay_mod.close_orp()
        if relay[5] == False:
            relay_mod.close_apf()
            
    def start_close_all(self,plc_all_out):
        if plc_all_out[1] == True:
            instrument = minimalmodbus.Instrument("/dev/usb_485",1)
            instrument.serial.port                     # this is the serial port name
            instrument.serial.baudrate = 9600         # Baud        instrument.serial.bytesize = 8
            instrument.serial.parity   = serial.PARITY_NONE
            instrument.serial.stopbits = 1
            instrument.serial.timeout  = 1
            instrument.write_bit(1,0,5)
            time.sleep(3)
        else:
            if plc_all_out[12] == True:
                instrument = minimalmodbus.Instrument("/dev/usb_485",1)
                instrument.serial.port                     # this is the serial port name
                instrument.serial.baudrate = 9600         # Baud        instrument.serial.bytesize = 8
                instrument.serial.parity   = serial.PARITY_NONE
                instrument.serial.stopbits = 1
                instrument.serial.timeout  = 1
                instrument.write_bit(12,0,5)
                time.sleep(3)
            else:
                for item in range(15, -1, -1):
                    if plc_all_out[item] == True:
                        instrument = minimalmodbus.Instrument("/dev/usb_485",1)
                        instrument.serial.port                     # this is the serial port name
                        instrument.serial.baudrate = 9600         # Baud        instrument.serial.bytesize = 8
                        instrument.serial.parity   = serial.PARITY_NONE
                        instrument.serial.stopbits = 1
                        instrument.serial.timeout  = 1
                        instrument.write_bit(item,0,5)
                        time.sleep(3)
                
            

