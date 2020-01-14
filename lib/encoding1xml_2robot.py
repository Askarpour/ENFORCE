# -*- coding: utf-8 -*-

#Dato numero di righe e colonne il programma crea un file xml che descrive la mappa della stanza
#per il robot a 4 gradi di libertà (su,giù,destra,sinistra)
#il file generato si può aprire direttamente in Uppaal





#-------------- FUNCTIONS ---------------
def isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1x>sourcePointx and p1x<(destinationPointx+radius) and p1y>destinationPointy-radius and p1y<(sourcePointy+radius)):
                return True
    return False
def isThereVerticalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1x<sourcePointx and p1x>(destinationPointx-radius) and p1y>destinationPointy-radius and p1y<(sourcePointy+radius)):
                return True
    return False
def isThereHorizontalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1y>sourcePointy and p1y<(destinationPointy+radius) and p1x>destinationPointx-radius and p1x<(sourcePointx+radius)):
                return True
    return False
def isThereHorizontalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1y<sourcePointy and p1y>(destinationPointy-radius) and p1x>destinationPointx-radius and p1x<(sourcePointx+radius)):
                return True
    return False
#-------------- PROGRAM -------------------------------------------------------------------------------------------------

import xml.etree.cElementTree as ET
from figure2wall_2robot import figure2wall_2robot #data immagine mappa restituisce le cordinate delle pareti in coordinate pixel
from create_robot1_4dof_tipoA import create_robot1_4dof_tipoA #scrive il codice del robot sul file xml e crea modello completo
from create_robot2_4dof_tipoA import create_robot2_4dof_tipoA
import numpy as np
import cv2
from PIL import Image
import sys


(wallx, wally)=figure2wall_2robot('JupiterImg.png') # importare immagine mappa
im=Image.open('JupiterImg.png')
im=Image.open('JupiterImg.png')


x_meter_side=60 # [m]                   #larghezza massima stanza
span_meter=1  # [m]                     #distanza fra gli stati
velocity_average=1 # [m/s]              #velocità media/sicura di movimento
tstay=5 #[s]                            #tempo comando stay
diameter_footprint=0.10 # [m]

# x orizzontale, y verticale
loadingp1_x=15
loadingp1_y=5
loadingp2_x=15
loadingp2_y=4
print("Loading point Robot1 = ("+str(loadingp1_y)+","+str(loadingp1_x)+")")
print("Loading point Robot2 = ("+str(loadingp2_y)+","+str(loadingp2_x)+")")


#########################################################################
#########################################################################


pix=im.load()
rgb_im = im.convert('RGB')
minx=0                     
maxx=im.size[0]
miny=0
maxy=im.size[1]


#SECONDARY PARAMETERS
#minx=min(wallx)                         #servono per trovare l'ultimo punto in basso a destra nella mappa
#maxx=max(wallx)
#miny=min(wally)
#maxy=max(wally)
scale=(maxx-minx)/x_meter_side          # 1 metro = scale pixels
tmove=int(span_meter/velocity_average)  # tempo di movimento tra due stati consecutivi in base a velocità e span
diameter=diameter_footprint*scale       # diametro convertito in pixels                                      
radius=diameter/2
x_meter_max=maxx/scale # coordinate in metri dell' ultimo punto in basso a destra
y_meter_max=maxy/scale
factor=scale*span_meter


print("INPUT:")
print("side=",x_meter_side)
print("span=",span_meter)
print("diameter=",diameter_footprint)
print("TIME:")
print("tmove=",tmove)
print("tstay=",tstay)

#rows=int(y_meter_max/span_meter)+int(0.2*(y_meter_max/span_meter)) # creo righe e colonne dall'origine fino all'ultimo punto in basso a destra, + un margine del 20% per il disegno in uppaal
#columns=int(x_meter_max/span_meter)+int(0.2*(x_meter_max/span_meter))


rows=int(y_meter_max/span_meter)
columns=int(x_meter_max/span_meter)

print("GEOMETRY:")
print("rows=",rows)
print("columns=",columns)
counter1 = range(0,rows)  
counter2 = range(0,columns)
print("writing ROOM XML file")

#ROOM XML 
nta = ET.Element ("nta")
declaration = ET.SubElement(nta,"declaration").text = "chan r1,l1,u1,d1,s1,r2,l2,u2,d2,s2,start_loading,end_loading; clock t; clock t1; clock t2; int x1=3; int y1=3; int x2=3; int y2=8; int tmove=%d; int tstay=%d; int tload1=10; int P1=0; int P2=0; int Loaded=0;" % (tmove,tstay) #clock x;

##### ENVIRONMENT1 #####
template = ET.SubElement(nta,"template")
name = ET.SubElement(template,"name").text = "Environment1"

pix=im.load()
rgb_im = im.convert('RGB')


#STATES
for counta in counter1:
    for countb in counter2:
        r, g, b = rgb_im.getpixel((countb*factor, counta*factor)) 
        if not (r==0 and g==0 and b==0): #if point not black
            location = ET.SubElement(template,"location",id="id%d-%d" % (counta,countb),x="%d" % (countb*100),y="%d" %(counta*100))
            name=ET.SubElement(location,"name").text = "id%dI%d" % (counta,countb)
        
        
        
        
        
#INITIAL STATE
init = ET.SubElement(template,"init",ref="id3-3") #INITIAL STATE E1                              <---------- settare initial state, qui, nelle declarations e anche nell'environment2
#TRANSITIONS
print("Process status Robot1:")

#right
print("1/5")
for counta in counter1:
    for countb in counter2:
        #moltiplicando per scale E PER LO SPAN abbiamo una corrispondenza tra sorce/target e le coordinate dei muri
        sourcePointx=countb*factor
        sourcePointy=counta*factor
        destinationPointx=(countb+1)*factor
        destinationPointy=counta*factor
        if not isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb+1))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "r1?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not ( (x2==x1+1) and (y2==y1)) )"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
            if(((countb+1)==loadingp1_x and (counta)==loadingp1_y)or((countb)==loadingp1_x and (counta)==loadingp1_y)):
                if( (countb+1)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=1, x1=x1+1"
                if( (countb)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=0, x1=x1+1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "x1=x1+1"
                
#left
print("2/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb+1)*factor
        sourcePointy=counta*factor
        destinationPointx=(countb)*factor
        destinationPointy=counta*factor
        if not isThereVerticalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb+1))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "l1?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not ( (x2==x1-1) and (y2==y1)) )"
            if(  ((countb)==loadingp1_x and (counta)==loadingp1_y)  or  ((countb+1)==loadingp1_x and (counta)==loadingp1_y)  ):
                if( (countb)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=1, x1=x1-1"
                if( (countb+1)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=0, x1=x1-1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "x1=x1-1"

                
                
#down
print("3/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb)*factor
        sourcePointy=counta*factor
        destinationPointx=(countb)*factor
        destinationPointy=(counta+1)*factor
        if not isThereHorizontalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta+1,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "d1?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not ( (y2==y1+1) and (x2==x1)) )"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
            if(  ((countb)==loadingp1_x and (counta+1)==loadingp1_y) or ((countb)==loadingp1_x and (counta)==loadingp1_y)   ):
                if( (countb)==loadingp1_x and (counta+1)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=1, y1=y1+1"
                if( (countb)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=0, y1=y1+1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "y1=y1+1"
                    
#up
print("4/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb)*factor
        sourcePointy=(counta+1)*factor
        destinationPointx=(countb)*factor
        destinationPointy=counta*factor
        if not isThereHorizontalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta+1,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "u1?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not ( (y2==y1-1) and (x2==x1)) )"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
            if(  ((countb)==loadingp1_x and (counta)==loadingp1_y)  or  ((countb)==loadingp1_x and (counta+1)==loadingp1_y)  ):
                if( (countb)==loadingp1_x and (counta)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=1, y1=y1-1"
                if( (countb)==loadingp1_x and (counta+1)==loadingp1_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P1=0, y1=y1-1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "y1=y1-1"
                
                
#stay
print("5/5")
for counta in counter1:
    for countb in counter2:
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "s1?"
            #label = ET.SubElement(transition,"label",kind="guard").text = "CONDIZIONE"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tstay"



##### ENVIRONMENT2 #####
template = ET.SubElement(nta,"template")
name = ET.SubElement(template,"name").text = "Environment2"

#STATES
for counta in counter1:
    for countb in counter2:
        r, g, b = rgb_im.getpixel((countb*factor, counta*factor)) 
        if not (r==0 and g==0 and b==0): #if point not black
            location = ET.SubElement(template,"location",id="id%d-%d" % (counta,countb),x="%d" % (countb*100),y="%d" %(counta*100))
            name=ET.SubElement(location,"name").text = "id%dI%d" % (counta,countb)

        #INITIAL STATE
init = ET.SubElement(template,"init",ref="id8-3")#INITIAL STATE E2                              <---------------------------- init
#TRANSITIONS
factor=scale*span_meter
print("Process status Robot2:")
#right
print("1/5")
for counta in counter1:
    for countb in counter2:
        #moltiplicando per scale E PER LO SPAN abbiamo una corrispondenza tra sorce/target e le coordinate dei muri
        sourcePointx=countb*factor
        sourcePointy=counta*factor
        destinationPointx=(countb+1)*factor
        destinationPointy=counta*factor
        if not isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb+1))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "r2?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not( (x1==x2+1) and (y1==y2) ))"
            if(  ((countb+1)==loadingp2_x and (counta)==loadingp2_y)  or  ((countb)==loadingp2_x and (counta)==loadingp2_y)  ):
                if( (countb+1)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=1, x2=x2+1"
                if( (countb)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=0, x2=x2+1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "x2=x2+1"
                
                
                
            
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
#left
print("2/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb+1)*factor
        sourcePointy=counta*factor
        destinationPointx=(countb)*factor
        destinationPointy=counta*factor
        if not isThereVerticalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb+1))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "l2?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not( (x1==x2-1) and (y1==y2) ))"
            if(  ((countb)==loadingp2_x and (counta)==loadingp2_y)  or  ((countb+1)==loadingp2_x and (counta)==loadingp2_y)  ):
                if( (countb)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=1, x2=x2-1"
                if( (countb+1)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=0, x2=x2-1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "x2=x2-1"
                
                
            #label = ET.SubElement(transition,"label",kind="guard").text = "CONDIZIONE"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
#down
print("3/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb)*factor
        sourcePointy=counta*factor
        destinationPointx=(countb)*factor
        destinationPointy=(counta+1)*factor
        if not isThereHorizontalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta+1,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "d2?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not( (y1==y2+1) and (x1==x2) ))"
            if(  ((countb)==loadingp2_x and (counta+1)==loadingp2_y)  or  ((countb)==loadingp2_x and (counta)==loadingp2_y)  ):
                if( (countb)==loadingp2_x and (counta+1)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=1, y2=y2+1"
                if( (countb)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=0, y2=y2+1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "y2=y2+1"
                
                
            #label = ET.SubElement(transition,"label",kind="guard").text = "CONDIZIONE"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
#up
print("4/5")
for counta in counter1:
    for countb in counter2:
        sourcePointx=(countb)*factor
        sourcePointy=(counta+1)*factor
        destinationPointx=(countb)*factor
        destinationPointy=counta*factor
        if not isThereHorizontalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta+1,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "u2?"
            label = ET.SubElement(transition,"label",kind="guard").text = "(not( (y1==y2-1) and (x1==x2) ))"
            if(  ((countb)==loadingp2_x and (counta)==loadingp2_y) or ((countb)==loadingp2_x and (counta+1)==loadingp2_y)  ):
                if( (countb)==loadingp2_x and (counta)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=1, y2=y2-1"
                if( (countb)==loadingp2_x and (counta+1)==loadingp2_y ):
                    label = ET.SubElement(transition,"label",kind="assignment").text = "P2=0, y2=y2-1"
            else:
                label = ET.SubElement(transition,"label",kind="assignment").text = "y2=y2-1"
                
            #label = ET.SubElement(transition,"label",kind="guard").text = "CONDIZIONE"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tmove"
#stay
print("5/5")
for counta in counter1:
    for countb in counter2:
            transition = ET.SubElement(template,"transition")
            source = ET.SubElement(transition,"source",ref="id%d-%d" % (counta,countb))
            target = ET.SubElement(transition,"target",ref="id%d-%d" % (counta,countb))
            label = ET.SubElement(transition,"label",kind="synchronisation").text = "s2?"
            #label = ET.SubElement(transition,"label",kind="guard").text = "CONDIZIONE"
            #label = ET.SubElement(transition,"label",kind="assignment").text = "t=t+tstay"



#ROBOT XML
create_robot1_4dof_tipoA(nta,tmove)
create_robot2_4dof_tipoA(nta,tmove)

#UPPAAL SYSTEM
system = ET.SubElement(nta,"system").text = "E1=Environment1(); E2=Environment2(); R1=Robot1(); R2=Robot2(); system R1, R2, E1, E2;"

tree = ET.ElementTree(nta)
tree.write("Output_XML_2Robot.xml")


print("END process")



