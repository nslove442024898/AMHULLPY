## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsGencylinder.py
#
#      PURPOSE:
#          The class holds information about a general cylinder. The general
#          cylinder consists of an origin, a direction, a length and a cross-section.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Origin         Point3D      The origin
#          Direction      Vector3D     The direction
#          Length         real         The length
#          CrossSection   Contour2D    The cross-section. The origin of this contour will
#                                      coincide with the origin of the general cylinder.
import KcsPoint3D
from KcsPoint3D import Point3D
import KcsVector3D
from KcsVector3D import Vector3D
import KcsContour2D
from KcsContour2D import Contour2D
import string
import copy
import types

class Gencylinder(object):

     __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Gencylinder class',
                       ValueError: 'not supported value, see documentation of Gencylinder class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          orig           The origin
#          dir            The direction
#          len            The length
#          crossSect     The cross section

     def __init__(self, orig, dir, len, crossSect):
        self.Origin = Point3D(orig.X,orig.Y,orig.Z)
        self.Direction = Vector3D(dir.X,dir.Y,dir.Z)
        self.Length = len
        self.CrossSection = crossSect

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
      tup = (
        'Gencylinder:',
        '   origin      : ' + str(self.Origin),
        '   direction   : ' + str(self.Direction),
        '   length      : ' + str(self.Length),
        '   crossSection: ' + str(self.CrossSection))
      return string.join (tup, '\n')

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
     def GetOrigin(self): return self.__Origin
     def SetOrigin(self,value):
        if not (isinstance(value,Point3D) or isinstance(value,KcsPoint3D.Point3D)):
           raise TypeError, Gencylinder.__ErrorMessages[TypeError]
        self.__Origin = Point3D(value.X,value.Y,value.Z)
     Origin = property (GetOrigin, SetOrigin, None, 'Origin - cylinder origin point')

     def GetDirection(self): return self.__Direction
     def SetDirection(self,value):
        if not (isinstance(value,Vector3D) or isinstance(value,KcsVector3D.Vector3D)):
           raise TypeError, Gencylinder.__ErrorMessages[TypeError]
        self.__Direction = Vector3D(value.X,value.Y,value.Z)
     Direction = property (GetDirection, SetDirection, None, 'Direction - cylinder direction vector')

     def GetLength(self): return self.__Length
     def SetLength(self,value):
        if not type(value) in [types.LongType, types.IntType, types.FloatType]:
           raise TypeError, Gencylinder.__ErrorMessages[TypeError]
        self.__Length = value
     Length = property (GetLength, SetLength, None, 'Length - cylinder length value')

     def GetCrossSection(self): return self.__CrossSection
     def SetCrossSection(self,value):
        if not (isinstance(value,Contour2D) or isinstance(value,KcsContour2D.Contour2D)):
           raise TypeError, Gencylinder.__ErrorMessages[TypeError]
        self.__CrossSection = copy.deepcopy(value)
     CrossSection = property (GetCrossSection, SetCrossSection, None, \
                              'CrossSection - contour, its origin will coincide with the origin of the cylinder')
