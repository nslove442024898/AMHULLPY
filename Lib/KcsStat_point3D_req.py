## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsStat_point3D_req.py
#
#      PURPOSE:
#          The Stat_point3D_req class holds information about some initial status when
#          defining a 3D point, using the "point3D_req" function.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Helpdef        integer       Help point defined?
#                                       0: No (default)
#                                       1: Yes
#          Helppnt        Point3D       The help point (if defined)
#          Lockstatic     integer       Initial lock protected?
#                                       0: No (default)
#                                       1: Yes
#          Locktype       integer       Type of lock:
#                                       = 0 No lock (default)
#                                       = 1 Lock plane
#                                       = 2 Lock line
#          Lockpnt        Point3D       A point through the plane/line (if lock)
#          Lockvec        Vector3D      A vector perpendicular to the plane /
#                                       parallel to the line (normalized) (if lock)
#          Initial3D      integer       The initial way of defining the 3D point:
#                                       = 1 Pick line (by indicating in a view)
#                                       = 2 Key in
#                                       = 3 Indicate event point (default)
#                                       = 4 Offset from current (the help point)
#          Initial2D      integer       The initial way of defining a 2D point (used by Pick line):
#                                       = 1   Key in (2D)
#                                       = 2   Cursor position (default)
#                                       = 3   End or node point
#                                       = 4   Existing point
#                                       = 5   Symbol connection
#                                       = 6   Auto point
#                                       = 7   Point on arc at angle
#                                       = 8   Arc centre
#                                       = 9   Point at distance along
#                                       = 10  Mid point
#                                       = 13  Intersecting point
#                                       = 20  Offset from current point
#                                       = 21  Closest segment point
#                                       = 22  Centre of gravity
#                                       = 23  Event point (2D)
import KcsPoint3D
import KcsVector3D
from KcsPoint3D import Point3D
from KcsVector3D import Vector3D
import string

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Stat_point3D_req class',
                  ValueError: 'wrong value for Point3D definition mode' }

class Stat_point3D_req(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          None
#

     def __init__(self):
        self.Helpdef = 0
        self.Helppnt = Point3D(0.0,0.0,0.0)

        self.Lockstatic = 0
        self.Locktype = 0
        self.Lockpnt = Point3D(0.0,0.0,0.0)
        self.Lockvec = Vector3D(1.0,0.0,0.0)

        self.Initial3D = 3
        self.Initial2D = 2

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
      tup = (
        'Stat_point3D_req:',
        '   Helpdef   : ' + str(self.Helpdef),
        '   Helppnt   : ' + str(self.Helppnt),
        '   Lockstatic: ' + str(self.Lockstatic),
        '   Locktype  : ' + str(self.Locktype),
        '   Lockpnt   : ' + str(self.Lockpnt),
        '   Lockvec   : ' + str(self.Lockvec),
        '   Initial3D : ' + str(self.Initial3D),
        '   Initial2D : ' + str(self.Initial2D))
      return string.join (tup, '\n')

#-----------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
     def GetHelpdef(self): return self.__Helpdef
     def GetHelppnt(self): return self.__Helppnt
     def GetLockstatic(self): return self.__Lockstatic
     def GetLocktype(self): return self.__Locktype
     def GetLockpnt(self): return self.__Lockpnt
     def GetLockvec(self): return self.__Lockvec
     def GetInitial3D(self): return self.__Initial3D
     def GetInitial2D(self): return self.__Initial2D

     def SetHelpdef(self,value):
        if value==None: self.__Helpdef=0
        if not isinstance(value,int):
           raise TypeError, ErrorMessages[TypeError]
        if value:
           self.__Helpdef = 1
        else:
           self.__Helpdef = 0
     def SetHelppnt(self,value):
        if not isinstance(value,Point3D) and not isinstance(value,KcsPoint3D.Point3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Helppnt = Point3D(value.X,value.Y,value.Z)
     def SetLockstatic(self,value):
        if value==None: self.__Lockstatic=0
        if not isinstance(value,int):
           raise TypeError, ErrorMessages[TypeError]
        if value:
           self.__Lockstatic = 1
        else:
           self.__Lockstatic = 0
     def SetLocktype(self,value):
        if value==None: self.__Locktype=0
        if not isinstance(value,int):
           raise TypeError, ErrorMessages[TypeError]
        if value>=0 and value<3:
           self.__Locktype = value
     def SetLockpnt(self,value):
        if not isinstance(value,Point3D) and not isinstance(value,KcsPoint3D.Point3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Lockpnt = Point3D(value.X,value.Y,value.Z)
     def SetLockvec(self,value):
        if not isinstance(value,Vector3D) and not isinstance(value,KcsVector3D.Vector3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Lockvec = Vector3D(value.X,value.Y,value.Z)
     def SetInitial3D(self,value):
        if not isinstance(value,int):
           raise TypeError, ErrorMessages[TypeError]
        if value>0 and value<5:
           self.__Initial3D = value
     def SetInitial2D(self,value):
        if not isinstance(value,int):
           raise TypeError, ErrorMessages[TypeError]
        if value>0 and value<24:
           self.__Initial2D = value

     Helpdef = property (GetHelpdef, SetHelpdef)
     Helppnt = property (GetHelppnt, SetHelppnt)
     Lockstatic = property (GetLockstatic , SetLockstatic)
     Locktype = property (GetLocktype , SetLocktype)
     Lockpnt = property (GetLockpnt , SetLockpnt)
     Lockvec = property (GetLockvec , SetLockvec)
     Initial3D = property (GetInitial3D , SetInitial3D)
     Initial2D = property (GetInitial2D , SetInitial2D)
