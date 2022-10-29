## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu5.py
## Purpose:
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu5.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsElementHandle
import KcsPoint2D
import KcsContour2D
import CommonSample

import kcs_draft
import kcs_ui

from wxPython.wx import *

import CtxContourPropDlg

# function used to round contour coordinates for better display performance
def RoundCoordinates(contour):
    for item in contour.Contour:
        item[0].X = round(item[0].X, 2)
        item[0].Y = round(item[0].Y, 2)
        if len(item)==2:
            item[1] = round(item[1], 2)

# main function
def run(*args):
    if not hasattr(kcs_draft, 'ContextElement'):
        return
    if kcs_draft.ContextElement == None:
        return

    try:
        # get contour properties
        contour = KcsContour2D.Contour2D(KcsPoint2D.Point2D())
        contour = kcs_draft.contour_properties_get(kcs_draft.ContextElement, contour)
        RoundCoordinates(contour)

        # display dialog
        app = wxPySimpleApp()
        dlg = CtxContourPropDlg.CtxContourPropDlg(NULL)
        dlg.SetContour(contour)

        if dlg.ShowModal() == wxID_OK:
            newcontour = dlg.GetContour()
            if newcontour != contour:
                try:
                    # recreate contour
                    parent = kcs_draft.element_parent_get(kcs_draft.ContextElement)
                    kcs_draft.subpicture_current_set(parent)
                    kcs_draft.element_delete(kcs_draft.ContextElement)
                    kcs_draft.contour_new(newcontour)
                except:
                    CommonSample.ReportTribonError(kcs_draft)
    except Exception, e:
        print e
