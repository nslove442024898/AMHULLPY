## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu7.py
## Purpose:     Implementation of context menu "Subpicture Properties" item
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu7.py $
## Licence:
##-----------------------------------------------------------------------------
import KcsElementHandle
import KcsLayer
import KcsColour
import KcsLinetype
import CommonSample
import KcsTransformation2D
import KcsTransformation3D
import KcsVector3D
import KcsVector2D
import KcsPoint3D
import KcsPoint2D
import KcsRectangle2D

import kcs_draft
import kcs_ui
import kcs_util
import sys

import math
import copy

import CtxSubpictPropDlg
from wxPython.wx import *

################################################################
## functions used to set subpicture properties
################################################################
def SetSubpictureColour(handle, colour):
    try:
        kcs_draft.element_colour_set(handle, colour)
    except:
        CommonSample.ReportTribonError(kcs_draft)

def SetSubpictureLinetype(handle, ltype):
    try:
        kcs_draft.element_linetype_set(handle, ltype)
    except:
        CommonSample.ReportTribonError(kcs_draft)

def SetSubpictureName(handle, name):
    try:
        kcs_draft.subpicture_name_set(handle, name)
    except:
        CommonSample.ReportTribonError(kcs_draft)

def SetSubpictureLayer(handle, layer):
    try:
        kcs_draft.element_layer_set(handle, layer)
    except:
        CommonSample.ReportTribonError(kcs_draft)

# function changes view transformation
def ChangeViewTransformation(view, transf, newViewRotation, newViewScale):
    ################################################################
    ## get existiong scale and rotation
    ################################################################

    oldViewScale     = round(transf.GetScale()[0], 4)
    oldViewRotation  = round(transf.GetRotation(), 4)

    if oldViewScale != newViewScale or oldViewRotation != newViewRotation:
        try:
            ################################################################
            ## find center of transformation = center of view extent
            ################################################################
            extents = kcs_draft.element_extent_get(view)
            center = KcsPoint2D.Point2D()
            center.SetFromMidpoint(extents[0], extents[1])

            ################################################################
            ## prepare transformations
            ################################################################
            move1  = KcsTransformation2D.Transformation2D()
            scale  = KcsTransformation2D.Transformation2D()
            rotate = KcsTransformation2D.Transformation2D()
            move2  = KcsTransformation2D.Transformation2D()

            move1.Translate(KcsVector2D.Vector2D(-center.X, -center.Y))

            if oldViewRotation != newViewRotation:
                rotate.Rotate(KcsPoint2D.Point2D(0, 0), newViewRotation - oldViewRotation)

            if oldViewScale != newViewScale:
                scale.Scale(newViewScale/oldViewScale)

            move2.Translate(KcsVector2D.Vector2D(center.X, center.Y))

            move1.Combine(scale)
            move1.Combine(rotate)
            move1.Combine(move2)

            ################################################################
            ## transform
            ################################################################
            kcs_draft.element_transform(view, move1)

        except Exception, e:
            print e

def ChangeViewProjection(handle, angle1, angle2):
    ################################################################
    ## change view projection
    ################################################################

    xAxis = KcsVector3D.Vector3D(1, 0, 0)
    yAxis = KcsVector3D.Vector3D(0, 1, 0)
    zAxis = KcsVector3D.Vector3D(0, 0, 1)

    ################################################################
    ## remember center of view extension
    ################################################################
    ext = kcs_draft.element_extent_get(handle)
    extcen = KcsPoint2D.Point2D((ext[0].X+ext[1].X)/2.0, (ext[0].Y+ext[1].Y)/2.0)

    ################################################################
    ## adjust Tribon coordinate system to view along
    ## X axis (Z goes up, Y right)
    ## Tribon coordinate system: view along Z axis, X right, Y up
    ################################################################

    # rotate 90 degrees around Y axis
    # view is then along X axis (Y goes up, Z left)
    center = KcsPoint3D.Point3D(0, 0, 0)
    proj1 = KcsTransformation3D.Transformation3D()
    proj1.Rotate(center, yAxis, (math.pi/2))

    # rotate 90 degrees around X axis
    # view is then along X axis (Y goes right, Z up)
    proj2 = KcsTransformation3D.Transformation3D()
    proj2.Rotate(center, xAxis, (math.pi/2))
    proj1.Combine(proj2)

    ################################################################
    ## apply user settings
    ################################################################

    ro = (angle1 * math.pi)/180.0
    fi = (angle2 * math.pi)/180.0

    # apply XY Plane rotation
    proj3 = KcsTransformation3D.Transformation3D()
    proj3.Rotate(center, yAxis, -fi)
    proj1.Combine(proj3)

    # apply rotation around Z axis
    proj4 = KcsTransformation3D.Transformation3D()
    proj4.Rotate(center, zAxis, ro)
    proj1.Combine(proj4)

    ################################################################
    ## calculate new U and V vectors and apply new projection
    ################################################################
    try:
        # transform X, Y axis vectors
        xAxis.Transform(proj1)
        yAxis.Transform(proj1)

        # change projection
        kcs_draft.view_projection_set(handle, xAxis, yAxis)
    except Exception, e:
        CommonSample.ReportTribonError(kcs_draft)

    ################################################################
    ## move view to fit previous center
    ################################################################
    ext = kcs_draft.element_extent_get(handle)
    newextcen = KcsPoint2D.Point2D((ext[0].X+ext[1].X)/2.0, (ext[0].Y+ext[1].Y)/2.0)
    move = KcsVector2D.Vector2D((extcen.X-newextcen.X), (extcen.Y-newextcen.Y))
    kcs_draft.view_move(handle, move)

def run(*args):
    if not hasattr(kcs_draft, 'ContextSubpictures'):
        return
    if kcs_draft.ContextSubpictures == None or len(kcs_draft.ContextSubpictures)==0:
        return

    try:
        app = wxPySimpleApp()

        dlg = CtxSubpictPropDlg.CtxSubpictPropDlg(NULL)
        app.SetTopWindow(dlg)

        viewextent, subextent, compextent, viewrestr = None, None, None, None

        try:
            view = kcs_draft.ContextSubpictures[0]
            oldViewName     = kcs_draft.subpicture_name_get(view)
            dlg.ViewName    = oldViewName

            oldViewLayerId = kcs_draft.element_layer_get(view, KcsLayer.Layer()).GetLayer()
            dlg.ViewLayerId = oldViewLayerId

            transf = KcsTransformation2D.Transformation2D()
            transf = kcs_draft.element_transformation_get(view, transf)

            oldViewScale  = round(transf.GetScale()[0], 4)
            dlg.ViewScale = oldViewScale

            oldViewRotation  = round(transf.GetRotation(), 4)
            dlg.ViewRotation = oldViewRotation

            viewextent = kcs_draft.element_extent_get(view)
            try:
                viewrestr = kcs_draft.view_restriction_area_get(view)
            except:
                pass

            # subview properties
            if len(kcs_draft.ContextSubpictures)>1:
                subview = kcs_draft.ContextSubpictures[1]
                oldSubName     = kcs_draft.subpicture_name_get(subview)
                dlg.SubName    = oldSubName

                oldSubLayerId = kcs_draft.element_layer_get(subview, KcsLayer.Layer()).GetLayer()
                dlg.SubLayerId = oldSubLayerId
                subextent  = kcs_draft.element_extent_get(subview)

            # component properties
            if len(kcs_draft.ContextSubpictures)>2:
                component = kcs_draft.ContextSubpictures[2]

                oldCompName     = kcs_draft.subpicture_name_get(component)
                dlg.CompName    = oldCompName

                oldCompLayerId = kcs_draft.element_layer_get(component, KcsLayer.Layer()).GetLayer()
                dlg.CompLayerId = oldCompLayerId
                compextent = kcs_draft.element_extent_get(component)

            dlg.SetAreas(viewextent, subextent, compextent, viewrestr)

        except Exception, e:
            print e
            CommonSample.ReportTribonError(kcs_draft)

        repaint = 0

        if dlg.ShowModal() == wxID_OK:

            # view name
            if oldViewName != dlg.ViewName:
                SetSubpictureName(view, dlg.ViewName)

            # view layer
            if oldViewLayerId != dlg.ViewLayerId:
                SetSubpictureLayer(view, KcsLayer.Layer(dlg.ViewLayerId))

            # view 2D transformation
            if oldViewScale != dlg.ViewScale or oldViewRotation != dlg.ViewRotation:
                ChangeViewTransformation(view, transf, dlg.ViewRotation, dlg.ViewScale)

            # view projection
            if dlg.ProjectionChanged:
                ChangeViewProjection(view, dlg.ProjAngle1, dlg.ProjAngle2)

            # view colour
            if dlg.ViewColourName != CtxSubpictPropDlg.EMPTY_NAME:
                SetSubpictureColour(view, KcsColour.Colour(dlg.ViewColourName))
                repaint = 1

            # view linetype
            if dlg.ViewLTypeName != CtxSubpictPropDlg.EMPTY_NAME:
                SetSubpictureLinetype(view, KcsLinetype.Linetype(dlg.ViewLTypeName))
                repaint = 1

            if len(kcs_draft.ContextSubpictures)>1:
                # subview colour
                if dlg.SubColourName != CtxSubpictPropDlg.EMPTY_NAME:
                    if repaint:
                        kcs_draft.dwg_repaint()
                    SetSubpictureColour(subview, KcsColour.Colour(dlg.SubColourName))

                # subview linetype
                if dlg.SubLTypeName != CtxSubpictPropDlg.EMPTY_NAME:
                    SetSubpictureLinetype(subview, KcsLinetype.Linetype(dlg.SubLTypeName))

                # subview name
                if oldSubName != dlg.SubName:
                    SetSubpictureName(subview, dlg.SubName)

                # subview layer
                if oldSubLayerId != dlg.SubLayerId:
                    SetSubpictureLayer(subview, KcsLayer.Layer(dlg.SubLayerId))

            if len(kcs_draft.ContextSubpictures)>2:
                # component colour
                if dlg.CompColourName != CtxSubpictPropDlg.EMPTY_NAME:
                    if repaint:
                        kcs_draft.dwg_repaint()
                    SetSubpictureColour(component, KcsColour.Colour(dlg.CompColourName))

                # component linetype
                if dlg.CompLTypeName != CtxSubpictPropDlg.EMPTY_NAME:
                    SetSubpictureLinetype(component, KcsLinetype.Linetype(dlg.CompLTypeName))

                # component name
                if oldCompName != dlg.CompName:
                    SetSubpictureName(component, dlg.CompName)

                # component layer
                if oldCompLayerId != dlg.CompLayerId:
                    SetSubpictureLayer(component, KcsLayer.Layer(dlg.CompLayerId))

    except Exception, e:
        print e
