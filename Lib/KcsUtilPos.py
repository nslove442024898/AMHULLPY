## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import string
import kcs_ui
import kcs_util

ok = kcs_util.success()
not_ok = kcs_util.failure()
bigcoord = 1e6

#-----------------------------------------------------------------------------
#  Utility methods to check if frame or longitudinal positions exist
#-----------------------------------------------------------------------------

def frp():
  frs = ok
  frpp = kcs_util.coord_to_pos(1,bigcoord)
  frpn = kcs_util.coord_to_pos(1,-bigcoord)
  if (frpp[1] == 0 and frpp[2] == bigcoord) or (frpn[1] == 0 and frpn[2] == -bigcoord):
    frs = not_ok
  return frs

def lyp():
  lps = ok
  lp = kcs_util.coord_to_pos(2,bigcoord)
  if lp[1] == 0 and lp[2] == bigcoord:
    lps = not_ok
  return lps

def lzp():
  lps = ok
  lp = kcs_util.coord_to_pos(3,bigcoord)
  if lp[1] == 0 and lp[2] == bigcoord:
    lps = not_ok
  return lps

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  print "Self test"
  if frp() == ok:
    print "Frame positions exist"
  else:
    print "No frame positions exist"
  if lyp() == ok:
    print "Longitudinal horizontal (Y) positions exist"
  else:
    print "No longitudinal horizontal (Y) positions exist"
  if lzp() == ok:
    print "Longitudinal vertical (Z) positions exist"
  else:
    print "No longitudinal vertical (Z) positions exist"
