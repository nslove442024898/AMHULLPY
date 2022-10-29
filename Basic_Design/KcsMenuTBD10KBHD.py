## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import string
import KcsStringlist
import KcsModel
import kcs_util
import kcs_ui
import kcs_draft
import kcs_dex
import kcs_hullpan

import stringutils
import cCoordRef
import cPanel
import Defaults

_ok, _cancel, _options = kcs_util.ok(), kcs_util.cancel(), kcs_util.options()

# 1, if "..., SUB='MAINK###';" is supported, and # matches exactly 1 character
# 0 - the given feature is NOT supported (only 'MAINK*')
FeatureSUB_Wildcard = 0

SB_SHIP = kcs_util.TB_environment_get("SB_SHIP")
KBHD_DefaultFile = SB_SHIP + "KBHD.DEF"

######################################################################
##
## Class for holding the bulkhead's parameters
##
######################################################################

class _EmptyContainer:
  pass

######################################################################
##
## Analyses Basic Design default file, and retrieves the setting of
## EARLY_DESIGN default
## Adds to BHD:
##   EarlyDesign - 1 (set), 0 (not set, or default file error)
##
######################################################################

def EarlyDesign(BHD):
  def VerFun(line):
    return (line[:12] == "EARLY_DESIGN")

  BasicDesign_DefFile = SB_SHIP + "SJ700.SBD"
  status, res = stringutils.ScanFile(BasicDesign_DefFile, VerFun, "SU1")
  BHD.EarlyDesign = (status == 0 and len(res) > 0)
  print "Status, Early Design:", status, BHD.EarlyDesign

######################################################################
##
## Uses Data Extraction to find the names of panels/subpanels having
## the names <name>K001, <name>K002, ... <name>K999.
## NOTE: The wildcard DEX command string does not "see" subpanels
## We have to ask specifically for the given subpanel name. It is not
## safe, because it does not check the existence of the subpanels
## with the names <name>K*, other than specified above.
##
######################################################################

def GetSubPanelsInModel(name):
  subpanList = []  #datatype 958
  panList = []     #datatype other than 958
  n, ex, nx, get = 1, kcs_dex.extract, kcs_dex.next_result, kcs_dex.get_int
  s = "HULL.PANEL('" + name + "K%03d').OC1"
  for n in range(1,1000):
    if ex(s % n) == 0:
      if nx() == 1:
        if get() == 958: subpanList.append(n)
        else: panList.append(n)
  return (subpanList, panList)

######################################################################
##
## Asks for the bulkhead's panel name. Makes extensive testing,
## to make sure, that the given panel can be safely constructed using
## the wildcard syntax for subpanels.
##
######################################################################

def GetBHD_Name(BHD):
  name = ""
  allowed = string.digits + string.uppercase + "-_" #allowed characters in the panel's name
  while 1:
    res = kcs_ui.string_req("Bulkhead's panel name", name)
    if res[0] != _ok: return res[0]
    name = string.upper(res[1])
    if not stringutils.IsStringAllowed(name, allowed):
      kcs_ui.message_noconfirm("Panel name contains unallowed characters")
      continue

    dt = cPanel.PanelDataType(name)
    if dt > 0: #Conflicting panel/subpanel found!
      ans = kcs_ui.answer_req("Corrugated bulkhead", "Panel %s already exists in the model! Delete?" % name)
      if ans != kcs_util.yes(): continue #Try another name

      res = cPanel.pan_delete(name, dt == 958) #Delete the conflicting panel (with subpanels)
      if res[0]:
        kcs_ui.message_confirm("Could not delete the panel %s!" % name)
        continue
      list = res[1] #Not deleted subpanels
      if len(list) > 0:
        print "While deleting the panel %s, the following subpanels could not be deleted:" % name
        for n in list: print "   ",n
        kcs_ui.message_confirm("Some subpanels could not be deleted!\nSee log file for details ...")
        continue # Try another name
      print "Panel %s deleted from the model" % name

    else: #Conflicting panel NOT found - try to find all the 'lost' (or 'free') subpanels
      subpanList, panList = GetSubPanelsInModel(name) # Get a list of subpanels
      lastSubID = len(BHD.Y)+1
      msg1="These names would be reused by Vitesse for creating bulkhead's subpanels!"
      if len(panList) > 0:
        if panList[0] <= lastSubID:
          print "The following panels have names, that match the bulkhead's subpanels naming convention."
          print msg1
        notPrinted = 1
        for n in panList:
          if notPrinted and n > lastSubID:
            print "The model contains also panels outside of the ID range of the bulkhead's subpanels:"
            notPrinted = 0
          print "   %sK%03d" % (name, n)
        st = "The model already contains panels with conflicting names!\n" + \
             "Some of them should not be deleted (see log file for details)"
        kcs_ui.message_confirm(st)
        continue # Try another name

      if len(subpanList) > 0:
        print "The following existing subpanels have names, that match the bulkhead's subpanels naming convention."
        print msg1
        status = 0
        for n in subpanList:
          subpanel = "%sK%03d" % (name, n)
          res = cPanel.pan_delete(subpanel, 1)
          if res[0]:
            print "   ", subpanel, "NOT deleted!"
            status = 1
          else:
            print "   ", subpanel, "deleted"
        s = "Some subpanels with conflicting names found.\nSee log file for details"
        if status:
          s = s + " (Some of them could not be deleted)"
        kcs_ui.message_confirm(s)
        if status: continue # Try another name

    BHD.Name = name
    return _ok

######################################################################
##
## Function compatible with validating functions of DefaultItem class
## Verifies the existence of the given hull block
##
######################################################################

def VerifyHullBlock(value, args):
  res = 0
  st = "HULL.BLOCK('%s').NAME" % value
  if kcs_dex.extract(st) == 0:
    if kcs_dex.next_result() == 3: res = 1
  if res == 0:
    kcs_ui.message_confirm("Hull block '%s' does not exist!" % value)
  return (res, value)

######################################################################
##
## Function compatible with validating functions of DefaultItem class
## Verifies the string input (value), which must be an integer lying
## between args[0], and args[1]. If not, it must be equal to args[2]
##
######################################################################

def ValidateIntOrStr(value, args):
  try:
    con = string.atoi(value)
    res = (args[0] <= con <= args[1])
  except:
    res = (string.upper(value) == args[2])
  if res == 0:
    kcs_ui.message_confirm("Invalid input (%s)!" % value)
  return (res, value)

######################################################################
##
## Define defaults for the macro
## Adds to BHD:
##   param - Defaults class instance with bulkhead's defaults parameters
## Defaults:
##   Block - default hull block name ('')
##   StripWidth - minimum width of the terminating subpanel (0).
##   MaterialSide - material side can be selected according to
##      the wave's direction ('Default' - default setting) or can be
##      chosen by the user ('Ask')
##   ConnectionCode - connection code for the subpanels (9999)
##   BevelCode - bevel code, or 'None' ('None')
##   SeamExcess - seam excess value, or 'None' ('None')
##   BoundaryExcess - is there an excess at external boundary? (NO)
##
######################################################################

def GetBHD_Defaults(BHD):
  defList = []

  d = Defaults.UpStrDefItem('Block', '<Undefined>', 'Hull block name')
  d.SetValidate(VerifyHullBlock)
  defList.append(d)

  d = Defaults.RealDefItem('StripWidth', 50.0, 'Minimal width of terminal bulkhead segments')
  d.SetValidate(Defaults.LowerLimitCheck, 1.0)
  defList.append(d)

  MS_list = KcsStringlist.Stringlist('Default')
  MS_list.AddString('Ask')
  d = Defaults.EnumDefItem('MaterialSide', 1, MS_list, \
    'Indicate the way material side is determined')
  defList.append(d)

  d = Defaults.IntDefItem('ConnectionCode', 9999, 'Connection code for the knuckled subpanels')
  d.SetValidate(Defaults.RangeCheck, (0, 9999))
  defList.append(d)

  d = Defaults.UpStrDefItem('BevelCode', 'NONE', 'Bevel code (None - no bevel)')
  d.SetValidate(ValidateIntOrStr, (-9999, 9999, 'NONE'))
  defList.append(d)

  d = Defaults.YesNoDefItem('AddSeams','YES')
  defList.append(d)

  d = Defaults.UpStrDefItem('SeamExcess', 'NONE', 'Seam excess (None - no excess)')
  d.SetValidate(ValidateIntOrStr, (-9999, 9999, 'NONE'))
  defList.append(d)

  d = Defaults.YesNoDefItem('BoundaryExcess', 'NO')
  defList.append(d)

  d = Defaults.EnumDefItem('WaveLocation', 1, MS_list, \
    'Choose the way of determining wave location')
  defList.append(d)

  BHD.param = Defaults.Defaults(defList, 'Corrugated bulkhead macro parameters', \
    'Parameters, and their current values')
  BHD.param.LoadFromFile(KBHD_DefaultFile, 0)

## Edit the parameters and verify the hull block (if not modified from initial '')
  block_ok = 0
  while block_ok == 0:
    res = BHD.param.Edit(KBHD_DefaultFile)
    if res == _ok:
      block_ok, block = VerifyHullBlock(BHD.param['Block'], None)
    else:
      block_ok = 1
  return res

######################################################################
##
## Returns the verified frame position of the bulkhead
## Adds to BHD:
##   position - frame position of the bulkhead as a CoordRef class instance
##
######################################################################

def GetBHD_Position(BHD):
  while 1:
    res = kcs_ui.string_req("Bulkhead position", "")
    if res[0] == _ok:
      try:
        BHD.position = [cCoordRef.CoordRef(1, res[1])]
        return _ok
      except:
        pass
    else:
      return res[0]

######################################################################
##
## Collects the bulkhead's limits, verifies them by creating a dummy panel,
## and retrieves the corner coordinates. Returns a status.
## Expects in BHD:
##   position[0] - position of the bulkhead (CoordRef)
##   param['BoundaryExcess'] - if YES, will ask for a boundary excess
## Adds to BHD:
##   Bou - the Panel class instance with the location and boundary list
##   Corners - the list of Point3D class instances being the corner
##             coordinates
##   YPS, YSB - Y coordinate limits of the bulkhead
##
######################################################################

def GetBHD_Limits(BHD):
  def GetExcess(limit):
    res = kcs_ui.real_req("Excess value at the limit", 0.0)
    if res[0] == _ok and abs(res[1]) > 0.01: limit.excess = res[1]
  plane = BHD.position[0].axis
  try:
    Bou = cPanel.Panel(plane, repr(BHD.position[0]))
  except:
    return _cancel
  OptionList = KcsStringlist.Stringlist("Intersecting panel")
  OptionList.AddString("Outer shell - portside")
  OptionList.AddString("Outer shell - starboard")
  CoordInfo = []
  for n in [1,2,3]:
    if plane != n:
      c = cCoordRef.axisChar[n-1]
      OptionList.AddString(c + " coordinate")
      CoordInfo.append((n,c + "="))
  OptionList.AddString("OK")
  OK_ind = len(OptionList.StrList)
  AskBoundary = BHD.param['BoundaryExcess']

  while 1:   # Until the indicated limits are verified to be correct
    choice = kcs_ui.choice_select("Bulkhead limits", \
             "Limit no. "+str(len(Bou.boundary)+1) + "(Options - remove last limit)", \
             OptionList)
    if choice[0] == _ok:
      typ = choice[1]
      if typ == OK_ind:          # All limits defined -> check the boundary!
        pan_name = cPanel.FindFreePanelName("DUMMY",6)
        # Location 'SP' can be valid for X-plane bhds, maybe not for other ones
        status, corners = Bou.CheckBoundary(BHD.param['Block'], pan_name, "SP")
        if status == 0:
          kcs_ui.message_noconfirm("Limits OK")
          BHD.Bou, BHD.Corners = Bou, corners
          YMin, YMax = 99999.0, -99999.0
          for cor in corners:
            y = cor.Y
            if y < YMin: YMin = y
            if y > YMax: YMax = y
#Check the __HULLFORM__ limits
          limID, nLim = 0, len(Bou.boundary)
          for lim in Bou.boundary:
            if isinstance(lim, cPanel.OuterShellLimit):
              y1 = corners[limID].Y
              y2 = corners[(limID+1) % nLim].Y
              if lim.ref:
                if y1>YMin: YMin = y1
                if y2>YMin: YMin = y2
              else:
                if y1<YMax: YMax = y1
                if y2<YMax: YMax = y2
            limID = limID + 1
          BHD.YPS = YMax
          BHD.YSB = YMin
          return _ok # OK, Limits and corners defined
        else:
          if status == 1:   s = "Error initialising the panel"
          elif status == 2: s = "Error in PANEL statement"
          elif status == 3: s = "Error in BOUNDARY specification"
          else:             s = "Error in retrieving the panel corners"
          Bou.boundary = [] # Clear the boundary list
          kcs_ui.message_confirm("%s: %s\nTry again ..." % (pan_name, s)) # Try again to get the boundary
      elif typ == 1:             # Intersecting panel
        res, model = cPanel.GetModelItem("Indicate intersecting panel", "plane panel")
        if res == _ok:
          new_lim = cPanel.PanelLimit(model.Name, model.ReflCode)
          if AskBoundary: GetExcess(new_lim)
          Bou.AddLimit(new_lim)
      elif typ == 2 or typ == 3: # Outer shell - portside or starboard (REF)
        new_lim = cPanel.OuterShellLimit(typ-2)
        if AskBoundary: GetExcess(new_lim)
        Bou.AddLimit(new_lim)
      else:                      # Coordinate limit
        info = CoordInfo[typ-4]
        last, cont = "", 1
        while cont:
          cont = 0
          res = kcs_ui.string_req(info[1], last) # Get the coordinate definition
          if res[0] == _ok:
            try:
              new_lim = cPanel.CoordinateLimit(info[0], res[1]) # Verify coordinate
              if AskBoundary: GetExcess(new_lim)
              Bou.AddLimit(new_lim)
            except:
              last, cont = string.upper(res[1]), 1
    elif choice[0] == _options:
      if len(Bou.boundary) > 0: Bou.RemoveLimitInd()
      else: return _options
    else:
      return _cancel # Limit type choice cancelled

######################################################################
##
## Presents a graphical form of a help, when defining bhd dimensions
##
######################################################################

def BHD_Help():
  font_id = 801
  symbols = [1,2,3]
  log_var = "SBB_SYMBDIR"
  pyth_var = "SB_PYTHON"

  try:
    old_dir = kcs_util.TB_environment_get(log_var)
  except:
    old_dir = ""
  pyth_dir = kcs_util.TB_environment_get(pyth_var)
  kcs_util.TB_environment_set(log_var, pyth_dir)
#  list = kcsSymbollist.Symbollist(font_id, symbols[id])
  try:
#    res = kcs_ui.symbol_select("The bulkhead's wave dimensions", list, 3)
    res = kcs_ui.symbol_select("The bulkhead's wave dimensions", font_id, 3)
  except:
    pass
  if old_dir != "":
    kcs_util.TB_environment_set(log_var, old_dir)

######################################################################
##
## Collect the Y coordinates - returns status
## status = -1 -> bulkhead connects to the side limit by a skew subpanel
## status = -2 -> cannot define even a single bulkhead 'wave'
## status = 0  -> O.K.
## status = 1  -> terminal bulkhead segment (X-plane) is narrower than StripWidth
## Expects in BHD:
##   YSB, YPS - starboard, and portside limit Y coordinates
##   A, B     - wave's dimensions (bases: B >= A)
##   param['WaveLocation'] - way of determining the location of he wave
## Adds to BHD:
##   Y        - list of Y coordinates of the subpanel joins sorted from PS to SB
##
######################################################################

def GetYCoords(BHD):
  Ymin, Ymax = BHD.YSB, BHD.YPS
  StripWidth, WaveLocation = BHD.param['StripWidth'], BHD.param['WaveLocation']

  D = (BHD.B - BHD.A) * 0.5   # Y distance between the inclined subpanel corners
  if WaveLocation == 1: #Default
    if Ymin < -0.1 and Ymax > 0.1:  # Really (!) different signs of limits
      Ysr = 0.0 # central Y coordinate
    else: Ysr = (Ymin + Ymax) * 0.5
  else: #Ask
    while 1:
      res = kcs_ui.real_req("Y location of the symmetry axis of a wave", 0.0)
      if res[0] == _ok:
        Ysr = res[1]
        if Ymin < Ysr < Ymax: break
        else: kcs_ui.message_noconfirm("Wave location outside of the bulkhead's Y limits!")
      else: return -2
  Y = []

# Fetch Y coordinates on PS
  curY = Ysr + 0.5 * BHD.A
  if curY >= Ymax: return -2
  status = 0
  while curY < Ymax:
    Y.append(curY)
    curY = curY + D
    if curY < Ymax:
      Y.append(curY)
      curY = curY + BHD.A
    else:
      status = -1
  if status == 0 and Ymax - Y[-1] < StripWidth: status = 1
  if status >= 0:
    Y.reverse()

# Fetch Y coordinates on SB
    curY = Ysr - 0.5 * BHD.A
    if curY <= Ymin: return -2
    while curY > Ymin:
      Y.append(curY)
      curY = curY - D
      if curY > Ymin:
        Y.append(curY)
        curY = curY - BHD.A
      else:
        status = -1
    if status == 0 and Y[-1] - Ymin < StripWidth: status = 1
    if status >= 0: BHD.Y = Y
  return status

######################################################################
##
## Auxiliary procedure getting the wave dimension from the user
##
######################################################################

def GetBHD_Dimension(msg, max_value, def_value, StartFrom):
  s = msg
  def_v = stringutils.TrimNum(def_value)
  while 1:
    res = kcs_ui.string_req(s, def_v)
    if res[0] == _ok:
      if res[1] == '?':
        pass
      else:
        try:
          v = string.atof(res[1])
          if 1.0 <= v <= max_value: return (StartFrom+1, v)
          else:
            kcs_ui.message_confirm("Input should be positive, and less than (or equal to) %s!" % \
                                   stringutils.TrimNum(max_value, 1))
        except:
          pass
    elif res[0] == _options:
      return (StartFrom-1, def_value) #back
    else:
      return (-2, def_value) #cancel

######################################################################
##
## Auxiliary procedure presenting a choice to the user
##
######################################################################

def GetBHD_Choice(msg, list, StartFrom):
  res = kcs_ui.choice_select("Bulkhead's wave parameters", msg, list)
  if res[0] == _ok:
    return (StartFrom+1, res[1])
  elif res[0] == _options:
    return (StartFrom-1, -1) #back
  else:
    return (-2, -1) #cancel)

######################################################################
##
## Reads the bulkhead's parmeters and finds the Y positions
## of the bulkhead's panels and verifies them
##                                            ^
##       B    B1 C                            | X-axis
##       /-------\           /------\         |
##      /         \         /        \        |
##  ---/           \-------/          \-- ... |
##     A            D                         |
##                                            |
## <------------------------------------------------
##  Y-axis
##
## Parameter A denotes the length of the BC line segment
## Parameter B denotes the horizontal distance between the points A and D
## Parameter C denotes the vertical distance between the points B and A (or C and D)
## Parameter B1 denotes the position of the seam on the BC segment
## The sign of the parameter C indicates the direction in which the bulkhead's
##   "waves" are directed (positive - towards the fore, negative - towards the aft)
## The MSIDE parameter of the PLATE statement is given independently or
##   by default chosen according to the direction of the "wave".
######################################################################

def GetBHD_Params(BHD):
  A, B, B1, C, Thickness, StartFrom = 0.0, 0.0, 0.0, 0.0, 0.0, 0
  list = KcsStringlist.Stringlist("FORE")
  list.AddString("AFT")

  while StartFrom >= 0:
    if StartFrom == 0: # Base 1 (greater) - B
      StartFrom, B = GetBHD_Dimension("Wave's bottom width", 999999.9, B, StartFrom)
    if StartFrom == 1: # Base 2 (smaller) - A
      BHD.B = B
      StartFrom, A = GetBHD_Dimension("Wave's top width", B, A, StartFrom)
    if StartFrom == 2: # Verification of BHD Y positions
      BHD.A = A
      res = GetYCoords(BHD)
      if res == 1:
        st = "At least one of the terminal bulkhead's segments is narrower\n" + \
             "than the allowed width (%0.1f)\n" + \
             "from PS: %0.1f, from SB %0.1f, Continue?"
        st = st % (BHD.param['StripWidth'], BHD.YPS-BHD.Y[0], BHD.Y[-1]-BHD.YSB)
        ans = kcs_ui.answer_req("Bulkhead's dimensions", st)
        if ans != kcs_util.yes(): StartFrom = 0
      elif res < 0:
        kcs_ui.message_confirm("Cannot build the builkhead with these parameters!\n" + \
                               "Try different top & bottom width values ...")
        StartFrom = 0
      B1 = 0.5*A
      if StartFrom == 2: # Seam position - B1
        if BHD.param['AddSeams']:
          StartFrom, B1 = GetBHD_Dimension("Seam position", A, B1, StartFrom)
        else:
          StartFrom, B1 = 3, -1.0
    if StartFrom == 3: # Height - C
      BHD.B1 = B1
      StartFrom, C = GetBHD_Dimension("Wave's height", 999999.9, abs(C), StartFrom)
    if StartFrom == 4: # Wave direction - sign of C
      StartFrom, choice = GetBHD_Choice("The waves are directed towards:", list, StartFrom)
      if choice == 2: BHD.C = -C
      else: BHD.C = C
    if StartFrom == 5: # Material side
      if BHD.param['MaterialSide'] == 1:
        if C < 0: BHD.MSide = "AFT"
        else: BHD.MSide = "FOR"
        StartFrom = 6
      else:
        StartFrom, choice = GetBHD_Choice("Plate's material side", list, StartFrom)
        if StartFrom == 6: BHD.MSide = list.StrList[choice-1]
    if StartFrom == 6: # Material thickness
      StartFrom, Thickness = GetBHD_Dimension("Material thickness", 999, Thickness, StartFrom)
    if StartFrom == 7: # End
      BHD.Thickness = Thickness
      del BHD.position[1:]
      BHD.position.append(BHD.position[0] + BHD.C) #__add__ should make it!!!
      return _ok
  if StartFrom == -1: return _options #back
  else: return _cancel

######################################################################
##
## Returns the location designator for the panel (X plane only!)
##
######################################################################

def GetLocation(Y00, Y01 = -88888):
  if Y01 == -88888: Y01 = Y00
  if Y00 >= 0:
    if Y01 >= 0: loc = "P"
    else: loc = "SP"
  else: loc = "S"
  return loc

######################################################################
##
## Defines a preliminary form of the subpanel boundary statement.
## Additionally returns the data for EXC statements, if any
## Input parameters:
##   LowCoord, HighCoord - min and max value of the Y coordinate
##   SeamCoord           - Y coordinate of the seam
## Expects in BHD:
##   Corners - list of bulkhead's corners
##   Bou     - boundary definition
##   param['BoundaryExcess'] - add excess at boundary (YES/NO)
## In the returned string the substrings __LOW__ and __HIGH__
## correspond to the definitions of the lower, and upper Y limit
##
######################################################################

def SubPanelBoundary(BHD, LowCoord, HighCoord, SeamCoord):
  corners = BHD.Corners
  Bou = BHD.Bou
  nCor = len(corners)
  BouExcess = BHD.param['BoundaryExcess']
  AddS = BHD.param['AddSeams']
  ExcessStmt = [] # list of excess statement data
  SeamLimits = [] # list of limit id's intersected by the seam
  stBOU, first, last = "BOU, ", -99, -99

  Y2, HighY, LowY = corners[0].Y, 0, 0
  for n in range(nCor):
    #Identify the next corner for the segment. Assumes that the boundary 'n'
    #has the first corner 'n' and the last corner ('n'+1) modulo nCor
    n1 = (n + 1) % nCor

    #Identify the coordinate interval for the boundary segment
    Y1, Y2 = Y2, corners[n1].Y
    if Y1 > Y2: minY, maxY = Y2, Y1
    else: minY, maxY = Y1, Y2

    #Test whether the boundary segment overlaps the Low & High coordinate interval
    if minY < LowCoord: overlap = (maxY >= LowCoord)
    else: overlap = (minY <= HighCoord)

    #If yes, add the limit 'n' to the boundary list
    if overlap:
      stBOU, last = stBOU + str(Bou.boundary[n]) + "/ ", n
      if first == -99: first, limID = n, 1
      else: limID = limID + 1
      if AddS != 0 and minY < SeamCoord < maxY: SeamLimits.append(limID)
      if BouExcess:
        try:
          M1 = Bou.boundary[n].excess
          ExcessStmt.append((limID, M1))
        except:
          pass #Excess has not been defined!
    elif last == n-1:
      #If not, just after the last limit add one of the coordinates
      #Low or High as a limit (in a coded form)
      if Y1 > HighCoord:
      	stBOU, HighY = stBOU + "__HIGH__/ ", 1
      else:
      	stBOU, LowY = stBOU + "__LOW__/ ", 1
      limID = limID + 1

#  if first+nCor-last > 1:
  if last == nCor-1 and first > 0:
    if HighY == 0 and LowY == 0:
      if Y1 > Y2:
        stBOU = stBOU + "__LOW__/ "
      else:
        stBOU = stBOU + "__HIGH__/ "
    elif HighY == 1:
      stBOU = stBOU + "__LOW__/ "
    else:
      stBOU = stBOU + "__HIGH__/ "

  return (stBOU[:-2] + ";", ExcessStmt, SeamLimits)

######################################################################
#
# Deletes all subpanels, included in the list 'panels'
# Invoked, when an error occurrs during the bulkhead panel's creation
#
######################################################################

def DelSubpanels(panels):
  print "The subpanels created so far are now deleted from the model"
  print "because of the failure in creation of the bulkhead's panel!"
  for name in panels:
    res = cPanel.pan_delete(name, 1)
    if res[0] == 0: print "Subpanel %s deleted!" % name
    else: print "Subpanel %s NOT deleted!" % name

######################################################################
##
## Generates the knuckled panel. Returns status
## Expects in BHD:
##   Name - name of the panel
##   param - defaults
##   Y - list of Y coordinates of the bulkhead
##   Bou - boundary list of the bulkhead
##   Thickness - plate thickness
##   MSide - material side
##
######################################################################

def MakeBHD_Panel(BHD):
  name = BHD.Name
  nYPos = len(BHD.Y)
  CON = ", CON=" + str(BHD.param['ConnectionCode'])
  SeamExcess = BHD.param['SeamExcess']
  BevelCode = BHD.param['BevelCode']
  AddS = BHD.param['AddSeams']
  model = KcsModel.Model("plane panel")
  panelType, i, iStart, nYP1 = 0, -1, -2, nYPos - 1
  Pos = [str(BHD.position[0]), str(BHD.position[1])]
  RPos = [repr(BHD.position[0]), repr(BHD.position[1])]
  SThickness = "PLA, MAT=" + stringutils.TrimNum(BHD.Thickness,1)+ "," + stringutils.TrimNum(-BHD.Thickness/2,1)  + ", MSI="
  Created = []

  while i<nYPos:
    if i == -1: # first subpanel (from PS)
      Y0, Y1 = 999999.9, BHD.Y[0]
    elif i == nYP1: # last subpanel (from SB)
      Y0, Y1 = BHD.Y[-1], -999999.9
    else:
      Y0, Y1 = BHD.Y[i], BHD.Y[i+1]
    SeamCoord = Y0-BHD.B1
    stBOU, ExcessStmt, SeamLimits = SubPanelBoundary(BHD, Y1, Y0, SeamCoord)
    n, PTrem = panelType >> 1, panelType & 1
    n1 = string.find(stBOU, '__HIGH__')
    if n1 >= 0:
      if PTrem == 1: lim = Pos[n]
      else: lim = "Y=" + stringutils.TrimNum(Y0,1)
      if i>-1: lim = lim + CON
      stBOU = stBOU[:n1] + lim + stBOU[n1+8:]
    n1 = string.find(stBOU, '__LOW__')
    if n1 >= 0:
      if PTrem == 1: lim = Pos[1-n]
      else: lim = "Y=" + stringutils.TrimNum(Y1,1)
      if i<nYP1: lim = lim + CON
      stBOU = stBOU[:n1] + lim + stBOU[n1+7:]

#    loc = GetLocation(Y0, Y1)
    nameSub = name + ("K%03d" % (i+2))
    stPAN = "PAN, '" + nameSub + "', SP, SUB, "

    if PTrem == 0:
      stPAN = stPAN + Pos[n] + ";"
      MS = BHD.MSide
      if AddS != 0 and -1 < i < nYP1:
        stSEA = "SEA"
        if BevelCode != "NONE": stSEA = stSEA + ", BEV=" + BevelCode
        if SeamExcess != "NONE": stSEA = stSEA + ", EXC=" + SeamExcess
        SeamPos = stringutils.TrimNum(SeamCoord, 1)
        stSEA = stSEA + ", Y=" + SeamPos + ";"
      else:
        stSEA = ""
    else:
      stmp = RPos[1-n] + "," + stringutils.TrimNum(Y1,1)
      stPAN = stPAN + "ORI=" + stmp + ",5000, UAX=" + RPos[n] + "," + \
         stringutils.TrimNum(Y0,1) + ",5000, VAX=" + stmp + ",10000;" # Not a terminal segment!
      if BHD.MSide != "FOR": n = 1-n
      if n == 0: MS = "PS"
      else: MS = "PS"
      stSEA = ""
    stPLA1 = SThickness + MS + ";"
    if stSEA == "":
      stPLA = [stPLA1]
    else:
      stPLA = ["POI, NO=1, INT, LIM=%d/Y2=%s;" % (SeamLimits[0], SeamPos), \
               "POI, NO=2, INT, LIM=%d/Y2=P1;" % SeamLimits[1], \
               "POI, NO=3, DU=3, XYZ=P1, X2Y=P2, F=0.5;", \
               stPLA1[:-1] + ", U=P3, V=P3;", \
               "POI, NO=4, DU=-3,XYZ=P1, X2Y=P2, F=0.5;", \
               stPLA1[:-1] + ", U=P4, V=P4;"]
    try:
      try:
        kcs_hullpan.pan_init(nameSub, nameSub + " - subpanel of " + name)

        print stPAN
        kcs_hullpan.stmt_exec(0, stPAN)
        print stBOU
        kcs_hullpan.stmt_exec(0, stBOU)
        if stSEA != "":
          print stSEA
          kcs_hullpan.stmt_exec(0, stSEA)
        for st in stPLA:
          print st
          kcs_hullpan.stmt_exec(0, st)
        for limID, excess in ExcessStmt:
          stEXC = "EXC, LIM=%d, M1=%s;" % (limID, stringutils.TrimNum(excess))
          print stEXC
          kcs_hullpan.stmt_exec(0, stEXC)

        kcs_hullpan.pan_store()
        Created.append(nameSub)
      finally:
        kcs_hullpan.pan_skip() # Always clean up the current panel and scheme
    except:
      print kcs_hullpan.error
      DelSubpanels(Created)
      return -1

    i = i + 1
    panelType = (panelType + 1) & 3
    # Continue to the next subpanel

# Create main (knuckled) panel

  if FeatureSUB_Wildcard == 0:
    st = "PAN, '%s', SP, BLO='%s', DT=191, SUB='%sK*';" % (name, BHD.param['Block'], name)
  else:
    st = "PAN, '%s', SP, BLO='%s', DT=191, SUB='%sK###';" % (name, BHD.param['Block'], name)

  try:
    try:
      kcs_hullpan.pan_init(name, name)
      print st
      kcs_hullpan.stmt_exec(0, st)
      kcs_hullpan.pan_store()
      try:
        model.SetName(name)
        kcs_draft.model_draw(model)
      except:
        pass
    finally:
      kcs_hullpan.pan_skip()
  except:
    print kcs_hullpan.error
    DelSubpanels(Created)
    return -1

  return 0

# Main ########################################

def makeKBHD():
  BHD = _EmptyContainer()         # Storage for all bulkhead's data
  EarlyDesign(BHD)
  StartFrom = 0

  while 1:
    if StartFrom == 0:
      res = GetBHD_Defaults(BHD)
      if res == _ok: StartFrom = 1

    if StartFrom == 1:
      res = GetBHD_Position(BHD)
      if res == _ok: StartFrom = 2

    if StartFrom == 2:
      res = GetBHD_Limits(BHD)
      if res == _ok: StartFrom = 3

    if StartFrom == 3:
      res = GetBHD_Params(BHD)
      if res == _ok: StartFrom = 4

    if StartFrom == 4:
      res = GetBHD_Name(BHD)
      if res == _ok:
        status = MakeBHD_Panel(BHD)
        print status
        break

    if res == _options:
      if StartFrom == 0:
        print _cancel
        break
      else:
        StartFrom = StartFrom - 1
    elif res != _ok:
      print _cancel
      break

#------------------------------------------------------------------------------
#  Menu interface Methods
#------------------------------------------------------------------------------

def getCaption():
  return "Corrugated bulkhead"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  makeKBHD()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
