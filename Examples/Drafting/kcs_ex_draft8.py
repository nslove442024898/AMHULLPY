## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft8.py
#
#      PURPOSE:
#
#          This program creates a few dimension elements
#

import kcs_util
import kcs_ui
import kcs_draft

import KcsStringlist

import KcsPoint2D
import KcsVector2D
import KcsPolygon2D
import KcsContour2D
import KcsRline2D
import KcsCircle2D

import math

#-------------------------------------------------------------------------------------------------------------
def GetLine():                               # get line
   pt1    = KcsPoint2D.Point2D(0, 0)
   pt2    = KcsPoint2D.Point2D(0, 0)
   resp, pt1 = kcs_ui.point2D_req('indicate start point of line', pt1)
   if resp == kcs_util.ok():
      resp, pt2 = kcs_ui.point2D_req('indicate end point of line', pt2)
      if resp == kcs_util.ok():
         return (1, KcsRline2D.Rline2D(pt1, pt2))
   return (0, None)

#-------------------------------------------------------------------------------------------------------------
def GetCircle():                             # get circle
   center = KcsPoint2D.Point2D(0, 0)
   pt1 = KcsPoint2D.Point2D(0, 0)
   resp, center = kcs_ui.point2D_req('indicate center of circle', center)
   if resp == kcs_util.ok():
      resp, pt1 = kcs_ui.point2D_req('indicate point on circle', pt1)
      if resp == kcs_util.ok():
         return (1, KcsCircle2D.Circle2D(center, math.sqrt(math.pow(pt1.X-center.X, 2)+math.pow(pt1.Y-center.Y, 2))))
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

try:
   try:                                         # build dimensions types list
      actions = KcsStringlist.Stringlist('linear dimension')
      actions.AddString('angle dimension')
      actions.AddString('diameter dimension')
      actions.AddString('radius dimension')

      dimtype = KcsStringlist.Stringlist('Normal')
      dimtype.AddString('Chain')
      dimtype.AddString('Staircase')
   except:
      print KcsStringlist.error
      exit()

   result = 1

   pt1 = KcsPoint2D.Point2D()
   pt2 = KcsPoint2D.Point2D()

   while result:
      res = kcs_ui.choice_select('Create', '', actions)     # get user choice and create element
      if res[0]==kcs_util.ok():

         if res[1] == 1:                                    # create new linear dimension
            polres, polygon = GetPolygon()
            if polres and len(polygon)>0:
               contour = KcsContour2D.Contour2D(polygon[0])
               for indeks in range(1, len(polygon)):
                  contour.AddLine(polygon[indeks])

               # create contour
               try:
                  kcs_draft.contour_new(contour)
               except:
                  print kcs_draft.error

               (resp, pt1) = kcs_ui.point2D_req('start point of direction vector', pt1)
               if resp == kcs_util.ok():
                  (resp, pt2) = kcs_ui.point2D_req('end point of direction vector', pt2)
                  if resp == kcs_util.ok():
                     vector = KcsVector2D.Vector2D(pt2.X-pt1.X, pt2.Y-pt1.Y)
                     position = KcsPoint2D.Point2D()
                     resp, position = kcs_ui.point2D_req('select position of dimension', position)
                     if resp == kcs_util.ok():
                        resp, type = kcs_ui.choice_select('Dimension type:', '', dimtype)
                        if resp == kcs_util.ok():
                           try:
                              handle = kcs_draft.dim_linear_new(polygon, type, vector, position)
                              print 'created dimension:', handle
                           except:
                              print kcs_draft.error
         elif res[1] == 2:                                    # create new angle dimension
            resp, line1 = GetLine()
            try:
               kcs_draft.line_new(line1)
            except:
               print kcs_draft.error
            if resp:
               resp, line2 = GetLine()
               if resp:
                  try:
                     kcs_draft.line_new(line2)
                  except:
                     print kcs_draft.error

                  arcpos = KcsPoint2D.Point2D()
                  resp, arcpos = kcs_ui.point2D_req('Indicate position of dimension', arcpos)
                  if resp == kcs_util.ok():
                     txtpos = KcsPoint2D.Point2D()
                     resp, txtpos = kcs_ui.point2D_req('Indicate text position', txtpos)
                     if resp == kcs_util.ok():
                        try:
                           handle = kcs_draft.dim_angle_new(line1, line2, arcpos, txtpos)
                           print 'created dimension:', handle
                        except:
                           print kcs_draft.error
         elif res[1] == 3:                                    # create new diameter dimension
            resp, circle = GetCircle()
            try:
               kcs_draft.circle_new(circle)
            except:
               print kcs_draft.error
            if resp:
                  pos1 = KcsPoint2D.Point2D()
                  pos2 = KcsPoint2D.Point2D()
                  resp, pos1 = kcs_ui.point2D_req('Indicate position of measure (optional)', pos1)
                  if resp == kcs_util.ok():
                     resp, pos2 = kcs_ui.point2D_req('Indicate position of the horizontal part (optional)', pos2)
                     if resp != kcs_util.ok():
                        pos2 = None
                  else:
                     pos1 = None

                  try:
                     if pos1!=None and pos2!=None:
                        handle = kcs_draft.dim_diameter_new(circle, pos1, pos2)
                     elif pos1!=None and pos2==None:
                        handle = kcs_draft.dim_diameter_new(circle, pos1)
                     else:
                        handle = kcs_draft.dim_diameter_new(circle)
                     print 'created dimension:', handle
                  except:
                     print kcs_draft.error
         elif res[1] == 4:                                    # create new radius dimension
            resp, circle = GetCircle()
            try:
               kcs_draft.circle_new(circle)
            except:
               print kcs_draft.error
            if resp:
                  pos1 = KcsPoint2D.Point2D()
                  pos2 = KcsPoint2D.Point2D()
                  resp, pos1 = kcs_ui.point2D_req('Indicate position of measure (optional)', pos1)
                  if resp == kcs_util.ok():
                     resp, pos2 = kcs_ui.point2D_req('Indicate position of the horizontal part (optional)', pos2)
                     if resp != kcs_util.ok():
                        pos2 = None
                  else:
                     pos1 = None

                  try:
                     if pos1!=None and pos2!=None:
                        handle = kcs_draft.dim_radius_new(circle, pos1, pos2)
                     elif pos1!=None and pos2==None:
                        handle = kcs_draft.dim_radius_new(circle, pos1)
                     else:
                        handle = kcs_draft.dim_radius_new(circle)
                     print 'created dimension:', handle
                  except:
                     print kcs_draft.error

      else:
         result = 0
except:
   print kcs_draft.error
