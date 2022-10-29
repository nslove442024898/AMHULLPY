## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
from wxPython.wx import *
import string
import sys
import re

import KcsColour

ValidationMessage1 = 'Point 3D value invalid!'
ValidationMessage2 = 'Numeric value invalid!'
ValidationMessage3 = 'Value must be greater then %s'
ValidationMessage4 = 'Range value invalid!'
ValidationMessage5 = 'Value can not be empty'
ValidationMessage6 = 'Point 2D value invalid!'
ValidationMessage7 = 'Invalid color!'
ValidationMessage8 = 'Value can not be empty!'
ValidationMessage9 = 'Scale value not valid!'

RE_REAL        = '[-+]?\d+(\.\d*)?|[-+]?\d*(\.\d+)'
RE_POSREAL     = '\d+(\.\d*)?|\d*(\.\d+)'
RE_SCALE       = '(' + RE_POSREAL + '):(' + RE_POSREAL + ')'

class ScaleValidator(wxPyValidator):
    """ This validator is used to simplify data transfer
        between scale and window. It uses 1:X display format"""

    def __init__(self, pyVar, pyKey):
        """ Standard constructor.
            Arguments:
                pyVar      Real               - scale value as real
                pyKey      String             - attribute name
        """
        wxPyValidator.__init__(self)
        self.pyVar  = pyVar
        self.pyKey  = pyKey

    def Clone(self):
        """ Standard cloner. """
        return ScaleValidator(self.pyVar, self.pyKey)

    def Validate(self, win):
        """ Validate the contents of scale input control. """

        val = self.GetWindow().GetValue()

        if not re.match(RE_SCALE+'$', val):
            self.GetWindow().SetFocus()
            wxMessageBox(ValidationMessage9, "Error")
            return false

        return true

    def TransferToWindow(self):
        """ Transfer data from validator to window. """
        try:
            value = getattr(self.pyVar, self.pyKey)
            X = 1.0/float(value)
            self.GetWindow().SetValue(('1:%g') % (X,))
            return true
        except Exception, e:
            print e
            return false

    def TransferFromWindow(self):
        """ Transfer data from window to validator. """

        try:
            strval = self.GetWindow().GetValue()
            x, y = map(float, string.split(strval, ':'))
            setattr(self.pyVar, self.pyKey, x/y)
            return true
        except:
            return false

class ColorValidator(wxPyValidator):
    """ This validator is used to simplify data transfer
        between Color and window"""

    def __init__(self, color):
        """ Standard constructor.
            Arguments:
                color    - instance of Color class
        """
        wxPyValidator.__init__(self)
        self.color = color

    def Validate(self, parent):
        """ Validate the contents input control. """

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = self.GetWindow().GetValue()
        else:
            text = self.GetWindow().GetTitle()

        try:
            color = KcsColour.Colour(text)
        except:
            wxMessageBox(ValidationMessage7, "Error")
            return false

        return true

    def TransferToWindow(self):
        """ Transfer data from validator to window. """
        if isinstance( self.GetWindow(), wxTextCtrl) :
            self.GetWindow().SetValue(self.color.Name())
        else:
            self.GetWindow().SetTitle(self.color.Name())
        return true

    def TransferFromWindow(self):
        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = self.GetWindow().GetValue()
        else:
            text = self.GetWindow().GetTitle()

        self.color.SetName(text)

        return true

    def Clone(self):
        """ Standard cloner.
            Note that every validator must implement the Clone() method. """
        return ColorValidator(self.color)

class TextValidator(wxPyValidator):
    """ This validator is used to simplify data transfer
        between text and window"""

    def __init__(self, object, attrname, empty=1):
        """ Standard constructor.
            Arguments:
                object                - any python object
                attrname    string    - name of object attribut to read/write
                empty       integer   - can be empty - flag
        """
        wxPyValidator.__init__(self)
        self.Object = object
        self.strAttrName = attrname
        self.bEmpty  = empty

    def Validate(self, parent):
        """ Validate the contents input control. """

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = self.GetWindow().GetValue()
        elif isinstance(self.GetWindow(), wxChoicePtr):
            text = self.GetWindow().GetStringSelection()
        else:
            text = self.GetWindow().GetTitle()

        if self.bEmpty==0 and len(text)==0:
            wxMessageBox(ValidationMessage8, "Error")
            self.GetWindow.SetFocus()
            return false
        setattr(self.Object, self.strAttrName, text)

        return true

    def TransferToWindow(self):
        """ Transfer data from validator to window. """

        if isinstance( self.GetWindow(), wxTextCtrl) :
            self.GetWindow().SetValue(str(getattr(self.Object, self.strAttrName)))
        elif isinstance(self.GetWindow(), wxChoicePtr):
            self.GetWindow().SetStringSelection(str(getattr(self.Object, self.strAttrName)))
        else:
            self.GetWindow().SetTitle(str(getattr(self.Object, self.strAttrName)))
        return true

    def TransferFromWindow(self):
        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = self.GetWindow().GetValue()
        elif isinstance(self.GetWindow(), wxChoicePtr):
            text = self.GetWindow().GetStringSelection()
        else:
            text = self.GetWindow().GetTitle()

        setattr(self.Object, self.strAttrName, text)

        return true

    def Clone(self):
        """ Standard cloner.
            Note that every validator must implement the Clone() method. """
        return TextValidator(self.Object, self.strAttrName, self.bEmpty)


class Point3DValidator(wxPyValidator):
    """ This validator is used to ensure that the user has entered correct
        values for 3D point. """

    def __init__(self, point):
        """ Standard constructor.
            Arguments:
                point      Point3D      - validation data
        """
        self.point = point
        wxPyValidator.__init__(self)

    def Clone(self):
        """ Standard cloner.
            Note that every validator must implement the Clone() method. """
        return Point3DValidator(self.point)

    def Validate(self, win):
        """ Validate the contents of point 3D input control. """

        textCtrl = self.GetWindow()

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = textCtrl.GetValue()
        else:
            text = textCtrl.GetTitle()

        try:
            values = map(float, string.split(text, ','))
            if len(values) == 3:
                return true
        except:
            wxMessageBox(ValidationMessage1, "Error")
            return false

    def TransferToWindow(self):
        """ Transfer data from validator to window. """

        textCtrl = self.GetWindow()
        textCtrl.SetTitle(('%g, %g, %g') % (self.point.X, self.point.Y, self.point.Z))

        return true


    def TransferFromWindow(self):
        """ Transfer data from window to validator. """

        textCtrl = self.GetWindow()

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = textCtrl.GetValue()
        else:
            text = textCtrl.GetTitle()

        try:
            apply(self.point.SetCoordinates, map(float, string.split(text, ',')))
            return true
        except:
            return false


class Point2DValidator(wxPyValidator):
    """ This validator is used to ensure that the user has entered correct
        values for 2D point. """

    def __init__(self, point):
        """ Standard constructor.
            Arguments:
                point      Point2D      - validation data
        """
        wxPyValidator.__init__(self)
        self.point = point

    def Validate(self, parent):
        """ Validate the contents of point 3D input control. """
        values = string.split(self.GetWindow().GetValue(), ',')
        if len(values) == 2:
            try:
                self.point.SetCoordinates(float(values[0]), float(values[1]))
                return 1
            except:
                pass
        wxMessageBox(ValidationMessage6, 'Error')
        self.GetWindow().SetFocus()
        return 0

    def TransferToWindow(self):
        """ Transfer data from validator to window. """
        self.GetWindow().SetTitle('%.2f, %.2f' % (self.point.X, self.point.Y))
        return 1

    def TransferFromWindow(self):
        """ Transfer data from window to validator. """
        values = string.split(self.GetWindow().GetValue(), ',')
        try:
            self.point.SetCoordinates(float(values[0]), float(values[1]))
            return 1
        except:
            pass
        return 0

    def Clone(self):
        """ Standard cloner.
            Note that every validator must implement the Clone() method. """
        return Point2DValidator(self.point)


#----------------------------------------------------------------------
POSITIVE_ONLY = 1

class NumericValidator(wxPyValidator):
    """ This validator is used to ensure that the user has entered value"""

    def __init__(self, pyVar, pyKey, tester=None, flag=0):
        """ Standard constructor.
            Arguments:
                pyVar      Integer, Real      - validation data
                pyKey      String             - attribute name
                tester     Object             - value range tester
                flag       Integer            - Flags
        """
        wxPyValidator.__init__(self)
        self.pyVar  = pyVar
        self.pyKey  = pyKey
        self.tester = tester
        self.flag   = flag
        EVT_CHAR(self, self.OnChar)


    def Clone(self):
        """ Standard cloner. """

        return NumericValidator(self.pyVar, self.pyKey, self.tester, self.flag)


    def Validate(self, win):
        """ Validate the contents of numeric input control. """

        try:
            return self.TestValue( self.ConvertToValue() )
        except:
            textCtrl = self.GetWindow()
            textCtrl.SetFocus()
            wxMessageBox(ValidationMessage2, "Error")
            return false


    def TransferToWindow(self):
        """ Transfer data from validator to window. """

        try:
            textCtrl = self.GetWindow()
            textCtrl.SetTitle( str(getattr(self.pyVar, self.pyKey)) )
            return true
        except:
            return false


    def TransferFromWindow(self):
        """ Transfer data from window to validator. """

        try:
            setattr(self.pyVar, self.pyKey, self.ConvertToValue())
            return true
        except:
            return false


    def OnChar(self, event):
        """ Cheracter input filter """
        key = event.KeyCode()

        if key < WXK_SPACE or key == WXK_DELETE or key > 255:
            event.Skip()
            return

        if type( getattr(self.pyVar, self.pyKey) )  == type(0.0):
            if chr(key) in string.digits \
               or chr(key) in ('.eE')    \
               or (self.flag != POSITIVE_ONLY and chr(key) in ('+-')) :
                event.Skip()
                return

        elif type( getattr(self.pyVar, self.pyKey) )  == type(0):
            if chr(key) in string.digits \
                or (self.flag != POSITIVE_ONLY and chr(key) in ('+-')):
                event.Skip()
                return

        if not wxValidator_IsSilent():
            wxBell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return


    def ConvertToValue(self):
        """ Converts text into digit """

        textCtrl = self.GetWindow()

        if isinstance( self.GetWindow(), wxTextCtrl) :
            val = textCtrl.GetValue()
        else:
            val = textCtrl.GetTitle()


        if type(getattr(self.pyVar, self.pyKey) )  == type(0):
            return int( val )
        elif type( getattr(self.pyVar, self.pyKey) )  == type(0.0):
            return float( val )
        else:
            raise TypeError

    def TestValue(self, value):
        """ Value range validateion """
        if self.tester != None :
            return self.tester.Test(value)

        return true

#----------------------------------------------------------------------

class RangeValidator(wxPyValidator):
    """ This validator is used validate controls containing range value"""

    def __init__(self, pyRange):
        """ Standard constructor.
            Arguments:
                pyRange    List               - list containing range values
        """

        wxPyValidator.__init__(self)
        self.pyRange  = pyRange
        EVT_CHAR(self, self.OnChar)

    def Clone(self):
        """ Standard cloner. """

        return RangeValidator(self.pyRange)


    def Validate(self, win):
        """ Validate the contents of numeric input control. """

        textCtrl = self.GetWindow()

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = textCtrl.GetValue()
        else:
            text = textCtrl.GetTitle()

        try:
            values = map(float, string.split(text, ','))
            if len(values) in [1,2]:
                return true
        except:
            wxMessageBox(ValidationMessage4, "Error")
            return false

    def TransferToWindow(self):
        """ Transfer data from validator to window. """

        textCtrl = self.GetWindow()
        if len ( self.pyRange ) == 1:
            textCtrl.SetTitle(('%g') % (self.pyRange[0]))
        elif len ( self.pyRange ) == 2:
            textCtrl.SetTitle('%g, %g' % (self.pyRange[0], self.pyRange[1]))
        else:
            textCtrl.SetTitle('')

        return true


    def TransferFromWindow(self):
        """ Transfer data from window to validator. """

        textCtrl = self.GetWindow()

        if isinstance( self.GetWindow(), wxTextCtrl) :
            text = textCtrl.GetValue()
        else:
            text = textCtrl.GetTitle()

        try:
            self.pyRange = map(float, string.split(text, ','))
            return true
        except:
            return false


    def OnChar(self, event):
        """ Cheracter input filter """
        key = event.KeyCode()

        if key < WXK_SPACE or key == WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits or chr(key) in ('+-.eE'):
            event.Skip()
            return

        if not wxValidator_IsSilent():
            wxBell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return




#----------------------------------------------------------------------

class MinLimitTester:
    """ This tester checks if value is greater then limit"""

    def __init__(self, minValue):
        """ Standard constructor.
            Arguments:
                value           - minimal value
        """

        self.minValue = minValue


    def Test(self, value):
        """ Tests if value is greater then limit"""

        if value > self.minValue :
            return true

        wxMessageBox((ValidationMessage3) % (self.minValue), "Error")
        return false
