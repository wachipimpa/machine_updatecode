import serial
import sys

from pymodbus.client import ModbusSerialClient
try:
            send = serial.Serial(
                port="/dev/usb_485",
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1)
            data_bytes = bytes([0x01,0x05,0x00,0x02,0x00,0x00,0x6C,0x0A])
            send.write(data_bytes)
            # send.write(b"\x01\x05\x26\x02\x00\x00\x67\x42")
except:
    pass
