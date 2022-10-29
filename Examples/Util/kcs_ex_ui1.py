## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui1.py
#
#      PURPOSE:
#
#          This example shows how to use kcs_ui.point2D_req function
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

from KcsStringlist            import Stringlist
from KcsPoint2D               import Point2D
from KcsCursorType            import CursorType, CursorTypes
from KcsStat_point2D_req      import Stat_point2D_req, Point2dDefModes
from KcsStat_point3D_req      import Stat_point3D_req
from KcsButtonState           import ButtonState
from KcsElementHandle         import ElementHandle
from KcsPoint3D               import Point3D
from KcsHighlightSet          import HighlightSet
from KcsArc2D                 import Arc2D
from KcsContour2D             import Contour2D	
from KcsRectangle2D           import Rectangle2D
from KcsPolygon3D             import Polygon3D
from KcsModel                 import Model
import CommonSample


#-------------------------------------------------------------------------------------------------------------
def PrintUIError():                                            # prints exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_ui.error)
   print kcs_ui.error

#-------------------------------------------------------------------------------------------------------------
def BuildActionsList(startpoint, helppoint, cursortype, defmode):   # build actions list
   # build actions list
   actions = Stringlist('Start point: ' + str(startpoint.X) + ' ' + str(startpoint.Y))
   if helppoint==None:
      actions.AddString('Help point: None')
   else:
      actions.AddString('Help point: ' + str(helppoint.X) + ' ' + str(helppoint.Y))
   actions.AddString('CurType: ' + cursortype)
   actions.AddString('Mode: ' + defmode)
   actions.AddString('Build drag cursor')
   actions.AddString('SelectPoint')
   actions.AddString('SelectPoint with lock')
   return actions

#-------------------------------------------------------------------------------------------------------------
def SelectHelpPoint():
   actions = Stringlist('None')
   actions.AddString('Select')

   res = kcs_ui.choice_select('Select 2D point function', '', actions)
   if res[0] == kcs_util.ok():
      if res[1]==1:
         return (kcs_util.ok(), None)
      else:
         point = Point2D()
         return kcs_ui.point2D_req('Select help point, OC to exit', point)
   else:
      return kcs_util.cancel(), point

#-------------------------------------------------------------------------------------------------------------
def CreatePoint2DReqStatus(defmode, cursortype, helppoint, highlight=None):
   status = Stat_point2D_req()
   status.SetDefMode(defmode)

   CurType = CursorType()
   if cursortype == 'CrossHair':
      CurType.SetCrossHair()
   elif cursortype == 'RubberBand':
      CurType.SetRubberBand(startpoint)
   elif cursortype == 'RubberRectangle':
      CurType.SetRubberRectangle(startpoint)
   elif cursortype == 'RubberCircle':
      CurType.SetRubberCircle(startpoint)
   elif cursortype == 'DragCursor':
      CurType.SetDragCursor( highlight, startpoint )

   status.SetCursorType(CurType)

   status.SetHelpPoint(helppoint)

   return status

#-------------------------------------------------------------------------------------------------------------
def PrintResult(resp, point):
   result = ''
   if resp == kcs_util.ok():
      result = 'ok'
   elif resp == kcs_util.cancel():
      result = 'cancel'
   elif resp == kcs_util.quit():
      result = 'quit'
   elif resp == kcs_util.options():
      result = 'options'
   elif resp == kcs_util.operation_complete():
      result = 'operation complete'
   else:
      result = str(resp)
   kcs_ui.message_noconfirm('Result: %s    Point: %s' % (result, str(point)))

#-------------------------------------------------------------------------------------------------------------
def ShowDragCursorMenu( highlight ):
    actions = [ 'Add point 2d',
                'Add line 2d',
                'Add rectangle',
                'Add contour',
                'Add point 3d',
                'Add polygon 3d',
                'Add subpicture',
                'Add model' ]

    point1 = Point2D()
    point2 = Point2D()
    highlight.Reset()

    while 1:
      (status, option) = kcs_ui.choice_select('Build drag cursor', 'Select option', actions)
      if status == kcs_util.ok() :
          if option == 1 :
              resp, point1 = kcs_ui.point2D_req('Select point, OC to exit', point1)
              if resp == kcs_util.ok():
                 highlight.AddGeometry2D( point1 )
          if option == 2 :
              resp, point1 = kcs_ui.point2D_req('Select first point, OC to exit', point1)
              if resp == kcs_util.ok():
                  resp, point2 = kcs_ui.point2D_req('Select second point, OC to exit', point2)
                  if resp == kcs_util.ok():
                     seg = Arc2D(point1, point2, 0.0)
                     highlight.AddGeometry2D( seg )
          if option == 3 :
                 resp, point1 = kcs_ui.point2D_req('Select first point, OC to exit', point1)
                 if resp == kcs_util.ok():
                     resp, point2 = kcs_ui.point2D_req('Select second point, OC to exit', point2)
                     if resp == kcs_util.ok():
                        seg = Rectangle2D(point1, point2)
                        highlight.AddGeometry2D( seg )
          if option == 4 :
                 resp, point1 = kcs_ui.point2D_req('Select first contour point, OC to exit', point1)
                 if resp == kcs_util.ok():
                    contour = Contour2D( point1 )
                    while resp == kcs_util.ok():
                       resp, point1 = kcs_ui.point2D_req('Select contour point, OC to exit', point1)
                       if resp == kcs_util.ok():
                          contour.AddArc( point1, 0.0 )
                    highlight.AddGeometry2D( contour )

          if option == 5 :
                status = Stat_point3D_req()
                point3d = Point3D()
                status.Initial3D = 3

                resp, handle = CommonSample.SelectView('Select view')

                res = kcs_ui.point3D_req('Select point', status, point3d)
                if res[0] == kcs_util.ok():
                   highlight.AddGeometry3D( point3d, handle )

          if option == 6 :
                 status  = Stat_point3D_req()
                 point3d = Point3D()
                 status.Initial3D = 1

                 resp, handle = CommonSample.SelectView('Select view')

                 resp, point3d = kcs_ui.point3D_req('Select polygon point', status, point3d)
                 if resp == kcs_util.ok():
                    polygon = Polygon3D( point3d )
                    while resp == kcs_util.ok():
                       resp, point1 = kcs_ui.point3D_req('Select polygon point', status, point3d)
                       if resp == kcs_util.ok():
                          polygon.AddPoint( point3d )
                    highlight.AddGeometry3D( polygon, handle )

          if option == 7 :
                 resp, handle = CommonSample.SelectSubpicture('Select view')
                 if resp in [1, 2, 3]:
                    highlight.AddSubpicture( handle )

          if option == 8 :
	              model = CommonSample.SelectModel()
	              highlight.AddModel( model )
 		
      else:
         break

#-------------------------------------------------------------------------------------------------------------

try:           # main
   CursorTypes =  CursorTypes.keys()
   DefModes    =  Point2dDefModes.keys()

   startpoint  = Point2D()
   helppoint   = None
   cursortype  = 'CrossHair'
   defmode     = 'ModeCursor'
   respoint    = Point2D()
   highlight   = HighlightSet()

   actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
   while 1:
      res = kcs_ui.choice_select('Select 2D point function', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:            # select start point
               resp, startpoint = kcs_ui.point2D_req('Select start point, OC to exit', startpoint)
               if resp == kcs_util.ok():
                  actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
            elif res[1] == 2:          # select help point
               resp, helppoint = SelectHelpPoint()
               if resp == kcs_util.ok():
                  actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
            elif res[1] == 3:          # select cursor type
               index = CursorTypes.index(cursortype)
               if index+1 > len(CursorTypes)-1:
                  index = 0
               else:
                  index = index+1
               cursortype = CursorTypes[index]
               actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
            elif res[1] == 4:          # select point definition mode
               index = DefModes.index(defmode)
               if index+1 > len(DefModes)-1:
                  index = 0
               else:
                  index = index+1
               defmode = DefModes[index]
               actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)

            elif res[1] == 5:
               ShowDragCursorMenu( highlight )

            elif res[1] == 6:          # select point
               status = CreatePoint2DReqStatus(defmode, cursortype, helppoint, highlight)

               resp, respoint = kcs_ui.point2D_req('Select 2D point', respoint, status)
               defmode = status.GetDefMode()

               PrintResult(resp, respoint)

               actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
            elif res[1] == 7:          # select point with lock
               status = CreatePoint2DReqStatus(defmode, cursortype, helppoint, highlight)

               buttons = ButtonState()
               buttons.EnableLock(1)
               buttons.SetCheckedLock('V')

               resp, respoint = CommonSample.Point2DLockReq('Select 2D point', respoint, status, buttons)

               defmode = status.GetDefMode()

               PrintResult(resp, respoint)

               actions = BuildActionsList(startpoint, helppoint, cursortype, defmode)
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintUIError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
   print kcs_ui.error;
