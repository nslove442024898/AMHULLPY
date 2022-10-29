## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#Boa:Dialog:CtxSubpictPropDlg
##-----------------------------------------------------------------------------
## Name:        CtxSubpictPropDlg.py
## Purpose:     Implementation of dialog box for subpicture properties
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: CtxSubpictPropDlg.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsLayer
import KcsColour
import KcsLinetype
import KcsTransformation2D
import KcsPoint2D
import kcs_draft

import CtxViewProjDlg
from wxPython.wx import *
from CtxValidators import *

def create(parent):
    return CtxSubpictPropDlg(parent)

EMPTY_NAME = "<don't change>"

[wxID_SUBPICTPROPDLGVIEWEXTENTS, wxID_SUBPICTPROPDLGCOMPEXTENTS, wxID_SUBPICTPROPDLGSTATICTEXT18, wxID_SUBPICTPROPDLGSTATICTEXT17, \
 wxID_SUBPICTPROPDLGSTATICTEXT16, wxID_SUBPICTPROPDLGSTATICTEXT15, wxID_SUBPICTPROPDLGSTATICTEXT14, wxID_SUBPICTPROPDLGVIEWLTYPECOMBO, \
 wxID_SUBPICTPROPDLGSTATICTEXT12, wxID_SUBPICTPROPDLGSTATICTEXT11, wxID_SUBPICTPROPDLGSTATICTEXT10, wxID_SUBPICTPROPDLGVIEWLAYEREDIT, \
 wxID_SUBPICTPROPDLGVIEWNAMEEDIT, wxID_SUBPICTPROPDLGSUBLAYEREDIT, wxID_SUBPICTPROPDLGCOMPNAMEEDIT, wxID_SUBPICTPROPDLGPROJECTIONBTN, \
 wxID_SUBPICTPROPDLGSUBEXTENTS, wxID_SUBPICTPROPDLGCOMPLTYPECOMBO, wxID_SUBPICTPROPDLGSUBCOLOURCOMBO, wxID_SUBPICTPROPDLGSUBLTYPECOMBO, \
 wxID_SUBPICTPROPDLGCOMPBOX, wxID_SUBPICTPROPDLGSUBVIEWBOX, wxID_SUBPICTPROPDLGSTATICBOX4, wxID_SUBPICTPROPDLGSTATICTEXT13, \
 wxID_SUBPICTPROPDLGCOMPLAYEREDIT, wxID_SUBPICTPROPDLGSTATICBOX1, wxID_SUBPICTPROPDLGVIEWSCALEEDIT, wxID_SUBPICTPROPDLGSUBNAMEEDIT, \
 wxID_SUBPICTPROPDLGRESTREXTENTS, wxID_SUBPICTPROPDLGSTATICTEXT1, wxID_SUBPICTPROPDLGSTATICTEXT3, wxID_SUBPICTPROPDLGSTATICTEXT2, \
 wxID_SUBPICTPROPDLGSTATICTEXT5, wxID_SUBPICTPROPDLGSTATICTEXT4, wxID_SUBPICTPROPDLGSTATICTEXT7, wxID_SUBPICTPROPDLGSTATICTEXT6, \
 wxID_SUBPICTPROPDLGSTATICTEXT9, wxID_SUBPICTPROPDLGSTATICTEXT8, wxID_SUBPICTPROPDLGVIEWROTATIONEDIT, wxID_SUBPICTPROPDLGCOMPCOLOURCOMBO, \
 wxID_SUBPICTPROPDLGVIEWCOLOURCOMBO, wxID_SUBPICTPROPDLG] = map(lambda _init_ctrls: wxNewId(), range(42))

class CtxSubpictPropDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(418, 491), id = wxID_SUBPICTPROPDLG, title = 'Subpicture properties', parent = prnt, name = 'SubpictPropDlg', \
               style = wxSTAY_ON_TOP | wxDOUBLE_BORDER | wxDEFAULT_FRAME_STYLE | wxDIALOG_MODAL, pos = wxPoint(449, 327))

        self._init_utils()

        self.ViewNameEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(32, 40), parent = self, name = 'ViewNameEdit', style = 0, id = wxID_SUBPICTPROPDLGVIEWNAMEEDIT)

        self.ViewLayerEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(32, 88), parent = self, name = 'ViewLayerEdit', style = 0, id = wxID_SUBPICTPROPDLGVIEWLAYEREDIT)

        self.ViewScaleEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(144, 40), parent = self, name = 'ViewScaleEdit', style = 0, id = wxID_SUBPICTPROPDLGVIEWSCALEEDIT)

        self.ViewRotationEdit = wxTextCtrl(size = wxSize(104, 21), value = '', pos = wxPoint(144, 88), parent = self, name = 'ViewRotationEdit', style = 0, id = wxID_SUBPICTPROPDLGVIEWROTATIONEDIT)

        self.staticText1 = wxStaticText(label = 'Name:', id = wxID_SUBPICTPROPDLGSTATICTEXT1, parent = self, name = 'staticText1', size = wxSize(52, 13), style = 0, pos = wxPoint(32, 24))

        self.staticText2 = wxStaticText(label = 'Layer:', id = wxID_SUBPICTPROPDLGSTATICTEXT2, parent = self, name = 'staticText2', size = wxSize(52, 13), style = 0, pos = wxPoint(32, 72))

        self.staticText3 = wxStaticText(label = 'Scale:', id = wxID_SUBPICTPROPDLGSTATICTEXT3, parent = self, name = 'staticText3', size = wxSize(52, 13), style = 0, pos = wxPoint(144, 24))

        self.staticBox1 = wxStaticBox(label = 'View', id = wxID_SUBPICTPROPDLGSTATICBOX1, parent = self, name = 'staticBox1', size = wxSize(392, 144), style = 0, pos = wxPoint(8, 8))

        self.staticText4 = wxStaticText(label = 'Rotation:', id = wxID_SUBPICTPROPDLGSTATICTEXT4, parent = self, name = 'staticText4', size = wxSize(52, 13), style = 0, pos = wxPoint(144, 72))

        self.SubviewBox = wxStaticBox(label = 'Subview', id = wxID_SUBPICTPROPDLGSUBVIEWBOX, parent = self, name = 'SubviewBox', size = wxSize(196, 144), style = 0, pos = wxPoint(8, 160))

        self.CompBox = wxStaticBox(label = 'Component', id = wxID_SUBPICTPROPDLGCOMPBOX, parent = self, name = 'CompBox', size = wxSize(192, 144), style = 0, pos = wxPoint(208, 160))

        self.ProjectionBtn = wxButton(label = 'Projection', id = wxID_SUBPICTPROPDLGPROJECTIONBTN, parent = self, name = 'ProjectionBtn', size = wxSize(75, 23), style = 0, pos = wxPoint(312, 120))
        EVT_BUTTON(self.ProjectionBtn, wxID_SUBPICTPROPDLGPROJECTIONBTN, self.OnProjectionbtnButton)

        self.ViewColourCombo = wxChoice(size = wxSize(125, 21), id = wxID_SUBPICTPROPDLGVIEWCOLOURCOMBO, choices = [], parent = self, name = 'ViewColourCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(264, 40))

        self.ViewLTypeCombo = wxChoice(size = wxSize(125, 21), id = wxID_SUBPICTPROPDLGVIEWLTYPECOMBO, choices = [], parent = self, name = 'ViewLTypeCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(264, 88))

        self.SubColourCombo = wxChoice(size = wxSize(128, 21), id = wxID_SUBPICTPROPDLGSUBCOLOURCOMBO, choices = [], parent = self, name = 'SubColourCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(68, 240))

        self.SubLTypeCombo = wxChoice(size = wxSize(128, 21), id = wxID_SUBPICTPROPDLGSUBLTYPECOMBO, choices = [], parent = self, name = 'SubLTypeCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(68, 272))

        self.staticText6 = wxStaticText(label = 'Colour:', id = wxID_SUBPICTPROPDLGSTATICTEXT6, parent = self, name = 'staticText6', size = wxSize(52, 13), style = 0, pos = wxPoint(264, 24))

        self.staticText7 = wxStaticText(label = 'Line type:', id = wxID_SUBPICTPROPDLGSTATICTEXT7, parent = self, name = 'staticText7', size = wxSize(52, 13), style = 0, pos = wxPoint(264, 72))

        self.staticText8 = wxStaticText(label = 'Colour:', id = wxID_SUBPICTPROPDLGSTATICTEXT8, parent = self, name = 'staticText8', size = wxSize(52, 13), style = 0, pos = wxPoint(16, 248))

        self.staticText9 = wxStaticText(label = 'Line type:', id = wxID_SUBPICTPROPDLGSTATICTEXT9, parent = self, name = 'staticText9', size = wxSize(52, 13), style = 0, pos = wxPoint(16, 280))

        self.SubNameEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(96, 176), parent = self, name = 'SubNameEdit', style = 0, id = wxID_SUBPICTPROPDLGSUBNAMEEDIT)

        self.SubLayerEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(96, 208), parent = self, name = 'SubLayerEdit', style = 0, id = wxID_SUBPICTPROPDLGSUBLAYEREDIT)

        self.staticText10 = wxStaticText(label = 'Name:', id = wxID_SUBPICTPROPDLGSTATICTEXT10, parent = self, name = 'staticText10', size = wxSize(58, 13), style = 0, pos = wxPoint(16, 184))

        self.staticText11 = wxStaticText(label = 'Layer:', id = wxID_SUBPICTPROPDLGSTATICTEXT11, parent = self, name = 'staticText11', size = wxSize(58, 13), style = 0, pos = wxPoint(16, 216))

        self.CompNameEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(292, 176), parent = self, name = 'CompNameEdit', style = 0, id = wxID_SUBPICTPROPDLGCOMPNAMEEDIT)

        self.CompLayerEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(292, 208), parent = self, name = 'CompLayerEdit', style = 0, id = wxID_SUBPICTPROPDLGCOMPLAYEREDIT)

        self.CompColourCombo = wxChoice(size = wxSize(128, 21), id = wxID_SUBPICTPROPDLGCOMPCOLOURCOMBO, choices = [], parent = self, name = 'CompColourCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(264, 240))

        self.CompLTypeCombo = wxChoice(size = wxSize(128, 21), id = wxID_SUBPICTPROPDLGCOMPLTYPECOMBO, choices = [], parent = self, name = 'CompLTypeCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(264, 272))

        self.staticText12 = wxStaticText(label = 'Name:', id = wxID_SUBPICTPROPDLGSTATICTEXT12, parent = self, name = 'staticText12', size = wxSize(58, 13), style = 0, pos = wxPoint(216, 184))

        self.staticText13 = wxStaticText(label = 'Layer:', id = wxID_SUBPICTPROPDLGSTATICTEXT13, parent = self, name = 'staticText13', size = wxSize(58, 13), style = 0, pos = wxPoint(216, 216))

        self.staticText14 = wxStaticText(label = 'Colour:', id = wxID_SUBPICTPROPDLGSTATICTEXT14, parent = self, name = 'staticText14', size = wxSize(40, 13), style = 0, pos = wxPoint(216, 248))

        self.staticText15 = wxStaticText(label = 'Line type:', id = wxID_SUBPICTPROPDLGSTATICTEXT15, parent = self, name = 'staticText15', size = wxSize(48, 13), style = 0, pos = wxPoint(216, 280))

        self.staticBox4 = wxStaticBox(label = 'Extensions and restriction', id = wxID_SUBPICTPROPDLGSTATICBOX4, parent = self, name = 'staticBox4', size = wxSize(392, 120), style = 0, pos = wxPoint(8, 310))

        self.ViewExtents = wxStaticText(label = '', id = wxID_SUBPICTPROPDLGVIEWEXTENTS, parent = self, name = 'ViewExtents', size = wxSize(272, 13), style = wxALIGN_CENTRE, pos = wxPoint(120, 328))

        self.SubExtents = wxStaticText(label = '', id = wxID_SUBPICTPROPDLGSUBEXTENTS, parent = self, name = 'SubExtents', size = wxSize(272, 13), style = wxALIGN_CENTRE, pos = wxPoint(120, 352))

        self.CompExtents = wxStaticText(label = '', id = wxID_SUBPICTPROPDLGCOMPEXTENTS, parent = self, name = 'CompExtents', size = wxSize(272, 13), style = wxALIGN_CENTRE, pos = wxPoint(120, 376))

        self.RestrExtents = wxStaticText(label = '', id = wxID_SUBPICTPROPDLGRESTREXTENTS, parent = self, name = 'RestrExtents', size = wxSize(272, 13), style = wxALIGN_CENTRE, pos = wxPoint(120, 400))

        self.staticText5 = wxStaticText(label = 'View extents:', id = wxID_SUBPICTPROPDLGSTATICTEXT5, parent = self, name = 'staticText5', size = wxSize(96, 13), style = 0, pos = wxPoint(16, 328))

        self.staticText16 = wxStaticText(label = 'Subview extents:', id = wxID_SUBPICTPROPDLGSTATICTEXT16, parent = self, name = 'staticText16', size = wxSize(88, 13), style = 0, pos = wxPoint(16, 352))

        self.staticText17 = wxStaticText(label = 'Component extents:', id = wxID_SUBPICTPROPDLGSTATICTEXT17, parent = self, name = 'staticText17', size = wxSize(96, 13), style = 0, pos = wxPoint(16, 376))

        self.staticText18 = wxStaticText(label = 'View restrictions:', id = wxID_SUBPICTPROPDLGSTATICTEXT18, parent = self, name = 'staticText18', size = wxSize(96, 13), style = 0, pos = wxPoint(16, 400))

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.OkButton = wxButton(self, wxID_OK,     " OK ", wxPoint(245, 435), wxDefaultSize)
        self.CancelButton = wxButton(self, wxID_CANCEL,     "Cancel", wxPoint(325, 435), wxDefaultSize)
        self.OkButton.SetDefault()

        self.CancelButton = wxButton(self, wxID_CANCEL,     "Cancel", wxPoint(440, 210), wxDefaultSize)

        self.ViewName = ''
        self.ViewNameEdit.SetValidator(TextValidator(self, 'ViewName'))

        self.ViewLayerId = 0
        self.ViewLayerEdit.SetValidator(NumericValidator(self, 'ViewLayerId'))

        self.ViewScale = 1.0
        self.ViewScaleEdit.SetValidator(ScaleValidator(self, 'ViewScale'))

        self.ViewRotation = 0.0
        self.ViewRotationEdit.SetValidator(NumericValidator(self, 'ViewRotation'))

        self.ViewTransf2d = KcsTransformation2D.Transformation2D()
        self.ProjAngle1   = 0
        self.ProjAngle2   = 0
        self.ProjectionChanged = 0

        self.FillColourCombo(self.ViewColourCombo)
        self.ViewColourName = EMPTY_NAME
        self.ViewColourCombo.SetValidator(TextValidator(self, 'ViewColourName'))

        self.FillLTypeCombo(self.ViewLTypeCombo)
        self.ViewLTypeName = EMPTY_NAME
        self.ViewLTypeCombo.SetValidator(TextValidator(self, 'ViewLTypeName'))

        self.DisableControls()

        # subview
        self.SubName = ''
        self.SubNameEdit.SetValidator(TextValidator(self, 'SubName'))

        self.SubLayerId = 0
        self.SubLayerEdit.SetValidator(NumericValidator(self, 'SubLayerId'))

        self.FillColourCombo(self.SubColourCombo)
        self.SubColourName = EMPTY_NAME
        self.SubColourCombo.SetValidator(TextValidator(self, 'SubColourName'))

        self.FillLTypeCombo(self.SubLTypeCombo)
        self.SubLTypeName = EMPTY_NAME
        self.SubLTypeCombo.SetValidator(TextValidator(self, 'SubLTypeName'))

        # component
        self.CompName = ''
        self.CompNameEdit.SetValidator(TextValidator(self, 'CompName'))

        self.CompLayerId = 0
        self.CompLayerEdit.SetValidator(NumericValidator(self, 'CompLayerId'))

        self.FillColourCombo(self.CompColourCombo)
        self.CompColourName = EMPTY_NAME
        self.CompColourCombo.SetValidator(TextValidator(self, 'CompColourName'))

        self.FillLTypeCombo(self.CompLTypeCombo)
        self.CompLTypeName = EMPTY_NAME
        self.CompLTypeCombo.SetValidator(TextValidator(self, 'CompLTypeName'))

    def FillLTypeCombo(self, combo):
        combo.Append(EMPTY_NAME)
        ltypes = KcsLinetype.GetLinetypes().values()
        ltypes.sort()
        for linetype in ltypes:
            combo.Append(linetype)

    def FillColourCombo(self, combo):
        combo.Append(EMPTY_NAME)
        for colour in KcsColour.ColourStrings:
            combo.Append(colour)

    def OnProjectionbtnButton(self, event):
        dlg = CtxViewProjDlg.CtxViewProjectDlg(self)

        dlg.SetAngles(self.ProjAngle1, self.ProjAngle2)
        if dlg.ShowModal() == wxID_OK:
            self.ProjectionChanged = 1
            self.ProjAngle1, self.ProjAngle2 = dlg.GetAngles()

    def SetAreas(self, view, sub, comp, restr):
        if view != None:
            text = '%g, %g   -   %g, %g' % (view[0].X, view[0].Y, view[1].X, view[1].Y)
            self.ViewExtents.SetTitle(text)
        if sub != None:
            text = '%g, %g   -   %g, %g' % (sub[0].X, sub[0].Y, sub[1].X, sub[1].Y)
            self.SubExtents.SetTitle(text)
        if comp != None:
            text = '%g, %g   -   %g, %g' % (comp[0].X, comp[0].Y, comp[1].X, comp[1].Y)
            self.CompExtents.SetTitle(text)
        if restr != None:
            text = '%g, %g   -   %g, %g' % (restr[0].X, restr[0].Y, restr[1].X, restr[1].Y)
        else:
            text = 'Not defined'
        self.RestrExtents.SetTitle(text)

    def DisableControls(self):
        # subview items
        enable = len(kcs_draft.ContextSubpictures)>1
        self.SubviewBox.Enable(enable)
        self.staticText8.Enable(enable)
        self.staticText9.Enable(enable)
        self.staticText10.Enable(enable)
        self.staticText11.Enable(enable)
        self.SubNameEdit.Enable(enable)
        self.SubLayerEdit.Enable(enable)
        self.SubColourCombo.Enable(enable)
        self.SubLTypeCombo.Enable(enable)
        self.SubExtents.Enable(enable)
        self.staticText16.Enable(enable)

        # component items
        enable = len(kcs_draft.ContextSubpictures)>2
        self.CompBox.Enable(enable)
        self.staticText12.Enable(enable)
        self.staticText13.Enable(enable)
        self.staticText14.Enable(enable)
        self.staticText15.Enable(enable)
        self.CompNameEdit.Enable(enable)
        self.CompLayerEdit.Enable(enable)
        self.CompColourCombo.Enable(enable)
        self.CompLTypeCombo.Enable(enable)
        self.CompExtents.Enable(enable)
        self.staticText17.Enable(enable)


