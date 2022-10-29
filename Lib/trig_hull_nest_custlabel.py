## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#-------------------------------------------------------------------------------
# Name:        trig_hull_nest_custlabel.py
# Purpose:     Trigger for nesting - custom label (in Hotworks used for equipment)
#
# Module:      Hotwork
#-------------------------------------------------------------------------------
import kcs_util
import kcs_ui
import kcs_att
import kcs_dex
import KcsModel
from KcsPoint3D import Point3D

try:
   from Hotwork import KcsHotworkTools
except:
   # print message
   kcs_ui.message_noconfirm("Error in inport KcsHotworkTools")
   # re-raise the exception
   raise

#-------------------------------------------------------------------------------
# GetNestingAtt - add nesting attribute with penetration name to panel
#-------------------------------------------------------------------------------
def GetEquNames(model):
    equNames = []
    try:
        #check if model have Hotwork attribute saved
        att=kcs_att.attribute_first_get(model,1)
        while att:
           if KcsHotworkTools.AttributeIs(att,"Hotwork","Nesting"):
              equName = kcs_att.string_get(att,0)
              equNames.append(equName)
           att = kcs_att.attribute_next_get()
    except:
        pass
    return equNames

#-------------------------------------------------------------------------------
# input:
#     args[0] - part name (plate name)
#     args[1] - panel name (plate originated from parent)
#-------------------------------------------------------------------------------
def pre(*args):
    result = []

    equNames = GetEquNames(KcsModel.Model('plane panel',args[1]))
    if len(equNames)==0:
       result.append(kcs_util.trigger_abort())
    else:
       result.append(kcs_util.trigger_ok())
       aryLabels = []
       for equName in equNames:
          model = KcsModel.Model('equipment',equName)
          point3D,discSign,refNum,strDescr = KcsHotworkTools.GetHotworkItemAtt(model)
          if discSign!= '':
             drawingComp, drawingPanel = KcsHotworkTools.GetDrawingNameAtt(model)
             hasPanelStage = (len(drawingPanel)>0)
             # when only compartment stage generated, nested ID is blank = not displayed
             if hasPanelStage:
                result.append((point3D, discSign+refNum))

    return result

#-------------------------------------------------------------------------------
def post(*args):

    result = kcs_util.trigger_ok()          # ok value
    return result
