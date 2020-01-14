
import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


def create_robot2_4dof_tipoA(nta,tmove):

    #ROBOT IN XML - 4 DOF TIPO A
    template = SubElement(nta,"template")
    name = SubElement(template,"name").text = "Robot2"

    print("writing ROBOT1 XML file")

    print("tmove = ",tmove)
    
    #STATES
    location = SubElement(template,"location",id="10",x="100",y="0")
    location = SubElement(template,"location",id="01",x="0",y="100")
    location = SubElement(template,"location",id="11",x="100",y="100")
    location = SubElement(template,"location",id="21",x="200",y="100")
    location = SubElement(template,"location",id="12",x="100",y="200")
    location = SubElement(template,"location",id="22",x="200",y="200")
    location = SubElement(template,"location",id="23",x="200",y="300")

    init = SubElement(template,"init",ref="11")

    #TRANSITIONS
    #UP
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="10")
    label = SubElement(transition,"label",kind="synchronisation").text = "u2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="01")
    target = SubElement(transition,"target",ref="10")
    label = SubElement(transition,"label",kind="synchronisation").text = "u2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="21")
    target = SubElement(transition,"target",ref="10")
    label = SubElement(transition,"label",kind="synchronisation").text = "u2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="10")
    target = SubElement(transition,"target",ref="10")
    label = SubElement(transition,"label",kind="synchronisation").text = "u2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    #RIGHT
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="10")
    target = SubElement(transition,"target",ref="21")
    label = SubElement(transition,"label",kind="synchronisation").text = "r2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="21")
    label = SubElement(transition,"label",kind="synchronisation").text = "r2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="12")
    target = SubElement(transition,"target",ref="21")
    label = SubElement(transition,"label",kind="synchronisation").text = "r2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="21")
    target = SubElement(transition,"target",ref="21")
    label = SubElement(transition,"label",kind="synchronisation").text = "r2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    #DOWN
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="01")
    target = SubElement(transition,"target",ref="12")
    label = SubElement(transition,"label",kind="synchronisation").text = "d2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="12")
    label = SubElement(transition,"label",kind="synchronisation").text = "d2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="21")
    target = SubElement(transition,"target",ref="12")
    label = SubElement(transition,"label",kind="synchronisation").text = "d2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="12")
    target = SubElement(transition,"target",ref="12")
    label = SubElement(transition,"label",kind="synchronisation").text = "d2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    #LEFT
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="10")
    target = SubElement(transition,"target",ref="01")
    label = SubElement(transition,"label",kind="synchronisation").text = "l2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="01")
    label = SubElement(transition,"label",kind="synchronisation").text = "l2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="12")
    target = SubElement(transition,"target",ref="01")
    label = SubElement(transition,"label",kind="synchronisation").text = "l2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="01")
    target = SubElement(transition,"target",ref="01")
    label = SubElement(transition,"label",kind="synchronisation").text = "l2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    #STAY
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="10")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "s2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="21")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "s2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="12")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "s2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="01")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "s2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "s2!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"

    #LOAD
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="22")
    label = SubElement(transition,"label",kind="synchronisation").text = "start_loading!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tload1"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"
    #label = SubElement(transition,"label",kind="guard").text = "P1==1 and P2==1 and Loaded==0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="22")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "end_loading!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=0"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"
    #label = SubElement(transition,"label",kind="assignment").text = "t1=t1"

    #UNLOAD
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="11")
    target = SubElement(transition,"target",ref="23")
    label = SubElement(transition,"label",kind="synchronisation").text = "start_unloading!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=tunload1"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"
    #label = SubElement(transition,"label",kind="guard").text = "P1==1 and P2==1 and Loaded==0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="23")
    target = SubElement(transition,"target",ref="11")
    label = SubElement(transition,"label",kind="synchronisation").text = "end_unloading!"
    label = SubElement(transition,"label",kind="guard").text = "t2>=0"
    label = SubElement(transition,"label",kind="assignment").text = "t2=0"
    #label = SubElement(transition,"label",kind="assignment").text = "t1=t1"
    
    return 
