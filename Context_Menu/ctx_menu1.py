## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu1.py
## Purpose:     Python implementation of context menu "Delete" item
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu1.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsModel
import KcsElementHandle
import KcsPoint2D
import CommonSample

import kcs_draft

from wxPython.wx import *
import sys
import CtxDeleteDlg

def run(*args):

    # check if there is something to delete
    if not hasattr(kcs_draft, 'ContextSubpictures'):
        return
    if not len(kcs_draft.ContextSubpictures):
        return

    try:
        app = wxPySimpleApp()

        type = 4    # type of element to delete (0-3), 4 will not be handled

        # if there is element display CtxDeleteDlg
        if hasattr(kcs_draft, 'ContextElement') and kcs_draft.ContextElement != None:
            dlg = CtxDeleteDlg.CtxDeleteDlg(NULL)

            if hasattr(kcs_draft, 'ContextModel') and kcs_draft.ContextModel != None:
                dlg.SetButtonTitle(1, 'Model subview')
                dlg.SetButtonTitle(2, 'Model component')

            if hasattr(kcs_draft, 'ContextElement') and kcs_draft.ContextElement != None:
                try:
                    if kcs_draft.element_is_text(kcs_draft.ContextElement):
                        dlg.SetButtonTitle(3, 'Text')
                    elif kcs_draft.element_is_contour(kcs_draft.ContextElement):
                        dlg.SetButtonTitle(3, 'Contour')
                    elif kcs_draft.element_is_symbol(kcs_draft.ContextElement):
                        dlg.SetButtonTitle(3, 'Symbol')
                except:
                    pass

            if dlg.ShowModal() == wxID_OK:
                type = dlg.SelectedType
            print type

        # if there is no element set index to last subpicture which is
        # relevant to  selected on tree view
        else:
            type = len(kcs_draft.ContextSubpictures)-1

        # delete element
        try:
            if type == 0:
                kcs_draft.element_delete(kcs_draft.ContextSubpictures[0])
            elif type == 1:
                kcs_draft.element_delete(kcs_draft.ContextSubpictures[1])
            elif type == 2:
                kcs_draft.element_delete(kcs_draft.ContextSubpictures[2])
            elif type == 3:
                kcs_draft.element_delete(kcs_draft.ContextElement)
        except:
            CommonSample.ReportTribonError(kcs_draft)

    except:
        print sys.exc_info()[1]
