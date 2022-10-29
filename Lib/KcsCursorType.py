## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsCursorType.py
#
#      PURPOSE:
#          The CursorType class holds information about cursor type
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          private:
#           __nType       integer        cursor type
#           __Arguments   list           additional data for specified cursor type
#
#      METHODS:
#        SetCrossHair                     sets cross hair cursor type
#        SetRubberBand                    sets rubber band cursor type
#        SetRubberRectangle               sets rubber rectangle cursor type
#        SetRubberCircle                  sets rubber circle cursor type

import types
from KcsPoint2D import Point2D
import KcsPoint2D
from KcsHighlightSet import HighlightSet
import KcsHighlightSet

ErrorMessages = { TypeError : 'not supported argument type, see documentation of CursorType class' }


CursorTypes = {'CrossHair' : 1, 'RubberBand' : 2, 'RubberRectangle' : 3, 'RubberCircle' : 4, 'DragCursor' : 5}

class CursorType:

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
      self.__nType      = CursorTypes['CrossHair']
      self.__Arguments  = []


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetCrossHair
#
#      PURPOSE:
#          To set cursor type to cross hair cursor
#
#      INPUT:
#          Parameters:
#            None
#

   def SetCrossHair(self):
      self.__nType      = CursorTypes['CrossHair']
      self.__Arguments  = []


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetRubberBand
#
#      PURPOSE:
#          To set cursor type to rubber band cursor
#
#      INPUT:
#          Parameters:
#           point          KcsPoint2D.Point2D         start point of line
#
   def SetRubberBand(self, point):
      if not isinstance(point,Point2D) and not isinstance(point,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.__nType      = CursorTypes['RubberBand']
      self.__Arguments  = [KcsPoint2D.Point2D(point.X, point.Y)]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetRubberRectangle
#
#      PURPOSE:
#          To set cursor type to rubber rectangle cursor
#
#      INPUT:
#          Parameters:
#           point          KcsPoint2D.Point2D         start point of rectangle
#
   def SetRubberRectangle(self, point):
      if not isinstance(point,Point2D) and not isinstance(point,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.__nType      = CursorTypes['RubberRectangle']
      self.__Arguments  = [KcsPoint2D.Point2D(point.X, point.Y)]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetRubberCircle
#
#      PURPOSE:
#          To set cursor type to rubber circle cursor
#
#      INPUT:
#          Parameters:
#
   def SetRubberCircle(self, point):
      if not isinstance(point,Point2D) and not isinstance(point,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.__nType      = CursorTypes['RubberCircle']
      self.__Arguments  = [KcsPoint2D.Point2D(point.X, point.Y)]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          SetDragCursor
#
#      PURPOSE:
#          To set cursor type to drag cursor
#
#      INPUT:
#          Parameters:
#           highlight          KcsHighlightSet.HighlightSet         Drag cursor data
#           point              KcsPoint2D.Point2D                   Reference point of cursur
#
   def SetDragCursor(self, highlight, point):
      if not isinstance(highlight, KcsHighlightSet.HighlightSet) and not isinstance(highlight, HighlightSet):
         raise TypeError, ErrorMessages[TypeError]

      if point!=None and not isinstance(point,Point2D) and not isinstance(point,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]

      self.__nType      = CursorTypes['DragCursor']
      self.__Arguments  = [point, highlight]


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          GetCursorType
#
#      PURPOSE:
#          To get cursor type
#
#      RESULT:
#           string                        cursor type:
#                                               'CrossHair'
#                                               'RubberBand'
#                                               'RubberRectangle'
#                                               'RubberCircle'
#
   def GetCursorType(self):
      return CursorTypes.keys()[CursorTypes.values().index(self.__nType)];

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

      if not isinstance(other, CursorType):
         raise TypeError, ErrorMessages[TypeError]

      if self.__nType != other.__nType or self.__Arguments != other.__Arguments:
         return 1
      else:
         return 0

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Cursor type: %s' % (self.GetCursorType())
