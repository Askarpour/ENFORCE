
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


def create_robot_4dof_tipoA(nta,tmove):

    #ROBOT IN XML - 4 DOF TIPO A
    template = SubElement(nta,"template")
    name = SubElement(template,"name").text = "Robot"

    print("writing ROBOT XML file")

    
    #STATES
    location = SubElement(template,"location",id="id1",x="100",y="0")
    location = SubElement(template,"location",id="id2",x="0",y="100")
    location = SubElement(template,"location",id="id3",x="100",y="100")
    location = SubElement(template,"location",id="id4",x="200",y="100")
    location = SubElement(template,"location",id="id5",x="100",y="200")
    location = SubElement(template,"location",id="id6",x="300",y="200")
    location = SubElement(template,"location",id="id7",x="200",y="300")

    #up id1
    #left id2
    #stay id3
    #right id4
    #down id5
    #actioB id6
    #actionA id7
    # gli stati dell'environment iniziano da id20


    init = SubElement(template,"init",ref="id3")

    #TRANSITIONS
    #UP
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id1")
    label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id2")
    target = SubElement(transition,"target",ref="id1")
    label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id4")
    target = SubElement(transition,"target",ref="id1")
    label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id1")
    target = SubElement(transition,"target",ref="id1")
    label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    #RIGHT
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id1")
    target = SubElement(transition,"target",ref="id4")
    label = SubElement(transition,"label",kind="synchronisation").text = "r!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id4")
    label = SubElement(transition,"label",kind="synchronisation").text = "r!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id5")
    target = SubElement(transition,"target",ref="id4")
    label = SubElement(transition,"label",kind="synchronisation").text = "r!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id4")
    target = SubElement(transition,"target",ref="id4")
    label = SubElement(transition,"label",kind="synchronisation").text = "r!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    #DOWN
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id2")
    target = SubElement(transition,"target",ref="id5")
    label = SubElement(transition,"label",kind="synchronisation").text = "d!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id5")
    label = SubElement(transition,"label",kind="synchronisation").text = "d!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id4")
    target = SubElement(transition,"target",ref="id5")
    label = SubElement(transition,"label",kind="synchronisation").text = "d!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id5")
    target = SubElement(transition,"target",ref="id5")
    label = SubElement(transition,"label",kind="synchronisation").text = "d!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    #LEFT
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id1")
    target = SubElement(transition,"target",ref="id2")
    label = SubElement(transition,"label",kind="synchronisation").text = "l!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id2")
    label = SubElement(transition,"label",kind="synchronisation").text = "l!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id5")
    target = SubElement(transition,"target",ref="id2")
    label = SubElement(transition,"label",kind="synchronisation").text = "l!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id2")
    target = SubElement(transition,"target",ref="id2")
    label = SubElement(transition,"label",kind="synchronisation").text = "l!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tmove"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    #STAY
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id1")
    target = SubElement(transition,"target",ref="id3")
    label = SubElement(transition,"label",kind="synchronisation").text = "s!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id4")
    target = SubElement(transition,"target",ref="id3")
    label = SubElement(transition,"label",kind="synchronisation").text = "s!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id5")
    target = SubElement(transition,"target",ref="id3")
    label = SubElement(transition,"label",kind="synchronisation").text = "s!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id2")
    target = SubElement(transition,"target",ref="id3")
    label = SubElement(transition,"label",kind="synchronisation").text = "s!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id3")
    label = SubElement(transition,"label",kind="synchronisation").text = "s!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tstay"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"
    
    #ACTION A
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id7")
    #label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "P2==1 and flagactionA==0 and t>=0"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id7")
    target = SubElement(transition,"target",ref="id3")
    #label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tactionA"
    label = SubElement(transition,"label",kind="assignment").text = "flagactionA=1,t=0"
    
    #ACTION B
    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id3")
    target = SubElement(transition,"target",ref="id6")
    #label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "P3==1 and flagactionB==0 and flagactionA==1 and t>=0"
    label = SubElement(transition,"label",kind="assignment").text = "t=0"

    transition = SubElement(template,"transition")
    source = SubElement(transition,"source",ref="id6")
    target = SubElement(transition,"target",ref="id3")
    #label = SubElement(transition,"label",kind="synchronisation").text = "u!"
    label = SubElement(transition,"label",kind="guard").text = "t>=tactionB"
    label = SubElement(transition,"label",kind="assignment").text = "workcompleted=1, flagactionB=1, t=0"

    return 
