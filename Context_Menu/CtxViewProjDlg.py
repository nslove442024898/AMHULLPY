## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#Boa:Dialog:CtxViewProjectDlg

from wxPython.wx import *
from KcsVector3D import Vector3D
from KcsVector2D import Vector2D
import math
import re
import os

def GetPath(file):
    if __name__ == '__main__':
        return file
    else:
        return os.path.dirname(__file__)+'\\'+file

# -----------------------------------------------------------------------------
#        PBEvent class
# -----------------------------------------------------------------------------

class PBEvent(wxPyCommandEvent):


    def __init__(self, evtType, id):

        wxPyCommandEvent.__init__(self, evtType, id)

        self.Angle1 = None
        self.Angle2 = None



    def SetAngle1(self, val):

        self.Angle1 = val


    def SetAngle2(self, val):

        self.Angle2 = val



    def GetAngle1(self):

        return self.Angle1


    def GetAngle2(self):

        return self.Angle2


wxEVT_ANGLE_CHANGED = 5015

def EVT_PB_CHANGE_ANGLE(win, id, func):
    win.Connect(id, -1, wxEVT_ANGLE_CHANGED, func)

# -----------------------------------------------------------------------------
#        wxProjectionBitmap class
# -----------------------------------------------------------------------------

class wxProjectionBitmap(wxStaticBitmap):

    def __init__(self, **args):
        self.Pen1 = wxPen(wxBLUE, 3, wxSOLID)
        self.Pen2 = wxPen(wxLIGHT_GREY, 3, wxSOLID)

        self.LeftCenter = wxPoint(93, 91)
        self.LeftRadius = 40
        self.LeftRect   = wxRect(13, 13, 160, 160)

        self.RightCenter = wxPoint(207, 91)
        self.RightRadius = 40
        self.RightRect   = wxRect(206, 13, 280, 160)

        self.Angle1 = 0
        self.Angle2 = 0

        apply(wxStaticBitmap.__init__, [self], args)

        EVT_MOUSE_EVENTS(self, self.OnMouseEvents)
        EVT_ERASE_BACKGROUND(self, self.OnEraseBackground)
        EVT_PAINT(self, self.OnPaint)

    def PointInRect(self, point, rect):
        try:
            if rect.x < point.x < rect.x + rect.width and\
               rect.y < point.y < rect.y + rect.height:
                   return 1
        except Exception, e:
            print e
        return 0

    def GetAngle(self, point1, point2):
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(point2.x-point1.x, point2.y-point1.y, 0)
        angle = (v2.AngleToVector(v1) * 180.0) / math.pi
        if point1.y < point2.y:
            return int(round(360-angle, 0))
        else:
            return int(round(angle, 0))

    def OnMouseEvents(self, event):
        try:
            if event.LeftIsDown() and self.PointInRect(event.GetPosition(), self.LeftRect):
                evt = PBEvent(wxEVT_ANGLE_CHANGED, self.GetId())
                self.Angle1 = self.GetAngle(self.LeftCenter, event.GetPosition())
                evt.SetAngle1(self.Angle1)
                self.GetEventHandler().ProcessEvent(evt)
                event.Skip()

            if event.LeftIsDown() and self.PointInRect(event.GetPosition(), self.RightRect):
                evt = PBEvent(wxEVT_ANGLE_CHANGED, self.GetId())
                self.Angle2 = self.GetAngle(self.RightCenter, event.GetPosition())
                if self.Angle2 > 90:
                    self.Angle2 -= 360
                evt.SetAngle2(self.Angle2)
                self.GetEventHandler().ProcessEvent(evt)
                event.Skip()

        except Exception, e:
            print e

        event.Skip()

    def OnPaint(self, event):
        dc = wxPaintDC(self)
        try:
            dc.DrawBitmap(self.GetBitmap(), 0, 0, 0)
            dc.SetPen(self.Pen1)

            # draw left vector
            v = Vector2D(self.LeftRadius, 0)
            v.Rotate((self.Angle1 * math.pi) / 180.0)
            dc.DrawLines([self.LeftCenter, wxPoint(v.X+self.LeftCenter.x, (-v.Y)+self.LeftCenter.y)])

            # draw right vector
            v = Vector2D(self.RightRadius, 0)
            v.Rotate((self.Angle2 * math.pi) / 180.0)
            dc.DrawLines([self.RightCenter, wxPoint(v.X+self.RightCenter.x, (-v.Y)+self.RightCenter.y)])

        except Exception, e:
            print e

    def OnEraseBackground(self, event):
        pass


def create(parent):
    return CtxViewProjectDlg(parent)

[wxID_VIEWPROJECTDLGBITMAPBUTTON10, wxID_VIEWPROJECTDLGANGLE2EDIT, wxID_VIEWPROJECTDLGBITMAPBUTTON3, wxID_VIEWPROJECTDLGBITMAPBUTTON2, \
 wxID_VIEWPROJECTDLGBITMAPBUTTON5, wxID_VIEWPROJECTDLGBITMAPBUTTON4, wxID_VIEWPROJECTDLGBITMAPBUTTON7, wxID_VIEWPROJECTDLGBITMAPBUTTON6, \
 wxID_VIEWPROJECTDLGBITMAPBUTTON9, wxID_VIEWPROJECTDLGBITMAPBUTTON8, wxID_VIEWPROJECTDLGBITMAPBUTTON1, wxID_VIEWPROJECTDLGANGLE1EDIT, \
 wxID_VIEWPROJECTDLGSTATICTEXT1, wxID_VIEWPROJECTDLGSTATICTEXT2, wxID_VIEWPROJECTDLG] = map(lambda _init_ctrls: wxNewId(), range(15))

class CtxViewProjectDlg(wxDialog):
    def _init_utils(self):
        pass

    def _init_ctrls(self, prnt):
        wxDialog.__init__(self, size = wxSize(593, 269), id = wxID_VIEWPROJECTDLG, title = 'Select view projection', parent = prnt, name = 'ViewProjectDlg', style = wxDEFAULT_DIALOG_STYLE, pos = wxPoint(380, 293))
        self._init_utils()

        self.Angle1Edit = wxTextCtrl(size = wxSize(72, 21), value = '', pos = wxPoint(96, 208), parent = self, name = 'Angle1Edit', style = 0, id = wxID_VIEWPROJECTDLGANGLE1EDIT)
        EVT_TEXT(self.Angle1Edit, wxID_VIEWPROJECTDLGANGLE1EDIT, self.OnAngle1EditText)
        EVT_KILL_FOCUS(self.Angle1Edit, self.OnAngle1EditKillFocus)

        self.Angle2Edit = wxTextCtrl(size = wxSize(72, 21), value = '', pos = wxPoint(240, 208), parent = self, name = 'Angle2Edit', style = 0, id = wxID_VIEWPROJECTDLGANGLE2EDIT)
        EVT_TEXT(self.Angle2Edit, wxID_VIEWPROJECTDLGANGLE2EDIT, self.OnAngle2EditText)
        EVT_KILL_FOCUS(self.Angle2Edit, self.OnAngle2EditKillFocus)

        self.bitmapButton1 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON1, parent = self, name = 'bitmapButton1', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(360, 8))
        EVT_BUTTON(self.bitmapButton1, wxID_VIEWPROJECTDLGBITMAPBUTTON1, self.OnBitmapbutton1Button)

        self.bitmapButton2 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON2, validator = wxDefaultValidator, parent = self, name = 'bitmapButton2', size = wxSize(102, 24), style = wxBU_AUTODRAW, pos = wxPoint(472, 8))
        EVT_BUTTON(self.bitmapButton2, wxID_VIEWPROJECTDLGBITMAPBUTTON2, self.OnBitmapbutton2Button)

        self.bitmapButton3 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON3, validator = wxDefaultValidator, parent = self, name = 'bitmapButton3', size = wxSize(102, 24), style = wxBU_AUTODRAW, pos = wxPoint(360, 40))
        EVT_BUTTON(self.bitmapButton3, wxID_VIEWPROJECTDLGBITMAPBUTTON3, self.OnBitmapbutton3Button)

        self.bitmapButton4 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON4, validator = wxDefaultValidator, parent = self, name = 'bitmapButton4', size = wxSize(102, 24), style = wxBU_AUTODRAW, pos = wxPoint(472, 40))
        EVT_BUTTON(self.bitmapButton4, wxID_VIEWPROJECTDLGBITMAPBUTTON4, self.OnBitmapbutton4Button)

        self.bitmapButton6 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON6, parent = self, name = 'bitmapButton6', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(472, 72))
        EVT_BUTTON(self.bitmapButton6, wxID_VIEWPROJECTDLGBITMAPBUTTON6, self.OnBitmapbutton6Button)

        self.bitmapButton5 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON5, parent = self, name = 'bitmapButton5', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(360, 72))
        EVT_BUTTON(self.bitmapButton5, wxID_VIEWPROJECTDLGBITMAPBUTTON5, self.OnBitmapbutton5Button)

        self.bitmapButton7 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON7, parent = self, name = 'bitmapButton7', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(472, 104))
        EVT_BUTTON(self.bitmapButton7, wxID_VIEWPROJECTDLGBITMAPBUTTON7, self.OnBitmapbutton7Button)

        self.bitmapButton8 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON8, parent = self, name = 'bitmapButton8', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(360, 104))
        EVT_BUTTON(self.bitmapButton8, wxID_VIEWPROJECTDLGBITMAPBUTTON8, self.OnBitmapbutton8Button)

        self.bitmapButton9 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON9, parent = self, name = 'bitmapButton9', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(360, 136))
        EVT_BUTTON(self.bitmapButton9, wxID_VIEWPROJECTDLGBITMAPBUTTON9, self.OnBitmapbutton9Button)

        self.bitmapButton10 = wxBitmapButton(bitmap = wxNullBitmap, id = wxID_VIEWPROJECTDLGBITMAPBUTTON10, parent = self, name = 'bitmapButton10', size = wxSize(102, 24), validator = wxDefaultValidator, style = wxBU_AUTODRAW, pos = wxPoint(472, 136))
        EVT_BUTTON(self.bitmapButton10, wxID_VIEWPROJECTDLGBITMAPBUTTON10, self.OnBitmapbutton10Button)

        self.staticText1 = wxStaticText(label = 'From:   X axis:', id = wxID_VIEWPROJECTDLGSTATICTEXT1, parent = self, name = 'staticText1', size = wxSize(80, 13), style = 0, pos = wxPoint(8, 216))

        self.staticText2 = wxStaticText(label = 'XY plane:', id = wxID_VIEWPROJECTDLGSTATICTEXT2, parent = self, name = 'staticText2', size = wxSize(52, 13), style = 0, pos = wxPoint(184, 216))

    def __init__(self, parent):
        self._init_ctrls(parent)

        wxID_VIEWPROJECTDLGPROJECTIONBMP = 100
        self.ProjectionBmp = wxProjectionBitmap(bitmap = wxBitmap(GetPath('ctxprojection.bmp'), wxBITMAP_TYPE_BMP), id = wxID_VIEWPROJECTDLGPROJECTIONBMP, parent = self, name = 'ProjectionBmp', size = wxSize(341, 184), style = 0, pos = wxPoint(8, 8))
        EVT_PB_CHANGE_ANGLE(self, self.ProjectionBmp.GetId(), self.OnChangeAngle)

        self.OkButton = wxButton(self, wxID_OK,     " OK ", wxPoint(420, 210), wxDefaultSize).SetDefault()
        self.CancelButton = wxButton(self, wxID_CANCEL,     "Cancel", wxPoint(500, 210), wxDefaultSize)

        self.ButtonsBmp = wxBitmap(GetPath('CtxButtons.bmp'), wxBITMAP_TYPE_BMP)
        width = self.ButtonsBmp.GetWidth()
        self.bitmapButton1.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,    0, width, 20)))
        self.bitmapButton2.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,   20, width, 20)))
        self.bitmapButton3.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,   40, width, 20)))
        self.bitmapButton4.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,   60, width, 20)))
        self.bitmapButton5.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,   80, width, 20)))
        self.bitmapButton6.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,  100, width, 20)))
        self.bitmapButton7.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,  120, width, 20)))
        self.bitmapButton8.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,  140, width, 20)))
        self.bitmapButton9.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0,  160, width, 20)))
        self.bitmapButton10.SetBitmapLabel(self.ButtonsBmp.GetSubBitmap(wxRect(0, 180, width, 20)))

        self.Angle1Edit.SetValue(str(self.ProjectionBmp.Angle1))
        self.Angle2Edit.SetValue(str(self.ProjectionBmp.Angle2))

    def OnChangeAngle(self, event):
        if event.GetAngle1() != None:
            self.Angle1Edit.SetValue(str(event.GetAngle1()))
        if event.GetAngle2() != None:
            self.Angle2Edit.SetValue(str(event.GetAngle2()))
        self.ProjectionBmp.Refresh()

    def OnAngle1EditText(self, event):
        event.Skip()
        try:
            self.ProjectionBmp.Angle1 = int(self.Angle1Edit.GetValue()) % 360
            if self.ProjectionBmp.Angle1 < 0:
                self.ProjectionBmp.Angle1 += 360
        except:
            self.ProjectionBmp.Angle1 = 0
        self.ProjectionBmp.Refresh()

    def OnAngle2EditText(self, event):
        event.Skip()
        try:
            self.ProjectionBmp.Angle2 = int(self.Angle2Edit.GetValue()) % 360
            if self.ProjectionBmp.Angle2 > 90:
                self.ProjectionBmp.Angle2 -= 360
        except:
            self.ProjectionBmp.Angle2 = 0
        self.ProjectionBmp.Refresh()

    def OnAngle1EditKillFocus(self, event):
        self.Angle1Edit.SetValue(str(self.ProjectionBmp.Angle1))
        event.Skip()

    def OnAngle2EditKillFocus(self, event):
        self.Angle2Edit.SetValue(str(self.ProjectionBmp.Angle2))
        event.Skip()

    def SetAngles(self, angle1, angle2):
        self.ProjectionBmp.Angle1 = angle1
        self.ProjectionBmp.Angle2 = angle2
        self.Angle1Edit.SetValue(str(self.ProjectionBmp.Angle1))
        self.Angle2Edit.SetValue(str(self.ProjectionBmp.Angle2))
        self.ProjectionBmp.Refresh()

    def GetAngles(self):
        return (self.ProjectionBmp.Angle1, self.ProjectionBmp.Angle2)

    def OnBitmapbutton1Button(self, event):
        self.SetAngles(270, 90)

    def OnBitmapbutton2Button(self, event):
        self.SetAngles(90, 90)

    def OnBitmapbutton3Button(self, event):
        self.SetAngles(270, 0)

    def OnBitmapbutton4Button(self, event):
        self.SetAngles(90, 0)

    def OnBitmapbutton5Button(self, event):
        self.SetAngles(180, 0)

    def OnBitmapbutton6Button(self, event):
        self.SetAngles(0, 0)

    def OnBitmapbutton7Button(self, event):
        self.SetAngles(225, 45)

    def OnBitmapbutton8Button(self, event):
        self.SetAngles(315, 45)

    def OnBitmapbutton9Button(self, event):
        self.SetAngles(45, 45)

    def OnBitmapbutton10Button(self, event):
        self.SetAngles(135, 45)

if __name__ == '__main__':
    try:
        app = wxPySimpleApp()

        dlg = CtxViewProjectDlg(NULL)

        if dlg.ShowModal() == wxID_OK:
            pass

    except Exception, e:
        print e

