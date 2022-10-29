## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft35.py
#
#      PURPOSE:
#
#          This example shows how to use zoom/extent functions
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

import KcsStringlist
import KcsPoint2D
import KcsElementHandle
import KcsRectangle2D

zoomstack = []

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def IndicateRectangle():                                          # asks user to indicate rectangle by 2 points
   point1 = KcsPoint2D.Point2D()
   point2 = KcsPoint2D.Point2D()

   prompt = 'Indicate first corner, OC to exit'
   resp, point1 = kcs_ui.point2D_req(prompt, point1)
   if resp == kcs_util.ok():
      resp, point2 = kcs_ui.point2D_req(prompt, point2)
      if resp == kcs_util.ok():
         return (1, KcsRectangle2D.Rectangle2D(point1, point2))

   return (0, KcsRectangle2D.Rectangle2D())

#-------------------------------------------------------------------------------------------------------------
def KeyInRectangle():                                             # asks user to key in coordinates of rectangle
   point1 = KcsPoint2D.Point2D()
   point2 = KcsPoint2D.Point2D()

   resp, point1.X = kcs_ui.real_req('X coordinate of corner 1', point1.X)
   if resp == kcs_util.ok():
      resp, point1.Y = kcs_ui.real_req('Y coordinate of corner 2', point1.Y)
      if resp == kcs_util.ok():
         resp, point2.X = kcs_ui.real_req('X coordinate of corner 2', point2.X)
         if resp == kcs_util.ok():
            resp, point2.Y = kcs_ui.real_req('Y coordinate of corner 2', point2.Y)
            return (1, KcsRectangle2D.Rectangle2D(point1, point2))
   return (0, KcsRectangle2D.Rectangle2D())

#-------------------------------------------------------------------------------------------------------------
def SelectRectangle():                                            # asks user to define rectangle
   # build actions list
   actions = KcsStringlist.Stringlist('Key in points')
   actions.AddString('Select')

   res = kcs_ui.choice_select('Define rectange', '', actions)
   try:
      if res[0]==kcs_util.ok():
         if res[1] == 1:         # key in points
            return KeyInRectangle()
         if res[1] == 2:
            return IndicateRectangle()
   except:
      print sys.exc_info()[1]
      PrintDraftError()

   return (0, KcsRectangle2D.Rectangle2D())

#-------------------------------------------------------------------------------------------------------------
try:           # main
   # build actions list
   actions = KcsStringlist.Stringlist('Repaint drawing')
   actions.AddString('Zoom drawing')
   actions.AddString('Zoom previous')
   actions.AddString('Get drawing extent')

   while 1:
      res = kcs_ui.choice_select('Drawing functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # repaint drawing
               kcs_draft.dwg_repaint()
            elif res[1] == 2:
               rectresp, rectangle = SelectRectangle()
               if rectresp==1:
                  previous = KcsRectangle2D.Rectangle2D()
                  kcs_draft.zoom_extent_get(previous)
                  if not previous.IsEmpty():
                     zoomstack = [previous] + zoomstack
                  kcs_draft.dwg_zoom(rectangle)
            elif res[1] == 3:
               if len(zoomstack)>0:
                  previous = zoomstack[0]
                  zoomstack = zoomstack[1:]
                  kcs_draft.dwg_zoom(previous)
               else:
                  kcs_ui.message_noconfirm('There is no previous zoom state!')
            elif  res[1] == 4:
                  rectangle = kcs_draft.element_extent_get()
                  if rectangle.IsEmpty():
                     kcs_ui.message_noconfirm('Drawing extents: empty rectangle')
                  else:
                     kcs_ui.message_noconfirm('Drawing extents: ' + str(rectangle))
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
   print kcs_draft.error;


