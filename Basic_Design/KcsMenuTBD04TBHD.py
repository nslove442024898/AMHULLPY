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
#  Main Method: Get TBH definition from user
#------------------------------------------------------------------------------

#  Prompt the user for TBHD position.

def defineTBHD():
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
    position = kcs_ui.req_string("Transversal bulkhead position")
    res = position[0]

  if res == ok:
    topcoord = kcs_ui.req_string("Upper limit")
    res = topcoord[0]
  if res == ok:
    if topcoord[1] == "":
      topchoice = kcs_ui.req_choice("Upper limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = topchoice[0]
      if res == ok:
        if topchoice[1] == 1:
          toppick = kcs_ui.req_pick_mod("Pick panel for upper limit",0,0)
          res = toppick[0]
          if res == ok:
            toplim = KcsUtilPanSch.getRef(toppick[2])
        else:
          toplim = KcsUtilPanSch.getDefSurf()
    else:
      toplim = KcsUtilPanSch.getGeo(3,"",topcoord[1])

  if res == ok:
    botcoord = kcs_ui.req_string("Lower limit")
    res = botcoord[0]
  if res == ok:
    if botcoord[1] == "":
      botchoice = kcs_ui.req_choice("Lower limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = botchoice[0]
      if res == ok:
        if botchoice[1] == 1:
          botpick = kcs_ui.req_pick_mod("Pick panel for lower limit",0,0)
          res = botpick[0]
          if res == ok:
            botlim = KcsUtilPanSch.getRef(botpick[2])
        else:
          botlim = KcsUtilPanSch.getDefSurf()
    else:
      botlim = KcsUtilPanSch.getGeo(3,"",botcoord[1])

  if res == ok:
    pscoord = kcs_ui.req_string("Portside limit")
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
    stiff = DefList['Stiff']
    stipos = DefList['StiPos']
    if stiff == "L" or stiff == "T" or stiff == "Y":
      profsidei = kcs_ui.req_choice("Stiffener side: 1=Aft 2=Forward", 2)
      res = profsidei[0]
      if res == ok:
        if profsidei[1] == 1:
          profside = "AFT"
        else:
          profside = "FOR"
        pdim = kcs_ui.req_string("Stiffener dimensions")
        res = pdim[0]
      if res == ok:
        profdim = pdim[1]
        profdir = 3
        grid = (KcsUtilPos.lyp() == ok)
        if stipos == "N":
          grid = 0
        if not grid:
          part = kcs_ui.req_string("Stiffener partition")
          res = part[0]
          try:
            profpart = string.atoi(part[1])
          except:
            res = not_ok
        else:
          profpart = 0
    else:
      profside = ""
      profdim = ""
      profdir = 0
      profpart = 0
  if res == ok:
    platedim = kcs_ui.req_string("Plate thickness")
    res = platedim[0]
  if res == ok:
    if position[1][-3:] == "000":
       pos = position[1][:-3]
    else:
       pos = position[1]
    pos = string.join(string.split(pos, '.'), '')
    pos = string.join(string.split(pos, 'FR-'), 'FR')
    pos = string.join(string.split(pos, '+'), '_')
    pos = string.join(string.split(pos, '-'), '_')
    name = KcsUtilPan.getUname(block, block + "-X" + pos + "_")
    result = make_TBHD(name[1],position[1],pslim,sblim,toplim,botlim,profside,profdir,sti_off,profdim,profpart,platedim[1])

#------------------------------------------------------------------------------
#  Main Method: Make a whole TBHD
#------------------------------------------------------------------------------
def make_TBHD(name,position,pslim,sblim,toplim,botlim,profside,stidir,sti_off,profdim,part,platedim):
  res = ok
  lps = (KcsUtilPos.lyp() == ok)

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    res = kcs_hull.pan_init(name,name)
  if res == ok:
    if position[:2] == "FR":
      try:
        posint = string.atoi(position[2:])
      except:
        posint = 0
      ptc = kcs_util.pos_to_coord(1,posint)
      posnumb = ptc[1]
    else:
      try:
        posnumb = string.atof(position)
      except:
        posnumb = 0.0
    loc = "SP"
    stmt = "PAN,  '" + name + "', " + loc + ", DT=101, X=" + position + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    stmt = "BOU,  " + botlim
    if pslim != botlim:
      stmt = stmt + "/ " + pslim
    if toplim != pslim:
      stmt = stmt + "/ " + toplim
    if sblim != toplim:
      stmt = stmt + "/ " + sblim
      if sblim == pslim:
        stmt = stmt + ", REF"
    if botlim == "'__HULLFORM__'" and sblim != "'__HULLFORM__'":
      stmt = stmt + "/ " + botlim + ", REF"
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
    add_stiffening( name, stidir, profside, "PS", profdim, part, part, sti_off)

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
  return "Trans bulkhead"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineTBHD()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
