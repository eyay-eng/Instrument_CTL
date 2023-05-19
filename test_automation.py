import io
import serial
import sys
import glob
import time
import pyvisa
from serial.serialutil import PortNotOpenError


class LowerClass:

    def __init__(self):
        self.ser = serial.Serial()
        com_s = input("Input COM port #: ")
        self.ser.port = "COM"+str(com_s)
        self.ser.baudrate = 115200
        self.ser.timeout = 10
        self.ser
        print("opening port....")
        try:
            self.ser.open()
        except (OSError, serial.SerialException):
            print("failed to open port...Terminating")

    def lowerEnable(self):
        print('Lower ENABLE\n')
        self.ser.write(b'\r\n')
        data = self.ser.readline()
        print(data)
        self.ser.flushInput()
        self.ser.write(b'le\n')
        data0 = self.ser.readline()
        data1 = self.ser.readline()
        data3 = self.ser.readline()
        data4 = self.ser.readline()
        print(data4)
      
    def lowerInitialize(self):
        print('Lower Initialize\n')
        self.ser.write(b'\r\n')
        data = self.ser.readline()
        print(data)
        self.ser.flushInput()
        self.ser.write(b'li\n')
        data0 = self.ser.readline()
        data1 = self.ser.readline()
        print(data1)
        self.ser.flushInput()
        



def serialPorts():
    """
    Lists Serial port names
    
    Returns
        a list of serial ports available on the system

    """
    if sys.platform.startswith("win"):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    else:
        raise EnvironmentError('Unspported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



def powerTest():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())
    inst = rm.open_resource("USB0::0x0483::0x7540::SPD3EEDQ5R1679::INSTR")
    inst.read_termination = '\n'
    inst.write_termination = '\n'
    inst.write('*IDN?') #Write instrument and ask for identification string
    time.sleep(1) #Wait
    qStr = inst.read() #Read instrument response
    print (str(qStr)) #Print returned string
    i = 0
    while i < 20:
        i = i+1
        inst.write('OUTput CH1,ON')
        time.sleep(5)
        inst.write('OUTput CH1,OFF')
        time.sleep(1)
    return(inst)


class instPower:
    
    def __init__(self):
        rm = pyvisa.ResourceManager()
        global inst
        inst = rm.open_resource("USB0::0x0483::0x7540::SPD3EEDQ5R1679::INSTR")
        inst.read_termination = '\n'
        inst.write_termination = '\n'
        inst.write('*IDN?')
    __init__

    def togglePower(self):
        #Get current status
        inst.write('SYSTem:STATus?')
        time.sleep(0.04)
        qHex = inst.read()

        #Convert Hex to binary
        scale = 16
        num_of_bits = 6
        bitMap = bin(int(qHex, scale))[2:].zfill(num_of_bits)
        if int(bitMap[1]) == 0:
            #Turn Power ON
            inst.write('OUTput CH1,ON')
            print('ON')
        else:
            #turn Power Off
            inst.write('OUTPut CH1,OFF')
            print('off')


def main():
    print("Starting program....\nPrinting available COM Ports:")
    print(serialPorts())
    x = LowerClass()

    inst = instPower()
    
    i = 0

    while i < 120:
        inst.togglePower()
        time.sleep(8)

        x.lowerEnable()
        time.sleep(.5)

        x.lowerInitialize()
        time.sleep(.5)

        inst.togglePower()
        time.sleep(1)
        i = i+1
    
    



if __name__ == '__main__':
    main()
    
