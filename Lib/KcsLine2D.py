## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsLine2D.py
#
#      PURPOSE:
#          The 2D line class is a representation of a unlimited line
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Point          Point2D       A point on the line
#          Direction      Vector2D      A vector along the line
import KcsPoint2D
from KcsPoint2D import Point2D
import KcsVector2D
from KcsVector2D import Vector2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Line2D class' }

class Line2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          pnt        Point2D       2D point on the line
#          dir        Vector2D      2D vector along the line

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
#          Name
#
#      PURPOSE:
#          To get the name of this objects class
#
#      INPUT:
#          Parameters:
#          none

     def Name(self):
        return self.__class__.__name__

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
#          vec       Vector2D   The vector to be projected on line self
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
#          Orthogonal projection of a 2D vector on the line. The result is
#          a 2D vector.
#
#          reference XB016
#
#      INPUT:
#          Parameters:
#          invec     Vector2D   The vector to be projected on line self
#
#      RESULT:
#          Parameters:
#          resvec    Vector2D   The resulting vector


     def VectorComponentOfVector(self, invec, resvec):
        scalar = self.ScalarComponentOfVector(invec)
        if (scalar <= 1.0E-15):
           resvec.SetComponents(0.0, 0.0)
        else:
           resvec.SetFromVector(self.Direction)
           resvec.SetToUnitVector()
           resvec.BlankProduct(scalar)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

     def GetPoint(self): return self.__Point
     def SetPoint(self,value):
        if not (isinstance(value,Point2D) or isinstance(value,KcsPoint2D.Point2D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Point = Point2D(value.X,value.Y)
     Point = property (GetPoint, SetPoint, None, 'Point - 2D point on the line')

     def GetDirection(self): return self.__Direction
     def SetDirection(self,value):
        if not (isinstance(value,Vector2D) or isinstance(value,KcsVector2D.Vector2D)):
           raise TypeError, ErrorMessages[TypeError]
        self.__Direction = Vector2D(value.X,value.Y)
     Direction = property (GetDirection, SetDirection, None, 'Direction - 2D vector along the line')
