## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsRline3D.py
#
#      PURPOSE:
#          The Rline3D class holds information about a restricted 3D line.
#          The restricted line consists of a start point and an end point.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Start        Point3D          The start point
#          End          Point3D          The end point

from KcsPoint3D import Point3D
import KcsPoint3D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Rline3D class'}

class Rline3D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          startp        Point3D        the start point
#          endp          Point3D        the end point

     def __init__(self, startp, endp):
        self.Start  = startp
        self.End = endp


#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Line Start: %s End: %s' % (self.Start, self.End)

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
     def GetStart(self): return self.__Start
     def SetStart(self,value):
        if not isinstance(value,Point3D) and not isinstance(value,KcsPoint3D.Point3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Start = Point3D(value.X, value.Y, value.Z)
     Start = property (GetStart, SetStart)

     def GetEnd(self): return self.__End
     def SetEnd(self,value):
        if not isinstance(value,Point3D) and not isinstance(value,KcsPoint3D.Point3D):
           raise TypeError, ErrorMessages[TypeError]
        self.__End = Point3D(value.X, value.Y, value.Z)
     End = property (GetEnd, SetEnd)
