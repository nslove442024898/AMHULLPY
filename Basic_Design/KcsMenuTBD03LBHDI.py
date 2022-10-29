## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_dex
import kcs_hull
import kcs_ui
import kcs_util
import KcsUtilPan
import KcsUtilPanSch
import KcsTBDVitDef
from KcsMenuTBD08Stiffener import add_stiffening
import math
import string

reload(KcsTBDVitDef)

ok = kcs_util.success()
not_ok = kcs_util.failure()

#------------------------------------------------------------------------------
#  Main Method: Get LBHD definition from user
#------------------------------------------------------------------------------

#  Prompt the user for LBHD_I position.

def defineLBHD_I():
  res = ok
  DefList = KcsTBDVitDef.getDefaults()
  try:
    sti_off = string.atoi(DefList['StiOff'])
  except:
    sti_off = 0

  block = DefList['Block']
  if block == "":
    name = kcs_ui.req_string("Block name")
    if name[0] == ok:
      block = name[1]
    else:
      res = not_ok
  if res == ok:
    longbulk = kcs_ui.req_pick_mod("Pick longitudinal bulkhead",0,0)
    res = longbulk[0]
    if longbulk[1] != "plane panel":
      res = not_ok
  if res == ok:
    tanktop = kcs_ui.req_pick_mod("Pick tanktop",0,0)
    res = tanktop[0]
    if tanktop[1] != "plane panel":
      res = not_ok
  if res == ok:
    aftlim = DefList['AftLim']
    if aftlim != "" and aftlim != "C":
      aftlim = KcsUtilPanSch.getGeo(1,"",aftlim)
    if aftlim == "" or aftlim == "C":
      aftcoord = kcs_ui.req_string("Aft limit")
      if aftcoord[1] != "":
        aftlim = KcsUtilPanSch.getGeo(1,"",aftcoord[1])
    if aftlim == "" or aftlim == "C":
      aftchoice = kcs_ui.req_choice("Aft limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = aftchoice[0]
      if res == ok:
        if aftchoice[1] == 1:
          aftpick = kcs_ui.req_pick_mod("Pick panel for aft limit",0,0)
          res = aftpick[0]
          if res == ok:
            aftlim = KcsUtilPanSch.getRef(aftpick[2])
        else:
          aftlim = KcsUtilPanSch.getDefSurf()

  if res == ok:
    forlim = DefList['ForLim']
    if forlim != "" and forlim != "C":
      forlim = KcsUtilPanSch.getGeo(1,"",forlim)
    if forlim == "" or forlim == "C":
      forcoord = kcs_ui.req_string("Forward limit")
      if forcoord[1] != "":
        forlim = KcsUtilPanSch.getGeo(1,"",forcoord[1])
    if forlim == "" or forlim == "C":
      forchoice = kcs_ui.req_choice("Forward limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = forchoice[0]
      if res == ok:
        if forchoice[1] == 1:
          forpick = kcs_ui.req_pick_mod("Pick panel for forward limit",0,0)
          res = forpick[0]
          if res == ok:
            forlim = KcsUtilPanSch.getRef(forpick[2])
        else:
          forlim = KcsUtilPanSch.getDefSurf()

  if res == ok:
    stiff = DefList['Stiff']
    stipos = DefList['StiPos']
    if stiff == "L" or stiff == "T" or stiff == "Y":
      pdim = kcs_ui.req_string("Stiffener dimensions")
      res = pdim[0]
      if res == ok:
        profdim = pdim[1]
        if stiff == "T":
          profdir = 3
          grid = (KcsUtilPos.frp() == ok)
        else:
          profdir = 1
          grid = 0
        if stipos == "N":
          grid = 0
        if not grid:
          profpart = kcs_ui.req_string("Stiffener partition")
          res = profpart[0]
          try:
            part = string.atoi(profpart[1])
          except:
            res = not_ok
        else:
          part = 0
    else:
      profdir = 0
      profdim = ""
      part = 0
  if res == ok:
    platedim = kcs_ui.req_string("Plate thickness")
    res = platedim[0]
  if res == ok:
    name = KcsUtilPan.getUname(block, block + "-LI_")
    result = make_LBHD_I(name[1],longbulk[2],tanktop[2],aftlim,forlim,profdir,sti_off,profdim,part,platedim[1])

#------------------------------------------------------------------------------
#  Main Method: Make a whole LBHD_I
#------------------------------------------------------------------------------
def make_LBHD_I(name,longbulk,deck,aftlim,forlim,stidir,sti_off,profdim,part,platedim):
  res = ok

#  Get the plane from the panels

  if res == ok:
    pln = KcsUtilPan.getPlane(longbulk)
  if pln[0] == 2:
    lby = pln[1]
  else:
    res = not_ok

  if res == ok:
    pln = KcsUtilPan.getPlane(deck)
  if pln[0] == 3:
    dkz = pln[1]
  else:
    res = not_ok

  if res == ok:
    est = "HULL.PANEL('" + deck + "').NBOU"
    res = kcs_dex.extract(est)
    if res == ok:
      type = kcs_dex.next_result()
      if type == 1:
        nbou = kcs_dex.get_int()

  if res == ok:
    pslim = 1
    dkpsy = -1E8
    for bou in range(nbou):
      est = "HULL.PANEL('" + deck + "').BOU(" + str(bou+1) + ").COR"
      res = kcs_dex.extract(est)
      if res == ok:
        type = kcs_dex.next_result()
        if type == 6:
          cor = kcs_dex.get_reavec2d()
          if cor[1] > dkpsy+1.0:
            dkpsy = cor[1]
            pslim = bou+1

  if res == ok:
    est = "HULL.PANEL('" + longbulk + "').NBOU"
    res = kcs_dex.extract(est)
    if res == ok:
      type = kcs_dex.next_result()
      if type == 1:
        nbou = kcs_dex.get_int()

  if res == ok:
    uplim = 1
    lowlim = 1
    lbupz = -1E8
    lblowz = 1E8
    for bou in range(nbou):
      est = "HULL.PANEL('" + longbulk + "').BOU(" + str(bou+1) + ").COR"
      res = kcs_dex.extract(est)
      if res == ok:
        type = kcs_dex.next_result()
        if type == 6:
          cor = kcs_dex.get_reavec2d()
          if cor[1] < lblowz-1.0:
            lblowz = cor[1]
            lowlim = bou+1
          if cor[1] > lbupz+1.0:
            lbupz = cor[1]
            uplim = bou+1

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    if dkz > lbupz:
      lblim = uplim
      ori = "ORI=0," + str(int(lby)) + "," + str(int(lbupz))
      uax = "UAX=1000," + str(int(lby)) + "," + str(int(lbupz))
      vax = "VAX=0," + str(int(dkpsy)) + "," + str(int(dkz))
    else:
      lblim = lowlim
      ori = "ORI=0," + str(int(dkpsy)) + "," + str(int(dkz))
      uax = "UAX=1000," + str(int(dkpsy)) + "," + str(int(dkz))
      vax = "VAX=0," + str(int(lby)) + "," + str(int(lblowz))
    loc = ori + ", " + uax + ", " + vax
  if res == ok:
    res = kcs_hull.pan_init(name,name+";")
  if res == ok:
    stmt = "PAN,  '" + name + "', SBP, DT=202, " + loc + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    if dkz > lbupz:
      stmt = "BOU,  '" + deck + "', LIM=" + str(pslim) + "/ " + aftlim + "/ '" + longbulk + "', LIM=" + str(lblim) + "/ " + forlim + ";"
    else:
      stmt = "BOU,  '" + longbulk + "', LIM=" + str(lblim) + "/ " + aftlim + "/ '" + deck + "', LIM=" + str(pslim) + "/ " + forlim + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Set plate

  if res == ok:
    stmt = "PLA,  MSI=SB, MAT=" + str(platedim) + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Get the panel box

  if res == ok and profdim != "":
    add_stiffening( name, stidir, "PS", "BOT", profdim, part, part, sti_off)

#  Store and draw the panel. Terminate the scheme.

  if res == ok:
    res = kcs_hull.pan_store()
  if res == ok:
    kcs_ui.pic_draw_mod("plane panel", name, 0)
    kcs_hull.pan_skip()

  return res

#------------------------------------------------------------------------------
#  Menu interface Methods
#------------------------------------------------------------------------------

def getCaption():
  return "Long inclined"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineLBHD_I()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
