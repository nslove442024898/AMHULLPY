## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import string
import kcs_dex
import kcs_ui
import kcs_util
import KcsProfSymb
from KcsConfNoteRec import *

ok = kcs_util.success()
not_ok = kcs_util.failure()

#------------------------------------------------------------------------------
#  NoteName - the list of note names to select from
#
#  !! Please make sure that the list of note names end with an empty string
#     as this is used as the signal to terminate the reading of names !!
#------------------------------------------------------------------------------
NoteName = (
  " Plate note",
  " Profile note",
  " Bracket standard note",
  " Bracket instance note",
  " Bracket profile note",
  ""
)

#------------------------------------------------------------------------------
#  NoteChar - the list of note characteristic records for each note
#------------------------------------------------------------------------------
NoteChar = (
  ("COG", "MidMid", "cyan", 200, 120),
  ("MidPoint", "MidOrigin", "white", 200, 120),
  ("COG", "MidMid", "cyan", 200, 120),
  ("MidPoint", "MidOrigin", "white", 200, 120),
  ("COG", "MidMid", "cyan", 200, 120),
)

#------------------------------------------------------------------------------
#  NoteFilter - the list of pick filters for each note
#
#  !! Note that a one-item tuple in python must end with a comma !!
#------------------------------------------------------------------------------
NoteFilter = (
  (
    ("plane panel", "plate", ""),
  ),
  (
    ("plane panel", "stiffener", ""),
    ("plane panel", "flange", ""),
  ),
  (
    ("plane panel", "bracket", ""),
  ),
  (
    ("plane panel", "bracket", ""),
  ),
  (
    ("plane panel", "bracket", "stiffener"),
    ("plane panel", "bracket", "flange"),
  ),
)

NoteData = []

#-----------------------------------------------------------------------------
#  Interface methods - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------
def getNoteName(NoteNo):
  try:
    return NoteName[NoteNo]
  except:
    return None

def getNoteChar(NoteNo):
  try:
    return NoteChar[NoteNo]
  except:
    return None

def getNoteFilter(NoteNo,FilterNo):
  try:
    return NoteFilter[NoteNo][FilterNo]
  except:
    return None

def getNoteData(ItemNo):
  try:
    return NoteData[ItemNo]
  except:
    return None

#-----------------------------------------------------------------------------
#  Help methods to ease data extraction calls used below
#-----------------------------------------------------------------------------
def getIntegerValue(est):
  int = -9999;
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 1:
      int = kcs_dex.get_int()
  return int

def getRealValue(est):
  real = -999999.99;
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

def getReaListValue(est):
  retval = [0];
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
#-----------------------------------------------------------------------------
def getCompInd( Model, PartType, Part, SubPartType, SubPart):
  inds = []
  compind = 0
  subcompind = 0
  est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(divmod(abs(Part),1000)[1]) + ").COMP_ID"
  comp_no = getIntegerValue(est)
  if comp_no == Part:
    compind = divmod(abs(Part),1000)[1]
  else:
    est = "HULL.PANEL('" + Model + "').N" + PartType
    no_of = getIntegerValue(est)
    for no in range( 1, no_of, 1):
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(no) + ").COMP_ID"
      comp_no = getIntegerValue(est)
      if comp_no == Part:
        compind = no
        break
  if SubPartType != "":
    est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(compind) + ")." + SubPartType + "(" + str(divmod(abs(SubPart),1000)[1]) + ").COMP_ID"
    subcomp_no = getIntegerValue(est)
    if subcomp_no == SubPart:
      subcompind = divmod(abs(SubPart),1000)[1]
    else:
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(compind) + ").N" + SubPartType
      no_of = getIntegerValue(est)
      for no in range( 1, no_of, 1):
        est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(compind) + ")." + SubPartType + "(" + str(no) + ").COMP_ID"
        comp_no = getIntegerValue(est)
        if comp_no == SubPart:
          subcompind = no
          break

  inds.append( compind)
  inds.append( subcompind)
  return inds

#-----------------------------------------------------------------------------
#  createProfNote - create a profile note
#-----------------------------------------------------------------------------
def createProfNote( Model, PartType, Part, SubPartType, SubPart):
  global NoteData

  inds = getCompInd( Model, PartType, Part, SubPartType, SubPart)
  if SubPartType == "":
    flange_type = 0
    if PartType == "FLA":
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ").TYPE"
      flange_type = getIntegerValue(est)

#  Folded flange

    if abs(flange_type) == 1:
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ").HEIGHT"
      txt = str(int(getRealValue(est))) + " FL"
      text = Text( text=txt, v=0.5)
      NoteData.append(text.getRecord())

#  Welded profile

    else:
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ").PRO.TYPE"
      typ = getIntegerValue(est)
      symbno = KcsProfSymb.getSymb(typ)
      symb = Symbol( font=8, number=symbno, height=10, conn=1, v=0.5, mirr=2)
      NoteData.append(symb.getRecord())
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ").PRO.PAR"
      par = getReaListValue(est)
      txt = " "
      for i in range(par[0]):
        spar = str(par[i+1])
        if spar[-2:] == ".0":
          spar = spar[:-2]
        txt = txt + (spar + "*")
      text = Text( text=txt[:-1], v=0.5)
      NoteData.append(text.getRecord())
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ").QUALITY.STRING"
      qual = " " + getStringValue(est)
      qualtext = Text( text=qual, v=0.5)
      NoteData.append(qualtext.getRecord())

#  Profile on brackets

  else:
    flange_type = 0
    if SubPartType == "FLA":
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ")." + SubPartType + "(" + str(inds[1]) + ").TYPE"
      flange_type = getIntegerValue(est)

#  Folded flange

    if abs(flange_type) == 1:
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ")." + SubPartType + "(" + str(inds[1]) + ").HEIGHT"
      height = getRealValue(est)
      txt = str(int(height)) + " FL"
      text = Text( text=txt, v=0.5)
      NoteData.append(text.getRecord())

#  Welded profile

    else:
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ")." + SubPartType + "(" + str(inds[1]) + ").PRO.TYPE"
      typ = getIntegerValue(est)
      symbno = KcsProfSymb.getSymb(typ)
      symb = Symbol( font=8, number=symbno, height=10, conn=1, v=0.5, mirr=2)
      NoteData.append(symb.getRecord())
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ")." + SubPartType + "(" + str(inds[1]) + ").PRO.PAR"
      par = getReaListValue(est)
      txt = " "
      for i in range(par[0]):
        spar = str(par[i+1])
        if spar[-2:] == ".0":
          spar = spar[:-2]
        txt = txt + (spar + "*")
      text = Text( text=txt[:-1], v=0.5)
      NoteData.append(text.getRecord())
      est = "HULL.PANEL('" + Model + "')." + PartType + "(" + str(inds[0]) + ")." + SubPartType + "(" + str(inds[1]) + ").QUALITY.STRING"
      qual = " " + getStringValue(est)
      qualtext = Text( text=qual, v=0.5)
      NoteData.append(qualtext.getRecord())
  return None

#-----------------------------------------------------------------------------
#  setNoteData - the Note definition method adding records to the NoteData list
#-----------------------------------------------------------------------------
def setNoteData(NoteNo,ModelType,Model,PartType,Part,SubPartType,SubPart):
  global NoteData
  NoteData = []

#-----------------------------------------------------------------------------
#  Plate Note
#-----------------------------------------------------------------------------
  if NoteNo == 1:
    ref = ReferenceSymbol(font=8, number=4)
    NoteData.append(ref.getRecord())
    if PartType == "plate":
      inds = getCompInd( Model, "PLA", Part, "", 0)
      est = "HULL.PANEL('" + Model + "').PLA(" + str(inds[0]) + ").THICKNESS"
      thi = getRealValue(est)
      txt = str(thi)
      if txt[-2:] == ".0":
        txt = txt[:-2]
      thitext = Text( text=txt, v=0.5)
      NoteData.append(thitext.getRecord())
      est = "HULL.PANEL('" + Model + "').PLA(" + str(inds[0]) + ").QUALITY.STRING"
      qual = " " + getStringValue(est)
      qualtext = Text( text=qual, v=0.5)
      NoteData.append(qualtext.getRecord())

#-----------------------------------------------------------------------------
#  Profile Note
#-----------------------------------------------------------------------------
  elif NoteNo == 2:
    ref = ReferenceSymbol(font=8, number=1)
    NoteData.append(ref.getRecord())
    if PartType == "stiffener":
      dum = createProfNote( Model, "STI", Part, "", 0)

    elif PartType == "flange":
      dum = createProfNote( Model, "FLA", Part, "", 0)

    elif PartType == "bracket" and SubPartType == "stiffener":
      dum = createProfNote( Model, "BRA", -Part, "STI", SubPart)

    elif PartType == "bracket" and SubPartType == "flange":
      dum = createProfNote( Model, "BRA", -Part, "FLA", SubPart)

#-----------------------------------------------------------------------------
#  Bracket Standard Note
#-----------------------------------------------------------------------------
  elif NoteNo == 3:
    ref = ReferenceSymbol(font=8, number=4)
    NoteData.append(ref.getRecord())
    if PartType == "bracket":
      inds = getCompInd( Model, "BRA", -Part, "", 0)
      est = "HULL.PANEL('" + Model + "').BRA(" + str(inds[0]) + ").THICKNESS"
      thi = getRealValue(est)
      txt = str(thi)
      if txt[-2:] == ".0":
        txt = txt[:-2]
      thitext = Text( text=txt, v=0.5)
      NoteData.append(thitext.getRecord())
      est = "HULL.PANEL('" + Model + "').BRA(" + str(inds[0]) + ").QUALITY.STRING"
      qual = getStringValue(est)
      txt = " " + qual
      qualtext = Text( text=txt, v=0.5)
      NoteData.append(qualtext.getRecord())

#-----------------------------------------------------------------------------
#  Bracket Instance Note
#-----------------------------------------------------------------------------
  elif NoteNo == 4:
    ref = ReferenceSymbol(font=8, number=4)
    NoteData.append(ref.getRecord())
    if PartType == "bracket":
      inds = getCompInd( Model, "BRA", -Part, "", 0)
      est = "HULL.PANEL('" + Model + "').BRA(" + str(inds[0]) + ").INSTANCE"
      inst = getStringValue(est)
      if inst == "":
        est = "HULL.PANEL('" + Model + "').BRA(" + str(inds[0]) + ").DESIGNATION"
        inst = getStringValue(est)
      txt = inst + "-"
      insttext = Text( text=txt, v=0.5)
      NoteData.append(insttext.getRecord())
      est = "HULL.PANEL('" + Model + "').BRA(" + str(inds[0]) + ").THICKNESS"
      thi = getRealValue(est)
      txt = str(thi)
      thitext = Text( text=txt, v=0.5)
      NoteData.append(thitext.getRecord())

#-----------------------------------------------------------------------------
#  Bracket Profile Note
#-----------------------------------------------------------------------------
  elif NoteNo == 5:
    ref = ReferenceSymbol(font=8, number=1)
    NoteData.append(ref.getRecord())

    if PartType == "bracket" and SubPartType == "stiffener":
      dum = createProfNote( Model, "BRA", -Part, "STI", SubPart)

    elif PartType == "bracket" and SubPartType == "flange":
      dum = createProfNote( Model, "BRA", -Part, "FLA", SubPart)

  return None

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  for no in range(len(NoteName) - 1):
    print getNoteName(no)
    print getNoteChar(no)
    for fi in range(len(NoteFilter[no])):
      print getNoteFilter(no,fi)
