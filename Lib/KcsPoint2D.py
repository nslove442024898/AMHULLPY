## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPoint2D.py
#
#      PURPOSE:
#          The Point2D class holds information about a 2D point
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          X              real          The X coordinate
#          Y              real          The Y coordinate

import math
import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Point2D class' }

class Point2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          X            real              The X coordinate of the point
#          Y            real              The Y coordinate of the point
#

   def __init__(self, x=0.0, y=0.0):
      self.X = x
      self.Y = y

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return '[X Y:%s,%s]' % (self.X, self.Y)

#
#      METHOD:
#          DistanceToPoint
#
#      PURPOSE:
#          calculate the distance between self and another point
#
#      INPUT:
#          Parameters:
#          p              Point2D       Point to calculate distance to
#
#      RESULT:
#          Returns:
#          real           The distance

   def DistanceToPoint(self, p):
      if not isinstance(p,Point2D):
         raise TypeError, ErrorMessages[TypeError]
      return (math.sqrt((self.X-p.X)*(self.X-p.X) + (self.Y-p.Y)*(self.Y-p.Y) ))

#
#      METHOD:
#          Move
#
#      PURPOSE:
#          Move (translate) the point
#
#      INPUT:
#          Parameters:
#          xmove           real         x-value for translation
#          ymove           real         y-value for translation
#
#      RESULT:
#          The point will be updated
#

   def Move(self, xmove, ymove):
      if (type(xmove) != types.FloatType and type(xmove) != types.IntType and type(xmove) != types.LongType) or \
         (type(ymove) != types.FloatType and type(ymove) != types.IntType and type(ymove) != types.LongType):
         raise TypeError, ErrorMessages[TypeError]
      self.X = self.X + xmove
      self.Y = self.Y + ymove

#
#      METHOD:
#          Round
#
#      PURPOSE:
#          The coordinate values are rounded to a given number of decimals
#
#      INPUT:
#          Parameters:
#          decimals       real          Numbers of decimals
#
#      RESULT:
#          The point will be updated
#

   def Round(self, decimals):
      if type(decimals) != types.IntType and type(decimals) != types.LongType:
         raise TypeError, ErrorMessages[TypeError]
      self.X =int(self.X * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
      self.Y =int(self.Y * math.pow(10, decimals)+0.5) / math.pow(10, decimals)

#
#      METHOD:
#          SetCoordinates
#
#      PURPOSE:
#          Update the point with given coordinates
#
#      INPUT:
#          Parameters:
#          X              real          The X coordinate
#          Y              real          The Y coordinate
#
#      RESULT:
#          The point will be updated
#
#

   def SetCoordinates(self, x, y):
      self.X = x
      self.Y = y

#
#      METHOD:
#          SetFromMidpoint
#
#      PURPOSE:
#          Update the point to be the midpoint of two other points
#
#      INPUT:
#          Parameters:
#          p1              Point2D       The first point
#          p2              Point2D       The second point
#
#      RESULT:
#          The point will be updated
#

   def SetFromMidpoint(self, p1, p2):
      if not isinstance(p1,Point2D) or not isinstance(p2,Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.X = p1.X + (p2.X-p1.X)*0.5
      self.Y = p1.Y + (p2.Y-p1.Y)*0.5

#
#      METHOD:
#          SetFromPoint
#
#      PURPOSE:
#          Update the point with coordinates from another point
#
#      INPUT:
#          Parameters:
#          p               Point2D       Point to copy values from
#
#      RESULT:
#          The point will be updated
#

   def SetFromPoint(self, p):
      if not isinstance(p,Point2D):
         raise TypeError, ErrorMessages[TypeError]
      self.X = p.X
      self.Y = p.Y

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):

      if not isinstance(other, Point2D):
         return 1

      if self.X != other.X or self.Y != other.Y:
         return 1
      else:
         return 0

#
#      METHOD:
#          Name
#
#      PURPOSE:
#          To get the name of this object's class
#
#      INPUT:
#          Parameters:
#          none

   def Name(self):
      return self.__class__.__name__

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetX(self): return self.__X
   def SetX(self,value):
      if type(value) != types.FloatType and type(value) != types.IntType and type(value) != types.LongType:
         raise TypeError, ErrorMessages[TypeError]
      self.__X = value + 0.0
   def GetY(self): return self.__Y
   def SetY(self,value):
      if type(value) != types.FloatType and type(value) != types.IntType and type(value) != types.LongType:
         raise TypeError, ErrorMessages[TypeError]
      self.__Y = value + 0.0
   X = property (GetX, SetX)
   Y = property (GetY, SetY)
