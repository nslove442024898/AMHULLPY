## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_dex
import kcs_hull
import kcs_ui
import kcs_util
import KcsUtilDexPan
import KcsUtilPan
import KcsUtilPanSch
import KcsUtilPos
from KcsPoint2D import Point2D
from KcsVector2D import Vector2D
from KcsVector3D import Vector3D
import KcsTBDVitDef
import math
import string

ok = kcs_util.success()
not_ok = kcs_util.failure()

ask_grid_fact = 0.1

#------------------------------------------------------------------------------
#  getAxis:  get coordinate axis for stiffener position and existence of
#            FR's or LP's along this axis from panel plane and stiffener
#            direction
#------------------------------------------------------------------------------
def getAxis( plane, direction):
  DefList = KcsTBDVitDef.getDefaults()
  stipos = DefList['StiPos']
  if direction == 1:
    if abs(plane) == 2:
      axis = 3
      grid = (KcsUtilPos.lzp() == ok)
    else:
      axis = 2
      grid = (KcsUtilPos.lyp() == ok)
  elif direction == 2:
    if abs(plane) == 1:
      axis = 3
      grid = (KcsUtilPos.lzp() == ok)
    else:
      axis = 1
      grid = (KcsUtilPos.frp() == ok)
  else:
    if abs(plane) == 1:
      axis = 2
      grid = (KcsUtilPos.lyp() == ok)
    else:
      axis = 1
      grid = (KcsUtilPos.frp() == ok)
  if stipos == "N":
    grid = 0

  return (axis, grid)

#------------------------------------------------------------------------------
#  Main Method: Get stiffener definition from user
#------------------------------------------------------------------------------

def defineStiffening():
  res = ok

  DefList = KcsTBDVitDef.getDefaults()
  try:
    offset = string.atoi(DefList['StiOff'])
  except:
    offset = 0

  cont = not_ok
  pdim = kcs_ui.req_string("Stiffener dimensions")
  res = pdim[0]
  if res == ok:
    profdim = pdim[1]
    cont = ok
    kcs_ui.init_highlight()
    pan = kcs_ui.req_pick_mod("Pick panel",1,2)
    cont = pan[0]
  while cont == ok:
    if pan[1] != "plane panel":
      kcs_ui.message_confirm("Not a planar panel")
      res = not_ok
    if res == ok:
      panel = pan[2]

    if res == ok:
      plane = KcsUtilPan.getPlane( panel)

    if res == ok:
      if abs(plane[0]) == 1:
        pdir = kcs_ui.req_choice("Stiffener direction: 1=Vertical 2=Horizontal", 2)
        res = pdir[0]
        if pdir[1] == 1:
          direction = 3
        else:
          direction = 2
      else:
        pdir = kcs_ui.req_choice("Stiffener direction: 1=Longitudinal 2=Transversal", 2)
        res = pdir[0]
        if pdir[1] == 1:
          direction = 1
        else:
          if abs(plane[0]) == 3:
            direction = 2
          else:
            direction = 3

    if res == ok:
      if abs(plane[0]) == 1:
        psid = kcs_ui.req_choice("Stiffener side: 1=Aft 2=Forward", 2)
        res = psid[0]
        if psid[1] == 1:
          side = "AFT"
        else:
          side = "FOR"
      elif abs(plane[0]) == 2:
        psid = kcs_ui.req_choice("Stiffener side: 1=Portside 2=Starboard", 2)
        res = psid[0]
        if psid[1] == 1:
          side = "PS"
        else:
          side = "SB"
      else:
        side = "BOT"

    if res == ok:
      gax = getAxis( plane[0], direction)
      axis = gax[0]
      grid = gax[1]
      if axis == 1:
        comp = plane[5].X
      elif axis == 2:
        comp = plane[5].Y
      else:
        comp = plane[5].Z

      if axis == 1 :
        psid = kcs_ui.req_choice("Stiffener material side: 1=Aft 2=Forward", 2)
        res = psid[0]
        if psid[1] == 1:
          matside = "AFT"
        else:
          matside = "FOR"
      elif axis == 2 :
        psid = kcs_ui.req_choice("Stiffener material side: 1=Portside 2=Starboard", 2)
        res = psid[0]
        if psid[1] == 1:
          matside = "PS"
        else:
          matside = "SB"
      else:
        psid = kcs_ui.req_choice("Stiffener material side: 1=Top 2=Bottom", 2)
        res = psid[0]
        if psid[1] == 1:
          matside = "TOP"
        else:
          matside = "BOT"

    if res == ok:
      if not grid or comp > ask_grid_fact:
        profpart = kcs_ui.req_string("Stiffener partition")
        res = profpart[0]
        try:
          part = string.atoi(profpart[1])
        except:
          if profpart[1] == '':
            part = 0
          else:
            res = not_ok
        profpart = kcs_ui.req_string("Distance from edge for first stiffener")
        res = profpart[0]
        try:
          dist = string.atoi(profpart[1])
        except:
          if profpart[1] == '':
            dist = part
          else:
            res = not_ok
      else:
        part = 0
        dist = 0

    if res == ok:
      res = kcs_hull.pan_modify(panel, 2)
    if res == ok:
      res = kcs_hull.pan_recreate()
    if res == ok:
      res = add_stiffening( panel, direction, side, matside, profdim, dist, part, offset)

#  Store and draw the panel. Terminate the scheme.

    if res == ok:
      res = kcs_hull.pan_store()
    if res == ok:
      kcs_ui.pic_draw_mod("plane panel", panel, 0)
      kcs_hull.pan_skip()

    if res == ok:
      kcs_ui.terminate_highlight()
      kcs_ui.init_highlight()
      pan = kcs_ui.req_pick_mod("Pick panel",1,2)
      cont = pan[0]
    else:
      cont = not_ok

  kcs_ui.terminate_highlight()

#------------------------------------------------------------------------------
#  Main Method: Add stiffening on coordinate to plane panel
#------------------------------------------------------------------------------
def add_stiffening( panel, direction, side, matside, profdim, dist, part, offset):
  res = ok

#  Get the panel box

  if res == ok:
    box = KcsUtilPan.getBox( panel)
    res = box[0]

  if res == ok:
    plane = KcsUtilPan.getPlane( panel)
    gax = getAxis( plane[0], direction)
    axis = gax[0]
    grid = gax[1]

    if part > 0:
      grid = 0
    elif not grid:
      res = not_ok

  if res == ok:
    if not grid:
      if axis == 1:
        avec = Vector3D( plane[3].X, plane[4].X, plane[5].X)
      elif axis == 2:
        avec = Vector3D( plane[3].Y, plane[4].Y, plane[5].Y)
      else:
        avec = Vector3D( plane[3].Z, plane[4].Z, plane[5].Z)
      if avec.X < avec.Y:
        axis = -2
      else:
        axis = -1

    if grid:
      if axis == 1:
        prefix = "FR"
      else:
        prefix = "LP"
    else:
      prefix = ""

    if axis == -1:
      if dist > 0:
        min = box[1] + dist
      else:
        min = box[1] + offset
      max = box[2] - offset
    elif axis == -2:
      if dist > 0:
        min = box[3] + dist
      else:
        min = box[3] + offset
      max = box[4] - offset
    else:
      if abs(plane[0]) == 1:
        if axis == 2:
          min = box[1] + plane[2].Y
          max = box[2] + plane[2].Y
        else:
          min = box[3] + plane[2].Z
          max = box[4] + plane[2].Z
      elif abs(plane[0]) == 2:
        if axis == 1:
          min = box[1] + plane[2].X
          max = box[2] + plane[2].X
        else:
          min = box[3] + plane[2].Z
          max = box[4] + plane[2].Z
      else:
        if axis == 1:
          min = box[1] + plane[2].X
          max = box[2] + plane[2].X
        else:
          min = box[3] + plane[2].Y
          max = box[4] + plane[2].Y
      min = min + offset
      max = max - offset

    if side == "":
      if abs(plane[0]) == 1:
        side == "AFT"
      elif abs(plane[0]) == 2:
        side == "PS"
      else:
        side == "BOT"

    if matside == "":
      if abs(plane[0]) == 2:
        matside == "BOT"
      else:
        matside == "SB"

#
    rev = ""
    if direction == 1:
      if matside == "SB" or matside == "BOT":
        rev = ", REV"
    elif direction == 2:
      if matside == "FOR" or matside == "BOT":
        rev = ", REV"
    else:
      if matside == "FOR" or matside == "PS":
        rev = ", REV"

    if grid:
      ctp = kcs_util.coord_to_pos( axis, max)
      if ctp[2] < 0.0:
        high = ctp[1]-1
      else:
        high = ctp[1]
      ctp = kcs_util.coord_to_pos( axis, min)
      if ctp[2] > 0.0:
        low = ctp[1]+1
      else:
        low = ctp[1]
    else:
      prefix = ""

#  Set longitudinals

  if res == ok:
    if profdim[0] == "4":
      long_end = "CON=15, CUT=3100"
    elif profdim[0] == "2" or profdim[0] == "3":
      long_end = "CON=15, CUT=2100"
    else:
      long_end = "CON=15, CUT=1100"

    if axis != 2 or (axis == 2 and max > 0.0):
      if axis == 2 and min < 0.0:
        if grid:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, 0, 1, high)
        else:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, 0, part, int(max))
      else:
        if grid:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, low, 1, high)
        else:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, int(min), part, int(max))
      for spno in range( len(stipos)):
        stmt = "STI,  PRO=" + profdim + ", SID=" + side + ", " + stipos[spno] + rev + ", " + long_end + "/ " + long_end + ";"
        print stmt
        res = kcs_hull.pan_exec_stmt( 0, stmt)
    if axis == 2 and min < 0.0:
      if rev == "":
        rev = ", REV"
      else:
        rev = ""
      if max > 0.0:
        if grid:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, -1, -1, low)
        else:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, -part, -part, int(min))
      else:
        if grid:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, high, -1, low)
        else:
          stipos = KcsUtilPanSch.getGeoRepSSE( axis, prefix, int(max), -part, int(min))
      for spno in range( len(stipos)):
        stmt = "STI,  PRO=" + profdim + ", SID=" + side + ", " + stipos[spno] + rev + ", " + long_end + "/ " + long_end + ";"
        print stmt
        res = kcs_hull.pan_exec_stmt( 0, stmt)

  return res

#------------------------------------------------------------------------------
#  Menu interface Methods
#------------------------------------------------------------------------------

def getCaption():
  return "Stiffening"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  defineStiffening()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
