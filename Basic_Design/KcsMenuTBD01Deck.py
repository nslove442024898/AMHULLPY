## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_dex
import kcs_hull
import kcs_ui
import kcs_util
import KcsUtilDexPan
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
#  Main Method: Get deck definition from user
#------------------------------------------------------------------------------

def defineDeck():
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
    decktype = kcs_ui.req_choice("Deck type: 1=Flat 2=Cranked 3=Raising", 3)
    res = decktype[0]
  if res == ok:

#  If it is a cranked deck, prompt the user for height, knuckle line
#  and height and halfbreadth. Otherwise just for the height

    if decktype[1] == 2:
      position = kcs_ui.req_string("Height of mid part")
      res = position[0]
      if res == ok:
        cline = kcs_ui.req_string("Knuckle line position")
        res = cline[0]
      if res == ok:
        pslim = KcsUtilPanSch.getGeo(2,"",cline[1])
        if cline[1][:2] == "LP":
#Change sign
          sblim = string.join(string.split(cline[1], '+'), '_')
          sblim = string.join(string.split(sblim, '-'), ';')
          sblim = string.join(string.split(sblim, '_'), '-')
          sblim = string.join(string.split(sblim, ';'), '+')
          sblim = KcsUtilPanSch.getGeo(2,"","LP-" + sblim[2:])
        else:
          sblim = KcsUtilPanSch.getGeo(2,"","-" + cline[1])
        ch = kcs_ui.req_string("Height at shell and halfbreadth")
        res = ch[0]
      if res == ok:
        chl = string.split(ch[1])
        shellpos = chl[0]
        halfbreadth = chl[1]
    elif decktype[1] == 3:
      aps = kcs_ui.req_string("Aft position and height")
      res = aps[0]
      if res == ok:
        aftpos = string.split(aps[1])
        fps = kcs_ui.req_string("Forward position and height")
        res = fps[0]
      if res == ok:
        forpos = string.split(fps[1])
        origin = ( aftpos[0], "0", aftpos[1])
        uaxis = ( forpos[0], "0", forpos[1])
        vaxis = ( aftpos[0], "1000", aftpos[1])
        position = aps
    else:
      position = kcs_ui.req_string("Deck height")
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

  if res == ok and (decktype[1] == 1 or decktype[1] == 3):
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
    if decktype[1] == 3:
      pos = string.join(string.split(pos, ' '), '_')
      pos = string.join(string.split(pos, '.'), '')
      name = KcsUtilPan.getUname(block, block + "-ZR" + pos + "_")
    else:
      pos = string.join(string.split(pos, '.'), '')
      name = KcsUtilPan.getUname(block, block + "-Z" + pos + "_")
    if decktype[1] == 2:
      cname = KcsUtilPan.getUname(block, block + "-ZI" + pos + "_")

    if decktype[1] == 2:
      res = make_cranked_deck(name[1],cname[1],position[1],shellpos,halfbreadth,aftlim,forlim,pslim,sblim,profdir,profdim,part,sti_off,platedim[1])
    elif decktype[1] == 3:
      res = make_sloping_deck(name[1],"SP",origin,uaxis,vaxis,aftlim,forlim,pslim,sblim,profdir,profdim,part,sti_off,platedim[1])
    else:
      res = make_flat_deck(name[1],position[1],aftlim,forlim,pslim,sblim,profdir,profdim,part,sti_off,platedim[1])

#------------------------------------------------------------------------------
#  make_cranked_deck
#------------------------------------------------------------------------------
def make_cranked_deck(name,cname,position,shellpos,halfbreadth,aftlim,forlim,pslim,sblim,stidir,profdim,part,offset,platedim):
  res = make_flat_deck(name,position,aftlim,forlim,pslim,sblim,stidir,profdim,part,0,platedim)
  if res == ok:
    sblim = pslim
    pslim = KcsUtilPanSch.getDefSurf()
    origin = ("0",sblim[2:],position)
    uaxis = ("1000",sblim[2:],position)
    vaxis = ("0",halfbreadth,shellpos)
    res = make_sloping_deck( cname, "SBP", origin, uaxis, vaxis, aftlim, forlim, pslim, sblim, stidir, profdim, part, 0, platedim)

#------------------------------------------------------------------------------
#  make_flat_deck
#------------------------------------------------------------------------------
def make_flat_deck(name,position,aftlim,forlim,pslim,sblim,stidir,profdim,part,offset,platedim):
  res = ok

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    res = kcs_hull.pan_init(name,name)
  if res == ok:
    stmt = "PAN,  '" + name + "', SP, DT=301, Z=" + position + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    stmt = "BOU,  " + pslim
    if aftlim != pslim:
      stmt = stmt + "/ " + aftlim
    if sblim != aftlim or (sblim == aftlim and sblim == pslim):
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
    add_stiffening( name, stidir, "BOT", "PS", profdim, part, part, offset)

#  Store and draw the panel. Terminate the scheme.

  if res == ok:
    res = kcs_hull.pan_store()
  if res == ok:
    kcs_ui.pic_draw_mod("plane panel", name, 0)
    kcs_hull.pan_skip()

  return res

#------------------------------------------------------------------------------
#  make_sloping_deck
#------------------------------------------------------------------------------
def make_sloping_deck( name, symm, origin, uaxis, vaxis, aftlim, forlim, pslim, sblim, stidir, profdim, part, offset, platedim):
  res = ok

#  Create the cranked panel.

  if res == ok:
    res = kcs_hull.pan_init( name, name)
    ori = "ORI=" + str(origin[0]) + "," + str(origin[1]) + "," + str(origin[2])
    uax = "UAX=" + str(uaxis[0]) + "," + str(uaxis[1]) + "," + str(uaxis[2])
    vax = "VAX=" + str(vaxis[0]) + "," + str(vaxis[1]) + "," + str(vaxis[2])
    loc = ori + ", " + uax + ", " + vax
  if res == ok:
    stmt = "PAN,  '" + name + "', " + symm + ", DT=302, " + loc + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    stmt = "BOU,  " + pslim
    if symm == "SBP" and pslim == "'__HULLFORM__'":
      stmt = stmt + ", YMI=" + sblim[2:]
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
    add_stiffening( name, stidir, "BOT", "PS", profdim, part, part, offset)

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
  return "Deck"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineDeck()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
