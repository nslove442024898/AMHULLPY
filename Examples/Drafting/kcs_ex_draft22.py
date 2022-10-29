## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft22.py
#
#      PURPOSE:
#
#          This example selects views, subviews, components, models,
#          dimensions, notes, position numbers, hatches, texts, symbols,
#          contours, points, geometries based on defined CaptureRegion2D
#

import sys, string
import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsStringlist
import KcsRectangle2D
import KcsContour2D
import KcsCaptureRegion2D
import CommonSample
from KcsCursorType            import CursorType, CursorTypes
from KcsStat_point2D_req      import Stat_point2D_req, Point2dDefModes

#-------------------------------------------------------------------------------------------------------------
def GetEntityHandles(elementkind, region):             # function calls corresponding capture function
    handles = []                                       # results list

    # call corresponding function
    if elementkind == 1:
        handles = kcs_draft.view_capture(region)       # views
    elif elementkind == 2:
        handles = kcs_draft.subview_capture(region)    # subviews
    elif elementkind == 3:
        handles = kcs_draft.component_capture(region)  # component
    elif elementkind == 4:
        handles = kcs_draft.model_capture(region)      # models
    elif elementkind == 5:
        handles = kcs_draft.dim_capture(region)        # dimensions
    elif elementkind == 6:
        handles = kcs_draft.note_capture(region)       # notes
    elif elementkind == 7:
        handles = kcs_draft.posno_capture(region)      # position numbers
    elif elementkind == 8:
        handles = kcs_draft.hatch_capture(region)      # hatches
    elif elementkind == 9:
        handles = kcs_draft.text_capture(region)       # texts
    elif elementkind == 10:
        handles = kcs_draft.symbol_capture(region)     # symbols
    elif elementkind == 11:
        handles = kcs_draft.contour_capture(region)    # contours
    elif elementkind == 12:
        handles = kcs_draft.point_capture(region)      # points
    elif elementkind == 13:
        handles = kcs_draft.geometry_capture(region)   # geometries

    return handles

#-------------------------------------------------------------------------------------------------------------
def FindEntities(elementkind, region):                  # function gets entities handles and reports it on screen
    try:                                                # if no entities found reports a message kcs_NotFound

        kcs_draft.highlight_off(0)                      # highlight off all highlighted entities

        handles = GetEntityHandles(elementkind, region) # get entity handles
        nSize = handles[0]

        # report number of captured entities
        kcs_ui.message_noconfirm('Captured entities:' + str(nSize))

        if nSize > 200:
            kcs_ui.message_noconfirm('Too many entities to highlight!');
        else:
            handles = handles[1:]
            for nHandle in handles:
                kcs_draft.element_highlight(nHandle)        # highlight founded entities

    except:
        print kcs_draft.error                           # print exception

        if kcs_draft.error == 'kcs_NotFound':
            kcs_ui.message_noconfirm('kcs_NotFound')

        return

#-------------------------------------------------------------------------------------------------------------

def DefineContour():
    point   = KcsPoint2D.Point2D()

    contour = None

    nCount = 0

    while 1:                      # get contour loop
        resp = kcs_ui.point2D_req('Indicate point of contour', point)  # request user for first corner
        if resp[0] == kcs_util.operation_complete():
            if nCount<2:
                return None
            if not contour.IsClosed():
                contour.AddLine(contour.Contour[0][0])
            return contour
        elif resp[0] == kcs_util.ok():
            if nCount==0:
                contour = KcsContour2D.Contour2D(point)
            else:
                contour.AddLine(point)

            nCount = nCount + 1
        else:
            return None

#-------------------------------------------------------------------------------------------------------------
def RegionFromContour(elementkind, Inside, Cut):        # funtion gets point and calls searching for entity
    point   = KcsPoint2D.Point2D()

    while 1:                                            # selecting loop
        try:
            contourready = 0
            nCount = 0

            while contourready==0:                      # get contour loop
                resp = kcs_ui.point2D_req('Indicate point of contour', point)  # request user for first corner
                if resp[0] == kcs_util.operation_complete():
                   contourready = 1
                elif resp[0] == kcs_util.ok():
                    if nCount==0:
                        contour = KcsContour2D.Contour2D(point)
                    else:
                        contour.AddLine(point)

                    nCount = nCount + 1
                else:
                    kcs_draft.highlight_off(0)          # highlight off all highlighted entities
                    return
        except:
            print kcs_ui.error
            return

        if contourready == 1 and nCount >= 3:
            region = KcsCaptureRegion2D.CaptureRegion2D()
            region.SetContour(contour)                  # create capture region

            if Inside==0:
                region.SetOutside()
            else:
                region.SetInside()

            if Cut==0:
                region.SetNoCut()
            else:
                region.SetCut()

            FindEntities(elementkind, region)

    return

#-------------------------------------------------------------------------------------------------------------
def RegionFromRectangle(elementkind, Inside, Cut):              # select region by rectangle
    point1 = KcsPoint2D.Point2D()
    point2 = KcsPoint2D.Point2D()

    while 1:
        try:
            resp = kcs_ui.point2D_req('Indicate first corner of rectangle', point1)  # request user for first corner
            if resp[0] != kcs_util.ok():
                kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
                return
            resp = kcs_ui.point2D_req('Indicate second corner of rectangle', point2) # request user for second corner
            if resp[0] != kcs_util.ok():
                kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
                return
        except:
            print kcs_ui.error
            return

        try:
            region = KcsCaptureRegion2D.CaptureRegion2D()
            rectangle = KcsRectangle2D.Rectangle2D(point1, point2)
            region.SetRectangle(rectangle)

            if Inside==0:
                region.SetOutside()
            else:
                region.SetInside()

            if Cut==0:
                region.SetNoCut()
            else:
                region.SetCut()

            FindEntities(elementkind, region)

        except:
            print 'Unexpected error:', sys.exc_info()[0]

    return

#-------------------------------------------------------------------------------------------------------------
def GetRegionSelectionMethod(elementkind, Inside, Cut):               # function gets selection method and selects entities
    try:
        # build options list
        actions = KcsStringlist.Stringlist('rectangle')
        actions.AddString('contour')
        actions.AddString('infinite')
    except:
        print KcsStringlist.error

    # get user choice and select entity
    result = 1
    try:
        while result:
            res = kcs_ui.choice_select('Region selection method', 'Create region based on:', actions)
            if res[0] == kcs_util.ok():
                method = res[1]
                if method == 1:
                    RegionFromRectangle(elementkind, Inside, Cut)
                elif method == 2:
                    RegionFromContour(elementkind, Inside, Cut)
                elif method == 3:
                    region = KcsCaptureRegion2D.CaptureRegion2D()
                    region.SetBoundaryInfinite()
                    FindEntities(elementkind, region)
            else:
                if res[0]==kcs_util.options():
                    Inside = GetInsideOption(Inside)
                    Cut = GetCutOption(Cut)
                else:
                    result = 0
    except:
        print kcs_ui.error

    return

#-------------------------------------------------------------------------------------------------------------
def GetInsideOption(Inside):                                # get Inside option
    actions = KcsStringlist.Stringlist('Inside Contour')
    actions.AddString('Outside Contour')
    res = kcs_ui.choice_select('Get Inside/Outside', 'Select method', actions)
    if res[0]==kcs_util.ok():
        if res[1] == 1:
            return 1
        else:
            return 0

    return Inside

#-------------------------------------------------------------------------------------------------------------
def GetCutOption(Cut):                                      # get Cut option
    actions = KcsStringlist.Stringlist('Cut')
    actions.AddString('No cut')
    res = kcs_ui.choice_select('Get Cut/No cut', 'Select method', actions)
    if res[0]==kcs_util.ok():
        if res[1] == 1:
            return 1
        else:
            return 0

    return Cut

#-------------------------------------------------------------------------------------------------------------
def DeleteElementsByArea():
    contour = DefineContour()
    if contour == None:
        return

    actions = { 'Outside' : kcs_draft.kcsDEL_OUTSIDE, 'Inside' : kcs_draft.kcsDEL_INSIDE }
    res, val = kcs_ui.choice_select('Delete', 'Select kind of parts', actions.keys())
    if res == kcs_util.ok():
       value = actions[actions.keys()[val-1]]
    else:
        return

    # capture elements
    point1 = KcsPoint2D.Point2D()
    point2 = KcsPoint2D.Point2D()

    try:
        resp = kcs_ui.point2D_req('Indicate first corner of rectangle', point1)  # request user for first corner
        if resp[0] != kcs_util.ok():
            return

        status = Stat_point2D_req()
        CurType = CursorType()
        CurType.SetRubberRectangle(point1)
        status.SetCursorType(CurType)

        resp = kcs_ui.point2D_req('Indicate second corner of rectangle', point2, status) # request user for second corner
        if resp[0] != kcs_util.ok():
            return

        region = KcsCaptureRegion2D.CaptureRegion2D()
        rectangle = KcsRectangle2D.Rectangle2D(point1, point2)
        region.SetRectangle(rectangle)
        region.SetInside()
        region.SetNoCut()

        handles = GetEntityHandles(13, region)

        kcs_draft.delete_by_area(handles[1:], value, contour)
    except Exception, e:
        kcs_ui.message_noconfirm(str(e))


#-------------------------------------------------------------------------------------------------------------
try:                                                        # get user choice and select entity
    Inside = 1
    Cut = 0

    # build elements kind list
    actions = ['view capture', 'subview capture', 'component capture', 'model capture', 'dim capture', 'note capture', 'posno capture', \
               'hatch capture', 'text capture', 'symbol capture', 'contour capture', 'point capture',  'geometry capture', 'delete by area' ]

    result = 1
    while result:
        res = kcs_ui.choice_select('Get identify', 'Select element kind', actions)
        if res[0]==kcs_util.ok():
            if res[1] == len(actions):
                DeleteElementsByArea()
            else:
                GetRegionSelectionMethod(res[1], Inside, Cut)
        else:
            if res[0]==kcs_util.options():
                Inside = GetInsideOption(Inside)
                Cut = GetCutOption(Cut)
            else:
                result = 0

    kcs_ui.message_noconfirm('Script interrupted')
    kcs_draft.highlight_off(0)                      # highlight off all highlighted entities

except:
    print kcs_ui.error
    kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
