## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsArc3D.py
#
#      PURPOSE:
#          The Arc3D class holds information about a 3D arc. The arc consists
#          of a start point, an end point and an amplitude
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Start          Point3D       The start point
#          End            Point3D       The end point
#          Amplitude      Vector3D      The amplitude

import types
from KcsPoint3D import Point3D
import KcsVector3D

class Arc3D(object):

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

     def __init__(self, inpoint1 = Point3D(), inpoint2 = Point3D(), amp = KcsVector3D.Vector3D(0,0,0)):
        if not isinstance(inpoint1, Point3D) or not isinstance(inpoint2, Point3D):
           raise TypeError, Arc3D.__ErrorMessages[TypeError]
        self.Start  = inpoint1
        self.End    = inpoint2
        self.Amplitude = amp


#
#     New style from Python version 2.2
#

     __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Arc3D class',
                         ValueError: 'not supported value, see documentation of Arc3D class' }

     def GetStart(self): return self.__Start
     def SetStart(self, value):
        if value==None or not isinstance(value, Point3D):
           raise TypeError, Arc3D.__ErrorMessages[TypeError]
        self.__Start = Point3D(value.X,value.Y,value.Z)

     def GetEnd(self): return self.__End
     def SetEnd(self, value):
        if value==None or not isinstance(value, Point3D):
           raise TypeError, Arc3D.__ErrorMessages[TypeError]
        self.__End = Point3D(value.X,value.Y,value.Z)

     def GetAmplitude(self): return self.__Amplitude
     def SetAmplitude(self, value):
        if value==None or not isinstance(value, KcsVector3D.Vector3D):
           raise TypeError, Arc3D.__ErrorMessages[TypeError]
        self.__Amplitude = KcsVector3D.Vector3D(value.X,value.Y,value.Z)

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Arc Start: %s End: %s Amplitude: %s' % (self.Start, self.End, self.Amplitude)


#--------------------------------------------------------------------------------------
# Propoerties
#--------------------------------------------------------------------------------------

     Start     = property(GetStart, SetStart, None, "'Start' property - defines start point of arc")
     End       = property(GetEnd, SetEnd, None, "'End' property - defines end point of arc")
     Amplitude = property(GetAmplitude, SetAmplitude, None, "'Amplitude' property - defines amplitude of the arc")
