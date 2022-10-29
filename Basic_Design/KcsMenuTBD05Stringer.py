## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_dex
import kcs_hull
import kcs_ui
import kcs_util
import KcsUtilPan
import KcsUtilPanSch
import KcsUtilPos
import KcsTBDVitDef
from KcsMenuTBD08Stiffener import add_stiffening
import math
import string

reload(KcsTBDVitDef)

ok = kcs_util.success()
not_ok = kcs_util.failure()

#------------------------------------------------------------------------------
#  Main Method: Get Stringer definition from user
#------------------------------------------------------------------------------

def defineStringer():
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
    position = kcs_ui.req_string("Stringer height")
    res = position[0]
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
    pscoord = kcs_ui.req_string("Portside limit")
    res = pscoord[0]
  if res == ok:
    if pscoord[1] == "":
      pschoice = kcs_ui.req_choice("Portside limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = pschoice[0]
      if res == ok:
        if pschoice[1] == 1:
          pspick = kcs_ui.req_pick_mod("Pick panel for portside limit",0,0)
          res = pspick[0]
          if res == ok:
            pslim = KcsUtilPanSch.getRef(pspick[2])
        else:
          pslim = KcsUtilPanSch.getDefSurf()
    else:
      pslim = KcsUtilPanSch.getGeo(2,"",pscoord[1])
  if res == ok:
    sbcoord = kcs_ui.req_string("Starboard limit")
    res = sbcoord[0]
  if res == ok:
    if sbcoord[1] == "":
      sbchoice = kcs_ui.req_choice("Starboard limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = sbchoice[0]
      if res == ok:
        if sbchoice[1] == 1:
          sbpick = kcs_ui.req_pick_mod("Pick panel for starboard limit",0,0)
          res = sbpick[0]
          if res == ok:
            sblim = KcsUtilPanSch.getRef(sbpick[2])
        else:
          sblim = KcsUtilPanSch.getDefSurf()
    else:
      sblim = KcsUtilPanSch.getGeo(2,"",sbcoord[1])
  if res == ok:
    outerlim = KcsUtilPanSch.getDefSurf()
  if res == ok:
    stiff = DefList['Stiff']
    stipos = DefList['StiPos']
    if stiff == "L" or stiff == "T" or stiff == "Y":
      pdim = kcs_ui.req_string("Stiffener dimensions")
      res = pdim[0]
      if res == ok:
        profdim = pdim[1]
        if stiff == "T":
          profdir = 2
          grid = (KcsUtilPos.frp() == ok)
        else:
          profdir = 1
          grid = (KcsUtilPos.lyp() == ok)
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
    if position[1][-3:] == "000":
       pos = position[1][:-3]
    else:
       pos = position[1]
    pos = string.join(string.split(pos, '.'), '')
    pos = string.join(string.split(pos, '+'), '_')
    pos = string.join(string.split(pos, '-'), '_')
    name = KcsUtilPan.getUname(block, block + "-Z" + pos + "_")
    result = make_Stringer(name[1],position[1],aftlim,forlim,pslim,sblim,profdir,sti_off,profdim,part,platedim[1])

#------------------------------------------------------------------------------
#  Main Method: Make a whole Stringer
#------------------------------------------------------------------------------

def make_Stringer(name,position,aftlim,forlim,pslim,sblim,stidir,sti_off,profdim,part,platedim):
  res = ok
  lps = (KcsUtilPos.lyp() == ok)

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    res = kcs_hull.pan_init(name,name)
  if res == ok:
    stmt = "PAN,  '" + name + "', SBP, DT=302, Z=" + position + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    stmt = "BOU,  " + pslim
    if aftlim != pslim:
      stmt = stmt + "/ " + aftlim
    if sblim != aftlim:
      stmt = stmt + "/ " + sblim
      if sblim == pslim:
        stmt = stmt + ", REF"
    if forlim != sblim:
      stmt = stmt + "/ " + forlim
    stmt = stmt + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Set plate

  if res == ok:
    stmt = "PLA,  MAT=" + str(platedim) + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add stiffening

  if res == ok and profdim != "":
    add_stiffening( name, stidir, "BOT", "PS", profdim, part, part, sti_off)

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
  return "Stringer"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineStringer()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
