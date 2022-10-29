## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import math
import string
import KcsPoint2D

#
#      NAME:
#          KcsPrintOptions.py
#
#      PURPOSE:
#          The PrintOptions class holds information about printing options.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __PrinterName       string               name of selected printer
#                                                         if empty default printer will be used
#          __Orientation       integer              paper orientation code
#                                                         0 - Default
#                                                         1 - Portrait
#                                                         2 - Landscape
#          __PrintToFile       integer              print to file: 1 active, 0 inactive
#          __FileName          string               file name for print to file
#          __NoOfCopies        integer              number of copies, 0 means to use defautl number of copies
#          __EffPrintArea      integer              effective print area code
#                                                         0 - Currently selected
#                                                         1 - Drawing Form
#                                                         2 - Drawing Extensions
#                                                         3 - Current Window
#                                                         4 - Capture Area
#	
#          __ColourMode         integer             color corection mode
#					                                           0 - COLOUR_STD
#					                                           1 - COLOUR_BW
#					                                           2 - COLOUR_GRAYSCALE
#					                                           3 - COLOUR_PLUS
#
#          __AutoOrient        integer              auto orientation
#                                                         0 - use default value
#                                                         1 - auto orient
#                                                         2 - no auto orient
#                                                         3 - rotate 90
#                                                         4 - rotate 180
#                                                         5 - rotate 270
#
#          __ScaleToFit        integer              scale to fit
#                                                         0 - use default value
#                                                         1 - scale to fit
#                                                         2 - no scale to fit
#          __Scale             real                 scale
#                                                         0  - use default value
#                                                         >0 - new scale value
#
#          __CenterOnPage      integer              center on page
#                                                         0 - use default value
#                                                         1 - center on page
#                                                         2 - do not center on page
#
#          __Point1            KcsPoint2D.Point2D   Point defining the capture area.
#
#          __Point2            KcsPoint2D.Point2D   Point defining the capture area.
#
#          __PaperName         string               name of selected paper size
#                                                       if empty default paper size will be used
#
#          __PaperLength       integer              paper length in 0,1 mm
#                                                       overrides the length of the paper specified by the __PaperName
#
#          __PaperWidth        integer              paper width in 0,1 mm
#                                                       overrides the width of the paper specified by the __PaperName
#
#      METHODS:
#          SetPrinterName                           sets name of printer device
#          GetPrinterName                           gets name of printer device
#          SetOrientation                           sets printer page orientation
#          GetOrientation                           gets printer page orientation
#          SetPrintToFile                           sets or clears print to file option
#          IsPrintToFile                            returns 1 if print to file option is set, otherwise 0
#          SetNumberOfCopies                        sets number of copies
#          GetNumberOfCopies                        gets number of copies
#          SetEffectivePrintArea                    sets effective print area
#          GetEffectivePrintArea                    gets effective print area
#          SetAutoOrient                            sets auto orientation code
#          GetAutoOrient                            gets auto orientation code
#          SetScaleToFit                            sets scale to fit code
#          GetScaleToFit                            gets scale to fit code
#          SetScale                                 sets scale
#          GetScale                                 gets scale
#          SetCenterOnPage                          sets center on page code
#          GetCenterOnPage                          gets center on page code
#          SetFileName                              sets file name for print to file option
#          GetFileName                              gets file name for print to file option
#          GetPaperLength                           sets paper length
#          SetPaperLength                           gets paper length
#          GetPaperWidth                            sets paper width
#          SetPaperWidth                            gets paper width
#          GetPaperName                             sets paper name
#          SetPaperName                             gets paper name

ErrorMessages = { TypeError : 'not supported argument type, see documentation of PrintOptions class' }

class PrintOptions(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          name        string        printer device name

    def __init__(self, name=''):
        if not isinstance(name,str):
           raise TypeError, ErrorMessages[TypeError]
        self.__PrinterName    = name
        self.__Orientation    = 0
        self.__PrintToFile    = 0
        self.__FileName       = ''
        self.__NoOfCopies     = 0
        self.__EffPrintArea   = 0
        self.__AutoOrient     = 0
        self.__ScaleToFit     = 0
        self.__Scale          = 0.0
        self.__CenterOnPage   = 0
        self.__Point1   = KcsPoint2D.Point2D()
        self.__Point2   = KcsPoint2D.Point2D()
        self.__PaperName = ''
        self.__PaperLength = 0
        self.__PaperWidth = 0
        self.__ColourMode = 0
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
      tup = (
        'Print options:'
        '   Printer name: ' + str( self.__PrinterName ),
        '   Orientation : ' + str( self.__Orientation ),
        '   PrintToFile : ' + str( self.__PrintToFile ),
        '   FileName    : ' + str( self.__FileName ),
        '   NoOfCopies  : ' + str( self.__NoOfCopies ),
        '   EffPrintArea: ' + str( self.__EffPrintArea ),
        '   AutoOrient  : ' + str( self.__AutoOrient ),
        '   ScaleToFit  : ' + str( self.__ScaleToFit ),
        '   Scale       : ' + str( self.__Scale ),
        '   Colour correction mode: ' + str(self.__ColourMode),
        '   CenterOnPage: ' + str( self.__CenterOnPage ),
        '   Point1: ' + str(self.__Point1),
        '   Point2: ' + str(self.__Point2),
        '   PaperName: '+self.__PaperName,
        '   PaperLength: ' + str(self.__PaperLength),
        '   PaperWidth: ' + str(self.__PaperWidth))
      return string.join (tup, '\n')

#
#      METHOD:
#         SetPrinterName
#
#      PURPOSE:
#          Set printer device name
#
#      INPUT:
#          Parameters:
#          name        string       printer device name
#
#      RESULT:
#          The printer device name will be set
#

    def SetPrinterName(self, name):
        if not isinstance(name,str):
           raise TypeError, ErrorMessages[TypeError]
        self.__PrinterName = name

#
#      METHOD:
#         GetPrinterName
#
#      PURPOSE:
#          Get printer device name
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The printer device name will be returned
#

    def GetPrinterName(self):
        return self.__PrinterName

#
#      METHOD:
#         SetOrientation
#
#      PURPOSE:
#         Set page orientation
#
#      INPUT:
#          Parameters:
#          orientation
#
#      RESULT:
#          The printer page orientation will be set
#

    def SetOrientation(self, orientation):
        if not isinstance(orientation,int):
           raise TypeError, ErrorMessages[TypeError]
        if orientation >= 0 and orientation <= 2:
            self.__Orientation = orientation

#
#      METHOD:
#         GetOrientation
#
#      PURPOSE:
#          Gets page orientation
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          page orientation
#

    def GetOrientation(self):
        return self.__Orientation

#
#      METHOD:
#         SetPrintToFile
#
#      PURPOSE:
#         Set page orientation to portrait
#
#      INPUT:
#          Parameters:
#          activate      integer        if positive print to file option will be set otherwise cleared
#
#      RESULT:
#          The print to file option will be set
#

    def SetPrintToFile(self, activate):
        if activate > 0:
            self.__PrintToFile = 1
        else:
            self.__PrintToFile = 0

#
#      METHOD:
#         IsPrintToFile
#
#      PURPOSE:
#          Checks if print to file option is set
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          1 if print to file option is set, otherwise 0
#

    def IsPrintToFile(self):
        if self.__PrintToFile == 1:
            return 1
        else:
            return 0

#
#      METHOD:
#         SetNumberOfCopies
#
#      PURPOSE:
#         Set number of copies
#
#      INPUT:
#          Parameters:
#          copies      integer        number of copies
#
#      RESULT:
#          The number of copies
#

    def SetNumberOfCopies(self, copies):
        if not isinstance(copies,int):
           raise TypeError, ErrorMessages[TypeError]
        if copies >= 0:
            self.__NoOfCopies = copies

#
#      METHOD:
#         GetNumberOfCopies
#
#      PURPOSE:
#          Gets number of copies
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          number of copies
#

    def GetNumberOfCopies(self):
        return self.__NoOfCopies

#
#      METHOD:
#         SetEffectivePrintArea
#
#      PURPOSE:
#         Set effective print area
#
#      INPUT:
#          Parameters:
#          area         integer         effective print area code
#
#      RESULT:
#          None
#

    def SetEffectivePrintArea(self, area):
        if not isinstance(area,int):
           raise TypeError, ErrorMessages[TypeError]
        print area
        if area >= 0 and area <= 4:
            self.__EffPrintArea = area

#
#      METHOD:
#         GetEffectivePrintArea
#
#      PURPOSE:
#          Returns effective print area code
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          effective print area code
#

    def GetEffectivePrintArea(self):
        return self.__EffPrintArea

#
#      METHOD:
#         SetAutoOrient
#
#      PURPOSE:
#         Set auto orientation flag
#
#      INPUT:
#          Parameters:
#          autoorient       integer         auto orient code
#
#      RESULT:
#          None
#

    def SetAutoOrient(self, autoorient):
        if not isinstance(autoorient,int):
           raise TypeError, ErrorMessages[TypeError]
        if autoorient >= 0 and autoorient <= 5:
            self.__AutoOrient = autoorient

#
#      METHOD:
#         GetAutoOrient
#
#      PURPOSE:
#          Gets auto orientation code
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          auto orientation code
#

    def GetAutoOrient(self):
        return self.__AutoOrient

#
#      METHOD:
#         SetScaleToFit
#
#      PURPOSE:
#         Set scale to fit code
#
#      INPUT:
#          Parameters:
#          scaletofit       integer         set scale to fit code
#
#      RESULT:
#          None
#

    def SetScaleToFit(self, scaletofit):
        if not isinstance(scaletofit,int):
           raise TypeError, ErrorMessages[TypeError]
        if scaletofit >= 0 and scaletofit <= 2:
            self.__ScaleToFit = scaletofit

#
#      METHOD:
#         GetScaleToFit
#
#      PURPOSE:
#          Gets scale to fit code
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          scale to fit code
#

    def GetScaleToFit(self):
        return self.__ScaleToFit


#
#      METHOD:
#         SetScale
#
#      PURPOSE:
#         Set scale
#
#      INPUT:
#          Parameters:
#          scale       real         scale
#
#      RESULT:
#          None
#

    def SetScale(self, scale):
        if not isinstance(scale,int) and not type(scale)==type(1.1):
           raise TypeError, ErrorMessages[TypeError]
        if scale >= 0:
            self.__Scale = scale

#
#      METHOD:
#         GetScale
#
#      PURPOSE:
#          Gets scale
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          scale
#

    def GetScale(self):
        return self.__Scale


#
#      METHOD:
#         SetFileName
#
#      PURPOSE:
#         Set file name for print to file option
#
#      INPUT:
#          Parameters:
#          name       string         name of file for print to file
#
#      RESULT:
#          None
#

    def SetFileName(self, name):
        if not isinstance(name,str):
           raise TypeError, ErrorMessages[TypeError]
        self.__FileName = name

#
#      METHOD:
#         GetFileName
#
#      PURPOSE:
#          Gets file name for print to file option
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          file name
#

    def GetFileName(self):
        return self.__FileName
#
#      METHOD:
#         SetCenterOnPage
#
#      PURPOSE:
#         Set center on page code
#
#      INPUT:
#          Parameters:
#          centeronpage       integer     set center on page code
#
#      RESULT:
#          None
#

    def SetCenterOnPage(self, centeronpage):
        if not isinstance(centeronpage,int):
           raise TypeError, ErrorMessages[TypeError]
        if centeronpage >= 0 and centeronpage <= 2:
            self.__CenterOnPage = centeronpage

#
#      METHOD:
#         GetCenterOnPage
#
#      PURPOSE:
#          Gets center on page code
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          center on page code
#

    def GetCenterOnPage(self):
        return self.__CenterOnPage

#
#      METHOD:
#         GetFirstX
#
#      PURPOSE:
#          Gets smalest x-coordinate
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          smalest x-coordinate
#
    def GetFirstX(self):
        return min(self.__Point1.X, self.__Point2.X)

#
#      METHOD:
#         GetFirstY
#
#      PURPOSE:
#          Gets smalest y-coordinate
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          smalest y-coordinate
#
    def GetFirstY(self):
        return min(self.__Point1.Y, self.__Point2.Y)

#
#      METHOD:
#         GetSecondX
#
#      PURPOSE:
#          Gets largest x-coordinate
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          largest x-coordinate
#
    def GetSecondX(self):
        return max(self.__Point1.X, self.__Point2.X)

#
#      METHOD:
#         GetSecondY
#
#      PURPOSE:
#          Gets largest y-coordinate
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          largest y-coordinate
#
    def GetSecondY(self):
        return max(self.__Point1.Y, self.__Point2.Y)

#
#      METHOD:
#         SetPoint1
#
#      PURPOSE:
#         Set one of the two points defining the capture area
#
#      INPUT:
#          Parameters:
#          point       KcsPoint2D.Point2D
#
#      RESULT:
#          None
#
    def SetPoint1(self, point):
        if not isinstance(point,KcsPoint2D.Point2D):
            raise TypeError, ErrorMessages[TypeError]
        self.__Point1.X = point.X
        self.__Point1.Y = point.Y

#
#      METHOD:
#         SetPoint2
#
#      PURPOSE:
#         Set one of the two points defining the capture area
#
#      INPUT:
#          Parameters:
#          point       KcsPoint2D.Point2D
#
#      RESULT:
#          None
#
    def SetPoint2(self, point):
        if not isinstance(point,KcsPoint2D.Point2D):
            raise TypeError, ErrorMessages[TypeError]
        self.__Point2.X = point.X
        self.__Point2.Y = point.Y

#
#      METHOD:
#         GetPoint1
#
#      PURPOSE:
#         Get one of the two points defining the capture area
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          point       KcsPoint2D.Point2D
#
    def GetPoint1(self):
        return self.__Point1

#
#      METHOD:
#         GetPoint2
#
#      PURPOSE:
#         Get one of the two points defining the capture area
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          point       KcsPoint2D.Point2D
#
    def GetPoint2(self):
        return self.__Point2

#
#      METHOD:
#        SetPaperLength
#
#      PURPOSE:
#         Set paper length
#
#      INPUT:
#         Parameters: paper length in 0,1 mm
#
#      RESULT:
#         The paper length will be set
#
    def SetPaperLength(self,len):
        if not isinstance(len,int):
           raise TypeError, ErrorMessages[TypeError]
        if len<0:
            len=0
        self.__PaperLength=len

#      METHOD:
#         GetPaperLength
#
#      PURPOSE:
#         Get paper length in 0,1 mm
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          int       paper length
#
    def GetPaperLength(self):
        return self.__PaperLength
#
#      METHOD:
#         SetPaperWidth
#
#      PURPOSE:
#         Set paper width
#
#      INPUT:
#         Parameters: paper width in 0,1 mm
#
#      RESULT:
#         The paper width will be set
#
    def SetPaperWidth(self,width):
        if not isinstance(width,int):
           raise TypeError, ErrorMessages[TypeError]
        if width<0:
            witdh=0
        self.__PaperWidth=width

#      METHOD:
#         GetPaperWidth
#
#      PURPOSE:
#         Get paper width in 0,1 mm
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          int       paper width

    def GetPaperWidth(self):
        return self.__PaperWidth

#      METHOD:
#         GetPaperName
#
#      PURPOSE:
#         Get paper name
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          string       get paper name
    def GetPaperName(self):
        return self.__PaperName

#
#      METHOD:
#         SetPaperName
#
#      PURPOSE:
#         Set paper name
#
#      INPUT:
#         Parameters: paper name
#
#      RESULT:
#         The paper name will be set
#
    def SetPaperName(self,pname):
        if not isinstance(pname,str):
           raise TypeError, ErrorMessages[TypeError]
        self.__PaperName=pname

#
#      METHOD:
#         SetColourMode
#
#      PURPOSE:
#         Set colour correction mode
#
#      INPUT:
#         Parameters: colour correction mode
#
#      RESULT:
#         Property set
#
    def SetColourMode(self,color_mode):
        if not isinstance(color_mode,int):
           raise TypeError, ErrorMessages[TypeError]
        self.__ColourMode=color_mode

#
#      METHOD:
#         GetColourMode
#
#      PURPOSE:
#         Get colour correction mode
#
#      INPUT:
#         None
#
#      RESULT:
#         Current colour correction mode
#
    def GetColourMode(self):
        return self.__ColourMode
#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    PrinterName    = property (GetPrinterName , SetPrinterName)
    Orientation    = property (GetOrientation , SetOrientation)
    PrintToFile    = property (IsPrintToFile , SetPrintToFile)
    FileName       = property (GetFileName , SetFileName)
    NoOfCopies     = property (GetNumberOfCopies , SetNumberOfCopies)
    EffPrintArea   = property (GetEffectivePrintArea , SetEffectivePrintArea)
    AutoOrient     = property (GetAutoOrient, SetAutoOrient)
    ScaleToFit     = property (GetScaleToFit, SetScaleToFit)
    Scale          = property (GetScale , SetScale)
    CenterOnPage   = property (GetCenterOnPage, SetCenterOnPage)
    Point1         = property (GetPoint1,SetPoint1)
    Point2         = property (GetPoint2,SetPoint2)
    PaperLength    = property (GetPaperLength,SetPaperLength)
    PaperWidth     = property (GetPaperWidth,SetPaperWidth)
    PaperName      = property (GetPaperName,SetPaperName)
    ColourCorrectionMode = property (GetColourMode, SetColourMode)