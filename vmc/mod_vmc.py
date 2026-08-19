import serial
import sys
sys.path.append('/home/pi/hottub_ma/setting/')
from path_url import Path_url

path_url = Path_url()
class Mod_vmc:
    def start_vmc_main(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.vmc1_address,0x06,0x00,0x02,0x00,0x01,0xE8,0x7D])
        send.write(data_bytes)

    def stop_vmc_main(self):
        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes([path_url.vmc1_address,0x06,0x00,0x02,0x00,0x05,0xE9,0xBE])
        send.write(data_bytes)

    def modbusCrc(msg:str) -> int:
        crc = 0xFFFF
        for n in range(len(msg)):
            crc ^= msg[n]
            for i in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def compute_crc_speed(self, speed):
        hex_set = hex(speed)
        data_1 = hex_set[2:4]      
        data_2 = hex_set[4:6]
        #รวม string ประกอบก่อนเพื่อหา crc16
        string = "06060001"+data_1+data_2
        #แปลงเป็น hex
        msg = bytes.fromhex(string)
        #generate crc16 ใน function
        crc = self.modbusCrc(msg)
      
        ba = crc.to_bytes(2, byteorder='little')
        #แยกค่าที่ gen crc16
        data = "%02X %02X"%(ba[0], ba[1])
        spit_data = data.split(' ')

        #รวม stringแล้วแปลง hex ก่อนส่ง serial 
        new_hex_string = string+spit_data[0]+spit_data[1]
        gen_sending = bytes.fromhex(new_hex_string)
        #สั้ง setค่า
        self.set_speed_from_vmc(gen_sending)


    def set_speed_from_vmc(self, data_string):

        send = serial.Serial(
                port=path_url.modbus_port,
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
        data_bytes = bytes.fromhex(data_string)
        send.write(data_bytes)
        print(send.readlines())

    def compute_speed(self, speed_data):
        set_original = 10000
        max_percent = 100
        percent_set = int((speed_data * set_original) / max_percent)
        self.compute_crc_speed(percent_set)
        # return int((speed_data * set_original) / max_percent)

