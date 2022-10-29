## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu3.py
## Purpose:     Python implementation of context menu "Text properties" item
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu3.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsElementHandle
import KcsPoint2D
import KcsText
import CommonSample

import kcs_draft
import kcs_ui

from wxPython.wx import *
import sys

import CtxTextPropDlg

def run(*args):
    if not hasattr(kcs_draft, 'ContextElement'):
        return
    if kcs_draft.ContextElement == None:
        return

    try:
        # get text properties
        text = KcsText.Text()
        text = kcs_draft.text_properties_get(kcs_draft.ContextElement, text)
        point = text.GetPosition()
        point.X = round(point.X, 2)
        point.Y = round(point.Y, 2)
        text.SetPosition(point)

        # display dialog
        app = wxPySimpleApp()

        dlg = CtxTextPropDlg.CtxTextPropDlg(NULL)
        dlg.SetText(text)

        if dlg.ShowModal() == wxID_OK:
            newtext = dlg.GetText()
            if newtext != text:
                try:
                    # recreate text
                    parent = kcs_draft.element_parent_get(kcs_draft.ContextElement)
                    kcs_draft.subpicture_current_set(parent)
                    kcs_draft.element_delete(kcs_draft.ContextElement)
                    kcs_draft.text_new(newtext)
                    kcs_ui.app_window_refresh()
                except:
                    CommonSample.ReportTribonError(kcs_draft)
    except:
        print sys.exc_info()[1]
