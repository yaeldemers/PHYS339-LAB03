# Import seaborn
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import serial
import time as t

# Apply the default theme
sns.set_theme()

statsA0 = np.zeros((2,255)) #PIN A0
statsA1 = np.zeros((2,255)) #PIN A1

max8bit = 256
maxVolt = 5

convertFrom8bit = maxVolt/max8bit

for  i in range(255): 
    #print("i: ", i)
    value=i
    arraySize=500
    serialPort=serial.Serial()
    serialPort.baudrate=9600
    serialPort.port="COM5"
    serialPort.open()
    dataRead=False
    data=[]

    while (dataRead==False):
        
        serialPort.write(bytes([value]))
        t.sleep(0.1)
        inByte = serialPort.in_waiting
    # This loop reads in data from the array until byteCount reaches the array size (arraySize)
        byteCount=0
        while ((inByte>0)&(byteCount<arraySize)):

            dataByte=serialPort.read()
            byteCount=byteCount+1
            data=data+[dataByte]
        if (byteCount==arraySize):
            dataRead=True
            
    serialPort.close()

    dataOut=np.zeros(arraySize)
    arrayIndex=range(arraySize)
    # Transform unicode encoding into integers
    for i in arrayIndex:
        dataOut[i]=ord(data[i])
        
    A0 = dataOut[:250]
    A1 = dataOut[250:]

    # Converting to voltage
    # The 50 first measurements show transient behavior
    A0 = A0[50:]*convertFrom8bit # reading * 5 / 1023 -> Voltage conversion 
    A1 = A1[50:]*convertFrom8bit
    
    # Saving the mean and error of each measurement on the voltage spectrum
    statsA0[0][value]=np.mean(A0)
    statsA0[1][value]=np.std(A0)

    statsA1[0][value]=np.mean(A1)
    statsA1[1][value]=np.std(A1)
    
    # Current array
    AI = np.abs(statsA0[0]-statsA1[0])/901

np.save("runs/greenVoltage2", statsA1)
np.save("runs/greenCurrent2", AI)

