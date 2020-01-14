
# -*- coding: utf-8 -*-

#P2 aggiungere transizione come P1
#FLAG PASSAGGIO aggiungere assegnamento e nuova variabile, no nuova transizione

#FUNZIONA MOLTO BENE CON PARETI PERPENDICOLARI (orizzontali/verticali), in caso contrario dovrebbe funzionare
#comunque considerando i punti singoli e guardie molto lunghe

#-------------- FUNCTIONS ---------------
def isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        radius=diameter/2
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1x>sourcePointx and p1x<(destinationPointx+radius) and p1y>destinationPointy-radius and p1y<(sourcePointy+radius)):
                return True
    return False
def isThereVerticalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        radius=diameter/2
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1x<sourcePointx and p1x>(destinationPointx-radius) and p1y>destinationPointy-radius and p1y<(sourcePointy+radius)):
                return True
    return False
def isThereHorizontalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        radius=diameter/2
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1y>sourcePointy and p1y<(destinationPointy+radius) and p1x>destinationPointx-radius and p1x<(sourcePointx+radius)):
                return True
    return False
def isThereHorizontalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
    for position1 in range(0, len(wallx)):
        radius=diameter/2
        p1x=wallx[position1]
        p1y=wally[position1]
        if(p1y<sourcePointy and p1y>(destinationPointy-radius) and p1x>destinationPointx-radius and p1x<(sourcePointx+radius)):
                return True
    return False

#-------------- PROGRAM -------------------------------------------------------------------------------------------------

import xml.etree.cElementTree as ET
from figure2wall_2robot import figure2wall_2robot #data immagine mappa restituisce le cordinate delle pareti in coordinate pixel
#from create_robot1_4dof_tipoA import create_robot1_4dof_tipoA #scrive il codice del robot sul file xml e crea modello completo
#from create_robot2_4dof_tipoA import create_robot2_4dof_tipoA
import numpy as np
import cv2
import sys
import xml.etree.cElementTree as ET
from figure2wall import figure2wall #data immagine mappa restituisce le cordinate delle pareti in coordinate pixel
from create_robot_4dof_tipoA import create_robot_4dof_tipoA #scrive il codice del robot sul file xml e crea modello completo
import numpy as np
import cv2
from PIL import Image
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def createEnvironmentEncoding2(nta, initstate, pointarray, x_meter_side, span_meter, diameter_footprint):
    #
    #
    # PERCHè CON figure2wall_2robot FUNZIONA MENTRE CON figure2wall NO?
    (wallx,wally)=figure2wall_2robot(sys.argv[1])
    #
    #

    im=Image.open(sys.argv[1])
    pix=im.load()
    rgb_im = im.convert('RGB')
    minx=0
    maxx=im.size[0]
    miny=0
    maxy=im.size[1]

    scale=(maxx-minx)/x_meter_side          # 1 metro = scale pixels
    factor=scale*span_meter
    diameter=diameter_footprint*scale       # diametro convertito in pixels
    radius=diameter/2
    x_meter_max=maxx/scale # coordinate in metri dell' ultimo punto in basso a destra
    y_meter_max=maxy/scale

    print("Image size:")
    print(im.size)

    rows=int(y_meter_max/span_meter)
    columns=int(x_meter_max/span_meter)

    print("GEOMETRY _ 2task:")
    print("equivalent rows=",rows)
    print("equivalent columns=",columns)

    counter1 = range(0,rows)
    counter2 = range(0,columns)

    print("writing ROOM XML file")

    template = SubElement(nta,"template")
    name = SubElement(template,"name").text = "Room" #chiamare il template environment oppure room?

    #INITIAL STATE
    #initial coordinates trasformation from pixel to idcoord
    for counta in counter1:
        for countb in counter2:
            if abs((counta*factor-float(initstate[1])))<factor and abs(countb*factor-float(initstate[0]))<factor:
                    initialy=counta
                    initialx=countb

    print("initial start ="+str(initialx)+","+str(initialy))

    declaration = SubElement(template,"declaration").text = "int x=%d,y=%d,factor=%d;" % (initialx,initialy,factor) #initial coordinates

    location = SubElement(template,"location",id="init")
    init = SubElement(template,"init",ref="init")


    #trasformazione array poi da pixel a ID
    for point in pointarray:
        for counta in counter1:
            for countb in counter2:
                if abs((counta*factor-float(point[1])))<factor and abs(countb*factor-float(point[0]))<factor:
                        point[1]=counta
                        point[0]=countb

    #gli stati sono espressi in xy discretizzati, se vado a destra stato x+1

    print ("POI: ",pointarray)
    lpoi=len(pointarray)

    # dichiarazione stringhe-guardie-poi ATTENZIONE !!!! le stringhe iniziano da zero mentre i poi da P1
    poilist = []
    for i in range (0,lpoi):
        poilist.append([])
        # print (poilist[i])

    #TRANSITIONS
    print("Process status Robot1:")

    #RIGHT                        # è possibile ottimizzare usando un solo ciclo for?
    print("--------------- 1/5")
    wallguard=""
    firstguard=True
    poi=""
    firstpoi=True
    murox = []
    muroy = []
    guardy = []
    guardx = []

    #voglio i muri verticali e array delle y ordinato, qui inverto ciclo, prima sulle colonne
    #murox,mury sono simili a wallx,wally ma in "coordinate id" e ordinate in base a muro verticale o orizzontale
    #guardx,guardy salvano solo gli estremi del muro SEPARATI DA UNO ZERO
    # 0,12,20,0,25,33,0,40,40,0
    #considera anche i punti singoli
    #da qui scriviamo le guardie con maggiore-minore evitando di scrivere tutti i punti
    #molto prob computazione lunga da ottimizzare ma dovrebbe essere meglio per uppaal

    #left e up diversi perchè hanno il source+1
    #ciclo esterno sulle colonne/righe per ordinare i punti del muro in base a muro verticale/orizzontale

    for countb in counter2: #cicla prima sulle colonne
        for counta in counter1:
            r, g, b = rgb_im.getpixel((countb*factor, counta*factor))
            if not (r==0 and g==0 and b==0): #if point not black
                sourcePointx=countb*factor
                sourcePointy=counta*factor
                destinationPointx=(countb+1)*factor
                destinationPointy=counta*factor

    #per ogni poi viene creata la relativa guardia, numero transizioni per ogni direzione = numero poi +1
                for i in range (0,lpoi):
                    if( (countb+1)==pointarray[i][0] and (counta)==pointarray[i][1] ): # poi guard
                        poilist[i]="(((x==%d) and (y==%d)))" % (countb,counta) # quando settiamo Pi = 1
                        if firstpoi==True:
                            firstpoi=False
                            poiguard="(((x==%d) and (y==%d)))" % (countb,counta) # quando non entriamo in un poi mettiamo P1,P2,P3=0 - da usare una volta per ogni direzione
                        else:
                            poiguard=poiguard+" or (((x==%d) and (y==%d)))" % (countb,counta)

                if isThereVerticalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
                    murox.append(countb)
                    muroy.append(counta)
        if(countb%5==0):
                print("   "+str(countb)+"/"+str(columns))

    murox.append(0)
    muroy.append(0)

    lenghtmy=len(muroy)-1
    for i in range(0,lenghtmy):
        ay=muroy[i]
        by=muroy[i+1]
        ax=murox[i]
        bx=murox[i+1]
        if ((muroy[i]+1) != (muroy[i+1])):
            guardy.append(ay)
            guardy.append(0)
            guardy.append(by)
            guardx.append(ax)
            guardx.append(0)
            guardx.append(bx)

    guardx.append(0)
    guardy.append(0)

    lenghtguardy=len(guardy)-3
    for i in range(0,lenghtguardy):
        if(guardy[i]==0 and guardy[i+1]!=0):
            if firstguard==True:
                firstguard=False
                #per alleggerire le guardie, se il punto è isolato mettiamo vincolo sulla coordinata altrimenti consideriamo l'intervallo
                if(guardy[i+1]==guardy[i+2]):
                    wallguard="(not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard="(not((y>=%d) and (y<=%d) and (x==%d)))" % (guardy[i+1],guardy[i+2],guardx[i+1])

            else:
                if(guardy[i+1]==guardy[i+2]):
                    wallguard=wallguard+"and (not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard=wallguard+"and (not((y>=%d) and (y<=%d) and (x==%d)))" % (guardy[i+1],guardy[i+2],guardx[i+1])

    i = 0
    for p in poilist:

        transition = SubElement(template,"transition")
        source = SubElement(transition,"source",ref="init")
        target = SubElement(transition,"target",ref="init")
        label = SubElement(transition,"label",kind="guard").text ="( "+p+" ) and ("+ wallguard+")"
        label = SubElement(transition,"label",kind="synchronisation").text = "r?"
        label = SubElement(transition,"label",kind="assignment").text = "P%s=1,x=x+1"%i
        i += 1

    #NO POI
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="init")
    target = SubElement(transition,"target",ref="init")
    label = SubElement(transition,"label",kind="guard").text = "( not ("+poiguard+") ) and ("+wallguard+")"
    label = SubElement(transition,"label",kind="synchronisation").text = "r?"
    label = SubElement(transition,"label",kind="assignment").text = "P1=0, P2=0, P3=0,P4=0,P5=0, x=x+1"
#---------------------------------------------------------------------------------------------------------------------------
    #LEFT
    print("--------------- 2/5")
    wallguard=""
    firstguard=True
    poi=""
    firstpoi=True
    murox = []
    muroy = []
    guardy = []
    guardx = []

    counterBBBB = range(0,columns-1)

    for countb in counterBBBB: #cicla prima sulle colonne
        for counta in counter1:
            r, g, b = rgb_im.getpixel(((countb+1)*factor, counta*factor))  #source non nero? attenzione che i poi sono i target a sinistra - in down è diveroo?
            if not (r==0 and g==0 and b==0):
                sourcePointx=(countb+1)*factor
                sourcePointy=counta*factor
                destinationPointx=(countb)*factor
                destinationPointy=counta*factor

                for i in range (0,lpoi):
                    #se il target è un poi
                    if( (countb)==pointarray[i][0] and (counta)==pointarray[i][1] ):
                        poilist[i]="(((x==%d) and (y==%d)))" % (countb+1,counta) # quando settiamo Pi = 1
                        if firstpoi==True:
                            firstpoi=False
                            #serve per il caso in cui non entriamo in nessun poi
                            poiguard="(((x==%d) and (y==%d)))" % (countb+1,counta) # quando non entriamo in un poi mettiamo P1,P2,P3=0 - da usare una volta per ogni direzione
                        else:
                            poiguard=poiguard+" or (((x==%d) and (y==%d)))" % (countb+1,counta)

                #if there is a wall
                if isThereVerticalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):  # if there is a wall
                    b=countb+1 #considero il source
                    murox.append(b)
                    muroy.append(counta)
        if(countb%5==0):
                print("   "+str(countb)+"/"+str(columns))

    murox.append(0)
    muroy.append(0)

    lenghtmy=len(muroy)-1
    for i in range(0,lenghtmy):
        ay=muroy[i]
        by=muroy[i+1]
        ax=murox[i]
        bx=murox[i+1]
        if ((muroy[i]+1) != (muroy[i+1])):
            guardy.append(ay)
            guardy.append(0)
            guardy.append(by)
            guardx.append(ax)
            guardx.append(0)
            guardx.append(bx)

    guardx.append(0)
    guardy.append(0)

    lenghtguardy=len(guardy)-3
    for i in range(0,lenghtguardy):
        if(guardy[i]==0 and guardy[i+1]!=0):
            if firstguard==True:
                firstguard=False
                #per alleggerire le guardie, se il punto è isolato mettiamo vincolo sulla coordinata altrimenti consideriamo l'intervallo
                if(guardy[i+1]==guardy[i+2]):
                    wallguard="(not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard="(not((y>=%d) and (y<=%d) and (x==%d)))" % (guardy[i+1],guardy[i+2],guardx[i+1])

            else:
                if(guardy[i+1]==guardy[i+2]):
                    wallguard=wallguard+"and (not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard=wallguard+"and (not((y>=%d) and (y<=%d) and (x==%d)))" % (guardy[i+1],guardy[i+2],guardx[i+1])

    i = 0
    for p in poilist:

        transition = SubElement(template,"transition")
        source = SubElement(transition,"source",ref="init")
        target = SubElement(transition,"target",ref="init")
        label = SubElement(transition,"label",kind="guard").text ="( "+p+" ) and ("+ wallguard+")"
        label = SubElement(transition,"label",kind="synchronisation").text = "r?"
        label = SubElement(transition,"label",kind="assignment").text = "P%s=1,x=x+1"%i
        i += 1


    #NO POI
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="init")
    target = SubElement(transition,"target",ref="init")
    label = SubElement(transition,"label",kind="guard").text = "( not ("+poiguard+") ) and ("+wallguard+")"
    label = SubElement(transition,"label",kind="synchronisation").text = "l?"
    label = SubElement(transition,"label",kind="assignment").text = "P1=0,P2=0,P3=0,P4=0,P5=0,x=x-1"
#----------------------------------------------------------------------------------------------------------------------------------------
    #DOWN
    print("--------------- 3/5")
    wallguard=""
    firstguard=True
    poi=""
    firstpoi=True
    murox = []
    muroy = []
    guardy = []
    guardx = []
    for counta in counter1: #ciclo sulle righe
        for countb in counter2:
            r, g, b = rgb_im.getpixel((countb*factor, counta*factor))
            if not (r==0 and g==0 and b==0):
                sourcePointx=(countb)*factor
                sourcePointy=counta*factor
                destinationPointx=(countb)*factor
                destinationPointy=(counta+1)*factor

                for i in range (0,lpoi):
                    if( (countb)==pointarray[i][0] and (counta+1)==pointarray[i][1] ):
                        poilist[i]="(((x==%d) and (y==%d)))" % (countb,counta) # quando settiamo Pi = 1
                        if firstpoi==True:
                            firstpoi=False
                            poiguard="(((x==%d) and (y==%d)))" % (countb,counta) # quando non entriamo in un poi mettiamo P1,P2,P3=0 - da usare una volta per ogni direzione
                        else:
                            poiguard=poiguard+" or (((x==%d) and (y==%d)))" % (countb,counta)

                if isThereHorizontalWallA(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
                    murox.append(countb)
                    muroy.append(counta)
        if(counta%5==0):
            print("   "+str(counta)+"/"+str(rows))

    murox.append(0)
    muroy.append(0)

    lenghtmy=len(murox)-1
    for i in range(0,lenghtmy):
        ay=muroy[i]
        by=muroy[i+1]
        ax=murox[i]
        bx=murox[i+1]
        if ((murox[i]+1) != (murox[i+1])):
            guardy.append(ay)
            guardy.append(0)
            guardy.append(by)
            guardx.append(ax)
            guardx.append(0)
            guardx.append(bx)

    guardx.append(0)
    guardy.append(0)

    lenghtguardx=len(guardx)-3
    for i in range(0,lenghtguardx):
        if(guardx[i]==0 and guardx[i+1]!=0):
            if firstguard==True:
                firstguard=False
                #per alleggerire le guardie, se il punto è isolato mettiamo vincolo sulla coordinata altrimenti consideriamo l'intervallo
                if(guardx[i+1]==guardx[i+2]):
                    wallguard="(not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard="(not((x>=%d) and (x<=%d) and (y==%d)))" % (guardx[i+1],guardx[i+2],guardy[i+1])

            else:
                if(guardx[i+1]==guardx[i+2]):
                    wallguard=wallguard+"and (not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard=wallguard+"and (not((x>=%d) and (x<=%d) and (y==%d)))" % (guardx[i+1],guardx[i+2],guardy[i+1])

    i = 0
    for p in poilist:

        transition = SubElement(template,"transition")
        source = SubElement(transition,"source",ref="init")
        target = SubElement(transition,"target",ref="init")
        label = SubElement(transition,"label",kind="guard").text ="( "+p+" ) and ("+ wallguard+")"
        label = SubElement(transition,"label",kind="synchronisation").text = "r?"
        label = SubElement(transition,"label",kind="assignment").text = "P%s=1,y=y+1"%i
        i += 1


    #NO POI
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="init")
    target = SubElement(transition,"target",ref="init")
    label = SubElement(transition,"label",kind="guard").text = "( not ("+poiguard+") ) and ("+wallguard+")"
    label = SubElement(transition,"label",kind="synchronisation").text = "d?"
    label = SubElement(transition,"label",kind="assignment").text = "P1=0,P2=0,P3=0,P4=0,P5=0,y=y+1"
#-----------------------------------------------------------------------------------------------------------------------------------
    #UP
    print("--------------- 4/5")

    counterAAAA = range(0,rows-1)  #se facessimo ciclo a decrescere sarebbe come down


    wallguard=""
    firstguard=True
    poi=""
    firstpoi=True
    murox = []
    muroy = []
    murox.append(0)
    muroy.append(0)
    guardy = []
    guardx = []
    for counta in counterAAAA: #ciclo sulle righe, il source è a+1, non mi interessa la prima riga e fermo il ciclo alla penultima per non uscire
        for countb in counter2:
            r, g, b = rgb_im.getpixel((countb*factor, (counta+1)*factor))
            if not (r==0 and g==0 and b==0):
                sourcePointx=(countb)*factor
                sourcePointy=(counta+1)*factor
                destinationPointx=(countb)*factor
                destinationPointy=counta*factor

                for i in range (0,lpoi):
                    if( (countb)==pointarray[i][0] and (counta)==pointarray[i][1] ): # se il target è un poi, assegnameto quando sono nel source ed eseguo la transizione
                        poilist[i]="(((x==%d) and (y==%d)))" % (countb,counta+1) # quando settiamo Pi = 1
                        if firstpoi==True:
                            firstpoi=False
                            poiguard="(((x==%d) and (y==%d)))" % (countb,counta+1) # quando non entriamo in un poi mettiamo P1,P2,P3=0 - da usare una volta per ogni direzione
                        else:
                            poiguard=poiguard+" or (((x==%d) and (y==%d)))" % (countb,counta+1)



                #if there is a wall
                if isThereHorizontalWallB(wallx, wally, sourcePointx, sourcePointy, destinationPointx, destinationPointy, diameter):
                    murox.append(countb)
                    a=counta+1
                    muroy.append(a)
        if(counta%5==0):
            print("   "+str(counta)+"/"+str(rows))

    murox.append(0)
    muroy.append(0)

    lenghtmy=len(murox)-1
    for i in range(0,lenghtmy):
        ay=muroy[i]
        by=muroy[i+1]
        ax=murox[i]
        bx=murox[i+1]
        if ((murox[i]+1) != (murox[i+1])):
            guardy.append(ay)
            guardy.append(0)
            guardy.append(by)
            guardx.append(ax)
            guardx.append(0)
            guardx.append(bx)

    guardx.append(0)
    guardy.append(0)

    lenghtguardx=len(guardx)-3
    for i in range(0,lenghtguardx):
        if(guardx[i]==0 and guardx[i+1]!=0):
            if firstguard==True:
                firstguard=False
                if(guardx[i+1]==guardx[i+2]):
                    wallguard="(not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard="(not((x>=%d) and (x<=%d) and (y==%d)))" % (guardx[i+1],guardx[i+2],guardy[i+1])

            else:
                if(guardx[i+1]==guardx[i+2]):
                    wallguard=wallguard+"and (not((y==%d) and (x==%d)))" % (guardy[i+1],guardx[i+1])
                else:
                    wallguard=wallguard+"and (not((x>=%d) and (x<=%d) and (y==%d)))" % (guardx[i+1],guardx[i+2],guardy[i+1])

    i = 0
    for p in poilist:
        transition = SubElement(template,"transition")
        source = SubElement(transition,"source",ref="init")
        target = SubElement(transition,"target",ref="init")
        label = SubElement(transition,"label",kind="guard").text ="( "+p+" ) and ("+ wallguard+")"
        label = SubElement(transition,"label",kind="synchronisation").text = "r?"
        label = SubElement(transition,"label",kind="assignment").text = "P%s=1,y=y-1"%i
        i += 1

    #NO POI
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="init")
    target = SubElement(transition,"target",ref="init")
    label = SubElement(transition,"label",kind="guard").text = "( not ("+poiguard+") ) and ("+wallguard+")"
    label = SubElement(transition,"label",kind="synchronisation").text = "u?"
    label = SubElement(transition,"label",kind="assignment").text = "P1=0,P2=0,P3=0,P4=0,P5=0,y=y-1"

    #STAY
    print("--------------- 5/5")
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="init")
    target = SubElement(transition,"target",ref="init")
    label = SubElement(transition,"label",kind="synchronisation").text = "s?"

    print("END process")
