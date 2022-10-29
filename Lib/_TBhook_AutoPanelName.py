## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_AutoPanelName - Automatic naming of plane panels
#
#  If this script is found in the PYTHONPATH it will be used to name panels
#  automatically. The signature of the interface methods must not be changed.
#
import string
import kcs_dex
import kcs_ui
import kcs_util

ok = kcs_util.success()
not_ok = kcs_util.failure()

MaxnoDict = {}

#-----------------------------------------------------------------------------
#  Interface method - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def InitPanelName():
  global MaxnoDict
  MaxnoDict = {}

#-----------------------------------------------------------------------------
#  Interface method - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def ExitPanelName():
  global MaxnoDict
#  print MaxnoDict
  MaxnoDict = {}

#-----------------------------------------------------------------------------
#  Interface method - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def getPanelName(Block,Valid,Axis,Location,DType,GType,Project,PartList,GPS1,GPS2,GPS3,GPS4):
  global MaxnoDict
#  print Block,Valid,Axis,Location,DType,GType,Project,PartList,GPS1,GPS2,GPS3,GPS4

  PanelName = ""
  prefix = ""
  if Block != "":
    prefix = Block
  elif DType == 957:
    prefix = "BRA"
  elif DType == 958:
    prefix = "SUB"
  if prefix != "":
    locs = string.split( Location, "+")
    loc = locs[0]
    locs = string.split( loc, "-")
    loc = locs[0]

#  For negative FR and LP positions splitting with "-" removes the position

    if len(locs) > 1 and (loc == "FR" or loc == "LP"):
	loc = loc + "-" + locs[1]

#  Build up the generic part of the name

    if Axis == "X":
      if loc[:2] == "FR":
         pan_gen = prefix + "-" + loc
      else:
         pan_gen = prefix + "-" + Axis + loc
    elif Axis == "Y" or Axis == "Z":
      if loc[:2] == "LP":
         pan_gen = prefix + "-" + loc
      else:
         pan_gen = prefix + "-" + Axis + loc
    elif Axis == "XYZ":
      pan_gen = prefix + "-" + Axis
    elif loc[:5] == "_RSO_":
      pan_gen = prefix + "-R" + loc[4:]
    else:
      pan_gen = prefix + "-" + loc

    if len(pan_gen) >= 20:
      pan_gen = pan_gen[:20] + "_"
    else:
      pan_gen = pan_gen + "_"
    pan_gen = string.upper(pan_gen)

#  Check if it is already registered in the local dictionary

    if MaxnoDict.has_key(pan_gen):
      maxno = MaxnoDict[pan_gen] + 1
      MaxnoDict[pan_gen] = maxno

#  if not, get the block and check if panels matching the generic name
#  already exists. Find the next free running number.

    elif Block != "":
      maxno = 0
      est = "HULL.BLOCK('" + Block + "').PANEL('" + pan_gen + "'*).NAME"
      res = kcs_dex.extract(est)
      if res == ok:
        cont = ok
        while cont == ok:
          type = kcs_dex.next_result()
          if type == 3:
            pan_name = kcs_dex.get_string()
            numbstr = pan_name[len(pan_gen):]
            try:
              numb = string.atoi(numbstr)
            except:
              numb = 0
            else:
              if numb > maxno:
                maxno = numb
          else:
            cont = not_ok
      maxno = maxno + 1
      MaxnoDict[pan_gen] = maxno

#  If no block given set no to 1

    else:
      maxno = 1
      MaxnoDict[pan_gen] = maxno

#  Create the new name

    PanelName = pan_gen + str(maxno)

#  Make sure the panel with this name does not exist even outside Block

    cont = ok
    while cont == ok:
      est = "HULL.PANEL('" + PanelName + "').NAME"
      res = kcs_dex.extract(est)
      if res == ok:
        type = kcs_dex.next_result()
        if type == 3:
          maxno = maxno + 1
          MaxnoDict[pan_gen] = maxno
          PanelName = pan_gen + str(maxno)
        else:
          cont = not_ok

#  print PanelName
  return PanelName

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  print "AutoPanelNote test start"
  print getPanelName("BLOCK","P","X","FR1+100",101,102,"","","","","","")
  print getPanelName("BLOCK","SBP","Y","LP2",101,102,"","","","","","")
  print getPanelName("BLOCK","S","Y","LP-2",101,102,"","","","","","")
  print getPanelName("BLOCK","SP","Z","LP3-300",101,102,"","","","","","")
  print getPanelName("BLOCK","P","X","1000",101,102,"","","","","","")
  print getPanelName("BLOCK","S","Y","2000",101,102,"","","","","","")
  print getPanelName("BLOCK","SP","Z","3000",101,102,"","","","","","")
  print getPanelName("BLOCK","SBP","XYZ","FR1,0,0,FR2,500,0,FR1,1000,LP3",101,102,"","","","","","")
  print getPanelName("BLOCK","SBP","","OBJ1",101,102,"","","","","","")
  print getPanelName("BLOCK","SBP","","A_VERY_LONG_OBJECT_NAME",101,102,"","","","","","")
  print getPanelName("","SBP","Y","LP3.5",957,102,"","","","","","")
  print getPanelName("","SBP","","_RSO_FR34",958,1000,"","","","","","")
  print getPanelName("","SBP","","NOWAY",181,101,"","","","","","")
  print "AutoPanelNote test end"
