## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.


#
#      NAME:
#          KcsRectangle2D.py
#
#      PURPOSE:
#          The Rectangle2D class holds information about a 2D rectangle. The
#          rectangle is axis parallel and is defined by two diagonal
#          corner points.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Corner1        Point2D       The first corner
#          Corner2        Point2D       The second corner

import types
from KcsPoint2D import Point2D
import KcsPoint2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Rectangle2D class',
                  IndexError: 'not valid index, valid values of index for Rectangle2D class are: 0, 1' }
Infinity = 10000000000.0

class Rectangle2D(object):
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          p1, p2           Point2D          corners of rectangle
#              or
#          x1, y1, x2, y2   real             rectangle corners coordinates
#              or
#          None

   def __init__(self, *args):
      self.__Corner1 = Point2D()
      self.__Corner2 = Point2D()
      if len(args)>0:
         self.SetCorners(*args)

#
#      METHOD:
#          SetCorners
#
#      PURPOSE:
#          To set rectangle corners
#
#      INPUT:
#          Parameters:
#          p1, p2           Point2D          corners of rectangle
#              or
#          x1, y1, x2, y2   real             rectangle corners coordinates

   def SetCorners(self, *args):
      if len(args)==2:              # 2 points p1, p2
         for arg in args:
            if not isinstance(arg,Point2D) and not isinstance(arg,KcsPoint2D.Point2D):
               raise TypeError, ErrorMessages[TypeError]
         self.__Corner1 = Point2D(args[0].X, args[0].Y)
         self.__Corner2 = Point2D(args[1].X, args[1].Y)
      elif len(args)==4:            # 4 coordinates x1, y1, x2, y2
         try:
            self.__Corner1 = Point2D(args[0], args[1])
            self.__Corner2 = Point2D(args[2], args[3])
         except TypeError:
            raise TypeError, ErrorMessages[TypeError]
      else:
         raise TypeError, ErrorMessages[TypeError]

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

      if not isinstance(other, Rectangle2D):
         raise TypeError, ErrorMessages[TypeError]

      if self.Corner1 != other.Corner1 or self.Corner2 != other.Corner2:
         return 1
      else:
         return 0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Rectangle first corner: %s second corner: %s' % (self.Corner1, self.Corner2)

#
#      METHOD:
#          __getitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __getitem__(self, index):
      if not isinstance(index,int):
         raise TypeError, ErrorMessages[TypeError]
      if index==0:
         return self.Corner1
      elif index==1:
         return self.Corner2
      else:
         raise IndexError, ErrorMessages[IndexError]

#
#      METHOD:
#          __setitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __setitem__(self, index, value):
      if not isinstance(index,int):
         raise TypeError, ErrorMessages[TypeError]
      if index==0:
         self.Corner1 = value
      elif index==1:
         self.Corner2 = value
      else:
         raise IndexError, ErrorMessages[IndexError]

#
#      METHOD:
#          IsEmpty()
#
#      PURPOSE:
#          returns 1 if rectangle is empty

   def IsEmpty(self):
      if ( self.Corner1.X == Infinity and self.Corner1.Y == Infinity and
           self.Corner2.X == -Infinity and self.Corner2.Y == -Infinity ):
         return 1
      else:
         return 0

#
#      METHOD:
#          SetEmpty()
#
#      PURPOSE:
#          sets empty rectangle

   def SetEmpty(self):
      self.Corner1.X =    Infinity
      self.Corner1.Y =    Infinity
      self.Corner2.X = -  Infinity
      self.Corner2.Y = -  Infinity

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetCorner1(self): return self.__Corner1
   def SetCorner1(self,value):
      if not isinstance(value,Point2D) and not isinstance(value,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.__Corner1 = Point2D(value.X,value.Y)
   def GetCorner2(self): return self.__Corner2
   def SetCorner2(self,value):
      if not isinstance(value,Point2D) and not isinstance(value,KcsPoint2D.Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.__Corner2 = Point2D(value.X,value.Y)
   Corner1 = property (GetCorner1 , SetCorner1)
   Corner2 = property (GetCorner2 , SetCorner2)

