## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPlane3D.py
#
#      PURPOSE:
#          The unlimited plane is defined by a point and a normal,
#          perpendicular to the plane
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Point     Point3D     A point on the plane
#          Normal    Vector3D    A vector, perpendicular to plane
#


from KcsPoint3D import Point3D
import KcsPoint3D
import KcsVector3D
import KcsTransformation3D
import math


ErrorMessages = { TypeError : 'not supported argument type, see documentation of Plane3D class' }

class Plane3D(object):

#--------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          pnt        Point3D       3D point in the plane
#          norm       Vector3D      3D vector indication normal to plane

     def __init__(self, pnt, norm):
        self.Point  = pnt
        self.Normal = norm

#--------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Plane point: %s normal: %s' % (self.Point, self.Normal)

#--------------------------------------------------------------------
#
#      METHOD:
#          IntersectLine
#
#      PURPOSE:
#          Intersect the plane with a line
#
#      INPUT:
#          Parameters:
#          line      Line3D    The line to intersect the plane with
#
#          Reference: xa011
#
#
#      RESULT:
#          Parameters:
#          point     Point3D    The point will be updated with the result
#
#          Returns:
#          integer        If an intersection is found the function resturns 0,
#                         otherwise -1

     def IntersectLine(self, line, point):
        from KcsVector3D import Vector3D
        from KcsLine3D import Line3D
        res = -1
        U = Vector3D(line.Direction.X, line.Direction.Y, line.Direction.Z)
        U.SetToUnitVector()
        V = Vector3D(self.Normal.X, self.Normal.Y, self.Normal.Z)
        V.SetToUnitVector()
        S = U.DotProduct(V)

#       Check if line is parallell to plane

        if S >= 1.0E-6 or S <= -1.0E-6:
           V.SetFromPoints(line.Point, self.Point)
           line_normal = Line3D(self.Point, self.Normal)
           S = V.ScalarComponentOnLine(line_normal) / S
           point.X = line.Point.X + (S*U.X)
           point.Y = line.Point.Y + (S*U.Y)
           point.Z = line.Point.Z + (S*U.Z)
           res = 0
        return(res)

#--------------------------------------------------------------------
#
#      METHOD:
#          Transform
#
#      PURPOSE:
#          Transform the plane using a transformation matrix
#          self will be updated with the result
#
#      INPUT:
#          Parameters:
#          tra      Transformation3D        The transformation matrix

     def Transform(self, tra):
        from KcsTransformation3D import Transformation3D
        if not (isinstance(tra,Transformation3D) or isinstance(tra,KcsTransformation3D.Transformation3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.Point.Transform(tra)
        self.Normal.Transform(tra)

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
     def GetPoint(self): return self.__Point
     def SetPoint(self, value):
        if not (isinstance(value, Point3D) or isinstance(value,KcsPoint3D.Point3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Point = Point3D(value.X,value.Y,value.Z)
     def GetNormal(self): return self.__Normal
     def SetNormal(self, value):
        from KcsVector3D import Vector3D
        if not (isinstance(value, Vector3D) or isinstance(value,KcsVector3D.Vector3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Normal = Vector3D(value.X,value.Y,value.Z)
     Point = property (GetPoint, SetPoint)
     Normal = property (GetNormal, SetNormal)
