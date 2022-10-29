## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPolygon2D.py
#
#      PURPOSE:
#          The Polygon2D class holds information about a 2D polygon. The
#          polygon is a list of points
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Polygon              [point]         list of points

import types

from KcsPoint2D import Point2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Polygon2D class' }

class Polygon2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          startp        Point2D        the start point of the polygon

   def __init__(self, startp=None):
      self.Polygon = []
      if startp!=None:
         if not isinstance(startp,Point2D):
            raise TypeError, ErrorMessages[TypeError]
         self.Polygon.append(Point2D(startp.X, startp.Y))

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Polygon: %s' % str(self.Polygon)

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __len__(self):
      return len(self.Polygon)

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

      if not isinstance(other, Polygon2D):
         raise TypeError, ErrorMessages[TypeError]

      if self.Polygon != other.Polygon:
         return 1
      else:
         return 0

#
#      METHOD:
#          __getitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __getitem__(self, index):
      return self.Polygon[index]

#
#      METHOD:
#          __setitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __setitem__(self, index, value):
      if not isinstance(value,Point2D):
            raise TypeError, ErrorMessages[TypeError]
      self.Polygon[index] = Point2D(value.X, value.Y)

#
#      METHOD:
#          __add__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __add__(self, other):
      if not isinstance(other,Point2D) and not isinstance(other,Polygon2D):
            raise TypeError, ErrorMessages[TypeError]
      if isinstance(other,Point2D):
         self.Polygon.append(Point2D(other.X, other.Y))
      else:
         for point in other:
            self.Polygon.append(Point2D(point.X, point.Y))


#
#      METHOD:
#         AddPoint
#
#      PURPOSE:
#          Add a point at the end of the polygon
#
#      INPUT:
#          Parameters:
#          nextp        Point2D         The next point of the polygon
#
#      RESULT:
#          The polygon will be updated
#

   def AddPoint(self, nextp):
      if not isinstance(nextp,Point2D):
         raise TypeError, ErrorMessages[TypeError]
      point = Point2D(nextp.X,nextp.Y)
      self.Polygon.append(point)

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetPolygon(self): return self.__Polygon
   def SetPolygon(self,value):
      if type(value) != type([]):
         raise TypeError, ErrorMessages[TypeError]
      points = []
      for point in value:
         if not isinstance(point,Point2D):
            raise TypeError, ErrorMessages[TypeError]
         points.append(Point2D(point.X,point.Y))
      self.__Polygon = points
   Polygon = property (GetPolygon, SetPolygon)
