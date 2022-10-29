## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft12.py
#
#      PURPOSE:
#
#          This program places a symbol positioned by user, in the current drawing.
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import CommonSample

try:
   kcs_ui.message_confirm('This script will create a symbol.')

   fontno = 21
   symbolsperrow = 15
   res = kcs_ui.symbol_select( "Select symbol", fontno, symbolsperrow)

   if res[0] == kcs_util.ok():
      symbno = res[1]
      try:
         mess = "Please locate the symbol"
         coord = KcsPoint2D.Point2D()
         res = kcs_ui.point2D_req( mess, coord)
         if res[0] == kcs_util.ok():
            try:
               symb_handle = kcs_draft.symbol_new(fontno,symbno,coord)
            except:
               CommonSample.ReportTribonError(kcs_draft)
         else:
            print "User interrupted"
      except:
         CommonSample.ReportTribonError(kcs_ui)
   else:
      print "User interrupted"
except:
   CommonSample.ReportTribonError(kcs_ui)
