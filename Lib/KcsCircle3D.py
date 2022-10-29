## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsCircle3D.py
#
#      PURPOSE:
#          The Circle3D class holds information about a 3D circle. The circle
#          consists of a centre point and a radius
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Centre         Point3D       The centre point
#          Radius         real          The radius

import math
import types
from KcsPoint3D import Point3D
import KcsVector3D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Point2D class' }
#ParamLimit = { ParamLimit : "Parameter contains invalid value" }

class Circle3D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          inpoint         the centre point
#          rad             The radius of the circle

     def __init__(self, inpoint, normal, rad):
        if not isinstance(inpoint,Point3D) or not isinstance(normal,KcsVector3D.Vector3D):
           raise TypeError, ErrorMessages[TypeError]
        if not type(rad) in (types.IntType, types.LongType, types.FloatType):
           raise TypeError, ErrorMessages[TypeError]
        self.Centre = Point3D(inpoint.X,inpoint.Y,inpoint.Z)
        self.Normal = KcsVector3D.Vector3D(normal.X,normal.Y,normal.Z)
        self.Radius = rad + 0.0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'My Circle Centre: %s Vector: %s Radius: %s' % (self.Centre, self.Normal, self.Radius)

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


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

     def getCentre(self): return self.__Centre
     def setCentre(self, point):
        if not isinstance(point, Point3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Centre = Point3D(point.X, point.Y, point.Z)
     Centre  = property (getCentre, setCentre, None, 'Centre - circle centre point')

     def getRadius(self): return self.__Radius
     def setRadius(self, value):
        if not type(value) in (types.IntType, types.LongType, types.FloatType):
           raise TypeError, ErrorMessages[TypeError]
        self.__Radius = value
     Radius  = property (getRadius, setRadius, None, 'Radius - circle radius')

     def getNormal(self): return self.__Normal
     def setNormal(self, vector):
        if not isinstance(vector, KcsVector3D.Vector3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Normal = KcsVector3D.Vector3D(vector.X, vector.Y, vector.Z)
     Normal  = property (getNormal, setNormal, None, 'Normal - circle plane vector')
