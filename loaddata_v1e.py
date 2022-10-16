# -*- coding: utf-8 -*-
"""
@author: Maryam Gadiali
Date: June 7th 2022
Reads physics data from text file about oscillations and writes peak, amplitude and baseline data
to a new file
Version : 0a
Initial creation
Version : 0b
Found the x-axis value of peak and trigger times
Version : 0c
Changed technique of finding x value of peak by using numpy.where
Version : 1a
Cleaned up code and performing on muon data now
Version : 1b
Now doing data for 31st of july
Version : 1c
Plotted for 4 simultaaneous muon results
Version : 1d
Found the range of minimum and maximum peaks
Version : 1e
Got rid of unusual data 
"""

import matplotlib.pyplot as plt
import numpy as np
import read_lecroy_trc as trc
import time
import datetime

file1 = open("MyFile.txt","w")
file1.write(" File Number \t Baseline \t Peak \t Amplitude \t Trigger Time \t Time where peak occured \t Unix Time \t Difference between min and max peak")

plt.xlabel("Time(secs)")
plt.ylabel("Voltage")

STARTNUM=39658 #46352, 39658
SAMPLES=1000

for i in range(STARTNUM, STARTNUM+SAMPLES):
    plt.title("Physics data for Muons - Event {}".format(i))
    minimumValue=10000
    maximumValue=-9999
    minimumSwitch=0
    maximumSwitch=0
    rangeList=[]
    for j in range(1,5):
        fileName='//uol.le.ac.uk/root/student/home/m/mzg1/My Documents/Pythonscript/MuonData/muons31072021_s3_TEST/Tx31072021_MINUS1_s3/C'+str(j)+'--scope3--'+str(i).zfill(5)+'.trc'
        x,y,d=trc.readTrc(fileName)
        y=-y
        triggerTime=d.get('TRIGGER_TIME')
        peak=np.max(y[192:250])   
        maximumPt=np.max(y[:])
        if peak > 0.14:
            file1.write("\n" +fileName.split("/")[-1]+"\t Saturated \n")
            continue
        
        if maximumPt == peak: #makes sure that the maximum is in the right place
            plt.plot(x,y)
            baseline=np.mean(y[0:200]) #outdated
        
            timeUnix=time.mktime(triggerTime.timetuple())+(triggerTime.microsecond*1e-6)
            xPeakValue=(x[np.where(y==peak)][0]) 
          
# =============================================================================
#             if xPeakValue < minimumValue:
#                 minimumValue=xPeakValue
#                 minimumSwitch=1
#              
#             elif xPeakValue> maximumValue:
#                 maximumValue=xPeakValue
#                 maximumSwitch=1
# =============================================================================
            rangeList.append(xPeakValue)
            
                
            amplitude=peak-baseline
            
            
            file1.write("\n "+ fileName.split("/")[-1] + " \t " +str(baseline)+" \t "+str(peak)+" \t "+str(amplitude)+" \t "+str(triggerTime)+" \t "+str(xPeakValue) +" \t "+str(timeUnix))
        
    #if (minimumSwitch==1) and (maximumSwitch==1):
        
    if len(rangeList)>1:
        minimumValue=min(rangeList)
        maximumValue=max(rangeList)
        ptRange=maximumValue-minimumValue
        file1.write(" \t " + str(ptRange))
    
XLIMITMIN=-2e-8
XLIMITMAX=4e-8
plt.xlim(XLIMITMIN, XLIMITMAX)
#plt.axhline(baseline) #outdated
plt.grid()
plt.show()

file1.close()

# =============================================================================
# file1 = open('MyFile.txt', 'r')
# Lines = file1.readlines()      
# count = 0
# for line in Lines:
#     count += 1
#     print("Line{}: {}".format(count, line.strip()))
# =============================================================================

#maximum == right place
#load in c1 to c4 data and over plot

#why is extra data given
#do histogram for time difference
