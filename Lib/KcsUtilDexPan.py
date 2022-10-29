## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import string
import kcs_dex
import kcs_ui
import kcs_util

ok = kcs_util.success()
not_ok = kcs_util.failure()

#-----------------------------------------------------------------------------
#  Help methods to ease data extraction calls. These methods have no error
#  code but will rather just return dummy value(s).
#-----------------------------------------------------------------------------

def getIntegerValue(est):
  int = -9999
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 1:
      int = kcs_dex.get_int()
  return int

def getRealValue(est):
  real = -999999.99
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 2:
      real = kcs_dex.get_real()
  return real

def getStringValue(est):
  string = "****"
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 3:
      string = kcs_dex.get_string()
  return string

def getRealVector3D(est):
  vec3d = [-999999.99,-999999.99,-999999.99]
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 4:
      vec3d = kcs_dex.get_reavec3d()
  return vec3d

def getRealVector2D(est):
  vec2d = [-999999.99,-999999.99]
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 6:
      vec2d = kcs_dex.get_reavec2d()
  return vec2d

def getBox(est):
  box = [999999.99,999999.99,999999.99,-999999.99,-999999.99,-999999.99]
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 5:
      box = kcs_dex.get_box()
  return box

def getReaListValue(est):
  retval = [0]
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ > 10:
      retval = [typ-10]
      for i in range(typ-10):
        retval.append(kcs_dex.get_indexedreal(i))
  return retval


#-----------------------------------------------------------------------------
#  getCompInd - to get a component index from a component number
#               to be used in data extraction
#
#  Parameters:
#
#     Model       : Name of the model object
#     CompType    : Type of component e.g. STIFFENER (capital letters)
#     Comp        : Component number e.g. 6012
#     SubCompType : Type of subcomponent, "" (empty string) if irrelevant
#     SubComp     : SubComponent number
#-----------------------------------------------------------------------------

def getCompInd( Model, CompType, Comp, SubCompType, SubComp):
  inds = []
  compind = 0
  subcompind = 0
  est = "HULL.PANEL('" + Model + "')." + CompType + "(" + str(divmod(abs(Comp),1000)[1]) + ").COMP_ID"
  comp_no = getIntegerValue(est)
  if comp_no == Comp:
    compind = divmod(abs(Comp),1000)[1]
  else:
    est = "HULL.PANEL('" + Model + "').N" + CompType
    no_of = getIntegerValue(est)
    for no in range( 1, no_of, 1):
      est = "HULL.PANEL('" + Model + "')." + CompType + "(" + str(no) + ").COMP_ID"
      comp_no = getIntegerValue(est)
      if comp_no == Comp:
        compind = no
        break
  if SubCompType != "":
    est = "HULL.PANEL('" + Model + "')." + CompType + "(" + str(compind) + ")." + SubCompType + "(" + str(divmod(abs(SubComp),1000)[1]) + ").COMP_ID"
    subcomp_no = getIntegerValue(est)
    if subcomp_no == SubComp:
      subcompind = divmod(abs(SubComp),1000)[1]
    else:
      est = "HULL.PANEL('" + Model + "')." + CompType + "(" + str(compind) + ").N" + SubCompType
      no_of = getIntegerValue(est)
      for no in range( 1, no_of, 1):
        est = "HULL.PANEL('" + Model + "')." + CompType + "(" + str(compind) + ")." + SubCompType + "(" + str(no) + ").COMP_ID"
        comp_no = getIntegerValue(est)
        if comp_no == SubComp:
          subcompind = no
          break

  inds.append( compind)
  inds.append( subcompind)
  return inds

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  print "Self test"
  pan = kcs_ui.req_string("Panel name")
  print pan
  if pan[0] == ok:
    pln = getPlane(pan[1])
    print pln
