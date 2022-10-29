## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsConic2D.py
#
#      PURPOSE:
#          The Conic2D class holds information about a 2D conic segment. The conic
#          segment is defined by a start point, an end point, an amplitude vector and a
#          form factor. The form factor controls the shape of the conic and should be
#          in the interval [0,1[. In mathematical terms, a value < 0.5 will yield a ellipse,
#          a value > 0.5 a hyperbola, while a value of exactly 0.5 will yield a parabola.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Start          Point2D       The start point
#          End            Point2D       The end point
#          Amplitude      Vector2D      The amplitude vector
#          Cff            real          The form factor

from KcsPoint2D import Point2D
from KcsVector2D import Vector2D
import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Conic2D class',
                  ValueError : 'not supported argument value, see documentation of Conic2D class'}

class Conic2D(object):



#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          stp             start point of conic
#          endp            end point of conic
#          ampl            amplitude vector of the conic
#          cff             form factor

     def __init__(self, stp, endp, ampl, cff):
        self.Start  = stp
        self.End = endp
        self.Amplitude = ampl
        self.Cff = cff

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Conic Start: %s End: %s Amplitude: %s Cff: %s' % (self.Start, self.End, self.Amplitude, self.Cff)



#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
     def getStart(self): return self.__Start
     def setStart(self, value):
        if not isinstance(value, Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Start = Point2D(value.X, value.Y)
     Start = property (getStart, setStart, None, 'Start - conic start point')

     def getEnd(self): return self.__End
     def setEnd(self, value):
        if not isinstance(value, Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__End = Point2D(value.X, value.Y)
     End = property (getEnd, setEnd, None, 'End - conic end point')

     def getAmplitude(self): return self.__Amplitude
     def setAmplitude(self, value):
        if not isinstance(value, Vector2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Amplitude = Vector2D(value.X, value.Y)
     Amplitude = property (getAmplitude, setAmplitude, None, 'Amplitude - conic amplitude vector')

     def getCff(self): return self.__Cff
     def setCff(self, value):
        if not type(value) in [types.IntType, types.LongType, types.FloatType]:
           raise TypeError, ErrorMessages[TypeError]
        if value<0 or value>=1:
           raise ValueError, ErrorMessages[ValueError]
        self.__Cff = value
     Cff = property (getCff, setCff, None, 'Cff - conic form factor')

