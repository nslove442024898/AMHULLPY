## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPanHoleOptions.py
#
#      PURPOSE:
#
#          To hold options for Pan Hole objects.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import string
import types
import KcsPoint3D
import KcsVector3D

class PanHoleOptions(object):

   X_AXIS     =  1
   Y_AXIS     =  2
   Z_AXIS     =  3

   UNDEF      = -1

#-----------------------------------------------------------------------
# Hole symmetry Option constants
#
# SYMM_AS_PANEL - Symmetry of hole is the same as panel symmetry (default)
# SYMM_PS       - The hole is on the portside side only (valid for symmetric panels)
# SYMM_SB       - The hole is on the starboard side only (valid for symmetric panels)
#-----------------------------------------------------------------------
   SYMM_AS_PANEL        = 0
   SYMM_PS              = 1
   SYMM_SB              = 12


#-----------------------------------------------------------------------
# Marking Option constants
#
# MARK_HOLE  - Only the hole should be marked
# MARK_CROSS - Only the hole should be marked
# MARK_HOLE  - Only the hole should be marked
#-----------------------------------------------------------------------
   MARK_HOLE        = 0
   MARK_CROSS       = 1
   MARK_BOTH        = 2


#-----------------------------------------------------------------------
# Mark Type constants - Controls the shape of the cross
#
# CROSS_BIG     - "Big" cross over the hole
# CROSS_SMALL   - "Small" cross inside the hole
# CROSS_SPECIAL -  Special marking, shape of a "4".
#-----------------------------------------------------------------------
   CROSS_BIG         = 0
   CROSS_SMALL       = 1
   CROSS_SPECIAL     = 2

#-----------------------------------------------------------------------
# Errors
#-----------------------------------------------------------------------

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of PanHoleOptions class',
                      ValueError: 'not supported value, see documentation of PanHoleOptions class' }

#-----------------------------------------------------------------------

   def __init__(self):
      'inits PanHoleOptions'

#-----------------------------------------------------------------------
#     Hole type, standard hole or name of the curve
#-----------------------------------------------------------------------
      self.__Designation                     = ''

#-----------------------------------------------------------------------
#     Origin of the hole. It is recommended to us the method 'SetOriginAlongLine',
#     'SetOriginAlongAxis' and 'SetOriginAsStored' to set these atributes.
#-----------------------------------------------------------------------
      self.__Axis                            = self.UNDEF
      self.__HasApprox                       = 0
      self.__Pt1                             = KcsPoint3D.Point3D(0,0,0)
      self.__Pt2                             = KcsPoint3D.Point3D(0,0,0)
      self.__AsStored                        = 0

#-----------------------------------------------------------------------
#     Orientaion of the hole (in case of symmetric hole)
#-----------------------------------------------------------------------
      self.__Rotation                        = KcsPoint3D.Point3D(0,0,0)

#-----------------------------------------------------------------------
#     Other hole properties.
#-----------------------------------------------------------------------
      self.__Develop                         = 0
      self.__BurnOption                      = 1
      self.__MarkOption                      = self.MARK_HOLE
      self.__MarkType                        = self.CROSS_BIG
      self.__MarkLen                         = 100.0
      self.__WCOGFictive                     = 0
      self.__Symm                            = self.SYMM_AS_PANEL

#-----------------------------------------------------------------------
#     Set Methods
#-----------------------------------------------------------------------

#-----------------------------------------------------------------------
#
#     SetOriginAlongLine:
#
#     Defines the origin of a hole in a curved panel, when defined "along line".
#     The line is an restricted line and defined by a start point and an
#     end point. The origin of the hole will be the intersection point between this
#     line and the curved panel.
#
#
#      INPUT:
#
#      Parameters:
#
#		 Pt1             The start point of the line
#
#		 Pt2             The coordinates values
#
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
#       Marking properties.
#-----------------------------------------------------------------------
   def SetOriginAlongLine(self, Pt1, Pt2 ):
      'Defines the origin of a hole in a curved panel, when defined along line limited by two end points'

      if not isinstance(Pt1, KcsPoint3D.Point3D) or not isinstance(Pt2, KcsPoint3D.Point3D):
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Pt1 = Pt1
      self.__Pt2 = Pt2
      self.__Axis = self.UNDEF
      self.__AsStored = 0


#-----------------------------------------------------------------------
#
#      SetOriginAlongAxis:
#
#      Defines the origin of a hole in a curved panel, when defined "along axis".
#      The line is defined by two coordinate values and will thus be parallel to one
#      of the coordinate axes.
#
#
#      INPUT:
#
#      Parameters:
#
#		 Axis            Selects the "parallel" axis. Possible values are:
#                      1 - X-axis
#                      2 - Y-axis
#                      3 - Z-axis
#
#                      If Axis = 1 then Y and Z coordinates should be given in Pt1
#                      If Axis = 2 then X and Z coordinates should be given in Pt1
#                      If Axis = 3 then X and Y coordinates should be given in Pt1
#
#		 Pt1             The coordinates values
#
#      HasApprox       In case of multiple intersection point an approximate coordinate
#                      may be supplied as the thrid coordinate value of Pt1.
#
#                      0 - No approximate coordinate value is given in Pt1
#                      1 - approximate Coordinate value is given in Pt1
#
#-----------------------------------------------------------------------

   def SetOriginAlongAxis(self, Axis, Pt1, HasApprox):
      'Defines the origin of a hole in a curved panel, when defined along an infinite line parallel to a coordinate axis'
      print "SetOriginAlongAxis in class 1"
      if not isinstance(Pt1, KcsPoint3D.Point3D):
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Pt1 = Pt1
      if Axis != 1 and Axis != 2 and Axis != 3:
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Axis = Axis
      print "Axis = ",
      print self.__Axis
      if HasApprox != 0:
         self.__HasApprox = 1
      else:
         self.__HasApprox = 0
      self.__AsStored = 0
      self.__Pt2 = KcsPoint3D.Point3D(0,0,0)

#-----------------------------------------------------------------------
#
#     SetOriginAsStored:
#
#     Defines the origin of a hole "as stored". This is used when the hole is created from
#     an existing contour which has a transformation. The contour will be projected
#     into the curved panel along the normal of the  plane in which the countour is defined.
#
#     In case of multiple intersection an approximate coordnate may be given.
#
#
#      INPUT:
#
#      Parameters:
#
#		 Axis            Integer              Coordinate axis
#
#		 Pt1             KcsPoint3D           The coordinates value
#
#-----------------------------------------------------------------------

   def SetOriginAsStored(self, Axis, Pt1):
      'Defines the origin of a hole in a curved panel'
      if not isinstance(Pt1, KcsPoint3D.Point3D):
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      if Axis != 1 and Axis != 2 and Axis != 3:
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Axis = Axis
      self.__AsStored = 1
      self.__Pt1 = Pt1
      self.__Pt2 = KcsPoint3D.Point3D(0,0,0)

#-----------------------------------------------------------------------
#
#     SetDirection:
#
#      In case of an asymmetrical hole, this selects the direction of the
#      U-axis of the hole.
#
#      "Dir" is either a vector or a point. Interpreted as a vector if
#      the length <= 1.0 If dir is a point the system will form a vector from
#      origin the the point. The vector will then be projected into the tangent
#      plane of the panel ( in the origin of the hole ).#     Defines the origin of a hole "as stored". This is used when the hole is created from
#      an existing contour which has a transformation. The contour will be projected
#      into the curved panel along the normal of the  plane in which the countour is defined.
#
#
#      INPUT:
#
#      Parameters:
#
#		 Dir             Coordinates for the vector/point
#
#
#-----------------------------------------------------------------------

   def SetDirection(self, Dir):
      'Defines the direction'
      print "Dir = ",
      print Dir
      if not isinstance(Dir, KcsPoint3D.Point3D) and not isinstance(Dir, KcsVector3D.Vector3D):
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Rotation = Dir

#-----------------------------------------------------------------------
   def SetDesign(self, HoleDes):
      'Defines the design'
      if type(HoleDes) != type(''):
         raise TypeError, PanHoleOptions.__ErrorMessages[TypeError]
      self.__Designation = HoleDes

#-----------------------------------------------------------------------
   def SetDevelop(self, DevOption):
      'Defines Develop option'
      self.__Develop = DevOption

#-----------------------------------------------------------------------
   def SetBurnOption(self, BurnOption):
      'Defines Burn option'
      self.__BurnOption = BurnOption

#-----------------------------------------------------------------------
   def SetMarkOption(self, MarkOption):
      'Defines MarkOption'
      self.__MarkOption = MarkOption

#-----------------------------------------------------------------------
   def SetMarkType(self, MarkType):
      'Defines MarkType'
      self.__MarkType = MarkType

#-----------------------------------------------------------------------
   def SetMarkLen(self, MarkLen):
      'Defines Marking length'
      self.__MarkLen = MarkLen

#-----------------------------------------------------------------------
   def SetWCOGFictive(self, WCOGFictive):
      'Defines WCOG option for marked hole'
      self.__WCOGFictive = WCOGFictive

#-----------------------------------------------------------------------
   def SetSymmetry(self, SymmCode):
      'Defines the symmetry options'
      self.__Symm = SymmCode

#-----------------------------------------------------------------------
#        Get Methods
#-----------------------------------------------------------------------
   def IsOriginAlongAxis(self):
      'Returns 1 if the origin is defined along axis, otherwise 0'
      if self.__AsStored == 0 and self.__Axis > 0:
         Flag = 1
      else:
         Flag = 0
      return (Flag)
#-----------------------------------------------------------------------
   def IsOriginAlongLine(self):
      'Returns 1 if the origin is defined along line, otherwise 0'
      if self.__AsStored == 0 and self.__Axis == self.UNDEF:
         Flag = 1
      else:
         Flag = 0
      return (Flag)
#-----------------------------------------------------------------------
   def IsOriginAsStored(self):
      'Returns 1 if the origin is defined along as stored, otherwise 0'
      if self.__AsStored == 1 and self.__Axis != self.UNDEF:
         Flag = 1
      else:
         Flag = 0
      return (Flag)

#-----------------------------------------------------------------------
   def GetOriginAlongLine(self):
      'Gets the origin of a hole in a curved panel, when defined along line'
      return[self.__Pt1,self.__Pt2]
#-----------------------------------------------------------------------
   def GetOriginAlongAxis(self):
      'Gets the origin of a hole in a curved panel, when defined along axis'
      return[self.__Axis, self.__Pt1, self.__HasApprox, ]
#-----------------------------------------------------------------------
   def GetOriginAsStored(self):
      'Gets the origin of a hole in a curved panel'
      return[self.__Axis, self.__Pt1]
#-----------------------------------------------------------------------
   def GetDirection(self):
      'Gets Direction'
      return (self.__Rotation)
#-----------------------------------------------------------------------
   def GetDesign(self):
      'Gets Design'
      return (self.__Designation)
#-----------------------------------------------------------------------
   def GetDevelop(self):
      'Gets Develop Flag'
      return (self.__Develop)
#-----------------------------------------------------------------------
   def GetBurnOption(self):
      'Gets BurnOption'
      return (self.__BurnOption)
#-----------------------------------------------------------------------
   def GetMarkOption(self):
      'Gets MarkOption'
      return (self.__MarkOption)
#-----------------------------------------------------------------------
   def GetMarkType(self):
      'Gets MarkType'
      return (self.__MarkType)
#-----------------------------------------------------------------------
   def GetMarkLen(self):
      'Gets Marking length'
      return (self.__MarkLen)
#-----------------------------------------------------------------------
   def GetWCOGFictive(self):
      'Gets WCOG option for marked hole'
      return (self.__WCOGFictive)
#-----------------------------------------------------------------------
   def GetSymmetry(self):
      'Gets the symmetry option'
      return self.__Symm

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Rotation = property (GetDirection, SetDirection, None, '')
   Designation = property (GetDesign, SetDesign, None, '')
   Develop = property (GetDevelop , SetDevelop, None, '')
   BurnOption = property (GetBurnOption , SetBurnOption, None, '')
   MarkOption = property (GetMarkOption , SetMarkOption, None, '')
   MarkType = property (GetMarkType , SetMarkType, None, '')
   MarkLen = property (GetMarkLen , SetMarkLen, None, '')
   WCOGFictive = property (GetWCOGFictive , SetWCOGFictive, None, '')
   Symmetry = property (GetSymmetry , SetSymmetry, None, '')

   def GetAxis(self): return self.__Axis
   Axis  = property (GetAxis)

   def GetHasApprox(self): return self.__HasApprox
   HasApprox = property(GetHasApprox)
   def GetPt1(self): return self.__Pt1
   Pt1 = property (GetPt1)
   def GetPt2(self): return self.__Pt2
   Pt2 = property (GetPt2)
   def GetAsStored(self): return self.__AsStored
   AsStored = property (GetAsStored)
