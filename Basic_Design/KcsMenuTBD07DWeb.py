## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_dex
import kcs_hull
import kcs_ui
import kcs_util
import KcsUtilPan
import KcsUtilPanSch
import KcsUtilPos
import KcsTBDVitDef
import math
import string

reload(KcsTBDVitDef)

ok = kcs_util.success()
not_ok = kcs_util.failure()

#------------------------------------------------------------------------------
#  Main Method: Get Deck Web definition from user
#------------------------------------------------------------------------------

def defineDeckWeb():
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
    position = kcs_ui.req_string("Deck web position")
    res = position[0]
  if res == ok:
    topcoord = kcs_ui.req_string("Upper limit")
    res = topcoord[0]
  if res == ok:
    topchoice = 0
    if topcoord[1] == "":
      topchoicei = kcs_ui.req_choice("Upper limit: 1=Intersecting Panel 2=Outer shell", 2)
      res = topchoicei[0]
      if res == ok:
        topchoice = topchoicei[1]
        if topchoice == 1:
          toppick = kcs_ui.req_pick_mod("Pick deck for upper limit",0,0)
          res = toppick[0]
          if res == ok:
            toplim = KcsUtilPanSch.getRef(toppick[2])
        else:
          toplim = KcsUtilPanSch.getDefSurf()
    else:
      toplim = KcsUtilPanSch.getGeo(3,"",topcoord[1])

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
    botcoord = kcs_ui.req_string("Offset for lower limit")
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
      if topchoice != 0:
        botlim = toplim + ", SID=BOT, COR=" + botcoord[1]
      else:
        botlim = KcsUtilPanSch.getGeo(3,"",botcoord[1])

  if res == ok:
    platedim = kcs_ui.req_string("Plate thickness")
    res = platedim[0]

  if res == ok:
    if topchoice == 1 and botcoord[1] != "":
      pdim = kcs_ui.req_string("Face plate dimensions")
      res = pdim[0]
    if res == ok:
      profdim = pdim[1]
      if profdim[:3] != "10,":
        profdim = "10," + profdim
    else:
      profdim = ""

  if res == ok:
    pilq = kcs_ui.req_answer("Pillars")
    res = pilq[0]
  if res == ok:
    pillars = pilq[1]
    if pillars == 0:
      pdim = kcs_ui.req_string("Pillar dimensions")
      res = pdim[0]
      if res == ok:
        pildim = pdim[1]
        ppos = kcs_ui.req_string("Pillar positions")
        res = ppos[0]
      if res == ok:
        pilpos = ppos[1]
        pilcoord = kcs_ui.req_string("Lower end of pillar")
        res = pilcoord[0]
      if res == ok:
        if pilcoord[1] == "":
          pilpick = kcs_ui.req_pick_mod("Pick panel for lower end of pillar",0,0)
          res = pilpick[0]
          if res == ok:
            pillim = KcsUtilPanSch.getRef(pilpick[2])
        else:
          pillim = KcsUtilPanSch.getGeo(3,"",pilcoord[1])
          pillim = "Z2" + pillim[:1]

    else:
      pildim = ""
      pilpos = ""
      pillim = ""

  if res == ok:
    if position[1][-3:] == "000":
       pos = position[1][:-3]
    else:
       pos = position[1]
    pos = string.join(string.split(pos, '.'), '')
    pos = string.join(string.split(pos, 'FR-'), 'FR')
    pos = string.join(string.split(pos, '+'), '_')
    pos = string.join(string.split(pos, '-'), '_')
    name = KcsUtilPan.getUname(block, block + "-GX" + pos + "_")
    result = make_DeckWeb(name[1],position[1],sblim,pslim,toplim,botlim,profdim,pildim,pilpos,pillim,platedim[1])

#------------------------------------------------------------------------------
#  Main Method: Make a whole Deck Web
#------------------------------------------------------------------------------

def make_DeckWeb(name,position,sblim,pslim,toplim,botlim,profdim,pildim,pilpos,pillim,platedim):
  res = ok
  lps = (KcsUtilPos.lyp() == ok)

#  The panel name is also used for the scheme.
#  Create the panel.

  if res == ok:
    res = kcs_hull.pan_init(name,name)
  if res == ok:
    loc = "SP"
    stmt = "PAN,  '" + name + "', " + loc + ", DT=102, X=" + position + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Add the boundary

  if res == ok:
    symm = 0
    stmt = "BOU,  " + toplim
    if sblim != toplim:
      stmt = stmt + "/ " + sblim
      if sblim == pslim:
        stmt = stmt + ", REF"
        symm = 1
    if botlim != sblim:
      stmt = stmt + "/ " + botlim
    if pslim != botlim:
      stmt = stmt + "/ " + pslim
    stmt = stmt + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)

#  Set plate

  if res == ok:
    stmt = "PLA,  MAT=" + str(platedim) + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)


#  Set face plate

  if res == ok and profdim != "":
    stmt = "FLA,  PRO=" + profdim + ", LIM=3, CON=14, CUT=1402,50/ CON=14, CUT=1402,50;"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)
    profdim = ""

#  Set pillars

  if res == ok and pildim != "" and pilpos != "":
    if pildim[0] == "4" or pildim[0] == "5" or pildim[0] == "6" or pildim[0] == "7":
      pil_end = "CON=70, CUT=3100"
    elif pildim[0] == "2" or pildim[0] == "3":
      pil_end = "CON=70, CUT=2100"
    else:
      pil_end = "CON=70, CUT=1100"

    pilposlist = KcsUtilPanSch.expandGeoRep( pilpos)
    if pilposlist[0][0][:2] == "LP":
      prefix = "LP"
    else:
      prefix = ""
    pilposn = pilposlist[1]

    if symm:
      npos = len(pilposn)
      for pos in range(npos):
        if (prefix == "LP" and pilposn[pos] > 0) or (prefix == "" and pilposn[pos] > 200):
          if -pilposn[pos] not in pilposn:
             pilposn.append(-pilposn[pos])
    npos = len(pilposn)
    pilpost = KcsUtilPanSch.getGeoRepT(2, prefix, pilposn)
    try:
      thoff = int(platedim)/2
    except:
      thoff = 6
#    for pno in range( npos):
#      if res == ok:
#        stmt = "POI,  R3, CRO, F1, Y=" + prefix + str(pilposn[pno]) + ", TOP, DX=" + str(thoff) + ";"
#        print stmt
#        res = kcs_hull.pan_exec_stmt( 0, stmt)
    stmt = "POI,  R3, CRO, F1, " + pilpost[0] + ", TOP, DX=" + str(thoff) + ";"
    print stmt
    res = kcs_hull.pan_exec_stmt( 0, stmt)
    if res == ok:
      stmt = "POI,  R3, INT, " + pilpost[0] + "/ " + pillim + ", SI2=TOP, DX=" + str(thoff) + ";"
      print stmt
      res = kcs_hull.pan_exec_stmt( 0, stmt)
    if res == ok:
      tppos = []
      for pno in range( npos):
        tppos.append(pno+1)
      pno1 = KcsUtilPanSch.getGeoRepT(0, "P", tppos)
      tppos = []
      for pno in range( npos, 2*npos):
        tppos.append(pno+1)
      pno2 = KcsUtilPanSch.getGeoRepT(0, "P", tppos)
      stmt = "PIL,  PRO=" + pildim + ", DIR=FOR, SID=PS, X1=" + pno1[0] + ", Y1=" + pno1[0] + ", Z1=" + pno1[0] + ", " + pil_end + "/ X2=" + pno2[0] + ", Y2=" + pno2[0] + ", Z2=" + pno2[0] + ", " + pil_end + ";"
      print stmt
      res = kcs_hull.pan_exec_stmt( 0, stmt)

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
  return "Deck web"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineDeckWeb()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
