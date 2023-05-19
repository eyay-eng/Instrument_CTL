import pyvisa as visa
import time
import sys


class FunctionClass():
    
    sl = 0.0005
    def __init__(self):
        rm = visa.ResourceManager()
        instVisa = rm.list_resources()

        for x in range(len(instVisa)):
            txt = instVisa[x]
            print(instVisa[x])

            if txt.find("SDG1X")>0:
                print("Found Function Generator!")
                funcGen = rm.open_resource(instVisa[x])
                funcGen.read_termination = '\n'
                funcGen.write_termination = '\n'
                self.inst = funcGen

            


    def getIDN(self):
        inst = self.inst
        #Query the instrument and have it identfy
        inst.write('*IDN?')
        time.sleep(self.sl)
        qStr = inst.read()
        return(qStr)
                
    def outputSet(self, channel, set):
        inst = self.inst
        if(set == 0):
            inst.write('C%d:OUTP OFF' % channel)
        else:
            inst.write('C%d:OUTP ON' % channel)

    
    #Use Basic Wave Command to set frequency (MHz)
    def freqSet(self, channel, freq):        
        inst = self.inst
        inst.write('C%d:BSWV FRQ,%dE6' % channel, freq)

