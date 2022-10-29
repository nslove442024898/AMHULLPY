## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft17.py
#
#      PURPOSE:
#
#          This program removes hidden lines from a user-indicated view
#
import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   view_handle = None

   try:
      kcs_ui.message_confirm('This script shows how to remove hidden lines from user-indicated view.')

      # select view
      point   = KcsPoint2D.Point2D()
      resp, point = kcs_ui.point2D_req('Indicate a view where to remove hidden lines', point)
      if resp:
         try:
            view_handle = kcs_draft.view_identify(point)
         except:
            CommonSample.ReportTribonError(kcs_draft)

   except:
      CommonSample.ReportTribonError(kcs_ui)

   # remove hidden lines from selected view
   if view_handle != None:
      try:
         kcs_draft.view_hl_remove(view_handle)
         kcs_ui.message_noconfirm('All hidden lines are removed!')
      except:
         CommonSample.ReportTribonError(kcs_draft)
   else:
      kcs_ui.message_noconfirm('View not defined!')

except:
   pass
