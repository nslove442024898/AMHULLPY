## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft13.py
#
#      PURPOSE:
#
#          This program highlights a point and a contour in the current drawing.
#          In the end of the program the highlighting is removed.
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsContour2D

#-------------------------------------------------------------------------------------------------------------
def DefineContour():

   points = []

   while 1:
      try:
         point = KcsPoint2D.Point2D()
         resp, point = kcs_ui.point2D_req('Define contour point number %d, OC to finish' % len(points), point)
         if resp == kcs_util.ok():
            points.append(point)
         elif resp == kcs_util.operation_complete():
            break
         else:
            points = []
            return None
      except:
         CommonSample.ReportTribonError(kcs_ui)

   if len(points)<2:
      kcs_ui.message_noconfirm('You must select at least 2 points!')
      return None
   else:
      contour = KcsContour2D.Contour2D(points[0])
      for index in range(1, len(points)):
         contour.AddLine(points[index])
      return contour


#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['point', 'contour']
   highlighted = []
   point = KcsPoint2D.Point2D()

   while(1):
      resp, index = kcs_ui.choice_select('Highlight', 'Select element kind to highlight', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # highlight point
            try:
               resp, point = kcs_ui.point2D_req('Select point which will be highlighted', point)
               try:
                  highlighted.append(kcs_draft.point_highlight(point))
               except:
                  CommonSample.ReportTribonError(kcs_draft)
            except:
               CommonSample.ReportTribonError(kcs_ui)
         elif index == 2:
            contour = DefineContour()
            if contour != None:
               try:
                  highlighted.append(kcs_draft.contour_highlight(contour))
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break
finally:
   for handle in highlighted:
      try:
         kcs_draft.highlight_off(handle)
      except:
         CommonSample.ReportTribonError(kcs_draft)
