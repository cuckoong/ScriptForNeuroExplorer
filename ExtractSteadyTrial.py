# This is to extract steady trial for anti, and pro trials (last 20)
# steps:
   #1) get the first anti/pro trial after switch (this is get from the extract event script)
   #2)for trials proceeded before the first anti/pro trial, get the last 20 trials as the previous block; (as event and interval)
   #3)name the block with index: Anti/Pro_steady_block_n, n (as index)
   #4) 
from __future__ import division
import nex
import math
import sys
import json

#input paramters, for the interval size
shiftMin = 0
shiftMax = 1
print('The interval for each block is 0-1s')

#get the file
doc = nex.GetActiveDocument()
filename = nex.GetDocTitle(doc)
print('You are extracting steady trials from this file: '+filename)

#usually the first channel is 1st_Anti_AfterPro
#The second channel is 1st_Pro_AfterAnti
first_Anti_AfterSwitch = nex.GetVarByName(doc,'1st_Anti_AfterPro').Timestamps()
first_Pro_AfterSwitch =  nex.GetVarByName(doc,'1st_Pro_AfterAnti').Timestamps()
ProTs =  nex.GetVarByName(doc,'Pro').Timestamps()
AntiTs = nex.GetVarByName(doc,'Anti').Timestamps()

Num_Pro_Steady = len(first_Anti_AfterSwitch)
Num_Anti_Steady = len(first_Pro_AfterSwitch)
print('Steady Trials in Pro Task has '+str(Num_Pro_Steady)+' blocks')
print('Steady Trials in Anti Task has '+str(Num_Anti_Steady)+' blocks')


#This is event based on pro and anti cue.
def GetSteadyBlock(Num_Steady,TrialTs,first_AfterSwitch,TrialType, shiftMin, shiftMax):
    #Get steady block from pro/anti trials
    for i in range(Num_Steady):
        steady_all_ts = [ts for ts in TrialTs if ts <= first_AfterSwitch[i]]
        steady_ts = steady_all_ts[-20:]
        #get the steady timestamp from last 20 trials
        print('1st '+TrialType+' trial after switch: '+ str(first_AfterSwitch[i]))
        print('the timestamps for the last 20 previous kind of trials before switch: '+str(steady_ts))  
        
        #add the timestamp as event in the file with name formated as pre/anti_steady_block_num_trial
        name_steady_block = TrialType + '_steady_block_'+str(i)
        doc[name_steady_block] = nex.NewEvent(doc, 0) 
        for j in steady_ts:
            temp = nex.GetVarByName(doc,name_steady_block)
            nex.AddTimestamp(temp,j)
            doc[name_steady_block+'_Trial'] = nex.MakeIntervals(doc[name_steady_block], shiftMin, shiftMax)

GetSteadyBlock(Num_Anti_Steady,AntiTs,first_Pro_AfterSwitch,'Anti',shiftMin, shiftMax)
GetSteadyBlock(Num_Pro_Steady,ProTs,first_Anti_AfterSwitch,'Pro',shiftMin, shiftMax)


#get each bin information for pro/anti steady reference in each pro/anti steady trial (help by the template)





