## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsMovePanOptions.py
#
#      PURPOSE:
#          The class holds information about a Moving Panel Options
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES

import types
import KcsPoint3D
from KcsPoint3D import Point3D


class MovePanOptions(object):
   'class holds information about Moving Panel Options'

   PRINCIPAL_PLANE = 1
   THREE_POINTS    = 2
   PLANE_OBJECT    = 3
   X               = 1
   Y               = 2
   Z               = 3

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of MovePanOptions class',
                       IndexError: 'not supported index value, see documentation of MovePanOptions class',
                       ValueError: 'not supported value, see documentation of MovePanOptions class' }
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#

   def __init__(self):
      'to create instance of the class'

      self.__LocationType        = self.PRINCIPAL_PLANE
      self.__Coordinate          = self.X
      self.__RelativePosition    = 0
      self.__CoordinateValue     = ''
      self.__Origin              = KcsPoint3D.Point3D()
      self.__Uaxis               = KcsPoint3D.Point3D()
      self.__Vaxis               = KcsPoint3D.Point3D()
      self.__ObjectName          = ''

#---------------------------------------------------------------------
   def __repr__(self):
      'returns string representation of SymbolicView object'
      planetup = ()

      if self.Coordinate == self.X:
         strCoord = 'X'
      elif self.Coordinate == self.Y:
         strCoord = 'Y'
      elif self.Coordinate == self.Z:
         strCoord = 'Z'

      if self.LocationType == self.PRINCIPAL_PLANE:
         strType = 'PRINCIPAL_PLANE'
         planetup = (
            '   Coordinate: ' + strCoord,
            '   RelativePosition: ' + str(self.RelativePosition),
            '   CoordinateValue: ' + self.CoordinateValue,
            )
      elif self.LocationType == self.THREE_POINTS:
         strType = 'THREE_POINTS'
         planetup = (
            '   Origin: ' + str(self.Origin),
            '   Uaxis: ' + str(self.Uaxis),
            '   Vaxis: ' + str(self.Vaxis),
            )
      elif self.LocationType == self.PLANE_OBJECT:
         strType = 'PLANE_OBJECT'
         planetup = (
            '   ObjectName: ' + self.ObjectName,
            )

      tup = (
         'MovePanOptions:',
         '   LocationType: ' + strType,
         ) + planetup
      return string.join(tup, '\n')

#
#      METHOD:
#           SetPrincipalPlane
#
#      PURPOSE:
#          Sets Location as a Principal Plane

   def SetPrincipalPlane(self, cord, relpos, cordval):
      'sets PrincipalPlane Arguments'
      self.__LocationType = self.PRINCIPAL_PLANE
      if cord not in [self.X, self.Y, self.Z]:
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__Coordinate = cord
      if relpos:
         self.__RelativePosition     = 1
      else:
         self.__RelativePosition     = 0

      if type(cordval) != types.StringType:
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__CoordinateValue          = cordval

#-------------------------------------------------------------------

   def GetPrincipalPlane(self):
      'gets Principal Plane type, relative position and coordinate value'
      return   [self.__Coordinate, self.__RelativePosition, self.__CoordinateValue]

#-------------------------------------------------------------------

   def GetLocationType(self):
      'gets Location Type'
      return   self.__LocationType

#-------------------------------------------------------------------

#
#      METHOD:
#           SetThreePoints
#
#      PURPOSE:
#          Sets Location as a Three Points

   def SetThreePoints(self, origin, uaxis, vaxis):
      'sets Three Points Arguments'
      self.__LocationType             = self.THREE_POINTS
      if not (isinstance(origin, KcsPoint3D.Point3D) or isinstance(origin, Point3D)) \
         or not (isinstance(uaxis, KcsPoint3D.Point3D) or isinstance(uaxis, Point3D)) \
         or not (isinstance(vaxis, KcsPoint3D.Point3D) or isinstance(vaxis, Point3D)):
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__Origin.SetCoordinates(origin.X, origin.Y, origin.Z)
      self.__Uaxis.SetCoordinates(uaxis.X, uaxis.Y, uaxis.Z)
      self.__Vaxis.SetCoordinates(vaxis.X, vaxis.Y, vaxis.Z)

#-------------------------------------------------------------------

   def GetThreePoints(self):
      'gets Principal Plane defines by Three Points origin, Uaxis, Vaxis'
      return   [self.__Origin, self.__Uaxis, self.__Vaxis]

#-------------------------------------------------------------------

#
#      METHOD:
#           SetPlaneObject
#
#      PURPOSE:
#          Sets Location as PlaneObject

   def SetPlaneObject(self, name):
      'sets Plane Object Arguments'
      self.__LocationType             = self.PLANE_OBJECT
      if type(name) != types.StringType:
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__ObjectName             = name

#-------------------------------------------------------------------

   def GetPlaneObject(self):
      'gets Principal Plane defined by Plane Object Object Name'
      return   self.__ObjectName

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   def SetLocationType(self, value):
      if value not in (self.PLANE_OBJECT,self.PRINCIPAL_PLANE, self.THREE_POINTS):
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__LocationType = value
   LocationType        = property (GetLocationType, SetLocationType, None, 'LocationType')

   def GetCoordinate(self): return self.__Coordinate
   Coordinate          = property (GetCoordinate, None, None, 'Coordinate')

   def GetRelativePosition(self): return self.__RelativePosition
   RelativePosition    = property (GetRelativePosition, None, None, 'RelativePosition')

   def GetCoordinateValue(self): return self.__CoordinateValue
   CoordinateValue     = property (GetCoordinateValue, None, None, 'CoordinateValue')

   def GetOrigin(self): return self.__Origin
   Origin              = property (GetOrigin, None, None, 'Origin')

   def GetUaxis(self): return self.__Uaxis
   Uaxis               = property (GetUaxis, None, None, 'Uaxis')

   def GetVaxis(self): return self.__Vaxis
   Vaxis               = property (GetVaxis, None, None, 'Vaxis')

   def SetPlaneObjectOnly(self, value):
      if type(value) != types.StringType:
         raise TypeError, MovePanOptions.__ErrorMessages[TypeError]
      self.__ObjectName             = value
   ObjectName          = property (GetPlaneObject, SetPlaneObjectOnly, None, 'ObjectName')
