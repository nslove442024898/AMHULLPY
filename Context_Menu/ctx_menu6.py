## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu6.py
## Purpose:     Translates element
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu6.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsElementHandle
import KcsPoint2D
import KcsTransformation2D
import KcsVector2D
from KcsCursorType import CursorType
from KcsStat_point2D_req      import Stat_point2D_req, Point2dDefModes
import CommonSample

import kcs_draft
import kcs_ui
import kcs_util

# creates Stat_point2D_req instance and returns it
def CreatePoint2DReqStatus(defmode, helppoint):

   status = Stat_point2D_req()



   status.SetDefMode(defmode)



   CurType = CursorType()

   CurType.SetRubberBand(helppoint)

   status.SetCursorType(CurType)



   status.SetHelpPoint(helppoint)



   return status


# gets vector 2D from two points indicated by user
def SelectVector2D():

    vector = KcsVector2D.Vector2D()

    start = KcsPoint2D.Point2D(0, 0)

    end   = KcsPoint2D.Point2D(0, 0)


    # request user for start point of vector

    prompt = 'Select start point of vector , OC to exit'


    pointres = kcs_ui.point2D_req(prompt, start)

    if pointres[0] == kcs_util.ok():
        # request user for end point of vector


        prompt = 'Select end point of vector , OC to exit'
        defmode     = 'ModeCursor'
        status = CreatePoint2DReqStatus(defmode, start)

        pointres = kcs_ui.point2D_req(prompt, end, status)
        if pointres[0] == kcs_util.ok():

            vector.X = end.X - start.X

            vector.Y = end.Y - start.Y

            return (1, vector)

    return (0, vector)


# moves given element
def MoveElement(handle):
    # init transformation matrix
    transf = KcsTransformation2D.Transformation2D()

    (set, vector) = SelectVector2D()

    if set:

        transf.Translate(vector)


    try:
        kcs_draft.element_transform(handle, transf)

        kcs_draft.dwg_repaint()

    except Exception, e:
        print e

# main entry
def run(*args):
    if not hasattr(kcs_draft, 'ContextElement'):
        return
    if kcs_draft.ContextElement == None:
        return
    MoveElement(kcs_draft.ContextElement)
