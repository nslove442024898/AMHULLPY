## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft14.py
#
#      PURPOSE:
#
#          This program creates a rectangle in the current drawing and puts a hatch to it.
#          Both the rectangle and the hatch is then deleted after user confirmation.
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsCircle2D
import KcsPoint2D
import KcsRectangle2D
import CommonSample


#-------------------------------------------------------------------------------------------------------------
def DefineRectangle():              # allows user to define rectangle
   point1 = KcsPoint2D.Point2D()
   point2 = KcsPoint2D.Point2D()

   try:
      resp, point1 = kcs_ui.point2D_req('Select first corner of rectangle', point1)
      if resp == kcs_util.ok():
         resp, point2 = kcs_ui.point2D_req('Select first corner of rectangle', point2)
         if resp == kcs_util.ok():
            rectangle = KcsRectangle2D.Rectangle2D(point1, point2)
            try:
               return kcs_draft.rectangle_new(rectangle)
            except:
               CommonSample.ReportTribonError(kcs_draft)
   except:
      CommonSample.ReportTribonError(kcs_ui)

   return None

#-------------------------------------------------------------------------------------------------------------
def CreateHatch(rect_handle):       # fills previously created rectangle with hatch
   try:
      return kcs_draft.hatch_new(rect_handle)
   except:
      return None

#-------------------------------------------------------------------------------------------------------------
try:
   kcs_ui.message_confirm('This script will create a hatch and then ask user if delete it.')

   rect_handle = DefineRectangle()
   if rect_handle != None:
      hatch_handle = CreateHatch(rect_handle)
      if hatch_handle != None:
         answer = kcs_ui.answer_req("Remove", 'Do you want to remove the rectangle and the hatch?')
         if answer == kcs_util.yes():                 # removes created elements
            kcs_draft.element_delete(rect_handle)
            kcs_draft.element_delete(hatch_handle)
except:
   CommonSample.ReportTribonError(kcs_draft)
