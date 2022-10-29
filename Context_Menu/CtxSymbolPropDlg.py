## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
##-----------------------------------------------------------------------------
## Name:        CtxSymbolPropDlg.py
## Purpose:     Implementation of dialog box used to display symbol properties
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: CtxSymbolPropDlg.py $
## Licence:
##-----------------------------------------------------------------------------

import KcsSymbol
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
    return CtxSymbolPropDlg(parent)

[wxID_SYMBOLPROPDLGFONTIDEDIT, wxID_SYMBOLPROPDLGROTATIONEDIT, wxID_SYMBOLPROPDLGREFLECTIONCOMBO, wxID_SYMBOLPROPDLGSTATICTEXT1,\
 wxID_SYMBOLPROPDLGSELECTPOSBTN, wxID_SYMBOLPROPDLGCOLORCOMBO, wxID_SYMBOLPROPDLGSTATICTEXT2, wxID_SYMBOLPROPDLGSTATICTEXT5, \
 wxID_SYMBOLPROPDLGSTATICTEXT7, wxID_SYMBOLPROPDLGPOSITIONEDIT, wxID_SYMBOLPROPDLGSTATICTEXT6, wxID_SYMBOLPROPDLGHEIGHTEDIT, \
 wxID_SYMBOLPROPDLGSTATICTEXT8, wxID_SYMBOLPROPDLGSTATICTEXT3, wxID_SYMBOLPROPDLGSTATICTEXT4, wxID_SYMBOLPROPDLGSYMBOLIDEDIT, \
 wxID_SYMBOLPROPDLGLAYEREDIT, wxID_SYMBOLPROPDLG] = map(lambda _init_ctrls: wxNewId(), range(18))

class CtxSymbolPropDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(406, 200), id = wxID_SYMBOLPROPDLG, title = 'Symbol properties', parent = prnt, name = 'SymbolPropDlg', style = wxDOUBLE_BORDER | wxCAPTION | wxDIALOG_MODAL, pos = wxPoint(643, 371))
        self._init_utils()

        self.SymbolIdEdit = wxTextCtrl(size = wxSize(128, 21), value = '', pos = wxPoint(64, 8), parent = self, name = 'SymbolIdEdit', style = 0, id = wxID_SYMBOLPROPDLGSYMBOLIDEDIT)

        self.FontIdEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(288, 8), parent = self, name = 'FontIdEdit', style = 0, id = wxID_SYMBOLPROPDLGFONTIDEDIT)

        self.staticText1 = wxStaticText(label = 'Symbol ID:', id = wxID_SYMBOLPROPDLGSTATICTEXT1, parent = self, name = 'staticText1', size = wxSize(51, 13), style = 0, pos = wxPoint(8, 16))

        self.staticText2 = wxStaticText(label = 'Font ID:', id = wxID_SYMBOLPROPDLGSTATICTEXT2, parent = self, name = 'staticText2', size = wxSize(38, 13), style = 0, pos = wxPoint(240, 16))

        self.ColorCombo = wxChoice(size = wxSize(128, 21), id = wxID_SYMBOLPROPDLGCOLORCOMBO, choices = [], parent = self, name = 'ColourCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(64, 48))

        self.staticText3 = wxStaticText(label = 'Colour:', id = wxID_SYMBOLPROPDLGSTATICTEXT3, parent = self, name = 'staticText3', size = wxSize(33, 13), style = 0, pos = wxPoint(8, 56))

        self.LayerEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(288, 48), parent = self, name = 'LayerEdit', style = 0, id = wxID_SYMBOLPROPDLGLAYEREDIT)

        self.staticText5 = wxStaticText(label = 'Layer:', id = wxID_SYMBOLPROPDLGSTATICTEXT5, parent = self, name = 'staticText5', size = wxSize(29, 13), style = 0, pos = wxPoint(240, 56))

        self.PositionEdit = wxTextCtrl(size = wxSize(128, 21), value = '', pos = wxPoint(64, 112), parent = self, name = 'PositionEdit', style = 0, id = wxID_SYMBOLPROPDLGPOSITIONEDIT)

        self.staticText6 = wxStaticText(label = 'Position:', id = wxID_SYMBOLPROPDLGSTATICTEXT6, parent = self, name = 'staticText6', size = wxSize(40, 13), style = 0, pos = wxPoint(8, 120))

        self.SelectPosBtn = wxButton(label = '<', id = wxID_SYMBOLPROPDLGSELECTPOSBTN, parent = self, name = 'SelectPosBtn', size = wxSize(24, 24), style = 0, pos = wxPoint(192, 112))
        EVT_BUTTON(self.SelectPosBtn, wxID_SYMBOLPROPDLGSELECTPOSBTN, self.OnSelectposbtnButton)

        self.HeightEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(288, 80), parent = self, name = 'HeightEdit', style = 0, id = wxID_SYMBOLPROPDLGHEIGHTEDIT)

        self.staticText7 = wxStaticText(label = 'Height:', id = wxID_SYMBOLPROPDLGSTATICTEXT7, parent = self, name = 'staticText7', size = wxSize(34, 13), style = 0, pos = wxPoint(240, 88))

        self.RotationEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(288, 112), parent = self, name = 'RotationEdit', style = 0, id = wxID_SYMBOLPROPDLGROTATIONEDIT)

        self.staticText8 = wxStaticText(label = 'Rotation:', id = wxID_SYMBOLPROPDLGSTATICTEXT8, parent = self, name = 'staticText8', size = wxSize(43, 13), style = 0, pos = wxPoint(240, 120))

        self.ReflectionCombo = wxChoice(size = wxSize(128, 21), id = wxID_SYMBOLPROPDLGREFLECTIONCOMBO, choices = ['None', 'in U axis', 'in V axis'], parent = self, name = 'ReflectionCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(64, 80))

        self.staticText4 = wxStaticText(label = 'Reflection:', id = wxID_SYMBOLPROPDLGSTATICTEXT4, parent = self, name = 'staticText4', size = wxSize(51, 13), style = 0, pos = wxPoint(8, 88))

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.OkButton = wxButton(self, wxID_OK, " OK ", wxPoint(232, 145), wxDefaultSize).SetDefault()
        self.CancelButton = wxButton(self, wxID_CANCEL, "Cancel", wxPoint(312, 145), wxDefaultSize)

        for colour in KcsColour.ColourStrings:
            self.ColorCombo.Append(colour)

        self.Symbol = KcsSymbol.Symbol()

    def SetSymbol(self, symbol):

        self.Symbol = copy.deepcopy(symbol)

        # symbol id
        self.SymbolId = self.Symbol.GetSymbolId()
        self.SymbolIdEdit.SetValidator(NumericValidator(self, 'SymbolId'))

        # font id
        self.FontId = self.Symbol.GetFontId()
        self.FontIdEdit.SetValidator(NumericValidator(self, 'FontId'))

        # layer
        self.LayerId = self.Symbol.GetLayer().GetLayer()
        self.LayerEdit.SetValidator(NumericValidator(self, 'LayerId'))

        # position point
        self.PosPoint = self.Symbol.GetPosition()
        self.PositionEdit.SetValidator(validator = Point2DValidator(self.PosPoint))

        # color
        self.ColorCombo.SetStringSelection(self.Symbol.GetColour().Name())

        # rotation
        self.RotAngle = self.Symbol.GetRotation()
        self.RotationEdit.SetValidator(NumericValidator(self, 'RotAngle'))

        # height
        self.Height = self.Symbol.GetHeight()
        self.HeightEdit.SetValidator(NumericValidator(self, 'Height'))

        # reflection
        if self.Symbol.IsReflectedInUAxis():
            self.ReflectionCombo.SetStringSelection('in U axis')
        elif self.Symbol.IsReflectedInVAxis():
            self.ReflectionCombo.SetStringSelection('in V axis')
        else:
            self.ReflectionCombo.SetStringSelection('None')

    def GetSymbol(self):
        self.Symbol.SetSymbolId(self.SymbolId)
        self.Symbol.SetFontId(self.FontId)
        self.Symbol.SetLayer(KcsLayer.Layer(self.LayerId))
        self.Symbol.SetPosition(self.PosPoint)
        self.Symbol.SetColour(KcsColour.Colour(self.ColorCombo.GetStringSelection()))
        self.Symbol.SetRotation(self.RotAngle)
        self.Symbol.SetHeight(self.Height)

        reflection = self.ReflectionCombo.GetStringSelection()
        if reflection == 'in U axis':
            self.Symbol.SetReflectionInUAxis()
        elif reflection == 'in V axis':
            self.Symbol.SetReflectionInVAxis()
        else:
            self.Symbol.SetNoReflection()

        return self.Symbol

    def OnSelectposbtnButton(self, event):
        point = KcsPoint2D.Point2D()
        self.TransferDataFromWindow()
        self.Show(0)
        try:
            res, point = kcs_ui.point2D_req('Select new symbol position', point)
        except:
            CommonSample.ReportTribonError(kcs_ui)
            res = kcs_util.cancel()
        if res == kcs_util.ok():
            self.PosPoint.SetCoordinates(point.X, point.Y)
        self.Show(1)
