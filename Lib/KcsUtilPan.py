## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#-----------------------------------------------------------------------------
#  Panel utility methods
#-----------------------------------------------------------------------------

import kcs_dex
import kcs_util
import KcsUtilDexPan
from KcsPoint2D import Point2D
from KcsPoint3D import Point3D
from KcsVector3D import Vector3D
import string

ok = kcs_util.success()
not_ok = kcs_util.failure()


#-----------------------------------------------------------------------------
#  Extract the least circumscribed box of the panel
#-----------------------------------------------------------------------------

def getBox( pan_name):
  umin = 1000000000.0
  vmin = 1000000000.0
  umax = -1000000000.0
  vmax = -1000000000.0
  res = not_ok
  start = []
  end = []
  st = "HULL.PANEL('" + pan_name + "').OUT.NSEG"
  kcs_dex.extract(st)
  a = kcs_dex.next_result()
  nseg = -1
  if a == 1:
    nseg = kcs_dex.get_int()
    for i in range (nseg):
      st = 'HULL.PANEL(\'' + pan_name + '\').OUT.SEG(' + `i+1` +  ').START'
      kcs_dex.extract(st)
      a = kcs_dex.next_result()
      if a == 6:
        start.append(kcs_dex.get_reavec2d())
      st = 'HULL.PANEL(\'' + pan_name + '\').OUT.SEG(' + `i+1` +  ').END'
      kcs_dex.extract(st)
      a = kcs_dex.next_result()
      if a == 6:
        end.append(kcs_dex.get_reavec2d())

#  Calculate the least circumscribed box parallel to the principal axes.

    for i in range(nseg):
      if start[i][0] < umin:
        umin = start[i][0]
      if start[i][0] > umax:
        umax = start[i][0]
      if end[i][0] < umin:
        umin = end[i][0]
      if end[i][0] > umax:
        umax = start[i][0]
      if start[i][1] < vmin:
        vmin = start[i][1]
      if start[i][1] > vmax:
        vmax = start[i][1]
      if end[i][1] < vmin:
        vmin = end[i][1]
      if end[i][1] > vmax:
        vmax = start[i][1]
    res = ok
  result = []
  result.append(res)
  result.append(umin)
  result.append(umax)
  result.append(vmin)
  result.append(vmax)
  return result

#-----------------------------------------------------------------------------
#  Extract the panel plane
#-----------------------------------------------------------------------------

def getPlane( pan_name):
  res = not_ok
  plane = 0
  coord = 0.0
  est = "HULL.PANEL('" + pan_name + "').TRA"
  res = kcs_dex.extract(est)
  if res == ok:
    type = kcs_dex.next_result()
    if type >= 25:
      ux = kcs_dex.get_indexedreal(0)
      uy = kcs_dex.get_indexedreal(1)
      uz = kcs_dex.get_indexedreal(2)
      vx = kcs_dex.get_indexedreal(4)
      vy = kcs_dex.get_indexedreal(5)
      vz = kcs_dex.get_indexedreal(6)
      wx = kcs_dex.get_indexedreal(8)
      wy = kcs_dex.get_indexedreal(9)
      wz = kcs_dex.get_indexedreal(10)
      ox = kcs_dex.get_indexedreal(12)
      oy = kcs_dex.get_indexedreal(13)
      oz = kcs_dex.get_indexedreal(14)
      if abs( abs(wx) - 1.0) < 0.0001:
        plane = 1
        coord = ox
      elif abs( abs(wy) - 1.0) < 0.0001:
        plane = 2
        coord = oy
      elif abs( abs(wz) - 1.0) < 0.0001:
        plane = 3
        coord = oz
      if plane == 0:
        if abs(wx) > abs(wy) and abs(wx) > abs(wz):
          plane = -1
          coord = ox
        elif abs(wy) > abs(wz):
          plane = -2
          coord = oy
        else:
          plane = -3
          coord = oz
    else:
      res = not_ok

  if res != ok:
     return None
  result = []
  result.append(plane)
  result.append(coord)
  result.append(Point3D(ox,oy,oz))
  result.append(Vector3D(ux,uy,uz))
  result.append(Vector3D(vx,vy,vz))
  result.append(Vector3D(wx,wy,wz))
  return result

#-----------------------------------------------------------------------------
#  Extract limit ends
#-----------------------------------------------------------------------------

def getLimitEnds( pan_name, limit):
  res = not_ok
  est = "HULL.PANEL('" + pan_name + "').NBOU"
  nbou = KcsUtilDexPan.getIntegerValue(est)
  if limit < 1 or limit > nbou:
    return None
  est = "HULL.PANEL('" + pan_name + "').BOU(" + str(limit) + ").COR"
  sp = KcsUtilDexPan.getRealVector2D(est)
  if limit == nbou:
    est = "HULL.PANEL('" + pan_name + "').BOU(1).COR"
  else:
    est = "HULL.PANEL('" + pan_name + "').BOU(" + str(limit+1) + ").COR"
  ep = KcsUtilDexPan.getRealVector2D(est)

  result = []
  result.append(Point2D(sp[0],sp[1]))
  result.append(Point2D(ep[0],ep[1]))
  return result

#-----------------------------------------------------------------------------
#  Get a unique panel name
#-----------------------------------------------------------------------------

def getUname( block, pan_gen):
  res = not_ok
  maxno = 0
  est = "HULL.BLOCK('" + block + "').PANEL('" + pan_gen + "'*).NAME"
  res = kcs_dex.extract(est)
  if res == ok:
    cont = ok
    while cont == ok:
      type = kcs_dex.next_result()
      if type == 3:
        pan_name = kcs_dex.get_string()
        numbstr = pan_name[len(pan_gen):]
        try:
          numb = string.atoi(numbstr)
        except:
          numb = 0
        else:
          if numb > maxno:
            maxno = numb
      else:
        cont = not_ok
  pan_name = pan_gen + str(maxno+1)
  result = []
  result.append(res)
  result.append(pan_name)
  return result

#-----------------------------------------------------------------------------
#  Main body
#-----------------------------------------------------------------------------

if __name__ == "__main__":
  print "KcsUtilPan"
