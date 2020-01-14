# -*- coding: utf-8 -*-
#argv1: mappa
#argv2: file destinatione
#argv3: posizione iniziale robot(s) coordinate in pixel x,y
#argv4: punti interesse
#argv5: tipo robot [tipo robot1, tipo robot2,...]
#argv6: grid 
#argv7: larghezza massima stanza

#-------------- PROGRAM -------------------------------------------------------------------------------------------------
import sys
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
from figure2wall import figure2wall #data immagine mappa restituisce le cordinate delle pareti in coordinate pixel
from create_robot_4dof_tipoA import create_robot_4dof_tipoA #scrive il codice del robot sul file xml e crea modello completo
from createEnvironmentEncoding1 import createEnvironmentEncoding1
from PIL import Image
from xml.dom import minidom

x_meter_side=float(sys.argv[7]) # [m]                   #larghezza massima stanza
span_meter=float(sys.argv[6])  # [m]                     #distanza fra gli stati
velocity_average=1 # [m/s]             #velocità media/sicura di movimento
ktime=int(sys.argv[8])
tstay=5*ktime #[s]   #tempo comando stay


#TEMPI AZIONI - se si fanno modifiche cambiare anche altro script
tactionA=60*ktime #[s]
tactionB=20*ktime #[s]
tactionC=30*ktime #[s]
tactionD=40*ktime #[s]
diameter_footprint=0.30 # [m]

tmove=int(span_meter/velocity_average*ktime)  # tempo di movimento tra due stati consecutivi in base a velocità e span

initstate=sys.argv[3].split(',')

#points of interest
poi=sys.argv[4].split('@') #x1,y1;x2,y2

pointarray=list()

#creation poi array
for i in range(0,len(poi)):
    values=poi[i].split(',')
    x=float(values[0])
    y=float(values[1])
    print("x = ",x)
    print("y = ",y)
    pointarray.append([x,y])
     
dec=""

print("TIME: tmove="+str(tmove)+"tstay="+str(tstay))


for i in range(0,len(poi)):
    dec=dec+"int P"+str(i+1)+"=0; int visitedP"+str(i+1)+"=0; "

nta = Element ("nta")

declaration = SubElement(nta,"declaration").text = "chan r,l,u,d,s; int tmove=%d; int tstay=%d; int tactionA=%d; int tactionB=%d; int tactionC=%d; int tactionD=%d; clock x; clock t; int flagactionA=0; int flagactionB=0; int flagactionC=0; int flagactionD=0; int task1completed=0; int task2completed=0; %s" % (tmove,tstay,tactionA,tactionB,tactionC,tactionD,dec) 


createEnvironmentEncoding1(nta, initstate, pointarray, x_meter_side, span_meter, diameter_footprint)
create_robot_4dof_tipoA(nta, tmove) #if(tipoA)


#UPPAAL SYSTEM
system = SubElement(nta,"system").text = "Room1=Room(); Robot1=Robot(); system Robot1, Room1;"

tree = ElementTree(nta)

a=ET.tostring(nta)
b=minidom.parseString(ET.tostring(nta)).toprettyxml()
 
with open(sys.argv[2], "w") as f:
    f.write(b)

print("END process")



