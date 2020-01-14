# coding=<encoding name>
# coding=utf-8
#-------------- FUNCTIONS ---------------
def isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter, factor, radius):
    ret=[0, 0, 0, 0]
    for p1x in wallx.keys():
        if (p1x>(destinationPointx*factor-radius) and p1x<((destinationPointx+1)*factor+radius)):
            for p1y in wallx[p1x]:
                # right
                if(p1x>(sourcePointx*factor) and p1x<((destinationPointx+1)*factor+radius) and p1y>destinationPointy*factor-radius and p1y<(sourcePointy*factor+radius)):
                        ret[0]=1
                # left
                if(p1x<((sourcePointx+1)*factor) and p1x>(destinationPointx*factor-radius) and p1y>destinationPointy*factor-radius and p1y<(sourcePointy*factor+radius)):
                        ret[1]=1
    for p1y in wally.keys():
        if (p1y>(destinationPointy*factor-radius) and p1y<((destinationPointy+1)*factor+radius)):
            for p1x in wally[p1y]:
               # up
                if(p1y>sourcePointy*factor and p1y<((destinationPointy+1)*factor+radius) and p1x>destinationPointx*factor-radius and p1x<(sourcePointx*factor+radius)):
                        ret[2]=1
                #down
                if(p1y<(sourcePointy+1)*factor and p1y>(destinationPointy*factor-radius) and p1x>destinationPointx*factor-radius and p1x<(sourcePointx*factor+radius)):
                        ret[3]=1
    return ret

def isPOI(point1Xpixel,point1Ypixel,point2Xpixel,point2Ypixel, factor):
    if abs(point1Xpixel-point2Xpixel)<=(factor/2) and abs(point1Ypixel-point2Ypixel)<=(factor/2):
        return True
    return False

def getPoi(a,b,pointarray, factor):
    setpoi=-1
    index=1
    for point in pointarray:
        #print(point)
        x=point[0]
        y=point[1]
        if isPOI(x, y,b*factor, a*factor, factor):
            print("Poi: id"+str(b)+"I"+str(a))
            setpoi=index
        index=index+1
    return setpoi


import sys
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import numpy as np
from figure2wall import figure2wall #data immagine mappa restituisce le cordinate delle pareti in coordinate pixel
from create_robot_4dof_tipoA import create_robot_4dof_tipoA #scrive il codice del robot sul file xml e crea modello completo
from PIL import Image

def createEnvironmentEncoding1(nta, initstate, pointarray, x_meter_side, span_meter, diameter_footprint):

    (wallx, wally)=figure2wall(sys.argv[1]) # importare immagine mappa

    im=Image.open(sys.argv[1])
    pix=im.load()
    rgb_im = im.convert('RGB')

    minx=0
    maxx=im.size[0]
    miny=0
    maxy=im.size[1]

    scale=(maxx-minx)/x_meter_side          # pixel for meter [px/m]
    factor=scale*span_meter                 # distance in pixel between states [px/state]
    diameter=diameter_footprint*scale       # diametro convertito in pixels
    radius=diameter/2
    x_meter_max=maxx/scale                  # coordinate in metri dell' ultimo punto in basso a destra
    y_meter_max=maxy/scale

    print("Image size:")
    print(im.size)
    template = SubElement(nta,"template")
    name = SubElement(template,"name").text = "Room"

    rows=int(y_meter_max/span_meter)
    columns=int(x_meter_max/span_meter)
    print("GEOMETRY:")
    print("rows=",rows)
    print("columns=",columns)

    counter1 = range(0,rows)
    counter2 = range(0,columns)

    print("writing ROOM XML file")

    initstatestring=""
    mapnameid={}
    countainit=0
    countbinit=0
    idcount=20
    #STATES
    for counta in counter1:
        for countb in counter2:

            if abs((counta*factor-float(initstate[1])))<factor and abs(countb*factor-float(initstate[0]))<factor:
                    initstatestring="id"+str(idcount)
                    countainit=counta
                    countbinit=countb

            r, g, b = rgb_im.getpixel((countb*factor, counta*factor)) #perchè non c' è ET.sub...
            if not (r==0 and g==0 and b==0):
                location = SubElement(template,"location",id="id%d" %(idcount),x="%d" % (countb*100),y="%d" %(counta*100))
                name=SubElement(location,"name").text = "id%dI%d" % (counta,countb)

                mapnameid["id"+str(counta)+"I"+str(countb)]=idcount
                idcount=idcount+1

    print("Initial state: "+str(countainit)+","+str(countbinit))
    print("Initial state: "+initstatestring)
    #INITIAL STATE

    init = SubElement(template,"init",ref="id%d" % mapnameid["id"+str(countainit)+"I"+str(countbinit)])

    counter1trans = range(0,rows-1)
    counter2trans = range(0,columns-1)

    #TRANSITIONS
    print("Process status:")
    for counta in counter1trans:
        for countb in counter2trans:
            r, g, b = rgb_im.getpixel((countb*factor, counta*factor))

            if not (r==0 and g==0 and b==0):      #se il punto corrente non è nero
                sourcePointx=countb
                sourcePointy=counta
                destinationPointx=countb
                destinationPointy=counta

                ret=isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter, factor, radius)

#horizontal, left to right
                if not ret[0]==1:
                    r, g, b = rgb_im.getpixel(((countb+1)*factor, counta*factor))
                    if not (r==0 and g==0 and b==0):                                #non cercare nel vuoto
                        setpoi=getPoi(counta,countb+1,pointarray, factor)
                        transition = SubElement(template,"transition")
                        source = SubElement(transition,"source",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                        target = SubElement(transition,"target",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb+1)])
                        label = SubElement(transition,"label",kind="synchronisation").text = "r?"
                        if not (setpoi == (-1)):
                            label = SubElement(transition,"label",kind="assignment").text = "P%d=1, visitedP%d=1" %(setpoi,setpoi)
                        point=getPoi(counta,countb,pointarray, factor)
                        if (setpoi==(-1) and not point==-1):
                            label = SubElement(transition,"label",kind="assignment").text = "P%d=0" %(point)

#horizontal, right to left
                if not ret[1]==1:
                    r, g, b = rgb_im.getpixel(((countb+1)*factor, counta*factor))
                    if not (r==0 and g==0 and b==0):
                        setpoi=getPoi(counta,countb,pointarray, factor)
                        transition = SubElement(template,"transition")
                        source = SubElement(transition,"source",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb+1)])
                        target = SubElement(transition,"target",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                        label = SubElement(transition,"label",kind="synchronisation").text = "l?"
                        if not (setpoi == (-1)):
                            label = SubElement(transition,"label",kind="assignment").text = "P%d=1, visitedP%d=1" %(setpoi,setpoi)
                        point=getPoi(counta,countb+1,pointarray, factor)
                        if setpoi==(-1) and not point==-1:
                             label = SubElement(transition,"label",kind="assignment").text = "P%d=0" %(point)
#vertical, up to down
                if not ret[2]==1:
                    r, g, b = rgb_im.getpixel(((countb)*factor, (counta+1)*factor))
                    if not (r==0 and g==0 and b==0):
                        setpoi=getPoi(counta+1,countb,pointarray, factor)
                        transition = SubElement(template,"transition")
                        source = SubElement(transition,"source",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                        target = SubElement(transition,"target",ref="id%d" % mapnameid["id"+str(counta+1)+"I"+str(countb)])
                        label = SubElement(transition,"label",kind="synchronisation").text = "d?"
                        if not (setpoi == (-1)):
                                label = SubElement(transition,"label",kind="assignment").text = "P%d=1, visitedP%d=1" %(setpoi,setpoi)
                        point=getPoi(counta,countb,pointarray, factor)
                        if setpoi==(-1) and not point==-1:
                                label = SubElement(transition,"label",kind="assignment").text = "P%d=0" %(point)
#vertical, down to up
                if not ret[3]==1:
                    r, g, b = rgb_im.getpixel(((countb)*factor, (counta+1)*factor))
                    if not (r==0 and g==0 and b==0):
                        setpoi=getPoi(counta,countb,pointarray, factor)
                        transition = SubElement(template,"transition")
                        source = SubElement(transition,"source",ref="id%d" % mapnameid["id"+str(counta+1)+"I"+str(countb)])
                        target = SubElement(transition,"target",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                        label = SubElement(transition,"label",kind="synchronisation").text = "u?"
                        if not (setpoi == (-1)):
                            label = SubElement(transition,"label",kind="assignment").text = "P%d=1, visitedP%d=1" %(setpoi,setpoi)
                        point=getPoi(counta+1,countb,pointarray, factor)
                        if setpoi==(-1) and not point==-1:
                             label = SubElement(transition,"label",kind="assignment").text = "P%d=0" %(point)
# stay
                r, g, b = rgb_im.getpixel(((countb)*factor, counta*factor))
                if not (r==0 and g==0 and b==0):
                    transition = SubElement(template,"transition")
                    source = SubElement(transition,"source",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                    target = SubElement(transition,"target",ref="id%d" % mapnameid["id"+str(counta)+"I"+str(countb)])
                    label = SubElement(transition,"label",kind="synchronisation").text = "s?"


        if (100*counta/len(counter1))%5==0:
            print(str(100*counta/len(counter1))+'%')
