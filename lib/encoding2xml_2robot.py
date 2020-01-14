import sys;
sys.path.insert(0, '../')
from  createEnc2_2robot import createEnc2_2robot
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
from  figure2wall import figure2wall
from  create_robot1_4dof_tipoA import create_robot1_4dof_tipoA
from  create_robot2_4dof_tipoA import create_robot2_4dof_tipoA
from PIL import Image
from xml.dom import minidom

x_meter_side=float(sys.argv[7])
span_meter=float(sys.argv[6])
velocity_average=1
ktime=int(sys.argv[8])
tstay=5*ktime
diameter_footprint=0.30
tmove=int(span_meter/velocity_average*ktime)
initstate=sys.argv[3].split(',')
poi=sys.argv[4].split('@')
pointarray=list()
for i in range(0,len(poi)):
    values=poi[i].split(',')
    x=float(values[0])
    y=float(values[1])
    print("x = ",x)
    print("y = ",y)
    pointarray.append([x,y])

print("TIME: tmove="+str(tmove)+"tstay="+str(tstay))

dec=""
for i in range(0,len(poi)):
    dec=dec+"int P"+str(i+1)+"; int visitedP"+str(i+1)+"; "

dec=dec+"int P5=0; int P6=0; "

#TEMPI AZIONI
tactionA=10*ktime #[s]
tactionB=15*ktime #[s]
tactionC=8*ktime #[s]
tactionD=13*ktime #[s]

nta = Element ("nta")

declaration = SubElement(nta,"declaration").text = "chan r1,l1,u1,d1,s1,r2,l2,u2,d2,s2,start_loading,end_loading,start_unloading,end_unloading; int Loaded=0; int tmove=%d; int tstay=%d;int tload1=10; int tunload1=15; int tactionA=%d; int tactionB=%d; int tactionC=%d; int tactionD=%d; clock x; clock t1; clock t2; int flagactionA=0; int flagactionC=0; int flagactionB=0; int flagactionD=0;int workcompleted=0; int task1completed=0; int task2completed=0; %s" % (tmove,tstay,tactionA,tactionB,tactionC,tactionD,dec)
createEnc2_2robot (nta, initstate, pointarray, x_meter_side, span_meter, diameter_footprint)
create_robot1_4dof_tipoA(nta, tmove)
create_robot2_4dof_tipoA(nta, tmove)
system = SubElement(nta,"system").text = "Room1=Room(); R1=Robot1(); R2=Robot2(); system R1, R2, Room1;"

tree = ElementTree(nta)
a=ET.tostring(nta)
b=minidom.parseString(ET.tostring(nta)).toprettyxml()

with open(sys.argv[2], "w") as f:
    f.write(b)

print("END process")
