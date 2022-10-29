## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsBox.py
#
#      PURPOSE:
#          The class holds information about a box (parallelepiped).
#          The box consists of a length, a height, a width,
#          an origin and two directions. The first direction is along the "length" axis,
#          the second direction is along the "height" axis (perpendicular to the "length" axis.
#          The direction of the "width" axis is implicit defined as the right normal of the
#          "length"-"height" plane.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Origin              Point3D       The origin
#          LengthDir           Vector3D      The direction of "length" axis
#          HeightDir           Vector3D      The direction of the "height" axis
#                                            (perpendicular to the "length" axis)
#          Length              real          The length
#          Height              real          The height
#          Width               real          The width

from KcsPoint3D import Point3D
from KcsVector3D import Vector3D

import types
import copy
import string

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Box class',
                  ValueError: 'wrong points, see documentationo of Box class' }

class Box(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          origin              The origin
#          lengthDir           The length direction
#          heightDir           The height direction
#          length              The length
#          height              The height (default length)
#          width               The width (default height)

   def __init__(self, origin = Point3D(0,0,0), lengthDir = Vector3D( 0,0,1 ),
                      heightDir = Vector3D(0,1,0), length = 0, height = 0, width = 0):
      self.Origin    = origin
      self.LengthDir = lengthDir
      self.HeightDir = heightDir
      self.Length    = length
      self.Height    = height
      self.Width     = width


#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      tup = (
            'Box:',
            '   origin   :' + str(self.Origin),
            '   lengthDir:' + str(self.LengthDir),
            '   heightDir:' + str(self.HeightDir),
            '   length   :' + str(self.Length),
            '   height   :' + str(self.Height),
            '   width    :' + str(self.Width))
      return string.join (tup, '\n')

#
#      METHOD:
#          SetAxisParallelBox
#
#      PURPOSE:
#          It will create axis parallel box. Height direction is parallel to Y axis and Length direction is parallel to Z axis.
#
#      INPUT:
#          Parameters:
#          p1                  Point3D       lower-left (min z) corner of box
#          p2                  Point3D       upper-right (max z) corner of box
#              or
#          x1, y1, z1          reals         lower-left (min z) corner of box
#          x2, y2, z2          reals         upper-right (max z) corner of box


   def SetAxisParallelBox(self, *args):
      if len(args) == 2:
         p1 = args[0]
         p2 = args[1]
         if not isinstance(p1, Point3D) or not isinstance(p2, Point3D):
            raise TypeError, ErrorMessages[TypeError]
      elif len(args) == 6:
         p1 = Point3D(args[0], args[1], args[2])
         p2 = Point3D(args[3], args[4], args[5])
      else:
         raise TypeError, ErrorMessages[TypeError]

      self.Width = p2.X - p1.X
      self.Height = p2.Y - p1.Y
      self.Length = p2.Z - p1.Z
      self.HeightDir.SetComponents(0, 1, 0)
      self.LengthDir.SetComponents(0, 0, 1)
      self.Origin = copy.deepcopy(p1)

   def IsEmpty(self):
      if self.Height == 0.0 and self.Width == 0.0 and self.Length == 0.0:
         return 1
      else:
         return 0

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetOrigin(self): return self.__Origin
   def SetOrigin(self,point):
      if not isinstance(point, Point3D):
         raise TypeError, ErrorMessages[TypeError]
      self.__Origin = Point3D(point.X,point.Y,point.Z)
   Origin = property (GetOrigin, SetOrigin, None, 'Origin - box origin')

   def GetLengthDir(self):
      if self.__LengthDir != None:
         return self.__LengthDir
      else:
         vec = Vector3D()
         vec.SetFromCrossProduct( self.WidthDir, self.HeightDir )
         return vec
   def SetLengthDir(self, vector):
      if not isinstance(vector, Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      self.__LengthDir = Vector3D(vector.X,vector.Y,vector.Z)
      self.__WidthDir = None
   LengthDir = property (GetLengthDir, SetLengthDir, None, 'LengthDir - the length direction vector')

   def GetHeightDir(self): return self.__HeightDir
   def SetHeightDir(self, vector):
      if not isinstance(vector, Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      self.__HeightDir = Vector3D(vector.X,vector.Y,vector.Z)
   HeightDir = property (GetHeightDir, SetHeightDir, None, 'HeightDir - the height direction vector')

   def GetWidthDir(self):
      if self.__WidthDir != None:
         return self.__WidthDir
      else:
         vec = Vector3D()
         vec.SetFromCrossProduct( self.HeightDir, self.LengthDir )
         return vec

   def SetWidthDir(self, vector):
      if not isinstance(vector, Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      self.__WidthDir = Vector3D(vector.X,vector.Y,vector.Z)
      self.__LengthDir = None
   WidthDir = property (GetWidthDir, SetWidthDir, None, 'WidthDir - the width direction vector')

   def GetLength(self): return self.__Length
   def SetLength(self, value):
      if type(value) not in [types.IntType,types.LongType,types.FloatType]:
         raise TypeError, ErrorMessages[TypeError]
      self.__Length = value + 0.0
   Length = property (GetLength, SetLength, None, 'Length - box length')

   def GetHeight(self): return self.__Height
   def SetHeight(self, value):
      if type(value) not in [types.IntType,types.LongType,types.FloatType]:
         raise TypeError, ErrorMessages[TypeError]
      self.__Height = value + 0.0
   Height = property (GetHeight, SetHeight, None, 'Height - box height')

   def GetWidth(self): return self.__Width
   def SetWidth(self, value):
      if type(value) not in [types.IntType,types.LongType,types.FloatType]:
         raise TypeError, ErrorMessages[TypeError]
      self.__Width = value + 0.0
   Width = property (GetWidth, SetWidth, None, 'Width - box width')
