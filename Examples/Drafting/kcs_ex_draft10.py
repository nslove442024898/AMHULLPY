## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft10.py
#
#      PURPOSE:
#
#          This program creates a note or moves a reference
#
import kcs_draft
import kcs_ui
import kcs_util

import KcsPoint2D
import KcsEllipse2D
import KcsPolygon2D
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def DefinePolygon():
   points = []

   try:
      while 1:
         point = KcsPoint2D.Point2D()
         resp, point = kcs_ui.point2D_req('Define polygon, OC to end definition', point)
         if resp == kcs_util.ok():
            points.append(point)
         elif resp == kcs_util.cancel():
            kcs_ui.message_noconfirm('Selection cancelled!')
            return None
         elif resp == kcs_util.operation_complete():
            break
   except:
      CommonSample.ReportTribonError(kcs_draft)
      return None

   if len(points)<2:
      kcs_ui.message_noconfirm('You must select at least 2 points!')
      return None
   else:
      polygon = KcsPolygon2D.Polygon2D(points[0])
      for index in range(1, len(points)):
         polygon.AddPoint(points[index])
      return polygon


#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['create note', 'move reference']

   while 1:
      res = kcs_ui.choice_select('Select action:', '', actions)
      if res[0] == kcs_util.ok():
         if res[1] == 1:
            polygon = DefinePolygon()

            if polygon != None:
               resp, text = kcs_ui.string_req('Enter note text:', '')
               if resp == kcs_util.ok():
                  try:
                     kcs_draft.note_new(text, polygon)
                     kcs_ui.message_noconfirm('Note created!')
                  except TBException, e:
                     kcs_ui.message_confirm(str(e))
         elif res[1] == 2:
            res, handle = CommonSample.SelectComponent('Select reference')
            if res:
               res, point = kcs_ui.point2D_req('New point for reference', KcsPoint2D.Point2D())
               if res==kcs_util.ok():
                  try:
                     kcs_draft.reference_move(handle, point)
                     kcs_draft.dwg_repaint()
                  except TBException, e:
                     kcs_ui.message_confirm(str(e))
      else:
         break


except:
   pass
