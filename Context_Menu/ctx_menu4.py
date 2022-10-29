## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu4.py
## Purpose:     Implementations of dialog box used to display symbol properties
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu4.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsElementHandle
import KcsPoint2D
import KcsSymbol
import CommonSample

import kcs_draft
import kcs_ui

from wxPython.wx import *
import sys

import CtxSymbolPropDlg

def run(*args):

    if not hasattr(kcs_draft, 'ContextElement'):
        return
    if kcs_draft.ContextElement == None:
        return

    try:
        symbol = KcsSymbol.Symbol()
        symbol = kcs_draft.symbol_properties_get(kcs_draft.ContextElement, symbol)
        point = symbol.GetPosition()
        point.X = round(point.X, 5)
        point.Y = round(point.Y, 5)
        symbol.SetPosition(point)

        app = wxPySimpleApp()

        dlg = CtxSymbolPropDlg.CtxSymbolPropDlg(NULL)
        dlg.SetSymbol(symbol)

        if dlg.ShowModal() == wxID_OK:
            newsymbol = dlg.GetSymbol()
            print symbol
            print newsymbol
            if newsymbol != symbol:
                try:
                    # recreate symbol
                    parent = kcs_draft.element_parent_get(kcs_draft.ContextElement)
                    kcs_draft.subpicture_current_set(parent)
                    kcs_draft.symbol_new(newsymbol)
                    kcs_draft.element_delete(kcs_draft.ContextElement)
                    kcs_ui.app_window_refresh()
                except:
                    CommonSample.ReportTribonError(kcs_draft)
    except:
        print sys.exc_info()[1]
