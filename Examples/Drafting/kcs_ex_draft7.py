## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft7.py
#
#      PURPOSE:
#
#          This program creates a new entities like: point, line, rectangle, ellipse, conic etc. in the current drawing
#

import KcsStringlist
import kcs_ui
import kcs_util
import kcs_draft

import KcsEllipse2D
import KcsCircle2D
import KcsPoint2D
import KcsArc2D
import KcsColour
import KcsContour2D
import KcsVector2D
import KcsConic2D
import KcsRline2D
import KcsRectangle2D
import KcsPolygon2D

import sys
import math

#-------------------------------------------------------------------------------------------------------------
def GetContour():                            # get contour definition
   point = KcsPoint2D.Point2D(0, 0)
   contour = KcsContour2D.Contour2D(point)
   count = 0
   while 1:
      resp, point = kcs_ui.point2D_req('Indicate point of contour', point)
      if resp==kcs_util.ok():
         if count==0:
            contour = KcsContour2D.Contour2D(point)
         else:
            amp = 0.0
            resp, amp = kcs_ui.real_req('amplitude: ', amp)
            if resp == kcs_util.ok() and amp != 0.0:
               contour.AddArc(point, amp)
            else:
               contour.AddLine(point)
         count = count + 1
      elif resp==kcs_util.operation_complete():
         break;
      else:
         count = 0
         break;

   if count>0:
      colour = KcsColour.Colour("Green")
      resp, colour = kcs_ui.colour_select('colour for contour', colour)
      if resp == kcs_util.ok():
         contour.SetColour(colour)
         return (1, contour)
   return (0, None)

#-------------------------------------------------------------------------------------------------------------
def GetPolygon():                               # get polygon definition
   point    = KcsPoint2D.Point2D(0, 0)
   polygon  = KcsPolygon2D.Polygon2D(point)
   count = 0
   while 1:
      resp, point = kcs_ui.point2D_req('Indicate point of spline', point)
      if resp==kcs_util.ok():
         if count==0:
            polygon = KcsPolygon2D.Polygon2D(point)
         else:
            polygon.AddPoint(point)
         count = count + 1
      elif resp==kcs_util.operation_complete():
         break;
      else:
         count = 0
         break;
   return (count>0, polygon)

#-------------------------------------------------------------------------------------------------------------
def SelectCornerRadius():                    # allows user to specify radius for rounded rectangle
   pt1 = KcsPoint2D.Point2D()
   ptres, pt1 = kcs_ui.point2D_req('indicate first point for radius length', pt1)
   if ptres == kcs_util.ok():
      pt2 = KcsPoint2D.Point2D()
      ptres, pt2 = kcs_ui.point2D_req('indicate second point for radius length', pt2)
      if ptres == kcs_util.ok():
         return (1, (math.sqrt(math.pow(pt1.X-pt2.X, 2) + math.pow(pt1.Y-pt2.Y, 2))))

   return (0, 0)

#-------------------------------------------------------------------------------------------------------------
try:
   try:                                         # build elements types list
      actions = KcsStringlist.Stringlist('new arc')
      actions.AddString('new circle')
      actions.AddString('new conic')
      actions.AddString('new contour')
      actions.AddString('new ellipse')
      actions.AddString('new line')
      actions.AddString('new point')
      actions.AddString('new rectangle')
      actions.AddString('new spline')
   except:
      print KcsStringlist.error

   result = 1
   while result:
      res = kcs_ui.choice_select('Create', '', actions)     # get user choice and create element
      if res[0]==kcs_util.ok():

         if res[1] == 1:                                    # create new arc
            point1 = KcsPoint2D.Point2D(0, 0)
            point2 = KcsPoint2D.Point2D(0, 0)
            amplitude = 0
            colour = KcsColour.Colour('Green')
            (ptres, point1) = kcs_ui.point2D_req('Indicate start point of arc', point1)
            if ptres == kcs_util.ok():
               (ptres, point2) = kcs_ui.point2D_req('Indicate end point of arc', point2)
               if ptres == kcs_util.ok():
                  (ampres, amplitude) = kcs_ui.real_req('amplitude:', amplitude)
                  if ampres == kcs_util.ok():
                     (colres, colour) = kcs_ui.colour_select('colour for arc', colour)
                     if colres == kcs_util.ok():
                        try:
                           arc = KcsArc2D.Arc2D(point1,point2,amplitude)
                           kcs_draft.colour_set(colour)
                           handle = kcs_draft.arc_new(arc)
                           print 'created arc: ', handle
                        except:
                           kcs_ui.message_noconfirm(kcs_draft.error)

         elif res[1] == 2:                                  # create new circle
            center = KcsPoint2D.Point2D(0, 0)
            radius = 0
            colour = KcsColour.Colour('Green')
            (ptres, center) = kcs_ui.point2D_req('Indicate center of circle', center)
            if ptres == kcs_util.ok():
               (ampres, radius) = kcs_ui.real_req('radius:', radius)
               if ampres == kcs_util.ok():
                  (colres, colour) = kcs_ui.colour_select('colour for circle', colour)
                  if colres == kcs_util.ok():
                     try:
                        circle = KcsCircle2D.Circle2D(center, radius)
                        kcs_draft.colour_set(colour)
                        handle = kcs_draft.circle_new(circle)
                        print 'created circle: ', handle
                     except:
                        kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 3:                                    # create new conic
            point1 = KcsPoint2D.Point2D(0, 0)
            point2 = KcsPoint2D.Point2D(0, 0)
            ampvect = KcsVector2D.Vector2D(0, 0)
            factor = 0.0
            colour = KcsColour.Colour('Green')
            (ptres, point1) = kcs_ui.point2D_req('Indicate start point of conic', point1)
            if ptres == kcs_util.ok():
               (ptres, point2) = kcs_ui.point2D_req('Indicate end point of conic', point2)
               if ptres == kcs_util.ok():
                  p1 = KcsPoint2D.Point2D(0, 0)
                  p2 = KcsPoint2D.Point2D(0, 0)
                  (ptres, p1) = kcs_ui.point2D_req('Indicate start point of amplitude vector', p1)
                  if ptres == kcs_util.ok():
                     (ptres, p2) = kcs_ui.point2D_req('Indicate end point of amplitude vector', p2)
                     if ptres == kcs_util.ok():
                        (facres, factor) = kcs_ui.real_req('factor:', factor)
                        if facres == kcs_util.ok():
                           ampvect = KcsVector2D.Vector2D(p2.X-p1.X, p2.Y-p1.Y)
                           (colres, colour) = kcs_ui.colour_select('colour for conic', colour)
                           if colres == kcs_util.ok():
                              try:
                                 conic = KcsConic2D.Conic2D(point1, point2, ampvect, factor)
                                 kcs_draft.colour_set(colour)
                                 handle = kcs_draft.conic_new(conic)
                                 print 'created conic: ', handle
                              except:
                                 kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 4:                                    # create new contour
            (resp, contour) = GetContour()
            if resp:
               try:
                  kcs_draft.colour_set(contour.GetColour())
                  handle = kcs_draft.contour_new(contour)
                  print 'created contour: ', handle
               except:
                  kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 5:                                    # create new ellipse
            point1 = KcsPoint2D.Point2D(0, 0)
            point2 = KcsPoint2D.Point2D(0, 0)
            colour = KcsColour.Colour('Green')
            (ptres, point1) = kcs_ui.point2D_req('Indicate first corner of ellipse', point1)
            if ptres == kcs_util.ok():
               (ptres, point2) = kcs_ui.point2D_req('Indicate second corner of ellipse', point2)
               if ptres == kcs_util.ok():
                  (colres, colour) = kcs_ui.colour_select('colour for conic', colour)
                  if colres:
                     try:
                        ellipse = KcsEllipse2D.Ellipse2D(point1, point2)
                        kcs_draft.colour_set(colour)
                        handle = kcs_draft.ellipse_new(ellipse)
                        print 'created ellipse: ', handle
                     except:
                        kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 6:                                    # create new line
            point1 = KcsPoint2D.Point2D(0, 0)
            point2 = KcsPoint2D.Point2D(0, 0)
            colour = KcsColour.Colour('Green')
            (ptres, point1) = kcs_ui.point2D_req('Indicate start point of line', point1)
            if ptres == kcs_util.ok():
               (ptres, point2) = kcs_ui.point2D_req('Indicate second end point of line', point2)
               if ptres == kcs_util.ok():
                  (colres, colour) = kcs_ui.colour_select('colour for conic', colour)
                  if colres:
                     try:
                        line = KcsRline2D.Rline2D(point1, point2)
                        kcs_draft.colour_set(colour)
                        handle = kcs_draft.line_new(line)
                        print 'created line: ', handle
                     except:
                        kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 7:                                    # create new point
            point = KcsPoint2D.Point2D(0, 0)
            colour = KcsColour.Colour("Green")
            (ptres, point) = kcs_ui.point2D_req('Indicate point', point)
            if ptres:
               (colres, colour) = kcs_ui.colour_select('colour for point', colour)
               if colres  == kcs_util.ok():
                  try:
                     kcs_draft.colour_set(colour)
                     handle = kcs_draft.point_new(point)
                     print 'created point: ', handle
                  except:
                     kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 8:                                    # create new rectangle
            point1 = KcsPoint2D.Point2D(0, 0)
            point2 = KcsPoint2D.Point2D(0, 0)
            colour = KcsColour.Colour("Green")
            (ptres, point1) = kcs_ui.point2D_req('Indicate first corner of rectangle', point1)
            if ptres == kcs_util.ok():
               (ptres, point2) = kcs_ui.point2D_req('Indicate second corner of rectangle', point2)
               if ptres == kcs_util.ok():
                  (colres, colour) = kcs_ui.colour_select('colour for rectangle', colour)
                  if colres == kcs_util.ok():
                     try:
                        kcs_draft.colour_set(colour)
                        # create rectangle
                        rectangle = KcsRectangle2D.Rectangle2D(point1, point2)

                        # draw help rectangle
                        handle = kcs_draft.rectangle_new(rectangle)

                        # select radius
                        (radres, radius) = SelectCornerRadius()
                        if radres:
                           kcs_draft.element_delete(handle)
                           handle = kcs_draft.rectangle_new(rectangle, radius)
                        print 'created rectangle: ', handle
                     except:
                        kcs_ui.message_noconfirm(kcs_draft.error)

         if res[1] == 9:                                 # create new spline
            polres, polygon = GetPolygon()
            if polres:
               colour = KcsColour.Colour("Green")
               resp, colour = kcs_ui.colour_select('colour for spline', colour)
               if resp == kcs_util.ok():
                  try:
                     kcs_draft.colour_set(colour)
                     handle = kcs_draft.spline_new(polygon)
                     print 'created spline: ', handle
                  except:
                     kcs_ui.message_noconfirm(kcs_draft.error)

      else:
         result = 0
except:
   print kcs_draft.error
