## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsPolygon3D.py
#
#      PURPOSE:
#          This class holds information about a 3D polygon.
#          The polygon consists of a list of points.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Polygon              [point]         list of points
#          point                Point3D         a 3D point

from KcsPoint3D import Point3D
import KcsPoint3D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Polygon3D class' }

class Polygon3D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          startp         Point3D    The start point

   def __init__(self, startp):
      if not isinstance(startp,Point3D) and not isinstance(startp,KcsPoint3D.Point3D):
         raise TypeError, ErrorMessages[TypeError]
      point = Point3D(startp.X,startp.Y,startp.Z)
      self.Polygon = [point]

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Polygon3D: %s' % self.Polygon


#
#      METHOD:
#          AddPoint
#
#      PURPOSE:
#          To add a point to the polygon
#
#      INPUT:
#          Parameters:
#          nextp         Point3D    Next point of the polygon

   def AddPoint(self, nextp):
      if not isinstance(nextp,Point3D) and not isinstance(nextp,KcsPoint3D.Point3D):
         raise TypeError, ErrorMessages[TypeError]
      point = Point3D(nextp.X,nextp.Y,nextp.Z)
      self.Polygon.append(point)

#
#      METHOD:
#          GetNoOfPoints
#
#      PURPOSE:
#          To retrieve number of points of polygon
#
#      INPUT:
#          Parameters:
#          None

   def GetNoOfPoints(self):
      return len(self.Polygon)

#
#      METHOD:
#          GetPoint
#
#      PURPOSE:
#          To retrieve point at specific index
#
#      INPUT:
#          Parameters:
#          index             integer          0 base index of point to retrieve

   def GetPoint(self, index):
      if not isinstance(index,int):
         raise TypeError, ErrorMessages[TypeError]
      if index>=0 and index<len(self.Polygon):
         return self.Polygon[index]

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
         if not isinstance(point,Point3D) and not isinstance(point,KcsPoint3D.Point3D):
            raise TypeError, ErrorMessages[TypeError]
         points.append(Point3D(point.X,point.Y,point.Z))
      self.__Polygon = points
   Polygon = property (GetPolygon, SetPolygon)
