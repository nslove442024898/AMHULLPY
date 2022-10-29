## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#-------------------------------------------------------------------------------
# Name:        trig_hull_nest_structlabel.py
# Purpose:     Trigger for nesting - custom label for structure.
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
# Get boss point for First Fixing attribute
#-------------------------------------------------------------------------------
def GetBossPoint(att, modelName):
   # get boss part id from First Fixing attribute
   bossID = kcs_att.integer_get(att,1)

   # search for part number for that part id
   est="STRUCT.ITEM('"+modelName+"').GROUP(1).NPART"
   nparts, res = KcsHotworkTools.ExtractInt(est)
   if not res:
      return None

   for partNum in range(1,nparts+1):
      est="STRUCT.ITEM('"+modelName+"').GROUP(1).PART("+ str(partNum)+").PART_ID"
      loopPartID, res = KcsHotworkTools.ExtractInt(est)
      if res:
         # part number identified
         if loopPartID == bossID:
            # get boss connection point
            est="STRUCT.ITEM('"+modelName+"').GROUP(1).PART("+ str(partNum)+").POINT"
            res2 = KcsHotworkTools.ExtractPoint3d(est)
            if res2[1]:
               return Point3D(res2[0][0],res2[0][1],res2[0][2])
   return None

#-------------------------------------------------------------------------------
# return: a FirstFixing attribute for given partID
def FindFFAttribute(model, partID):
   import kcs_att_FirstFixing

   if partID<=0:
      return None

   isFound = False
   try:
      att=kcs_att.attribute_first_get(model,1)
      while att and not isFound:
         if KcsHotworkTools.AttributeIs(att,"FirstFixing","BaseStiffener"):
            idList = []
            # get all PART IDs for this attribute
            for index in range(5):
               id = kcs_att.integer_get(att,index)
               # check if it is the attribute with given partID
               if id==partID:
                  isFound = True
                  break
         if not isFound:
            att = kcs_att.attribute_next_get()
   except:
      return None
   if isFound:
      return att
   else:
      return None

def GetHotworkLabels(model):
   import kcs_att_Hotwork

   retList = []
   try:
      att = kcs_att.attribute_first_get(model,1)
      while att:
         if KcsHotworkTools.AttributeIs(att,"Hotwork","Hotwork_item"):
            point3D=Point3D();
            point3D.X=kcs_att.real_get(att,0)
            point3D.Y=kcs_att.real_get(att,1)
            point3D.Z=kcs_att.real_get(att,2)
            refNum=kcs_att.string_get(att,1)
            discSign=kcs_att.string_get(att,0)
            # add pair - label and point - to the list
            retList.append((discSign + refNum, point3D))
         att = kcs_att.attribute_next_get()
   except:
      pass
   return retList

#-------------------------------------------------------------------------------
def GetLabel(modelName, partId):
    model = KcsModel.Model('struct',modelName)
    retList = GetHotworkLabels(model)
    if len(retList)==0:
       return ""
    if len(retList)==1:
       return retList[0][0]
    # if len(retList)>1
    #
    # If more than one label (First Fixing case)
    # partId must be used for identification with FirstFixing attributes
    att = FindFFAttribute(model, partId)
    if att== None:
       return ""
    point3D =  GetBossPoint(att, modelName)
    if point3D == None:
       return ""

    # compare points and return the right label (or the closest one)
    minDist = None
    bestLabel = ""
    for label, hotworkPoint3D in retList:
       dist = point3D.DistanceToPoint(hotworkPoint3D)
       # if same point
       if dist<0.0001:
          return label
       if minDist == None:
          dist = minDist
       elif dist<minDist:
          bestLabel = label

    return bestLabel

#-------------------------------------------------------------------------------
def pre(*args):
    result = []
    # check drawing name
    drawingComp, drawingPanel = KcsHotworkTools.GetDrawingNameAtt(KcsModel.Model('struct',args[0]))
    hasPanelStage = (len(drawingPanel)>0)
    # when only compartment stage generated, nested ID is blank = not displayed
    if hasPanelStage:

       label = GetLabel(args[0], args[1])
       if len(label)>0:
          result.append(kcs_util.trigger_ok())
          result.append(label)
       else:
          result.append(kcs_util.trigger_abort())
          result.append("")
       return result

#-------------------------------------------------------------------------------
def post(*args):

    result = kcs_util.trigger_ok()          # ok value
    return result
