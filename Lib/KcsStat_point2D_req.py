## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsStat_point2D_req.py
#
#      PURPOSE:
#          The Stat_point2D_req class holds information about some initial status when
#          defining a 2D point, using the "point2D_req" function.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#        __CursorType            KcsCursorType.CursorType         Cursor type
#        __Point2dDefMode        integer                          2D point definition mode. Look for SetDefMode() documentation.
#        __HelpPoint             KcsPoint2D.Point2D()             Definition of help point. This attribute is optional.
#        __Scale                 real                             Scale used in point selection. This attribute is optional.
#
#      METHODS:
#
#        SetDefMode                                               sets 2D point definition mode
#        GetDefMode                                               returns 2D point definition mode
#        SetCursorType                                            sets cursor type
#        GetCursorType                                            returns cursor type
#        SetHelpPoint                                             sets help point to specified point:
#                                                                       - use SetHelpPoint(p) to set help point to p
#                                                                       - use SetHelpPoint(None) to delete help point
#        GetHelpPoint                                             gets help point
#        SetScale                                                 scale value
#        GetScale


import types
import copy
import KcsCursorType
from KcsCursorType import CursorType
import KcsPoint2D
from KcsPoint2D import Point2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Stat_point2D_req class',
                  ValueError: 'wrong value for Point2D definition mode' }

Point2dDefModes = { 'ModeKeyIn' : 1, 'ModeCursor' : 2, 'ModeNode' : 3, 'ModeExist' : 4, 'ModeSymbConnection' : 5, 'ModeAuto' : 6,
                    'ModeArcAtAngle' : 7, 'ModeArcCentre' : 8, 'ModeDistanceAlong' : 9, 'ModeMidPoint' : 10, 'ModeIntersect' : 11,
                    'ModeOffsetCurrent' : 12, 'ModeNearest' : 13, 'ModeCOG' : 14, 'ModeEvent' : 15 }


class Stat_point2D_req(object):

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#

   def __init__(self):
      self.__CursorType          = KcsCursorType.CursorType()
      self.__Point2dDefMode      = Point2dDefModes['ModeCursor']
      self.__Scale               = 1.0


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetDefMode
#
#      PURPOSE:
#          To set point2D definition mode
#
#      INPUT:
#          Parameters:
#              mode        string         2D point definition mode:
#                                            'ModeKeyIn'
#                                            'ModeCursor'
#                                            'ModeNode'
#                                            'ModeExist'
#                                            'ModeSymbConnection'
#                                            'ModeAuto'
#                                            'ModeArcAtAngle'
#                                            'ModeArcCentre'
#                                            'ModeDistanceAlong'
#                                            'ModeMidPoint'
#                                            'ModeIntersect'
#                                            'ModeOffsetCurrent'
#                                            'ModeNearest'
#                                            'ModeCOG'
#                                            'ModeEvent'
#

   def SetDefMode(self, mode):
      if not isinstance(mode,str):
         raise TypeError, ErrorMessages[TypeError]
      if Point2dDefModes.has_key(mode):
         self.__Point2dDefMode = Point2dDefModes[mode]
      else:
         raise ValueError, ErrorMessages[ValueError]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          GetDefMode
#
#      PURPOSE:
#          To get point2D definition mode
#
#      RESULT:
#              mode        string         2D point definition mode:
#                                            'ModeKeyIn'
#                                            'ModeCursor'
#                                            'ModeNode'
#                                            'ModeExist'
#                                            'ModeSymbConnection'
#                                            'ModeAuto'
#                                            'ModeArcAtAngle'
#                                            'ModeArcCentre'
#                                            'ModeDistanceAlong'
#                                            'ModeMidPoint'
#                                            'ModeIntersect'
#                                            'ModeOffsetCurrent'
#                                            'ModeNearest'
#                                            'ModeCOG'
#                                            'ModeEvent'
#

   def GetDefMode(self):
      return Point2dDefModes.keys()[Point2dDefModes.values().index(self.__Point2dDefMode)];

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetCursorType
#
#      PURPOSE:
#          To set cursor type
#
#      INPUT:
#          Parameters:
#           cursortype     KcsCursorType.CursorType         cursor type
#

   def SetCursorType(self, cursortype):
      if not isinstance(cursortype,CursorType) and not isinstance(cursortype,KcsCursorType.CursorType):
         raise TypeError, ErrorMessages[TypeError]
      self.__CursorType = copy.deepcopy(cursortype)


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          GetCursorType
#
#      PURPOSE:
#          To get cursor type
#
#      RESULT:
#
#          instance of KcsCursorType.CursorType         current cursor type
#

   def GetCursorType(self):
      cursortype = copy.deepcopy(self.__CursorType)
      return cursortype

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetHelpPoint
#
#      PURPOSE:
#          To set help point for ModeOffsetCurrent point definition mode
#
#      INPUT:
#          Parameters:
#           point             KcsPoint2D.Point2D            help point
#

   def SetHelpPoint(self, point):
      if (point == None):
         if hasattr(self, '_Stat_point2D_req__HelpPoint'):
            delattr(self, '_Stat_point2D_req__HelpPoint')
      else:
         if not isinstance(point,Point2D) and not isinstance(point,KcsPoint2D.Point2D):
            raise TypeError, ErrorMessages[TypeError]
         self.__HelpPoint = copy.deepcopy(point)


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          GetHelpPoint
#
#      PURPOSE:
#          To get help point defined for ModeOffsetCurrent point definition mode
#
#      RESULT:
#
#          point                 help point
#

   def GetHelpPoint(self):
      if hasattr(self, '_Stat_point2D_req__HelpPoint'):
         point = copy.deepcopy(self.__HelpPoint)
         return point
      else:
         return None

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          GetScale
#
#      PURPOSE:
#          To get scale
#
#      RESULT:
#
#          real or None if scale not defined
#

   def GetScale(self):
      if hasattr(self, '_Stat_point2D_req__Scale'):
         return self.__Scale
      else:
         return None

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetScale
#
#      PURPOSE:
#          To set scale value
#
#      INPUT:
#          Parameters:
#           real or None             Scale value or None to delete scale definition
#

   def SetScale(self, scale):
      if scale == None:
         if hasattr(self, '_Stat_point2D_req__Scale'):
            delattr(self, '_Stat_point2D_req__Scale')
      else:
         if type(scale) != type(1.0) and type(scale) != type(1):
            raise TypeError, ErrorMessages[TypeError]
         self.__Scale = float(scale)

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, Stat_point2D_req):
         raise TypeError, ErrorMessages[TypeError]

      if self.__CursorType != other.__CursorType or self.__Point2dDefMode != other.__Point2dDefMode:
         return 1
      else:
         if self.GetHelpPoint() == other.GetHelpPoint():
            return 0
         else:
            return 1

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      strMode     = Point2dDefModes.keys()[Point2dDefModes.values().index(self.__Point2dDefMode)];
      strCurType  = str(self.__CursorType)
      return 'Definition mode: %s       %s' % (strMode, strCurType)

#-----------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Cursor              = property (GetCursorType , SetCursorType)
   DefMode             = property (GetDefMode , SetDefMode)
   Scale               = property (GetScale , SetScale)
   HelpPoint           = property (GetHelpPoint , SetHelpPoint)
