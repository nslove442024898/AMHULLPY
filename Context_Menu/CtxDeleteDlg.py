## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#Boa:Dialog:CtxDeleteDlg
##-----------------------------------------------------------------------------
## Name:        CtxDeleteDlg.py
## Purpose:     Dialog box with delete options
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: CtxDeleteDlg.py $
## Licence:
##-----------------------------------------------------------------------------

from wxPython.wx import *

def create(parent):
    return CtxDeleteDlg(parent)

[wxID_DELETEDLGCANCELBTN, wxID_DELETEDLGVIEWBTN, wxID_DELETEDLGCOMPONENTBTN, wxID_DELETEDLGELEMENTBTN, wxID_DELETEDLGSUBVIEWBTN, wxID_DELETEDLG] = map(lambda _init_ctrls: wxNewId(), range(6))

class CtxDeleteDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(130, 211), id = wxID_DELETEDLG, title = 'Delete', parent = prnt, name = 'DeleteDlg', style = wxDEFAULT_DIALOG_STYLE | wxCAPTION | wxTHICK_FRAME | wxDOUBLE_BORDER | wxSTAY_ON_TOP | wxDIALOG_MODAL, pos = wxPoint(

        self._init_utils()

        self.ViewBtn = wxButton(label = 'View', id = wxID_DELETEDLGVIEWBTN, parent = self, name = 'ViewBtn', size = wxSize(104, 32), style = 0, pos = wxPoint(8, 8))
        EVT_BUTTON(self.ViewBtn, wxID_DELETEDLGVIEWBTN, self.OnViewbtnButton)

        self.SubviewBtn = wxButton(label = 'Subview', id = wxID_DELETEDLGSUBVIEWBTN, parent = self, name = 'SubviewBtn', size = wxSize(104, 32), style = 0, pos = wxPoint(8, 40))
        EVT_BUTTON(self.SubviewBtn, wxID_DELETEDLGSUBVIEWBTN, self.OnSubviewbtnButton)

        self.ComponentBtn = wxButton(label = 'Component', id = wxID_DELETEDLGCOMPONENTBTN, parent = self, name = 'ComponentBtn', size = wxSize(104, 32), style = 0, pos = wxPoint(8, 72))
        EVT_BUTTON(self.ComponentBtn, wxID_DELETEDLGCOMPONENTBTN, self.OnComponentbtnButton)

        self.ElementBtn = wxButton(label = 'Element', id = wxID_DELETEDLGELEMENTBTN, parent = self, name = 'ElementBtn', size = wxSize(104, 32), style = 0, pos = wxPoint(8, 104))
        EVT_BUTTON(self.ElementBtn, wxID_DELETEDLGELEMENTBTN, self.OnElementbtnButton)

        self.CancelBtn = wxButton(label = 'Cancel', id = wxID_DELETEDLGCANCELBTN, parent = self, name = 'CancelBtn', size = wxSize(104, 32), style = 0, pos = wxPoint(8, 144))
        EVT_BUTTON(self.CancelBtn, wxID_DELETEDLGCANCELBTN, self.OnCancelbtnButton)

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.SelectedType = 3

    def SetButtonTitle(self, index, title):
        if index == 0:
            self.ViewBtn.SetTitle(title)
        elif index == 1:
            self.SubviewBtn.SetTitle(title)
        elif index == 2:
            self.ComponentBtn.SetTitle(title)
        elif index == 3:
            self.ElementBtn.SetTitle(title)

    def EnableButton(self, index, enable):
        if index == 0:
            self.ViewBtn.Enable(enable)
        elif index == 1:
            self.SubviewBtn.Enable(enable)
        elif index == 2:
            self.ComponentBtn.Enable(enable)
        elif index == 3:
            self.ElementBtn.Enable(enable)

    def OnViewbtnButton(self, event):
        self.SelectedType = 0
        self.EndModal(wxID_OK)

    def OnSubviewbtnButton(self, event):
        self.SelectedType = 1
        self.EndModal(wxID_OK)

    def OnComponentbtnButton(self, event):
        self.SelectedType = 2
        self.EndModal(wxID_OK)

    def OnElementbtnButton(self, event):
        self.SelectedType = 3
        self.EndModal(wxID_OK)

    def OnCancelbtnButton(self, event):
        self.EndModal(wxID_CANCEL)
