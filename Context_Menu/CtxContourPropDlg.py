## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#Boa:Dialog:CtxContourPropDlg

import KcsContour2D
import KcsColour
import KcsLinetype
import KcsPoint2D
import KcsLayer
import KcsElementHandle
import CommonSample

from wxPython.wx import *
from wxPython.grid import *
from CtxValidators import *

import string
import copy
import sys
from math import *

import kcs_ui
import kcs_util
import kcs_draft

GridValidationMessage1 = 'Wrong value in selected cell!'
GridValidationMessage2 = 'Amplitude in selected cell is biger than half of the distance beetwen segment vertexes!'

def create(parent):
    return CtxContourPropDlg(parent)

[wxID_CONTOURPROPDLGDELETEVERTEXBTN, wxID_CONTOURPROPDLGCANCELBTN, wxID_CONTOURPROPDLGCOLORCOMBO, \
 wxID_CONTOURPROPDLGSTATICTEXT3, wxID_CONTOURPROPDLGSTATICTEXT2, wxID_CONTOURPROPDLGSTATICTEXT1, \
 wxID_CONTOURPROPDLGNEWVERTEXBTN, wxID_CONTOURPROPDLGOKBTN, wxID_CONTOURPROPDLGSELECTPOINTSBTN, \
 wxID_CONTOURPROPDLGLAYEREDIT, wxID_CONTOURPROPDLGLINETYPECOMBO, wxID_CONTOURPROPDLG] = map(lambda _init_ctrls: wxNewId(), range(12))

class CtxContourPropDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(396, 379), id = wxID_CONTOURPROPDLG, title = 'Contour properties', parent = prnt, name = 'ContourPropDlg', style = wxDEFAULT_DIALOG_STYLE, pos = wxPoint(414, 324))
        self._init_utils()
        EVT_CLOSE(self, self.OnContourpropdlgClose)

        self.NewVertexBtn = wxButton(label = 'New vertex', id = wxID_CONTOURPROPDLGNEWVERTEXBTN, parent = self, name = 'NewVertexBtn', size = wxSize(80, 24), style = 0, pos = wxPoint(192, 288))
        EVT_BUTTON(self.NewVertexBtn, wxID_CONTOURPROPDLGNEWVERTEXBTN, self.OnNewvertexbtnButton)

        self.DeleteVertexBtn = wxButton(label = 'Delete vertex', id = wxID_CONTOURPROPDLGDELETEVERTEXBTN, parent = self, name = 'DeleteVertexBtn', size = wxSize(80, 24), style = 0, pos = wxPoint(104, 288))
        EVT_BUTTON(self.DeleteVertexBtn, wxID_CONTOURPROPDLGDELETEVERTEXBTN, self.OnDeletevertexbtnButton)

        self.SelectPointsBtn = wxButton(label = 'Pick vertexes', id = wxID_CONTOURPROPDLGSELECTPOINTSBTN, parent = self, name = 'SelectPointsBtn', size = wxSize(80, 24), style = 0, pos = wxPoint(280, 288))
        EVT_BUTTON(self.SelectPointsBtn, wxID_CONTOURPROPDLGSELECTPOINTSBTN, self.OnSelectpointsbtnButton)

        self.ColorCombo = wxChoice(size = wxSize(125, 21), id = wxID_CONTOURPROPDLGCOLORCOMBO, choices = [], parent = self, name = 'ColorCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(8, 24))

        self.LinetypeCombo = wxChoice(size = wxSize(125, 21), id = wxID_CONTOURPROPDLGLINETYPECOMBO, choices = [], parent = self, name = 'LinetypeCombo', validator = wxDefaultValidator, style = 0, pos = wxPoint(144, 24))

        self.LayerEdit = wxTextCtrl(size = wxSize(100, 21), value = '', pos = wxPoint(280, 24), parent = self, name = 'LayerEdit', style = 0, id = wxID_CONTOURPROPDLGLAYEREDIT)

        self.CancelBtn = wxButton(label = 'Cancel', id = wxID_CONTOURPROPDLGCANCELBTN, parent = self, name = 'CancelBtn', size = wxSize(80, 24), style = 0, pos = wxPoint(280, 320))
        EVT_BUTTON(self.CancelBtn, wxID_CONTOURPROPDLGCANCELBTN, self.OnCancelbtnButton)

        self.staticText1 = wxStaticText(label = 'Colour', id = wxID_CONTOURPROPDLGSTATICTEXT1, parent = self, name = 'staticText1', size = wxSize(30, 13), style = 0, pos = wxPoint(8, 8))

        self.staticText2 = wxStaticText(label = 'Linetype', id = wxID_CONTOURPROPDLGSTATICTEXT2, parent = self, name = 'staticText2', size = wxSize(40, 13), style = 0, pos = wxPoint(144, 8))

        self.staticText3 = wxStaticText(label = 'Layer', id = wxID_CONTOURPROPDLGSTATICTEXT3, parent = self, name = 'staticText3', size = wxSize(26, 13), style = 0, pos = wxPoint(280, 8))

        self.OkBtn = wxButton(label = 'OK', id = wxID_CONTOURPROPDLGOKBTN, parent = self, name = 'OkBtn', size = wxSize(80, 24), style = 0, pos = wxPoint(192, 320))
        EVT_BUTTON(self.OkBtn, wxID_CONTOURPROPDLGOKBTN, self.OnOkbtnButton)

    def __init__(self, parent):
        self._init_ctrls(parent)
        try:
            self.OkBtn.SetDefault()

            wxID_SELECTPNTBTN = wxNewId()
            self.wxROW_LABEL_SIZE      = 30
            self.wxCOL_LABEL_SIZE      = 20

            self.SelectPntBtn = wxButton(size = wxSize(23, 23), pos = wxPoint(352, 280), label = '<', id = wxID_SELECTPNTBTN, parent = self)
            EVT_BUTTON(self.SelectPntBtn, wxID_SELECTPNTBTN, self.OnSelectPntButton)

            # create grid control
            self.GridCtrl = wxGrid(parent = self, id = -1, size = wxSize(350, 220), pos = wxPoint(10, 60))

            # grid messages
            EVT_GRID_SELECT_CELL(self.GridCtrl, self.OnSelectCell)

            # create columns
            self.GridCtrl.CreateGrid(0, 3)

            self.GridCtrl.SetColLabelValue(0, 'X coord')
            self.GridCtrl.SetColLabelValue(1, 'Y coord')
            self.GridCtrl.SetColLabelValue(2, 'amplitude')

            # set other properties of grid control
            self.GridCtrl.SetRowLabelSize(self.wxROW_LABEL_SIZE)
            self.GridCtrl.SetColLabelSize(self.wxCOL_LABEL_SIZE)
            self.GridCtrl.SetColLabelAlignment(wxALIGN_CENTER, wxALIGN_CENTER)
            self.GridCtrl.SetRowLabelAlignment(wxALIGN_CENTER, wxALIGN_CENTER)
            rowHeight = self.GridCtrl.GetDefaultRowSize()
            self.SelectPntBtn.SetSize(wxSize(rowHeight, rowHeight))
            self.GridCtrl.SetMargins(0, 0)

            # set columns width
            width = self.GridCtrl.GetGridWindow().GetSizeTuple()[0]
            width = int(width/3.0)
            self.GridCtrl.SetColSize(0, width)
            self.GridCtrl.SetColSize(1, width)
            self.GridCtrl.SetColSize(2, width)

            self.attr1 = wxGridCellAttr()
            self.attr1.SetTextColour(wxBLACK)
            self.attr1.SetBackgroundColour(wxColour(255, 255, 255))
            self.attr1.SetAlignment(wxALIGN_LEFT, wxALIGN_CENTER)

            self.attr2 = wxGridCellAttr()
            self.attr2.SetTextColour(wxBLACK)
            self.attr2.SetBackgroundColour(wxColour(220, 220, 220))
            self.attr2.SetAlignment(wxALIGN_LEFT, wxALIGN_CENTER)

            for colour in KcsColour.ColourStrings:
                self.ColorCombo.Append(colour)

            ltypes = KcsLinetype.GetLinetypes().values()
            ltypes.sort()
            for linetype in ltypes:
                self.LinetypeCombo.Append(linetype)

            self.HighlightPoints = []
        except:
            print sys.exc_info()[1]

    def ContourToGrid(self):
        row = 0
        self.GridCtrl.DeleteRows(0, self.GridCtrl.GetNumberRows())
        self.GridCtrl.AppendRows(len(self.Contour.Contour))
        for vertex in self.Contour.Contour:
            point = vertex[0]
            if len(vertex)==2:
                ampl = vertex[1]
            else:
                ampl = 0.0
            self.GridCtrl.SetCellValue(row, 0, str(round(point.X, 2)) )
            self.GridCtrl.SetCellValue(row, 1, str(round(point.Y, 2)) )
            self.GridCtrl.SetCellValue(row, 2, str(round(ampl, 2)) )
            row = row + 1
        self.SetGridCoolors()

    def GridToContour(self):
        contour = None
        for row in range(0, self.GridCtrl.GetNumberRows()):
            try:
                col = 0
                x     = float(self.GridCtrl.GetCellValue(row, col))
                col += 1
                y     = float(self.GridCtrl.GetCellValue(row, col))
                col += 1
                amp   = float(self.GridCtrl.GetCellValue(row, col))

                if amp != 0.0 and contour != None and len(contour.Contour)>=1:
                    px = contour.Contour[row-1][0].X
                    py = contour.Contour[row-1][0].Y
                    dist = sqrt(pow(x-px, 2)+pow(y-py, 2))
                    if fabs(amp) > dist/2.0:
                        self.GridCtrl.SelectBlock(row, col, row, col)
                        self.GridCtrl.SetGridCursor(row, col)
                        wxMessageBox(GridValidationMessage2, "Error")
                        return 0
            except Exception, e:
                print e
                self.GridCtrl.SelectBlock(row, col, row, col)
                self.GridCtrl.SetGridCursor(row, col)
                wxMessageBox(GridValidationMessage1, "Error")
                return 0

            if contour == None:
                contour = KcsContour2D.Contour2D(KcsPoint2D.Point2D(x, y))
            else:
                if amp == 0.0:
                    contour.AddLine(KcsPoint2D.Point2D(x, y))
                else:
                    contour.AddArc(KcsPoint2D.Point2D(x, y), amp)

        # copy table of segments
        self.Contour.Contour = contour.Contour

        return 1


    def UpdateButtons(self):
        if self.GridCtrl.GetNumberRows()>0:
            self.DeleteVertexBtn.Enable(1)
        else:
            self.DeleteVertexBtn.Enable(0)

    def SetGridCoolors(self):
        attribnum = 0
        for row in range(0, self.GridCtrl.GetNumberRows()):
            if attribnum:
                self.GridCtrl.SetRowAttr(row, self.attr1.Clone())
                attribnum = 0
            else:
                self.GridCtrl.SetRowAttr(row, self.attr2.Clone())
                attribnum = 1
            if row == 0:
                self.GridCtrl.SetReadOnly(0, 2)


    def SetContour(self, contour):
        self.Contour = copy.deepcopy(contour)
        self.ContourToGrid()

        # layer
        self.LayerId = self.Contour.GetLayer().GetLayer()
        self.LayerEdit.SetValidator(NumericValidator(self, 'LayerId'))

        # color
        self.ColorCombo.SetStringSelection(self.Contour.GetColour().Name())

        # linetype
        self.LinetypeCombo.SetStringSelection(KcsLinetype.GetAliasName(self.Contour.GetLineType().Name()))

        #highlight elements
        self.ElementHighlight(kcs_draft.ContextElement)
        self.HighlightCurrentVertex(self.GridCtrl.GetGridCursorRow())

    def GetContour(self):
        return self.Contour

    def OnNewvertexbtnButton(self, event):
        index = self.GridCtrl.GetNumberRows()
        self.GridCtrl.AppendRows()

        self.GridCtrl.SetCellValue(index, 0, '0.0')
        self.GridCtrl.SetCellValue(index, 1, '0.0')
        self.GridCtrl.SetCellValue(index, 2, '0.0')

        self.UpdateButtons()
        self.SetGridCoolors()

    def OnDeletevertexbtnButton(self, event):
        index = self.GridCtrl.GetGridCursorRow()
        if index>=0:
            self.GridCtrl.DeleteRows(index)
            self.UpdateButtons()
        self.SetGridCoolors()

    def OnSelectPntButton(self, event):
        selected = self.GridCtrl.GetGridCursorRow()
        if selected>=0:
            point = KcsPoint2D.Point2D()
            self.TransferDataFromWindow()
            self.Show(0)
            try:
                res, point = kcs_ui.point2D_req('Select new contour vertex', point)
            except:
                CommonSample.ReportTribonError(kcs_ui)
                res = kcs_util.cancel()
            if res == kcs_util.ok():
                self.GridCtrl.SetCellValue(selected, 0, str(round(point.X, 2)) )
                self.GridCtrl.SetCellValue(selected, 1, str(round(point.Y, 2)) )

            self.Show(1)


    def OnSelectCell(self, event):
        ################################################################
        ## change position of 'select point' button
        ################################################################
        # find selected row and get top Y of first cell in that row
        selected = event.GetRow()
        cellcoords = wxGridCellCoords(selected, 0)
        rowYPos = self.GridCtrl.BlockToDeviceRect(cellcoords, cellcoords).GetTop()

        # convert Y position of selected row to dialog coordinates
        rowYPos = self.GridCtrl.ClientToScreenXY(0, rowYPos)[1]
        rowYPos = self.ScreenToClientXY(0, rowYPos)[1] + self.wxCOL_LABEL_SIZE

        # get button x position
        gridXPos  = self.GridCtrl.GetPositionTuple()[0]
        gridWidth = self.GridCtrl.GetSizeTuple()[0]
        btnXPos = gridXPos + gridWidth

        # move button
        self.SelectPntBtn.MoveXY(btnXPos, rowYPos)

        ################################################################
        ## update buttons and highlight selected vertex
        ################################################################
        self.UpdateButtons()
        self.HighlightCurrentVertex(selected)

        # process default handler
        event.Skip()

    def OnSelectpointsbtnButton(self, event):
        points = []
        self.TransferDataFromWindow()

        self.Show(0)
        while 1:
            point = KcsPoint2D.Point2D()
            try:
                res, point = kcs_ui.point2D_req(('Select vertex %d') % (len(points)+1), point)
            except:
                CommonSample.ReportTribonError(kcs_ui)
                res = kcs_util.cancel()
                break
            if res == kcs_util.ok():
                points.append(point)
            elif res == kcs_util.operation_complete():
                self.Contour.Contour = []
                for point in points:
                    self.Contour.AddLine(point)
                self.ContourToGrid()
                break
            else:
                break

        self.Show(1)

    def OnOkbtnButton(self, event):
        if self.Validate() and self.GridToContour():
            self.TransferDataFromWindow()
            self.Contour.SetLayer(KcsLayer.Layer(self.LayerId))
            self.Contour.SetColour(KcsColour.Colour(self.ColorCombo.GetStringSelection()))
            self.Contour.SetLineType(KcsLinetype.Linetype(self.LinetypeCombo.GetStringSelection()))
            self.EndModal(wxID_OK)
            self.ElementHighlight()
        pass

    def ElementHighlight(self, *args):
        try:
            if len(args)==0:
                kcs_draft.highlight_off(0)
                kcs_ui.app_window_refresh()
            else:
                for item in args:
                    if isinstance(item, KcsElementHandle.ElementHandle):
                        kcs_draft.element_highlight(item)
                        kcs_ui.app_window_refresh()
        except Exception, e:
            print e

    def OnCancelbtnButton(self, event):
        self.ElementHighlight()
        self.EndModal(wxID_CANCEL)

    def HighlightCurrentVertex(self, index=None):
        for item in self.HighlightPoints:
            kcs_draft.highlight_off(item)
        self.HighlightPoints = []

        if index!=None and index >= 0:
            try:
                x = float(self.GridCtrl.GetCellValue(index, 0))
                y = float(self.GridCtrl.GetCellValue(index, 1))
                self.HighlightPoints.append(kcs_draft.point_highlight(KcsPoint2D.Point2D(x, y)))
                kcs_ui.app_window_refresh()
            except Exception, e:
                pass

    def OnContourpropdlgClose(self, event):
        self.ElementHighlight()
        event.Skip()

