## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsArc2D.py
#
#      PURPOSE:
#          The Arc2D class holds information about a 2D arc. The arc consists
#          of a start point, an end point and an amplitude
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Start          Point2D       The start point
#          End            Point2D       The end point
#          Amplitude      real          The amplitude

import types
from KcsPoint2D import Point2D
class Arc2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          inpoint1        start point of arc
#          inpoint2        end point of arc
#          amp             The amplitude of the arc

     def __init__(self, inpoint1, inpoint2, amp):
        self.Start  = inpoint1
        self.End    = inpoint2
        self.Amplitude = amp


#
#     New style from Python version 2.2
#

     __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Arc2D class',
                         ValueError: 'not supported value, see documentation of Arc2D class' }

     def getStart(self): return self.__Start
     def setStart(self, value):
        if value==None or not isinstance(value, Point2D):
           raise TypeError, Arc2D.__ErrorMessages[TypeError]
        self.__Start = Point2D(value.X, value.Y)
     Start = property(getStart, setStart, None, "'Start' property - defines start point of arc")

     def getEnd(self): return self.__End
     def setEnd(self, value):
        if value==None or not isinstance(value, Point2D):
           raise TypeError, Arc2D.__ErrorMessages[TypeError]
        self.__End = Point2D(value.X, value.Y)
     End = property(getEnd, setEnd, None, "'End' property - defines end point of arc")

     def getAmplitude(self): return self.__Amplitude
     def setAmplitude(self, value):
        if type(value) != types.FloatType and type(value) != types.IntType and type(value) != types.LongType:
           raise TypeError, Arc2D.__ErrorMessages[TypeError]
        self.__Amplitude = value
     Amplitude = property(getAmplitude, setAmplitude, None, "'Amplitude' property - defines amplitude of the arc")

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Arc Start: %s End: %s Amplitude: %s' % (self.Start, self.End, self.Amplitude)

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
