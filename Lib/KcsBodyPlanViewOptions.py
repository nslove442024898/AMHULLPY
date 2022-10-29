## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsBodyPlanViewOptions.py
#
#      PURPOSE:
#
#          To hold options for Body Plan view objects.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import KcsLinetype
import string
import types
import KcsColour
import KcsPoint3D

class BodyPlanViewOptions(object):

   SIDE_PORT               =  0
   SIDE_STARBOARD          =  1
   PLANE_BY_SEAMS          =  1
   PLANE_BY_X              = -1
   PLANE_BY_Y              = -2
   PLANE_BY_Z              = -3
   LOOKING_FOR             =  4
   LOOKING_AFT             =  3
   LOOKING_PS              =  1
   LOOKING_SB              =  2
   LOOKING_TOP             =  5
   LOOKING_BOT             =  6
   IMAGE_THICK             =  2
   IMAGE_MOULD             =  1
   IMAGE_FULL              =  0
   COLORS                  =  ['Green', 'Black', 'Cyan', 'White', 'Blue', 'Magenta', 'Red', 'Yellow']

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of BodyPlanViewOptions class',
                      ValueError: 'not supported value, see documentation of BodyPlanViewOptions class' }

#-----------------------------------------------------------------------

   def __init__(self):
      'inits BodyPlanViewOptions'
      self.__BodyPlanName                    = 'TB_BP_VIEW'
      self.__bAutoSeams                      = 0
      self.__bAutoLongTrace                  = 0
      self.__bAutoLongSection                = 0
      self.__SurfacesFilter                  = []
      self.__SurfacesExclude                 = 0
      self.__Scale                           = 50
      self.__AftLimits                      = KcsPoint3D.Point3D(-500000,0,-500000)
      self.__FwdLimits                      = KcsPoint3D.Point3D(500000,500000,500000)
      self.__bLooking                        = 0
      self.__LongSectionImage                = self.IMAGE_FULL
      self.__LongSectionFrame                = 0
      self.__DrawFrame                       = 5
      self.__SeamColour                      = KcsColour.Colour('White')
      self.__LongColour                      = KcsColour.Colour('Red')
      self.__FrameColour                     = KcsColour.Colour('White')
      self.__GridSpacing                     = 0
      self.__PanelFilter                     = []
      self.__SeamsFilter                     = []
      self.__SeamsExclude                    = 0
      self.__TraceFilter                     = []
      self.__TraceExclude                    = 0
      self.__SectionFilter                   = []
      self.__SectionExclude                  = 0
      self.__SelectCurves                    = {}
#-----------------------------------------------------------------------

   def SetBodyPlanViewName(self, name):
      'sets view name'

      if type(name) != type(''):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__BodyPlanName = string.upper(name)

#-----------------------------------------------------------------------

   def GetBodyPlanViewName(self):
      'gets view name'
      return self.__BodyPlanName

#-----------------------------------------------------------------------
   def SetSurfaceExclude(self):
      'specify exclude/include surfaces'
      self.__SurfacesExclude = 1;
#-----------------------------------------------------------------------
   def SetSurfaces(self, filter):
      'allows user to specify surfaces filter'
      if type(filter) != type([]):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      for item in filter:
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SurfacesFilter.append(item)
#-----------------------------------------------------------------------

   def GetSurfaces(self):
      'gets Surfaces'
      return [self.__SurfacesExclude, self.__SurfacesFilter]

#-----------------------------------------------------------------------
   def SetScale(self, value):
      'allows user to specify the scale'
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      else:
         self.__Scale = int(value)
#-----------------------------------------------------------------------
   def GetScale(self):
      'gets scale'
      return [self.__Scale]

#-----------------------------------------------------------------------

   def SetGrid(self, value):
      'allows user to specify the grid space'
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      else:
         self.__GridSpacing = int(value)

#-----------------------------------------------------------------------

   def GetGrid(self):
      'gets grid'
      return [self.__GridSpacing]

#-----------------------------------------------------------------------

   def SetAftLimits(self, Coord):
      'allows user to specify plane by X, Y or Z coordinate'
      if not isinstance(Coord, KcsPoint3D.Point3D):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__AftLimits = Coord
#-----------------------------------------------------------------------

   def GetAftLimits(self):
      'gets AftLimits'
      return [self.__AftLimits]

#-----------------------------------------------------------------------

   def SetFwdLimits(self, Coord):
      'allows user to specify plane by X, Y or Z coordinate'
      if not isinstance(Coord, KcsPoint3D.Point3D):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__FwdLimits = Coord
#-----------------------------------------------------------------------

   def GetFwdLimits(self):
      'gets AftLimits'
      return [self.__FwdLimits]

#-----------------------------------------------------------------------
   def SetLooking(self, looking):
      'specify looking way'

      if type(looking) != type(self.LOOKING_FOR):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]

      if looking != self.LOOKING_FOR and looking != self.LOOKING_AFT \
         and looking != self.LOOKING_PS and looking != self.LOOKING_SB \
         and looking != self.LOOKING_TOP and looking != self.LOOKING_BOT:
         raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]

      self.__bLooking  = int(looking)
#-----------------------------------------------------------------------

   def GetLooking(self):
      'gets Looking'
      return [self.__bLooking]

#-----------------------------------------------------------------------
   def SetSection(self, image, frame):
      'specify Section image and frame'

      if type(frame) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]

      if type(image) != type(self.IMAGE_FULL):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]

      if image != self.IMAGE_FULL and image != self.IMAGE_MOULD \
         and image != self.IMAGE_THICK:
         raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]

      self.__LongSectionImage  = int(image)
      self.__LongSectionFrame  = int(frame)
#-----------------------------------------------------------------------

   def GetSection(self):
      'gets Section'
      return [self.__LongSectionImage, self.__LongSectionFrame]

#----------------------------
   def SetColours(self, long, seam, frame):
      'specify colours of longs, seams and frames'
      if not isinstance(long, KcsColour.Colour):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      if not isinstance(seam, KcsColour.Colour):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      if not isinstance(frame, KcsColour.Colour):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      bFoundLong = 0;
      bFoundSeam = 0;
      bFoundFrame = 0;
      for item in self.COLORS:
         if item == long.ColourString:
            bFoundLong = 1;
         if item == seam.ColourString:
            bFoundSeam = 1;
         if item == frame.ColourString:
            bFoundFrame = 1;
      if bFoundLong != 1 or bFoundSeam != 1 or bFoundFrame != 1:
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[ValueError]

      self.__SeamColour  = seam
      self.__LongColour  = long
      self.__FrameColour = frame
#-----------------------------------------------------------------------

   def GetColours(self):
      'gets Colours'
      return [self.__SeamColour, self.__LongColour, self.__FrameColour]

#-----------------------------------------------------------------------

   def SetAutoSeams(self):
      'specify auto include seams'
      self.__bAutoSeams = 1;

#-----------------------------------------------------------------------
   def SetAutoLongTrace(self):
      'specify auto traces'
      self.__bAutoLongTrace = 1;
#-----------------------------------------------------------------------
   def SetAutoLongSection(self):
      'specify auto sections'
      self.__bAutoLongSection = 1;
#-----------------------------------------------------------------------
   def SetPanels(self, filter):
      'allows user to specify panels filter'
      if type(filter) != type([]):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      for item in filter:
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         else:
            self.__PanelFilter.append(item)
#-----------------------------------------------------------------------
   def SetSeams(self, filter):
      'allows user to specify seams filter'
      if type(filter) != type([]):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      for item in filter:
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SeamsFilter.append(item)
#-----------------------------------------------------------------------
   def GetSeams(self):
      'Get Seams Filter'
      return [self.__SeamsExclude, self.__SeamsFilter]
#-----------------------------------------------------------------------
   def SetSeamsExclude(self):
      'specify exclude/include seams'
      self.__SeamsExclude = 1;
#-----------------------------------------------------------------------
   def GetLongTrace(self):
      'Get Longitudals Trace'
      return [self.__TraceExclude, self.__TraceFilter]
#-----------------------------------------------------------------------
   def SetLongTrace(self, filter):
      'allows user to specify Long Trace filter'
      if type(filter) != type([]):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      for item in filter:
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         else:
            self.__TraceFilter.append(item)
#-----------------------------------------------------------------------
   def SetTraceExclude(self):
      'specify exclude/include Long Trace'
      self.__TraceExclude = 1;
#-----------------------------------------------------------------------
   def GetLongSection(self):
      'Get Longitudals Section'
      return [self.__SectionExclude, self.__SectionFilter]
#-----------------------------------------------------------------------
   def SetLongSection(self, filter):
      'allows user to specify Long Section filter'
      if type(filter) != type([]):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      for item in filter:
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SectionFilter.append(item)
#-----------------------------------------------------------------------
   def SetSectionExclude(self):
      'specify exclude/include section'
      self.__SectionExclude = 1;
#-----------------------------------------------------------------------
   def SetLineTypes(self, dict):
      'Set Curves and Types'
      if type(dict) != type({'':''}):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      lines = KcsLinetype.GetLinetypes()
      for item in dict.values():
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
         if not item in lines:
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
      for item in dict.keys():
         if type(item) != type(''):
            raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
      self.__SelectCurves = dict
#-----------------------------------------------------------------------

   def GetCurves(self):
      'Get Selected Curves and Line Types'
      return [self.__SelectCurves]

#-----------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
   def __repr__(self):
      'returns string representation of BodyPlanViewOptions instance'
      if self.__bLooking == 0:         lookingstr = '   Looking: Not set'
      elif self.__bLooking == self.LOOKING_PS:        lookingstr = '   Looking: LOOKING_PS'
      elif self.__bLooking == self.LOOKING_SB:        lookingstr = '   Looking: LOOKING_SB'
      elif self.__bLooking == self.LOOKING_AFT:       lookingstr = '   Looking: LOOKING_AFT'
      elif self.__bLooking == self.LOOKING_FOR:       lookingstr = '   Looking: LOOKING_FOR'
      elif self.__bLooking == self.LOOKING_TOP:       lookingstr = '   Looking: LOOKING_TOP'
      elif self.__bLooking == self.LOOKING_BOT:       lookingstr = '   Looking: LOOKING_BOT'

      if self.__LongSectionImage == self.IMAGE_FULL:    imagestr = '   Longitudal Section Image: IMAGE_FULL'
      elif self.__LongSectionImage == self.IMAGE_MOULD:  imagestr = '   Longitudal Section Image: IMAGE_MOULD'
      elif self.__LongSectionImage == self.IMAGE_THICK:  imagestr = '   Longitudal Section Image: IMAGE_THICK'

      curvedict = '   Select Curves: '
      if len(self.__SelectCurves)>0:
         for name in self.__SelectCurves.keys():
            curvedict += str(name) + ' : ' + str(self.__SelectCurves[name]) + ', '
         curvedict = curvedict[:-2]

      tup = (
         'BodyPlanViewOptions:',
         '   Body Plan Name: ' + self.__BodyPlanName,
         '   Scale: ' + str(self.__Scale),
         '   Aft Limits: %f, %f, %f'  % (self.__AftLimits.X, self.__AftLimits.Y, self.__AftLimits.Z),
         '   Fore Limits: %f, %f, %f' % (self.__FwdLimits.X, self.__FwdLimits.Y, self.__FwdLimits.Z),
         lookingstr,
         '   Grid Spacing: ' + str(self.__GridSpacing),
         curvedict,
         '   Draw Frame: ' + str(self.__DrawFrame),
         imagestr,
         '   Longitudal Section Frame: ' + str(self.__LongSectionFrame),
         '   Seam Colour: ' + str(self.__SeamColour.ColourString),
         '   Longitudal Colour: ' + str(self.__LongColour.ColourString),
         '   Frame Colour: ' + str(self.__FrameColour.ColourString),
         '   Auto Include Seams: ' + str(self.__bAutoSeams),
         '   Auto Longitudal Trace: ' + str(self.__bAutoLongTrace),
         '   Auto Longitudal Section: ' + str(self.__bAutoLongSection),
         '   Panel Filter: ' + str(self.__PanelFilter),
         '   Seams Filter: ' + str(self.__SeamsFilter),
         '   Longitudal Trace Filter: ' + str(self.__TraceFilter),
         '   Longitudal Section Filter: ' + str(self.__SectionFilter),
         '   Surfaces Filter: ' + str(self.__SurfacesFilter),
         '   Seams Exclude: ' + str(self.__SeamsExclude),
         '   Trace Exclude: ' +str(self.__TraceExclude),
         '   Section Exclude: ' + str(self.__SectionExclude),
         '   Surfaces Exclude: ' + str(self.__SurfacesExclude),
         )
      return string.join(tup, '\n')

#-----------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   BodyPlanName      = property (GetBodyPlanViewName, SetBodyPlanViewName, None, 'BodyPlanName - view name')
   Scale             = property (GetScale, SetScale, None, 'Scale - view scale')
   AftLimits         = property (GetAftLimits, SetAftLimits, None, 'AftLimits - coordinates of aft limits')
   FwdLimits         = property (GetFwdLimits, SetFwdLimits, None, 'AftLimits - coordinates of fore limits')
   bLooking          = property (GetLooking, SetLooking, None, 'bLooking - looking way code')
   GridSpacing       = property (GetGrid, SetGrid, None, 'GridSpacing - grid spacing')
   SelectCurves      = property (GetCurves , SetLineTypes, None, 'SelectCurves - curve name/type dictionary')

   def setDrawFrame(self, frame):
      if type(frame)!=type (0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__DrawFrame = frame
   def getDrawFrame(self): return self.__DrawFrame
   DrawFrame         = property (getDrawFrame, setDrawFrame, None, 'DrawFrame - drawing frame')

   #sections

   def setLongSectionImage(self, image):
      if type(image) != type(self.IMAGE_FULL):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      if image != self.IMAGE_FULL and image != self.IMAGE_MOULD and image != self.IMAGE_THICK:
         raise ValueError, BodyPlanViewOptions.__ErrorMessages[ValueError]
      self.__LongSectionImage  = int(image)
   def getLongSectionImage(self):         return self.__LongSectionImage
   LongSectionImage  = property (getLongSectionImage, setLongSectionImage, None, 'LongSectionImage - longitudal section image type')

   def setLongSectionFrame(self, frame):
      if type(frame) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__LongSectionFrame  = int(frame)
   def getLongSectionFrame(self):         return self.__LongSectionFrame
   LongSectionFrame  = property (getLongSectionFrame, setLongSectionFrame, None, 'LongSectionFrame - longitudal section frame')

   #colours

   def setSeamColour(self, seam):  self.SetColours(self.__LongColour, seam, self.__FrameColour)
   def getSeamColour(self):        return self.__SeamColour
   SeamColour        = property (getSeamColour, setSeamColour, None, 'SeamColour - seam colour')

   def setLongColour(self, long):  self.SetColours(long, self.__SeamColour, self.__FrameColour)
   def getLongColour(self):        return self.__LongColour
   LongColour        = property (getLongColour, setLongColour, None, 'LongColour - longitudal colour')

   def setFrameColour(self, frame):  self.SetColours(self.__LongColour, self.__SeamColour, frame)
   def getFrameColour(self):        return self.__FrameColour
   FrameColour       = property (getFrameColour, setFrameColour, None, 'FrameColour - frame colour')

   #auto flags

   def getbAutoSeams(self): return self.__bAutoSeams
   def setbAutoSeams(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__bAutoSeams = value
   bAutoSeams        = property (getbAutoSeams, setbAutoSeams, None, 'bAutoSeams - auto include seams flag')

   def getbAutoLongTrace(self): return self.__bAutoLongTrace
   def setbAutoLongTrace(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__bAutoLongTrace = value
   bAutoLongTrace    = property (getbAutoLongTrace, setbAutoLongTrace, None, 'bAutoLongTrace - auto longitudal trace flag')

   def getbAutoLongSection(self): return self.__bAutoLongSection
   def setbAutoLongSection(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__bAutoLongSection = value
   bAutoLongSection    = property (getbAutoLongSection, setbAutoLongSection, None, 'bAutoLongSection - auto longitudal section flag')

   #filters

   def getPanelFilter(self): return self.__PanelFilter
   def setPanelFilter(self, filter):
      if type(filter) == type([]): self.__PanelFilter = [] #there is an append call in SetPanels
      self.SetPanels(filter)
   PanelFilter       = property (getPanelFilter, setPanelFilter, None, 'PanelFilter - panel filters list')

   def getSeamsFilter(self): return self.__SeamsFilter
   def setSeamsFilter(self, filter):
      if type(filter) == type([]): self.__SeamsFilter = [] #there is an append call in SetSeams
      self.SetSeams(filter)
   SeamsFilter       = property (getSeamsFilter, setSeamsFilter, None, 'SeamsFilter - seams filter list')

   def getTraceFilter(self): return self.__TraceFilter
   def setTraceFilter(self, filter):
      if type(filter) == type([]): self.__TraceFilter = [] #there is an append call in SetLongTrace
      self.SetLongTrace(filter)
   TraceFilter       = property (getTraceFilter, setTraceFilter, None, 'TraceFilter - longitudal trace filter list')

   def getSectionFilter(self): return self.__SectionFilter
   def setSectionFilter(self, filter):
      if type(filter) == type([]): self.__SectionFilter = [] #there is an append call in SetLongSection
      self.SetLongSection(filter)
   SectionFilter     = property (getSectionFilter, setSectionFilter, None, 'SectionFilter - longitudal section filter list')

   def getSurfacesFilter(self):  return self.__SurfacesFilter
   def setSurfacesFilter(self, filter):
      if type(filter) == type([]): self.__SurfacesFilter = [] #there is an append call in SetSurfaces
      self.SetSurfaces(filter)
   SurfacesFilter    = property (getSurfacesFilter, setSurfacesFilter, None, 'SurfacesFilter - list of surface for filtering')

   #exclude flags

   def getSeamsExclude(self): return self.__SeamsExclude
   def setSeamsExclude(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__SeamsExclude = value
   SeamsExclude      = property (getSeamsExclude, setSeamsExclude, None, 'SeamsExclude - exclude/include seams flag')

   def getTraceExclude(self): return self.__TraceExclude
   def setTraceExclude(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__TraceExclude = value
   TraceExclude      = property (getTraceExclude, setTraceExclude, None, 'TraceExclude - exclude/include long trace flag')

   def getSectionExclude(self): return self.__SectionExclude
   def setSectionExclude(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__SectionExclude = value
   SectionExclude    = property (getSectionExclude, setSectionExclude, None, 'SectionExclude - exclude/include section flag')

   def getSurfacesExclude(self):  return self.__SurfacesExclude
   def setSurfacesExclude(self, value):
      if type(value) != type(0):
         raise TypeError, BodyPlanViewOptions.__ErrorMessages[TypeError]
      self.__SurfacesExclude = value
   SurfacesExclude   = property (getSurfacesExclude, setSurfacesExclude, None, 'SurfacesExclude - exclude/include surfaces flag')

