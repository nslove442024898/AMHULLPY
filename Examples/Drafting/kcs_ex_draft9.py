## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft9.py
#
#      PURPOSE:
#
#          This program shows user how to use hatch functions
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsCircle2D
import KcsPoint2D
import KcsRectangle2D
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def DefineHatchPattern():
   resp, angle = kcs_ui.real_req('Enter hatch pattern angle:', 45.0)
   if resp == kcs_util.ok():
      resp, distance = kcs_ui.real_req('Enter hatch pattern distance:', 10.0)
      if resp == kcs_util.ok():
         try:
            kcs_draft.hatch_pattern_set( angle, distance)
         except:
            CommonSample.ReportTribonError(kcs_draft)


#-------------------------------------------------------------------------------------------------------------
def CreateHatch():
   try:
      point = KcsPoint2D.Point2D()
      resp, point = kcs_ui.point2D_req('Select contour', point)
      if resp == kcs_util.ok():
         contour_handle = None
         try:
            contour_handle = kcs_draft.contour_identify(point)
         except:
            CommonSample.ReportTribonError(kcs_draft)
            kcs_ui.message_noconfirm('Can not find a contour!')
         if contour_handle != None:
            try:
               hatch_handle = kcs_draft.hatch_new(contour_handle)
               return hatch_handle
            except:
               CommonSample.ReportTribonError(kcs_draft)
      return None
   except:
      CommonSample.ReportTribonError(kcs_ui)

#-------------------------------------------------------------------------------------------------------------
def CreateIslands(hatchhandle):
   try:
      point = KcsPoint2D.Point2D()
      resp, point = kcs_ui.point2D_req('Select contour', point)
      if resp == kcs_util.ok():
         contour_handle = None
         try:
            contour_handle = kcs_draft.contour_identify(point)
         except:
            CommonSample.ReportTribonError(kcs_draft)
            kcs_ui.message_noconfirm('Can not find a contour!')
         if contour_handle != None:
            try:
               newhatch = kcs_draft.hatch_island_new(hatchhandle, contour_handle)
               return 1, newhatch
            except:
               CommonSample.ReportTribonError(kcs_draft)
      return 0, None
   except:
      CommonSample.ReportTribonError(kcs_ui)


#-------------------------------------------------------------------------------------------------------------
try:
   hatch = None

   actions = ['define pattern', 'create hatch']

   while(1):
      resp, index = kcs_ui.choice_select('Hatch functions', 'Select operation', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # define pattern
            DefineHatchPattern()
         elif index == 2:                                   # set current modal colour
            hatch = CreateHatch()
         elif index == 3:
            resp, newhatch = CreateIslands(hatch)
            if resp:
               hatch = newhatch
      else:
         break;
      if hatch != None:
         actions = ['define pattern', 'create hatch', 'create island']
      else:
         actions = ['define pattern', 'create hatch']

except:
   CommonSample.ReportTribonError(kcs_ui)
