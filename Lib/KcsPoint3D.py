## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPoint3D.py
#
#      PURPOSE:
#          The Point3D class holds information about a 3D point
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          X              real          The X coordinate
#          Y              real          The Y coordinate
#          Z              real          The Z coordinate

import math
import types

class Point3D(object):
     ErrorMessages = { TypeError : 'not supported argument type, see documentation of Point3D class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          x              real          The X coordinate
#          y              real          The Y coordinate
#          z              real          The Z coordinate
#

     def __init__(self, x=0.0, y=0.0, z=0.0):
        self.X = x + 0.0
        self.Y = y + 0.0
        self.Z = z + 0.0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return '[X Y Z:%s,%s,%s]' % (self.X, self.Y, self.Z)


#
#      METHOD:
#          DistanceToPoint
#
#      PURPOSE:
#          calculate the distance between self and point p
#
#      INPUT:
#          Parameters:
#          p              Point3D       Point to calculate distance to
#
#      RESULT:
#          Returns:
#          real           The distance

     def DistanceToPoint(self, p):
        if not isinstance(p,Point3D):
           raise TypeError, self.ErrorMessages[TypeError]
        return (math.sqrt((self.X-p.X)*(self.X-p.X) + (self.Y-p.Y)*(self.Y-p.Y) + (self.Z-p.Z)*(self.Z-p.Z)))


#
#      METHOD:
#          Round
#
#      PURPOSE:
#          The coordinate values are rounded to given number of decimals
#
#      INPUT:
#          Parameters:
#          decimals       Numbers of decimales
#
#      RESULT:
#          The point will be updated
#

     def Round(self, decimals):
        if type(decimals) != types.IntType and type(decimals) != types.LongType:
           raise TypeError, self.ErrorMessages[TypeError]
        self.X =int(self.X * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
        self.Y =int(self.Y * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
        self.Z =int(self.Z * math.pow(10, decimals)+0.5) / math.pow(10, decimals)


#
#      METHOD:
#          SetCoordinates
#
#      PURPOSE:
#          Set the point from given coordinates
#
#      INPUT:
#          Parameters:
#          x              real          The X coordinate
#          y              real          The Y coordinate
#          z              real          The Z coordinate
#
#
#      RESULT:
#          The point will be updated
#

     def SetCoordinates(self, x, y, z):
        self.X = x + 0.0
        self.Y = y + 0.0
        self.Z = z + 0.0

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

        if not isinstance(other, Point3D):
           raise TypeError, self.ErrorMessages[TypeError]

        if self.X != other.X or self.Y != other.Y or self.Z != other.Z:
           return 1

        return 0

#
#      METHOD:
#          SetFromMidpoint
#
#      PURPOSE:
#          Set the point to be the midpoint between two other points
#
#      INPUT:
#          Parameters:
#          p1              Point3D       First point
#          p2              Point3D       Second point
#
#      RESULT:
#          The point will be updated
#

     def SetFromMidpoint(self, p1, p2):
         if not isinstance(p1,Point3D) or not isinstance(p2,Point3D):
            raise TypeError, self.ErrorMessages[TypeError]
         self.X = p1.X + (p2.X-p1.X)*0.5
         self.Y = p1.Y + (p2.Y-p1.Y)*0.5
         self.Z = p1.Z + (p2.Z-p1.Z)*0.5


#
#      METHOD:
#          SetFromPoint
#
#      PURPOSE:
#          Set the point with values from another point (copy)
#
#      INPUT:
#          Parameters:
#          p            Point3D       3D point to copy from
#
#      RESULT:
#          The point will be updated
#

     def SetFromPoint(self, p):
        if not isinstance(p,Point3D):
            raise TypeError, self.ErrorMessages[TypeError]
        self.X = p.X
        self.Y = p.Y
        self.Z = p.Z


#
#      METHOD:
#          Transform
#
#      PURPOSE:
#          Transform the point using a transformation matrix.
#          self will be updated with the result
#
#          reference XA750
#
#      INPUT:
#          Parameters:
#          tra            Transformation3D       The transformation matrix
#
#      RESULT:
#          The point will be updated
#

     def Transform(self, tra):
        from KcsTransformation3D import Transformation3D
        if not isinstance(tra,Transformation3D):
            raise TypeError, self.ErrorMessages[TypeError]
        proj = self.X*tra.matrix14 + self.Y*tra.matrix24 +self.Z*tra.matrix34 + tra.matrix44;
        if proj <= 1.0E-15 and proj >= -1.0E-15:
           proj = 1.0
        X = (self.X*tra.matrix11 + self.Y*tra.matrix21 + self.Z*tra.matrix31 + tra.matrix41)/proj
        Y = (self.X*tra.matrix12 + self.Y*tra.matrix22 + self.Z*tra.matrix32 + tra.matrix42)/proj
        Z = (self.X*tra.matrix13 + self.Y*tra.matrix23 + self.Z*tra.matrix33 + tra.matrix43)/proj
        self.X = X
        self.Y = Y
        self.Z = Z

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
     def GetZ(self): return self.__Z
     def SetZ(self,value):
        if type(value) != types.FloatType and type(value) != types.IntType and type(value) != types.LongType:
           raise TypeError, ErrorMessages[TypeError]
        self.__Z = value + 0.0
     X = property (GetX, SetX)
     Y = property (GetY, SetY)
     Z = property (GetZ, SetZ)
