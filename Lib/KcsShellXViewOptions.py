## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsShellXViewOptions.py
#
#      PURPOSE:
#
#          To hold options view objects.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import KcsLinetype
import string
import types

class ShellXViewOptions(object):

   SIDE_DEFAULT           = 0
   SIDE_PORT              = 0
   SIDE_STARBOARD         = 1
   SIDE_BOTH              = 2
   PLANE_DEFAULT          = 0
   PLANE_BY_SEAMS         = 1
   PLANE_BY_X             = -1
   PLANE_BY_Y             = -2
   PLANE_BY_Z             = -3

   SIDE_TYPE  = [SIDE_DEFAULT, SIDE_PORT, SIDE_STARBOARD, SIDE_BOTH ]
   PLANE_TYPE = [PLANE_DEFAULT, PLANE_BY_SEAMS, PLANE_BY_X, PLANE_BY_Y, PLANE_BY_Z]

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of ShellXViewOptions class',
                       ValueError: 'not supported value, see documentation of ShellXViewOptions class' }


#-----------------------------------------------------------------------
   def __init__(self):
      'inits ShellXViewOptions'

      self.__ShellXName                = 'TB_VIEW'
      self.__SurfaceName               = 'SPHULL'
      self.__DevelopedFromCode         = -2
      self.__DevelopedFromCoordinate   = 0.0
      self.__SternLimitsCode           = 0
      self.__SternLimitsSeams          = []
      self.__SternLimitsCoordinate     = 0.0
      self.__StemLimitsCode            = 0
      self.__StemLimitsSeams           = []
      self.__StemLimitsCoordinate      = 0.0
      self.__UpperLimitsCode           = 0
      self.__UpperLimitsSeams          = []
      self.__UpperLimitsCoordinate     = 0.0
      self.__LowerLimitsCode           = 0
      self.__LowerLimitsSeams          = []
      self.__LowerLimitsCoordinate     = 0.0
      self.__SideCode                  = 1
      self.__bAutoPenetrations         = 0
      self.__bExceptPanels             = 0
      self.__bExceptBlocks             = 0
      self.__bExceptSeams              = 0
      self.__bExceptLongitudals        = 0
      self.__bExceptTransversals       = 0
      self.__SelectBlocks              = []
      self.__SelectLongitudals         = []
      self.__SelectSeams               = []
      self.__SelectPanels              = []
      self.__SelectTransversals        = []
      self.__SelectCurves              = {}


#-----------------------------------------------------------------------

   def SetShellXViewName(self, name):
      'sets symbolic view name'

      if type(name) != type(''):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      self.__ShellXName = string.upper(name)

#-----------------------------------------------------------------------

   def SetSurfName(self, name):
      'sets symbolic view name'

      if type(name) != type(''):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      self.__SurfaceName = string.upper(name)
#-----------------------------------------------------------------------

   def GetShellXViewName(self):
      'returns symbolic view name'
      return self.__ShellXName
#-----------------------------------------------------------------------

   def GetSurfName(self):
      'returns symbolic view name'
      return self.__SurfaceName

#-----------------------------------------------------------------------

   def SetDevelopedFromX(self, coord):
      'allows user to specify plane by X, Y or Z coordinate'
      self.__DevelopedFromCode  = ShellXViewOptions.PLANE_BY_X
      self.__DevelopedFromCoordinate = coord
#-----------------------------------------------------------------------

   def SetDevelopedFromY(self, coord):
      'allows user to specify plane by X, Y or Z coordinate'
      self.__DevelopedFromCode  = ShellXViewOptions.PLANE_BY_Y
      self.__DevelopedFromCoordinate = coord

#-----------------------------------------------------------------------

   def SetDevelopedFromZ(self, coord):
      'allows user to specify plane by X, Y or Z coordinate'
      self.__DevelopedFromCode  = ShellXViewOptions.PLANE_BY_Z
      self.__DevelopedFromCoordinate = coord

#-----------------------------------------------------------------------

   def GetDevelopedFrom(self):
      'Gets Developed From code and coordinate'
      return [self.__DevelopedFromCode, self.__DevelopedFromCoordinate]

#-----------------------------------------------------------------------
   def SetSternLimits(self, code, value):
      'Sets Stern Limits'

      if code != self.PLANE_BY_X and code != self.PLANE_BY_SEAMS:
         raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      self.__SternLimitsCode = int(code)

      if code == self.PLANE_BY_SEAMS:
         if type(value) != type([]):
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         else:
            for item in value:
               if type(item) != type(''):
                  raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
               self.__SternLimitsSeams.append(item)
      else:
         if type(value) != types.FloatType and type(value) != types.IntType:
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         self.__SternLimitsCoordinate  = float( value)
#-----------------------------------------------------------------------

   def SetStemLimits(self, code, value):
      'Set Stem Limits'
      if code != self.PLANE_BY_X and code != self.PLANE_BY_SEAMS:
         raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]

      elif code == self.PLANE_BY_SEAMS:
         if type(value) != type([]):
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]

         else:
            for item in value:
               if type(item) != type(''):
                  raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
               self.__StemLimitsSeams.append(item)

      else:
         if type(value) != types.FloatType and type(value) != types.IntType:
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         self.__StemLimitsCoordinate  = float(value)

      self.__StemLimitsCode = code

#-----------------------------------------------------------------------

   def GetSternLimits(self):
      'gets SternLimits'
      return [self.__SternLimitsCode, self.__SternLimitsCoordinate, self.__SternLimitsSeams]


#---------------------------------------------------------------------
   def GetStemLimits(self):
      'gets StemLimits'
      return [self.__StemLimitsCode, self.__StemLimitsCoordinate, self.__StemLimitsSeams]

#-----------------------------------------------------------------------
   def SetUpperLimits(self, code, value):
      'Set Upper Limits'

      if code != self.PLANE_BY_Y and code != self.PLANE_BY_Z \
         and code != self.PLANE_BY_SEAMS:
         raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      self.__UpperLimitsCode = int(code)

      if code == self.PLANE_BY_SEAMS:
         if type(value) != type([]):
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         else:
            for item in value:
               if type(item) != type(''):
                  raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
               self.__UpperLimitsSeams.append(item)
      else:
         if type(value) != types.FloatType and type(value) != types.IntType:
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         self.__UpperLimitsCoordinate  = float(value)


#-----------------------------------------------------------------------

   def GetUpperLimits(self):
      'gets Upper Limits'
      return [self.__UpperLimitsCode, self.__UpperLimitsCoordinate, self.__UpperLimitsSeams]

#-----------------------------------------------------------------------

   def SetLowerLimits(self, code, value):
      'Set Lowet Limits'

      if code != self.PLANE_BY_Y and code != self.PLANE_BY_Z \
         and code != self.PLANE_BY_SEAMS:
         raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      self.__LowerLimitsCode = int(code)

      if code == self.PLANE_BY_SEAMS:
         if type(value) != type([]):
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         else:
            for item in value:
               if type(item) != type(''):
                  raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
               self.__LowerLimitsSeams.append(item)
      else:
         if type(value) != types.FloatType and type(value) != types.IntType:
            raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
         self.__LowerLimitsCoordinate  = float(value)

#-----------------------------------------------------------------------

   def GetLowerLimits(self):
      'gets Lower Limits'
      return [self.__LowerLimitsCode, self.__LowerLimitsCoordinate, self.__LowerLimitsSeams]

#-----------------------------------------------------------------------

   def SetSideCode(self, code):
      'Set Side Code'
      if code not in ShellXViewOptions.SIDE_TYPE:
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      else:
         self.__SideCode = int(code)
#-----------------------------------------------------------------------
   def GetSideCode(self):
      'Get SideCode'
      return [self.__SideCode]

#-----------------------------------------------------------------------

   def SetSelectPanels(self, list):
      'Set Selected Panels'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SelectPanels.append(item)


#-----------------------------------------------------------------------
   def SetSelectBlocks(self, list):
      'Set Selected Blocks'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SelectBlocks.append(item)

#-----------------------------------------------------------------------
   def SetExceptPanels(self, bSet = 1):
      'Set Excepted Panels'
      self.__bExceptPanels = int( bSet )

#-----------------------------------------------------------------------
   def GetPanels(self):
      'Get Panels'
      return [self.__bExceptPanels, self.__SelectPanels]

#-----------------------------------------------------------------------
   def SetExceptBlocks(self, bSet = 1):
      'Set Excepted Blocks'
      self.__bExceptBlocks = int( bSet )
#-----------------------------------------------------------------------
   def GetBlocks(self):
      'Get Blocks'
      return [self.__bExceptBlocks, self.__SelectBlocks]

#-----------------------------------------------------------------------
   def SetSelectSeams(self, list):
      'Set Selected Seams'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SelectSeams.append(item)

#-----------------------------------------------------------------------
   def SetExceptSeams(self, bSet = 1):
      'Set Excepted Seams'
      self.__bExceptSeams = int( bSet)
#-----------------------------------------------------------------------
   def GetSeams(self):
      'Get Seams'
      return [self.__bExceptSeams, self.__SelectSeams]

#-----------------------------------------------------------------------
   def SetSelectLongitudals(self, list):
      'Set Selected Longitudinals'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SelectLongitudals.append(item)

#-----------------------------------------------------------------------
   def SetExceptLongitudals(self, bSet = 1):
      'Set Excepted Longitudinals'
      self.__bExceptLongitudals = int(bSet)
#-----------------------------------------------------------------------
   def GetLongitudals(self):
      'Get Longitudals'
      return [self.__bExceptLongitudals, self.__SelectLongitudals]
#-----------------------------------------------------------------------
   def SetSelectTransversals(self, list):
      'Set Selected Longitudinals'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            self.__SelectTransversals.append(item)

#-----------------------------------------------------------------------
   def SetExceptTransversals(self, bSet = 1):
      'Set Excepted Longitudinals'
      self.__bExceptTransversals = int( bSet )

#-----------------------------------------------------------------------
   def GetTransversals(self):
      'Get Transversals'
      return [self.__bExceptTransversals, self.__SelectTransversals]
#-----------------------------------------------------------------------

   def SetLineTypes(self, dict):
      'Set Curves and Types'
      if type(dict) != type({'':''}):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      lines = KcsLinetype.GetLinetypes()
      for item in dict.values():
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         if not item in lines:
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      for item in dict.keys():
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      self.__SelectCurves = dict

#-----------------------------------------------------------------------
   def GetCurves(self):
      'Get Selected Curves and Line Types'
      return [self.__SelectCurves]

#-----------------------------------------------------------------------

   def SetAutoPenetrations(self, code = 1):
      'Set Auto Penetrations'

      self.__bAutoPenetrations = int(code)

#-----------------------------------------------------------------------
   def GetAutoPenetrations(self):
      'Get AutoPenetrations'
      return self.__bAutoPenetrations

#-----------------------------------------------------------------------
   def __repr__(self):
      SIDE_TYPE_str  = {self.SIDE_PORT:'SIDE_PORT', \
                        self.SIDE_STARBOARD:'SIDE_STARBOARD', self.SIDE_BOTH:'SIDE_BOTH'}
      PLANE_TYPE_str = {self.PLANE_DEFAULT:'PLANE_DEFAULT',\
                        self.PLANE_BY_SEAMS:'PLANE_BY_SEAMS', self.PLANE_BY_X:'PLANE_BY_X',\
                        self.PLANE_BY_Y:'PLANE_BY_Y', self.PLANE_BY_Z:'PLANE_BY_Z'}
      tup = ( 'ShellXViewOptions:',
         "   ShellXName:" + str(self.__ShellXName),
         "   SurfaceName:" + str(self.__SurfaceName),
         "   DevelopedFromCode:" + PLANE_TYPE_str[self.__DevelopedFromCode],
         "   DevelopedFromCoordinate:" + str(self.__DevelopedFromCoordinate),
         "   SternLimitsCode:" + PLANE_TYPE_str[self.__SternLimitsCode],
         "   SternLimitsSeams:" + str(self.__SternLimitsSeams),
         "   SternLimitsCoordinate:" + str(self.__SternLimitsCoordinate),
         "   StemLimitsCode:" + PLANE_TYPE_str[self.__StemLimitsCode],
         "   StemLimitsSeams:" + str(self.__StemLimitsSeams),
         "   StemLimitsCoordinate:" + str(self.__StemLimitsCoordinate),
         "   UpperLimitsCode:" + PLANE_TYPE_str[self.__UpperLimitsCode],
         "   UpperLimitsSeams:" + str(self.__UpperLimitsSeams),
         "   UpperLimitsCoordinate:" + str(self.__UpperLimitsCoordinate),
         "   LowerLimitsCode:" + PLANE_TYPE_str[self.__LowerLimitsCode],
         "   LowerLimitsSeams:" + str(self.__LowerLimitsSeams),
         "   LowerLimitsCoordinate:" + str(self.__LowerLimitsCoordinate),
         "   SideCode:" + SIDE_TYPE_str[self.__SideCode],
         "   bAutoPenetrations:" + str(self.__bAutoPenetrations),
         "   bExceptPanels:" + str(self.__bExceptPanels),
         "   bExceptBlocks:" + str(self.__bExceptBlocks),
         "   bExceptSeams:" + str(self.__bExceptSeams),
         "   bExceptLongitudals:" + str(self.__bExceptLongitudals),
         "   bExceptTransversals:" + str(self.__bExceptTransversals),
         "   SelectBlocks:" + str(self.__SelectBlocks),
         "   SelectLongitudals:" + str(self.__SelectLongitudals),
         "   SelectSeams:" + str(self.__SelectSeams),
         "   SelectPanels:" + str(self.__SelectPanels),
         "   SelectTransversals:" + str(self.__SelectTransversals),
         "   SelectCurves:" + str(self.__SelectCurves),
             )
      return string.join (tup, '\n')

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   ShellXName                = property (GetShellXViewName , SetShellXViewName)
   SurfaceName               = property (GetSurfName , SetSurfName)
   def GetDevelopedFromCode(self): return self.__DevelopedFromCode
   def SetDevelopedFromCode(self,value):
      if not isinstance(value,int):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      if value not in [self.PLANE_BY_X, self.PLANE_BY_Y, self.PLANE_BY_Z]:
         raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
      self.__DevelopedFromCode = value
   DevelopedFromCode         = property (GetDevelopedFromCode , SetDevelopedFromCode)
   def GetDevelopedFromCoordinate(self): return self.__DevelopedFromCoordinate
   def SetDevelopedFromCoordinate(self, value):
      self.__DevelopedFromCoordinate = value
   DevelopedFromCoordinate   = property ( GetDevelopedFromCoordinate, SetDevelopedFromCoordinate)

   # readonly (set by methods)
   def GetSternLimitsCode(self): return self.__SternLimitsCode
   def GetSternLimitsSeams(self): return self.__SternLimitsSeams
   def GetSternLimitsCoordinate(self): return self.__SternLimitsCoordinate
   SternLimitsCode           = property (GetSternLimitsCode )
   SternLimitsSeams          = property (GetSternLimitsSeams )
   SternLimitsCoordinate     = property (GetSternLimitsCoordinate )

   def GetStemLimitsCode(self): return self.__StemLimitsCode
   def GetStemLimitsSeams(self): return self.__StemLimitsSeams
   def GetStemLimitsCoordinate(self): return self.__StemLimitsCoordinate
   StemLimitsCode            = property (GetStemLimitsCode )
   StemLimitsSeams           = property (GetStemLimitsSeams )
   StemLimitsCoordinate      = property (GetStemLimitsCoordinate )

   def GetUpperLimitsCode(self): return self.__UpperLimitsCode
   def GetUpperLimitsSeams(self): return self.__UpperLimitsSeams
   def GetUpperLimitsCoordinate(self): return self.__UpperLimitsCoordinate
   UpperLimitsCode           = property (GetUpperLimitsCode )
   UpperLimitsSeams          = property (GetUpperLimitsSeams )
   UpperLimitsCoordinate     = property (GetUpperLimitsCoordinate )

   def GetLowerLimitsCode(self): return self.__LowerLimitsCode
   def GetLowerLimitsSeams(self): return self.__LowerLimitsSeams
   def GetLowerLimitsCoordinate(self): return self.__LowerLimitsCoordinate
   LowerLimitsCode           = property (GetLowerLimitsCode )
   LowerLimitsSeams          = property (GetLowerLimitsSeams )
   LowerLimitsCoordinate     = property (GetLowerLimitsCoordinate )

   def GetSideCodeOnly(self): return self.__SideCode
   SideCode                  = property (GetSideCodeOnly , SetSideCode)
   bAutoPenetrations         = property (GetAutoPenetrations , SetAutoPenetrations)
   def GetExceptPanels(self): return self.__bExceptPanels
   bExceptPanels             = property (GetExceptPanels , SetExceptPanels)
   def GetExceptBlocks(self): return self.__bExceptBlocks
   bExceptBlocks             = property (GetExceptBlocks , SetExceptBlocks)
   def GetExceptSeams(self): return self.__bExceptSeams
   bExceptSeams              = property (GetExceptSeams , SetExceptSeams)
   def GetExceptLongitudals(self): return self.__bExceptLongitudals
   bExceptLongitudals        = property (GetExceptLongitudals , SetExceptLongitudals)
   def GetExceptTransversals(self): return self.__bExceptTransversals
   bExceptTransversals       = property (GetExceptTransversals , SetExceptTransversals)
   def GetSelectBlocks(self): return self.__SelectBlocks
   def SetSelectBlocksC(self, list):
      'set selected blocks with clear'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      blocks = []
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            blocks.append(item)
      self.__SelectBlocks = blocks
   SelectBlocks              = property (GetSelectBlocks , SetSelectBlocksC)
   def GetSelectLongitudals(self): return self.__SelectLongitudals
   def SetSelectLongitudalsC(self, list):
      'set selected longitudals with clear'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      longitudals = []
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            longitudals.append(item)
      self.__SelectLongitudals = longitudals
   SelectLongitudals         = property (GetSelectLongitudals , SetSelectLongitudalsC)
   def GetSelectSeams(self): return self.__SelectSeams
   def SetSelectSeamsC(self, list):
      'Set selected seams with clear'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      seams = []
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            seams.append(item)
      self.__SelectSeams = seams
   SelectSeams               = property (GetSelectSeams , SetSelectSeamsC)
   def GetSelectPanels(self): return self.__SelectPanels
   def SetSelectPanelsC(self, list):
      'Set selected panels with clear'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      panels = []
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            panels.append(item)
      self.__SelectPanels = panels
   SelectPanels              = property (GetSelectPanels , SetSelectPanelsC)
   def GetSelectTransversals(self): return self.__SelectTransversals
   def SetSelectTransversalsC(self, list):
      'Set selected transversals with clear'
      if type(list) != type([]):
         raise TypeError, ShellXViewOptions.__ErrorMessages[TypeError]
      transversals = []
      for item in list:
         if type(item) != type(''):
            raise ValueError, ShellXViewOptions.__ErrorMessages[ValueError]
         else:
            transversals.append(item)
      self.__SelectTransversals = transversals
   SelectTransversals        = property (GetSelectTransversals , SetSelectTransversalsC)
   def GetSelectCurves(self): return self.__SelectCurves
   SelectCurves              = property (GetSelectCurves, SetLineTypes)
