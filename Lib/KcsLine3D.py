## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsLine3D.py
#
#      PURPOSE:
#          The 3D line class is a representation of a unlimited line
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Point          Point3D       A point on the line
#          Direction      Vector3D      A vector along the line

import KcsPoint3D
import KcsTransformation3D
from KcsPoint3D import Point3D
import KcsVector3D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Line3D class' }

class Line3D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          pnt        Point3D       3D point on the line
#          dir        Vector3D      3D vector along the line

     def __init__(self, pnt, dir):
        self.Point  = pnt
        self.Direction = dir

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Line point: %s direction: %s' % (self.Point, self.Direction)


#
#      METHOD:
#          ScalarComponentOfVector
#
#      PURPOSE:
#          Orthogonal scalar projection of a vector on the line
#
#          reference XB015
#
#      INPUT:
#          Parameters:
#          vec       Vector3D   The vector to be projected on line self
#
#      RESULT:
#          Returns:
#          real           The scalar component (with sign)

     def ScalarComponentOfVector(self, vec):
        len = self.Direction.Length()
        if (len <= 1.0E-15):
           return(0.0)
        else:
           return(self.Direction.DotProduct(vec) / len)


#
#      METHOD:
#          VectorComponentOfVector
#
#      PURPOSE:
#          Orthogonal projection of a 3D vector on the line. The result is
#          a 3D vector.
#
#          reference XB016
#
#      INPUT:
#          Parameters:
#          invec     Vector3D   The vector to be projected on line self
#
#      RESULT:
#          Parameters:
#          resvec    Vector3D   The resulting vector


     def VectorComponentOfVector(self, invec, resvec):
        scalar = self.ScalarComponentOfVector(invec)
        if (scalar <= 1.0E-15):
           resvec.SetCoordinates(0.0, 0.0, 0.0)
        else:
           resvec.SetFromVector(self.Direction)
           resvec.SetToUnitVector()
           resvec.BlankProduct(scalar)

#
#      METHOD:
#          Transform
#
#      PURPOSE:
#          Transform the line using a transformation matrix.
#          self will be updated with the result
#
#      INPUT:
#          Parameters:
#          M              Transformation3D      The transformation matrix
#
#      RESULT:
#          The line will be updated
#

     def Transform(self, M):
        from KcsTransformation3D import Transformation3D
        if not (isinstance(M,Transformation3D) or isinstance(M,KcsTransformation3D.Transformation3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.Point.Transform(M)
        self.Direction.Transform(M)

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

     def GetPoint(self): return self.__Point
     def SetPoint(self,value):
        if not (isinstance(value,Point3D) or isinstance(value,KcsPoint3D.Point3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Point = Point3D(value.X,value.Y,value.Z)
     Point = property (GetPoint, SetPoint, None, 'Point - 3D point on the line')

     def GetDirection(self): return self.__Direction
     def SetDirection(self,value):
        from KcsVector3D import Vector3D
        if not (isinstance(value,Vector3D) or isinstance(value,KcsVector3D.Vector3D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Direction = Vector3D(value.X,value.Y,value.Z)
     Direction = property (GetDirection, SetDirection, None, 'Direction - 3D vector along the line')
