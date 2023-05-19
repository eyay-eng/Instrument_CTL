import pyvisa as visa
import time

class PowerSupply():
    #Class built for Siglent SPD3303C

    sl = 0.0005
    def __init__(self):
        rm = visa.ResourceManager()
        instVisa = rm.list_resources()

        #search tuple of resources and find correct Power Supply
        for x in range(len(instVisa)):
            txt = instVisa[x]
            if txt.find("SPD3")>0:
                print("Found Power Supply!")
                powSupply = rm.open_resource(instVisa[x])

        powSupply.read_termination = '\n'
        powSupply.write_termination = '\n'
        
        self.inst = powSupply

    def togPowCh1(self):
        inst = self.inst

        inst.write("*IDN?")
        time.sleep(self.sl)
        dat = inst.read()
        return(dat)

    def saveState(self, name):
        #Saves current state in nonvolatile memory with the specified name <1, 2, 3...>
        inst = self.inst
        inst.write("*SAV %s" % name)
        
    def rcl(self, name):
        #Recall state that previously saved
        inst = self.inst
        inst.write("*RCL %s" % name)

    def chSelect(self, channel):
        inst = self.inst
        inst.write('INSTrument CH%d' % channel)

    def chQuery(self):
        inst = self.inst
        #returns the current operating channel
        inst.write('INSTrument?')
        time.sleep(self.sl)
        qStr = inst.read()
        return(qStr)

    def chMeasureCurrent(self, channel):
        inst = self.inst
        #Query current value for specified channel
        inst.write('MEASure:CURRent? CH%d' % channel)
        time.sleep(self.sl)
        qStr = inst.read()
        return(qStr)

    def chMeasureVoltage(self, channel):
        inst = self.inst
        #Queary voltage calue for specified channel
        inst.write('MEASure:VOLTage? CH%d' % channel)
        time.sleep(self.sl)
        qStr = inst.read()
        return(qStr)

    def setCurrent(self, channel, value):
        inst = self.inst
        #Set current value for the current channel
        self.chSelect(channel)
        time.sleep(self.sl)
        inst.write("CH%d:CURRent %f" % (channel,value))

    def getCurrent(self, channel):
        inst = self.inst
        #Get the current value for the current channel
        self.chSelect(channel)
        time.sleep(self.sl)
        inst.write('CH%d:CURRent?' % channel)
        time.sleep(self.sl)
        dat = inst.read()
        return(dat)

    def setVoltage(self, channel, volt):
        inst = self.inst
        #Set voltage value for the current channel
        self.chSelect(channel)
        time.sleep(self.sl)
        inst.write('CH%d:VOLTage %f' % (channel, volt))

    def getVoltage(self, channel):
        inst = self.inst
        #get voltage for the current channel
        self.chSelect(channel)
        time.sleep(self.sl)
        inst.write('CH%d:VOLTage?' % channel)
        time.sleep(self.sl)
        dat = inst.read()
        return(dat)

    def outputSet(self, channel, set):
        inst = self.inst
        if(set == 0):
            inst.write('OUTPut CH%d,OFF' % channel)
        else:
            inst.write('OUTPut CH%d,ON' % channel)
