## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft40.py
#
#      PURPOSE:
#
#          This example shows how to use primitives 2D functions
#

import sys
import copy
import kcs_ui
import kcs_util
import kcs_draft
from math import *

import KcsElementHandle
import KcsStringlist
import KcsRectangle2D
import KcsPolygon2D
import KcsPoint2D
import CommonSample
import KcsContour2D
import KcsColour
from KcsRline2D import Rline2D
from KcsText import Text
from KcsStat_point2D_req      import Stat_point2D_req, Point2dDefModes
from KcsCursorType            import CursorType, CursorTypes

#-------------------------------------------------------------------------------------------------------------
def DefineRectangle():
   point1 = KcsPoint2D.Point2D()
   point2 = KcsPoint2D.Point2D()
   resp, point1 = kcs_ui.point2D_req('First corner', point1)
   if resp == kcs_util.ok():
      status = Stat_point2D_req()
      status.SetDefMode('ModeCursor')

      CurType = CursorType()
      CurType.SetRubberRectangle(point1)
      status.SetCursorType(CurType)
      status.SetHelpPoint(point1)

      resp, point2 = kcs_ui.point2D_req('Second corner', point2, status)

      if resp == kcs_util.ok():
         return 1, KcsRectangle2D.Rectangle2D(point1, point2)
      else:
         return 0, None
   else:
      return 0, None

#-------------------------------------------------------------------------------------------------------------
def CreateContour(polygon):
   if polygon == None:
      return None

   if len(polygon)<=1:
      return None

   contour = KcsContour2D.Contour2D(polygon[0])
   for index in range(1, len(polygon)):
      contour.AddLine(polygon[index])
   contour.SetColour(KcsColour.Colour('Blue'))

   try:
      return kcs_draft.contour_new(contour)
   except Exception, e:
      print e
      return None

#-------------------------------------------------------------------------------------------------------------
def DefinePolygon():
   polygon = KcsPolygon2D.Polygon2D()
   result = 0

   handle = None
   while 1:
      try:
         status = None
         if len(polygon):
            status = Stat_point2D_req()
            status.SetDefMode('ModeCursor')
            CurType = CursorType()
            CurType.SetRubberBand(polygon[-1])
            status.SetCursorType(CurType)

         point = KcsPoint2D.Point2D()
         if status != None:
            res, point = kcs_ui.point2D_req('Select vertex, OC to exit', point, status)
         else:
            res, point = kcs_ui.point2D_req('Select vertex, OC to exit', point)

         try:
            if handle != None:
               kcs_draft.element_delete(handle)
         except:
            pass

         print res
         if res == kcs_util.ok():
            polygon.AddPoint(point)
         elif res == kcs_util.cancel() or res == kcs_util.quit():
            result = 0
            break
         else:
            result = 1
            break

         try:
            handle = CreateContour(polygon)
         except:
            pass

      except Exception, e:
         break

   return result, polygon

#-------------------------------------------------------------------------------------------------------------
def BuildTextOptions(text):                                             # function builds actions list for text
    list = KcsStringlist.Stringlist('Text: '+text.GetString())
    list.AddString('Font: '+text.GetFont())
    pos = text.GetPosition()
    list.AddString('Height: ' + str(text.GetHeight()))
    list.AddString('Slant: ' + str(text.GetSlanting()))
    list.AddString('Aspect: ' + str(text.GetAspect()))
    list.AddString('Rotation: ' + str(text.GetRotation()))
    list.AddString('------------------')
    list.AddString('acept changes')

    return list;

#-------------------------------------------------------------------------------------------------------------
def EditText(text):                                     # function allows to change properties of text
    # build elements kind list
    actions = KcsStringlist.Stringlist('')
    actions = BuildTextOptions(text)

    result = 1
    while result:
        res = kcs_ui.choice_select('Edit text', '', actions)
        if res[0]==kcs_util.ok():
            if res[1] == 1:                                                             # text string
                (set, str) = kcs_ui.string_req('Input string:', text.GetString())
                if set == kcs_util.ok():
                    text.SetString(str)
                    actions = BuildTextOptions(text);
            elif res[1] == 2:                                                           # font name
                (set, str) = kcs_ui.string_req('Font name:', text.GetFont())
                if set == kcs_util.ok():
                    text.SetFont(str)
                    actions = BuildTextOptions(text);
            elif res[1] == 3:                                                           # height
                pos1 = KcsPoint2D.Point2D()
                pos2 = KcsPoint2D.Point2D()
                (set, pos1) = kcs_ui.point2D_req('Indicate first point:', pos1)
                if set == kcs_util.ok():
                        (set, pos2) = kcs_ui.point2D_req('Indicate first point:', pos2)
                        if set == kcs_util.ok():
                            height = sqrt( pow(pos1.X-pos2.X, 2) + pow(pos1.Y-pos2.Y, 2) )
                            text.SetHeight(height)
                            actions = BuildTextOptions(text);
            elif res[1] == 4:                                                           # slant
                (set, slant) = kcs_ui.real_req('New slanting:', text.GetSlanting())
                if set == kcs_util.ok():
                        text.SetSlanting(slant)
                        actions = BuildTextOptions(text);
            elif res[1] == 5:                                                           # aspect
                (set, aspect) = kcs_ui.real_req('New aspect ratio:', text.GetAspect())
                if set == kcs_util.ok():
                        text.SetAspect(aspect)
                        actions = BuildTextOptions(text);
            elif res[1] == 6:                                                           # rotation
                (set, rotation) = kcs_ui.real_req('Rotation:', text.GetRotation())
                if set == kcs_util.ok():
                        text.SetRotation(rotation)
                        actions = BuildTextOptions(text);
            elif res[1] == 7:                                                           # separator
                pass
            elif res[1] == 8:                                                           # accept changes
               return 1
        else:
            return 0

#-------------------------------------------------------------------------------------------------------------
def IndicateLine():                                          # asks user to indicate line by 2 points
   point1 = KcsPoint2D.Point2D()
   point2 = KcsPoint2D.Point2D()

   prompt = 'Indicate start point, OC to exit'
   resp, point1 = kcs_ui.point2D_req(prompt, point1)

   if resp == kcs_util.ok():
      status = Stat_point2D_req()
      status.SetDefMode('ModeCursor')

      CurType = CursorType()
      CurType.SetRubberBand(point1)
      status.SetCursorType(CurType)
      status.SetHelpPoint(point1)

      resp, point2 = kcs_ui.point2D_req('Second point', point2, status)

      if resp == kcs_util.ok():
         return (1, Rline2D(point1, point2))

   return (0, Rline2D(point1, point2))

#-------------------------------------------------------------------------------------------------------------
def CreateCross():                                          # define cross
   line1 = Rline2D(KcsPoint2D.Point2D(0,0), KcsPoint2D.Point2D(100,100))
   line2 = Rline2D(KcsPoint2D.Point2D(0,100), KcsPoint2D.Point2D(100,0))
   text  = Text('test')
   parent = None

   while 1:
      linestr1 = 'Line1: %d,%d : %d,%d' % (line1.Start.X, line1.Start.Y, line1.End.X, line1.End.Y)
      linestr2 = 'Line2: %d,%d : %d,%d' % (line2.Start.X, line2.Start.Y, line2.End.X, line2.End.Y)
      if parent != None:
         parentstr = 'Subview: '+str(parent)
      else:
         parentstr = 'Subview: Not selected'

      actions = [linestr1, linestr2, 'Text: '+text.GetString(), parentstr, '--------------', 'create cross']

      res = kcs_ui.choice_select('Cross parameters', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:
               res, line = IndicateLine()
               if res:
                  line1 = line
            elif res[1] == 2:
               res, line = IndicateLine()
               if res:
                  line2 = line
            elif res[1] == 3:
               t = copy.deepcopy(text)
               try:
                  if EditText(t):
                     text = t
               except Exception, e:
                  print e
            elif res[1] == 4:
               res, handle = CommonSample.SelectSubview('Select parent subview')
               if res:
                  parent = handle
            elif res[1] == 5:
               pass
            elif res[1] == 6:
               try:
                  resHandle = kcs_draft.cross_new(parent, text, line1, line2)
                  kcs_ui.message_noconfirm('Cross created: '+str(resHandle))
               except Exception, e:
                  kcs_ui.message_confirm(kcs_draft.error)
                  kcs_ui.message_confirm(str(e))
         else:
            break
      except:
         break

#-------------------------------------------------------------------------------------------------------------
def CreateCloud():
   while 1:
      shape = None
      actions = ['by rectangle', 'by polygon']
      res = kcs_ui.choice_select('Shape for cloud', '', actions)           # define shape for cloud symbol
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:
               res, shape = DefineRectangle()
            else:
               res, shape = DefinePolygon()
         else:
            break;
      except:
         break
      if shape != None and res:
         res, parent = CommonSample.SelectSubview('Select parent subview')
         if res:
            try:
               resHandle = kcs_draft.cloud_new(parent, shape)
               kcs_ui.message_noconfirm('Cloud created: '+str(resHandle))
            except Exception, e:
               kcs_ui.message_confirm(kcs_draft.error)
               kcs_ui.message_confirm(str(e))

#-------------------------------------------------------------------------------------------------------------

def CreateRuler():
   (res, handle) = CommonSample.SelectSubview('Select subpicture to create ruler')

   if( res != 0 ):
      startPt = KcsPoint2D.Point2D()
      endPt   = KcsPoint2D.Point2D()
      text  = Text()

      resp = kcs_ui.point2D_req('Select ruler starting point', startPt)
      if resp[0] == kcs_util.ok():
         resp = kcs_ui.point2D_req('Select ruler ending point', endPt)
         if resp[0] == kcs_util.ok():
            dist = endPt.X-startPt.X
            dist = dist / 100.0

            try:
               resHandle = kcs_draft.ruler_new(handle, startPt, dist,0,100,20, text )
               kcs_ui.message_noconfirm('Cloud created: '+str(resHandle))
            except Exception, e:
               kcs_ui.message_confirm(kcs_draft.error)
               kcs_ui.message_confirm(str(e))

#-------------------------------------------------------------------------------------------------------------

def CreatePositionRuler():
   [res, model] = CommonSample.SelectView('Podaj View')

   while 1:
      actions = (
         'Base Line',
         'Center Line',
         'Frame Ruler',
         'Longitudinal horizontal ruler',
         'Longitudinal vertical ruler'
         )
      (status, index) = kcs_ui.choice_select('','Position Ruler', actions)
      if status == kcs_util.ok():
         if index == 1:
            [res, Line2D] = IndicateLine()
            resHandle = kcs_draft.position_ruler_new(1, model, Line2D.Start, Line2D.End)
            kcs_draft.dwg_repaint()
         elif index == 2:
            [res, Line2D] = IndicateLine()
            resHandle = kcs_draft.position_ruler_new(2, model, Line2D.Start, Line2D.End)
            kcs_draft.dwg_repaint()
         elif index == 3:
            [res, Line2D] = IndicateLine()
            resHandle = kcs_draft.position_ruler_new(3, model, Line2D.Start, Line2D.End)
            kcs_draft.dwg_repaint()
         elif index == 4:
            [res, Line2D] = IndicateLine()
            resHandle = kcs_draft.position_ruler_new(4, model, Line2D.Start, Line2D.End)
            kcs_draft.dwg_repaint()
         elif index == 5:
            [res, Line2D] = IndicateLine()
            resHandle = kcs_draft.position_ruler_new(5, model, Line2D.Start, Line2D.End)
            kcs_draft.dwg_repaint()
      else:
         print "User interrupted!"
         break;
   kcs_ui.message_noconfirm('Ruler created: '+str(resHandle))

#-------------------------------------------------------------------------------------------------------------
def CreateGeneralRestrictionSymbol():

   (res, handle) = CommonSample.SelectSubview('Select subpicture to create pipe restriction symbol')

   if( res != 0 ):
      res, line = IndicateLine()
      if res:
         try:
            resHandle = kcs_draft.general_restr_symbol_new(handle, line.Start, line.End, 1)
            kcs_ui.message_noconfirm('General restriction symbol created: '+str(resHandle))
         except Exception, e:
            kcs_ui.message_confirm(kcs_draft.error)
            kcs_ui.message_confirm(str(e))

#-------------------------------------------------------------------------------------------------------------

def CreatePipeRestrictionSymbol():

   (res, handle) = CommonSample.SelectSubview('Select subpicture to create pipe restriction symbol')

   if( res != 0 ):
      res, line = IndicateLine()
      if res:
         try:
            resHandle = kcs_draft.pipe_restr_symbol_new(handle, line.Start, line.End)
            kcs_ui.message_noconfirm('Pipe restriction symbol created: '+str(resHandle))
         except Exception, e:
            kcs_ui.message_confirm(kcs_draft.error)
            kcs_ui.message_confirm(str(e))

#-------------------------------------------------------------------------------------------------------------
try:           # main
   while 1:
      actions = ['cloud_new', 'cross_new', 'ruler_new', 'pipe_restr_symbol_new', 'general_restr_symbol_new']
      res = kcs_ui.choice_select('Functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # cross new
               CreateCloud()
            elif res[1] == 2:
               CreateCross()
            elif res[1] == 3:
               CreateRuler()
            elif res[1] == 4:
               CreatePipeRestrictionSymbol()
            elif res[1] == 5:
               CreateGeneralRestrictionSymbol()
         else:
            break;
      except:
         break
except:
   pass
