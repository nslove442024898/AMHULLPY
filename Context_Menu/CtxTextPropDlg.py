## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
##-----------------------------------------------------------------------------
## Name:        CtxTextPropDlg.py
## Purpose:     Implementation of dialog box used to display text properties
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: CtxTextPropDlg.py $
## Licence:
##-----------------------------------------------------------------------------


import KcsText
import KcsColour
import KcsLinetype
import KcsPoint2D
import KcsLayer
import CommonSample

from wxPython.wx import *
from CtxValidators import *

import string
import copy

import kcs_ui
import kcs_util

def create(parent):
    return CtxTextPropDlg(parent)

[wxID_TEXTPROPDLGCONTENTSEDIT, wxID_TEXTPROPDLGCOLORCOMBO, wxID_TEXTPROPDLGHEIGHTEDIT, wxID_TEXTPROPDLGLAYEREDIT,\
 wxID_TEXTPROPDLGLINETYPECOMBO, wxID_TEXTPROPDLGFONTCOMBO, wxID_TEXTPROPDLGPOSITIONEDIT, wxID_TEXTPROPDLGASPECTEDIT, \
 wxID_TEXTPROPDLGSLANTINGEDIT, wxID_TEXTPROPDLGSTATICTEXT1, wxID_TEXTPROPDLGSELECTPOSBTN, wxID_TEXTPROPDLGSTATICTEXT3, \
 wxID_TEXTPROPDLGSTATICTEXT2, wxID_TEXTPROPDLGSTATICTEXT5, wxID_TEXTPROPDLGSTATICTEXT4, wxID_TEXTPROPDLGSTATICTEXT7, \
 wxID_TEXTPROPDLGSTATICTEXT9, wxID_TEXTPROPDLGSTATICTEXT8, wxID_TEXTPROPDLGSTATICTEXT6, wxID_TEXTPROPDLGROTATIONEDIT, \
 wxID_TEXTPROPDLG] = map(lambda _init_ctrls: wxNewId(), range(21))

class CtxTextPropDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(392, 263), id = wxID_TEXTPROPDLG, title = 'Text properties', parent = prnt, name = 'TextPropDlg', style = wxDEFAULT_DIALOG_STYLE, pos = wxPoint(498, 318))
        self._init_utils()

        self.ContentsEdit = wxTextCtrl(size = wxSize(368, 64), value = '', pos = wxPoint(8, 8), parent = self, name = 'ContentsEdit', style = wxTE_MULTILINE, id = wxID_TEXTPROPDLGCONTENTSEDIT)

        self.ColorCombo = wxChoice(size = wxSize(125, 21), id = wxID_TEXTPROPDLGCOLORCOMBO, choices = [], parent = self, name = 'ColorCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(64, 80))

        self.LinetypeCombo = wxChoice(size = wxSize(125, 21), id = wxID_TEXTPROPDLGLINETYPECOMBO, choices = [], parent = self, name = 'LinetypeCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(64, 112))

        self.PositionEdit = wxTextCtrl(size = wxSize(128, 21), value = '0, 0, 0', pos = wxPoint(64, 208), parent = self, name = 'PositionEdit', style = 0, id = wxID_TEXTPROPDLGPOSITIONEDIT)

        self.HeightEdit = wxTextCtrl(size = wxSize(120, 21), value = '0', pos = wxPoint(64, 176), parent = self, name = 'HeightEdit', style = 0, id = wxID_TEXTPROPDLGHEIGHTEDIT)

        self.staticText1 = wxStaticText(label = 'Position:', id = wxID_TEXTPROPDLGSTATICTEXT1, parent = self, name = 'staticText1', size = wxSize(40, 13), style = 0, pos = wxPoint(8, 216))

        self.staticText2 = wxStaticText(label = 'Height:', id = wxID_TEXTPROPDLGSTATICTEXT2, parent = self, name = 'staticText2', size = wxSize(34, 13), style = 0, pos = wxPoint(8, 184))

        self.staticText3 = wxStaticText(label = 'Layer:', id = wxID_TEXTPROPDLGSTATICTEXT3, parent = self, name = 'staticText3', size = wxSize(29, 13), style = 0, pos = wxPoint(208, 88))

        self.staticText4 = wxStaticText(label = 'Linetype:', id = wxID_TEXTPROPDLGSTATICTEXT4, parent = self, name = 'staticText4', size = wxSize(43, 13), style = 0, pos = wxPoint(8, 120))

        self.staticText5 = wxStaticText(label = 'Colour:', id = wxID_TEXTPROPDLGSTATICTEXT5, parent = self, name = 'staticText5', size = wxSize(33, 13), style = 0, pos = wxPoint(8, 88))

        self.RotationEdit = wxTextCtrl(size = wxSize(120, 21), value = '0', pos = wxPoint(64, 144), parent = self, name = 'RotationEdit', style = 0, id = wxID_TEXTPROPDLGROTATIONEDIT)

        self.staticText7 = wxStaticText(label = 'Rotation:', id = wxID_TEXTPROPDLGSTATICTEXT7, parent = self, name = 'staticText7', size = wxSize(43, 13), style = 0, pos = wxPoint(8, 152))

        self.AspectEdit = wxTextCtrl(size = wxSize(128, 21), value = '0', pos = wxPoint(248, 144), parent = self, name = 'AspectEdit', style = 0, id = wxID_TEXTPROPDLGASPECTEDIT)

        self.staticText8 = wxStaticText(label = 'Aspect:', id = wxID_TEXTPROPDLGSTATICTEXT8, parent = self, name = 'staticText8', size = wxSize(36, 13), style = 0, pos = wxPoint(200, 152))

        self.SlantingEdit = wxTextCtrl(size = wxSize(128, 21), value = 'textCtrl2', pos = wxPoint(248, 176), parent = self, name = 'SlantingEdit', style = 0, id = wxID_TEXTPROPDLGSLANTINGEDIT)

        self.staticText9 = wxStaticText(label = 'Slanting:', id = wxID_TEXTPROPDLGSTATICTEXT9, parent = self, name = 'staticText9', size = wxSize(41, 13), style = 0, pos = wxPoint(200, 184))

        self.LayerEdit = wxTextCtrl(size = wxSize(128, 21), value = '', pos = wxPoint(248, 80), parent = self, name = 'LayerEdit', style = 0, id = wxID_TEXTPROPDLGLAYEREDIT)

        self.SelectPosBtn = wxButton(label = '<', id = wxID_TEXTPROPDLGSELECTPOSBTN, parent = self, name = 'SelectPosBtn', size = wxSize(24, 23), style = 0, pos = wxPoint(192, 208))
        EVT_BUTTON(self.SelectPosBtn, wxID_TEXTPROPDLGSELECTPOSBTN, self.OnSelectposbtnButton)

        self.FontCombo = wxChoice(size = wxSize(128, 21), id = wxID_TEXTPROPDLGFONTCOMBO, choices = ['TBSystemFont1', 'TBSystemFont2', 'TBSystemFont3', 'TBSystemFont4', 'TBSystemFont5', 'TBSystemFont6', 'TBSystemFont7'], parent = self, \
                         name = 'FontCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(248, 112))

        self.staticText6 = wxStaticText(label = 'Font:', id = wxID_TEXTPROPDLGSTATICTEXT6, parent = self, name = 'staticText6', size = wxSize(24, 13), style = 0, pos = wxPoint(208, 120))

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.OkButton = wxButton(self, wxID_OK,     " OK ", wxPoint(305, 210), wxDefaultSize).SetDefault()
        self.CancelButton = wxButton(self, wxID_CANCEL,     "Cancel", wxPoint(225, 210), wxDefaultSize)

        # fill combo boxes
        for colour in KcsColour.ColourStrings:
            self.ColorCombo.Append(colour)


        ltypes = KcsLinetype.GetLinetypes().values()
        ltypes.sort()
        for linetype in ltypes:
            self.LinetypeCombo.Append(linetype)

        # enumerate font facenames and append them to font combo box
        fontEnum = wxFontEnumerator()
        fontEnum.EnumerateFacenames()
        fonts = fontEnum.GetFacenames()
        for fontName in fonts:
            self.FontCombo.Append(fontName)

        self.Text = KcsText.Text()

    def SetText(self, text):
        self.Text = copy.deepcopy(text)

        # text contents
        self.strContents = self.Text.GetString()
        self.ContentsEdit.SetValidator(TextValidator(self, 'strContents', 0))

        # layer
        self.LayerId = self.Text.GetLayer().GetLayer()
        self.LayerEdit.SetValidator(NumericValidator(self, 'LayerId'))

        # position point
        self.PosPoint = self.Text.GetPosition()
        self.PositionEdit.SetValidator(validator = Point2DValidator(self.PosPoint))

        # color
        self.ColorCombo.SetStringSelection(text.GetColour().Name())

        # linetype
        self.LinetypeCombo.SetStringSelection(KcsLinetype.GetAliasName(text.GetLineType().Name()))

        # rotation
        self.RotAngle = text.GetRotation()
        self.RotationEdit.SetValidator(NumericValidator(self, 'RotAngle'))

        # aspect
        self.AspectRatio = text.GetAspect()
        self.AspectEdit.SetValidator(NumericValidator(self, 'AspectRatio'))

        # height
        self.Height = text.GetHeight()
        self.HeightEdit.SetValidator(NumericValidator(self, 'Height'))

        # slanting
        self.Slanting = text.GetSlanting()
        self.SlantingEdit.SetValidator(NumericValidator(self, 'Slanting', None, POSITIVE_ONLY))

        # font
        self.FontCombo.SetStringSelection(text.GetFont())

    def GetText(self):
        self.Text.SetLayer(KcsLayer.Layer(self.LayerId))
        self.Text.SetString(self.strContents)
        self.Text.SetPosition(self.PosPoint)
        self.Text.SetColour(KcsColour.Colour(self.ColorCombo.GetStringSelection()))
        self.Text.SetLineType(KcsLinetype.Linetype(self.LinetypeCombo.GetStringSelection()))
        self.Text.SetRotation(self.RotAngle)
        self.Text.SetAspect(self.AspectRatio)
        self.Text.SetHeight(self.Height)
        self.Text.SetSlanting(self.Slanting)
        self.Text.SetFont(self.FontCombo.GetStringSelection())

        return self.Text

    def OnSelectposbtnButton(self, event):
        # select new position for text using kcs_ui.point2D_req function
        point = KcsPoint2D.Point2D()
        self.TransferDataFromWindow()
        self.Show(0)
        try:
            res, point = kcs_ui.point2D_req('Select new text position', point)
        except:
            CommonSample.ReportTribonError(kcs_ui)
            res = kcs_util.cancel()
        if res == kcs_util.ok():
            self.PosPoint.SetCoordinates(point.X, point.Y)
        self.Show(1)
