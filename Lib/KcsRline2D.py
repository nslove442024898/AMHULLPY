## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsRline2D.py
#
#      PURPOSE:
#          The Rline2D class holds information about a restricted 2D line.
#          The restricted line consists of a start point and an end point.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Start        Point2D          The start point
#          End          Point2D          The end point

from KcsPoint2D import Point2D
import KcsPoint2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Rline2D class'}

class Rline2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          startp        Point2D        the start point
#          endp          Point2D        the end point

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
        if not isinstance(value,Point2D) and not isinstance(value,KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Start = Point2D(value.X, value.Y)
     Start = property (GetStart, SetStart)

     def GetEnd(self): return self.__End
     def SetEnd(self,value):
        if not isinstance(value,Point2D) and not isinstance(value,KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__End = Point2D(value.X, value.Y)
     End = property (GetEnd, SetEnd)
