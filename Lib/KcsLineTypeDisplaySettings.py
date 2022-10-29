## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsLineTypeDisplaySettings.py
#
#      PURPOSE:
#          The class holds information about a line type display settings.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import string
import copy

class LineTypeDisplaySettings(object):
    ErrorMessages = { TypeError : 'not supported argument type, see documentation of LineTypeDisplaySettings class',
                      ValueError: 'not supported argument value, see documentation of LineTypeDisplaySettings class' }

    def __init__(self):
        # widths
        self.__ThinWidth                = 1 #0.125
        self.__WideWidth                = 0.0 #0.250
        self.__XWideWidth               = 0.0 #0.500
        self.__DashedAndSolidWidth      = 0.0
        self.__TrackWidth               = 0.0
        self.__System5Width             = 0.0
        self.__System6Width             = 0.0
        self.__System8Width             = 0.0
        self.__System9Width             = 0.0
        self.__System15Width            = 0.0
        self.__System16Width            = 0.0
        self.__System22Width            = 0.0
        self.__System23Width            = 0.0
        self.__System24Width            = 0.0
        self.__System25Width            = 0.0
        self.__System26Width            = 0.0
        self.__System27Width            = 0.0

        # scale factor
        self.__ScaleFactor              = None

        # patterns
        self.__Patterns                 = { 'Dash'              : [7.5, 2.5],
                                            'DashDot'           : [24.0, 5.0, 1.0, 5.0],
                                            'DashDoubleDot'     : [29.0, 4.0, 1.0, 1.0, 1.0, 4.0],
                                            'ShortDash'         : [3.75, 1.25],
                                            'Track'             : [10.0, 10.0],
                                            'System5'           : [5.0, 5.0],
                                            'System7'           : [20.0, 1.0, 1.0, 1.0]}
        # patterns length
        self.__PatternsLength           = { 'Dash'              : None,
                                            'DashDot'           : None,
                                            'DashDoubleDot'     : None,
                                            'ShortDash'         : None,
                                            'Track'             : None,
                                            'System5'           : None,
                                            'System6'           : None,
                                            'System7'           : None,
                                            'System8'           : None,
                                            'System9'           : None,
                                            'System22'          : None,
                                            'System23'          : None,
                                            'System24'          : None,
                                            'System25'          : None,
                                            'System26'          : None,
                                            'System27'          : None, }


    def SetPattern(self, name, pattern):
        if name not in self.__Patterns.keys():
            raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        if len(pattern) != len(self.__Patterns[name]):
            raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        for value in pattern:
            if type(value) != type(0.0) and type(value) != type(1):
                raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        self.__Patterns[name] = copy.deepcopy(pattern)

    def GetPattern(self, name):
        if name not in self.__Patterns.keys():
            raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        return copy.deepcopy(self.__Patterns[name])

    def SetPatternLength(self, name, length):
        if name not in self.__PatternsLength.keys():
            raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        if type(length) != type(0.0) and type(length) != type(1) and length != None:
                raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        self.__PatternsLength[name] = length

    def GetPatternLength(self, name):
        if name not in self.__PatternsLength.keys():
            raise ValueError, LineTypeDisplaySettings.ErrorMessages[ValueError]
        return self.__PatternsLength[name]

    def SetThinWidth(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__ThinWidth = width

    def GetThinWidth(self):
        return self.__ThinWidth

    def SetWideWidth(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__WideWidth = width

    def GetWideWidth(self):
        return self.__WideWidth

    def SetXWideWidth(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__XWideWidth = width

    def GetXWideWidth(self):
        return self.__XWideWidth

    def SetDashedAndSolidWidth(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__DashedAndSolidWidth = width

    def GetDashedAndSolidWidth(self):
        return self.__DashedAndSolidWidth

    def SetTrackWidth(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__TrackWidth = width

    def GetTrackWidth(self):
        return self.__TrackWidth

    def SetSystem5Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System5Width = width

    def GetSystem5Width(self):
        return self.__System5Width

    def SetSystem6Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System6Width = width

    def GetSystem6Width(self):
        return self.__System6Width

    def SetSystem8Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System8Width = width

    def GetSystem8Width(self):
        return self.__System8Width

    def SetSystem9Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System9Width = width

    def GetSystem9Width(self):
        return self.__System9Width

    def SetSystem15Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System15Width = width

    def GetSystem15Width(self):
        return self.__System15Width

    def SetSystem16Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System16Width = width

    def GetSystem16Width(self):
        return self.__System16Width

    def SetSystem22Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System22Width = width

    def GetSystem22Width(self):
        return self.__System22Width

    def SetSystem23Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System23Width = width

    def GetSystem23Width(self):
        return self.__System23Width

    def SetSystem24Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System24Width = width

    def GetSystem24Width(self):
        return self.__System24Width

    def SetSystem25Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System25Width = width

    def GetSystem25Width(self):
        return self.__System25Width

    def SetSystem26Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System26Width = width

    def GetSystem26Width(self):
        return self.__System26Width

    def SetSystem27Width(self, width):
        if type(width) != type(0.0) and type(width) != type(0):
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__System27Width = width

    def GetSystem27Width(self):
        return self.__System27Width

    def SetScaleFactor(self, factor):
        if type(factor) != type(0.0) and type(factor) != type(0) and factor != None:
            raise TypeError, LineTypeDisplaySettings.ErrorMessages[TypeError]
        else:
            self.__ScaleFactor = factor

    def GetScaleFactor(self):
        return self.__ScaleFactor

    def __repr__(self):
        'returns string representation of LineTypeDisplaySettings instance'

        if self.__ScaleFactor == None:
            scalefactor = 'Not defined'
        else:
            scalefactor = str(self.__ScaleFactor)

        tup = (
            'LineTypeDisplaySettings:',
            '   ThinWidth:\t' + str(self.__ThinWidth),
            '   WideWidth:\t ' + str(self.__WideWidth),
            '   XWideWidth:\t' + str(self.__XWideWidth),
            '   DashedAndSolidWidth:\t' + str(self.__DashedAndSolidWidth),
            '   TrackWidth:\t' + str(self.__TrackWidth),
            '   System5Width:\t' + str(self.__System5Width),
            '   System6Width:\t' + str(self.__System6Width),
            '   System8Width:\t' + str(self.__System8Width),
            '   System9Width:\t' + str(self.__System9Width),
            '   System15Width:\t' + str(self.__System15Width),
            '   System16Width:\t' + str(self.__System16Width),
            '   System22Width:\t' + str(self.__System22Width),
            '   System23Width:\t' + str(self.__System23Width),
            '   System24Width:\t' + str(self.__System24Width),
            '   System25Width:\t' + str(self.__System25Width),
            '   System26Width:\t' + str(self.__System26Width),
            '   System27Width:\t' + str(self.__System27Width),
            '   ScaleFactor:\t' + scalefactor,
            )
        return string.join(tup, '\n')

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

    ThinWidth = property (GetThinWidth, SetThinWidth, None, 'ThinWidth')
    WideWidth = property (GetWideWidth, SetWideWidth, None, 'WideWidth')
    XWideWidth = property (GetXWideWidth, SetXWideWidth, None, 'XWideWidth')
    DashedAndSolidWidth = property (GetDashedAndSolidWidth, SetDashedAndSolidWidth, None, 'DashedAndSolidWidth')
    TrackWidth = property (GetTrackWidth, SetTrackWidth, None, 'TrackWidth')
    System5Width = property (GetSystem5Width, SetSystem5Width, None, 'System5Width')
    System6Width = property (GetSystem6Width, SetSystem6Width, None, 'System6Width')
    System8Width = property (GetSystem8Width, SetSystem8Width, None, 'System8Width')
    System9Width = property (GetSystem9Width, SetSystem9Width, None, 'System9Width')
    System15Width = property (GetSystem15Width, SetSystem15Width, None, 'System15Width')
    System16Width = property (GetSystem16Width, SetSystem16Width, None, 'System16Width')
    System22Width = property (GetSystem22Width, SetSystem22Width, None, 'System22Width')
    System23Width = property (GetSystem23Width, SetSystem23Width, None, 'System23Width')
    System24Width = property (GetSystem24Width, SetSystem24Width, None, 'System24Width')
    System25Width = property (GetSystem25Width, SetSystem25Width, None, 'System25Width')
    System26Width = property (GetSystem26Width, SetSystem26Width, None, 'System26Width')
    System27Width = property (GetSystem27Width, SetSystem27Width, None, 'System27Width')
    ScaleFactor = property (GetScaleFactor, SetScaleFactor, None, 'ScaleFactor')

    def GetPatterns(self): return self.__Patterns
    Patterns = property (GetPatterns, None, None, 'Patterns')
    def GetPatternsLength(self): return self.__PatternsLength
    PatternsLength = property (GetPatternsLength, None, None, 'PatternsLength')

