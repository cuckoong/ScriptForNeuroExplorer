#apply the template to get each bin counts, for different bin window(0.2-1.0s), and interval time window (1.0s-2.0s), and each cue reference


from __future__ import division
import nex
import math
import sys
import json
import os


doc = nex.GetActiveDocument()
filename = nex.GetDocTitle(doc)
print(filename)

print('You are extracting steady trials from this file: '+filename)


def changeValueinTemp(tempfile, Reference, Bin,Xmin,Xmax, resultFolder):    
    nex.ModifyTemplate(doc, tempfile, "Bin (sec)", Bin)
    nex.ModifyTemplate(doc, tempfile, "Reference", Reference)
    nex.ModifyTemplate(doc, tempfile, "XMin (sec)", Xmin)
    nex.ModifyTemplate(doc, tempfile, "XMax (sec)", Xmax)
    nex.ModifyTemplate(doc, tempfile, 'Send to Excel', 'None')  #no need send to excel, but save result in csv file
    nex.ApplyTemplate(doc, tempfile)    
    resultPath =  resultFolder + '/'+Reference+'_Bin'+Bin + '_Xmin'+Xmin+'_Xmax'+Xmax+'.csv'
    nex.SaveNumResults(doc, resultPath)
    
#Example
tempfile = "C:/Users/309i7/Documents/NeuroExplorer 5/Templates/PandaShift/BinCounts/post_steadycue.ntp"
FileFolder = 'E:/Panda/PandaData/AnalysedData/ProAnti-trialbincount/'+filename

#Reference = 'Anti_steady_block_0'
#Bin = '0.02'
#Xmin = '0'
#Xmax = '1'

eventnames = doc.EventNames()

#return reference in this file
References =  [eventname \
    for eventname in eventnames \
    if 'steady_block_' in eventname and (eventname.endswith('Anti') or eventname.endswith('Pro')) ]
    
Bins = ['0.02','0.04','0.1']
Xmins = ['0','-0.5']
Xmaxs = ['1','1.5']



for Bin, Xmin, Xmax in \
    [(Bin, Xmin, Xmax) \
    for Bin in Bins \
    for Xmin in Xmins \
    for Xmax in Xmaxs]:
        resultFolder = FileFolder + '/Bin' + Bin  + '_Xmin' + Xmin + '_Xmax' + Xmax
        if not os.path.exists(resultFolder):
            os.makedirs(resultFolder)
        for Reference in References:
            print(Reference, Bin, Xmin, Xmax)
            changeValueinTemp(tempfile, Reference, Bin, Xmin,Xmax, resultFolder)


print('This is the end of the analysis')