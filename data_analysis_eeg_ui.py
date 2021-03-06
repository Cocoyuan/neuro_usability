# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 12:09:06 2017

@author: Stephane
"""

import csv
import matplotlib.pyplot as plt
import scipy.stats as stat

tab = [] #table
T1 = [] #time from ui
T2 = [] #time from eeg
S1 = [] #time in seconds since beginning of the DAY from the UI
S2 = [] #idem with eeg
A = [] #arousal from UI
P = [] #pleasure from UI
STE = [] #short term excitement from EEG
LTE = [] #long term excitement from EEG
EB = [] #engagement/boredom from EEG
EB_ = [] #average engagement/boredom on the last 3 seconds before ui event

#reading data from UI
with open('data/001_ui.csv', 'rt') as ui:
    reader = csv.reader(ui)
    next(reader) #jump the header
    for row in reader:
        T1.append(row[0])
        A.append(float(row[2]))
        P.append(float(row[3]))
        
#reading data from eeg
with open('data/001_eeg.csv', 'rt') as eeg:
    reader = csv.reader(eeg)
    next(reader) #jump the header
    for row in reader:
        if(row[0] != 'Time from start'):
            T2.append(row[0])
            STE.append(float(row[16])) 
            LTE.append(float(row[17]))
            EB.append(float(row[18]))

#converting time clock to seconds from the beginning of the DAY
for t in T1:
     DateAndTime = t.split(' ')
     Clock = DateAndTime[1].split(":")
     sec = int(Clock[0]) * 3600 + int(Clock[1]) * 60 + int(Clock[2])
     S1.append(sec)
     
for t in T2:
     DateAndTime = t.split(' ')
     Clock = DateAndTime[1].split(":")
     sec = int(Clock[0]) * 3600 + int(Clock[1]) * 60 + int(Clock[2])
     S2.append(sec)
     
#crop eeg data on S1 (UI time)
#the ten first images are just for training
#so the real data begin at S1[9] - 3s
#c = 0
#while S2[c] <  S1[9] - 3:
#    c += 1
#
#S2 = S2[c:] #from the c th element
#A = A[c:]
#P = P[c:]

#average
for k in range(9, len(S1)):
    
    d = 0.1
    
    tCurrent = S1[k]  #current event time
    tPast = S1[k-1]  #last past event time
    tInit = tPast + 1 #init data after the black screen
    
    #definition of time frame for average computation
    if (tCurrent - tPast < d+1):  #quick answer from user (1s black + 3s reflexion)
        tEnd = tCurrent
    else: 
        tEnd = tInit + d
    
    #converting S1 index into S2 index
    i = 0
    while(S2[i]<tInit):
        i += 1
    ia = i;
    while(S2[i]<tEnd):
        i+= 1
    ib = i;
    
    EB_.append(sum(EB[ia:ib])/len(EB[ia:ib]))
    

plt.plot(S1[9:], A[9:])
plt.plot(S1[9:], EB_)
#plt.plot(A[9:], EB_, 'ro')
#plt.axis([0, 1, 0, 1])

D = [] #rating duration 
for i in range(9, len(S1)):
    D.append(S1[i]-S1[i-1])
print(sum(D)/len(D))
    
print(S1)

print(stat.spearmanr(A[9:], EB_))




    
    

