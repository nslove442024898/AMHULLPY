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
#  Main Method: Get LBH definition from user
#------------------------------------------------------------------------------

#  Prompt the user for LBHD position.

def defineLBHD():
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
    position = kcs_ui.req_string("Longitudinal bulkhead position")
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
    stiff = DefList['Stiff']
    stipos = DefList['StiPos']
    if stiff == "L" or stiff == "T" or stiff == "Y":
      profsidei = kcs_ui.req_choice("Stiffener side: 1=Portside 2=Starboard", 2)
      res = profsidei[0]
      if res == ok:
        if profsidei[1] == 1:
          profside = "PS"
        else:
          profside = "SB"
        pdim = kcs_ui.req_string("Stiffener dimensions")
        res = pdim[0]
      if res == ok:
        profdim = pdim[1]
        if stiff == "T":
          profdir = 3
          grid = (KcsUtilPos.frp() == ok)
        else:
          profdir = 1
          grid = (KcsUtilPos.lzp() == ok)
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
      if res == ok:
        if not grid:
          dist = kcs_ui.req_string("Distance from edge for first stiffener")
          res = dist[0]
          if dist[1] == "":
            profdist = profpart
          else:
            try:
              profdist = string.atoi(dist[1])
            except:
              res = not_ok
        else:
          profdist = 0
    else:
      profside = ""
      profdir = 0
      profdim = ""
      profpart = 0
      profdist = 0
  if res == ok:
    platedim = kcs_ui.req_string("Plate thickness")
    res = platedim[0]
  if res == ok:
    if position[1][-3:] == "000":
       pos = position[1][:-3]
    else:
       pos = position[1]
    pos = string.join(string.split(pos, '.'), '')
    pos = string.join(string.split(pos, 'LP-'), 'LP')
    pos = string.join(string.split(pos, '+'), '_')
    pos = string.join(string.split(pos, '-'), '_')
    name = KcsUtilPan.getUname(block, block + "-Y" + pos + "_")
    result = make_LBHD(name[1],position[1],aftlim,forlim,toplim,botlim,profside,profdir,sti_off,profdim,profpart,profdist,platedim[1])

#------------------------------------------------------------------------------
#  Main Method: Make a whole LBHD
#------------------------------------------------------------------------------
def make_LBHD(name,position,aftlim,forlim,toplim,botlim,profside,stidir,sti_off,profdim,part,profdist,platedim):
  res = ok
  lps = (KcsUtilPos.lzp() == ok)

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    res = kcs_hull.pan_init(name,name)
  if res == ok:
    if position[:2] == "LP":
      try:
        posint = string.atoi(position[2:])
      except:
        posint = 0
      ptc = kcs_util.pos_to_coord(2,posint)
      posnumb = ptc[1]
    else:
      try:
        posnumb = string.atof(position)
      except:
        posnumb = 0.0
    if posnumb < 50 or position == "LP0":
       loc = "SP"
    else:
       loc = "SBP"
    stmt = "PAN,  '" + name + "', " + loc + ", DT=201, Y=" + position + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    stmt = "BOU,  " + toplim
    if aftlim != toplim:
      stmt = stmt + "/ " + aftlim
    if botlim != aftlim:
      stmt = stmt + "/ " + botlim
    if forlim != botlim:
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
    add_stiffening( name, stidir, profside, "BOT", profdim, profdist, part, sti_off)

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
  return "Long bulkhead"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineLBHD()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
