## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsGeoContour3D.py
#
#      PURPOSE:
#          The GeoContour3D class holds information about a 3D dimensional
#          contour. The contour is a list of segments. The segment is a
#          list of end coordinate and amplitude if applicable
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Contour        [segment]     list of 3D segments

import KcsPoint3D
from KcsPoint3D     import Point3D
import KcsVector3D
from KcsVector3D     import Vector3D
import string

class GeoContour3D(object):

    __ErrorMessages = { TypeError : 'not supported argument type, see documentation of GeoContour3D class',
                       ValueError: 'not supported value, see documentation of GeoContour3D class' }
# -----------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:

    def __init__(self):
        self.Contour    = []

# -----------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
     nseg = len( self.Contour)
     if nseg > 0:
        nseg = nseg - 1

     segdata = '\n'
     segno = 0
     for seg in self.Contour:
        segdata = segdata + '              ' + str(segno) + ': ' + str( seg) + '\n'
        segno = segno + 1

     tup = (
        'GeoContour3D:',
        '   number of segments:  ' + str(nseg),
         '   segments:  ' + segdata)

     return string.join (tup, '\n')

# -----------------------------------------------------------------------------
#
#      METHOD:
#         AddLine
#
#      PURPOSE:
#          Add a line (straight) segment to the contour
#
#      INPUT:
#          Parameters:
#          inpoint        Point3D       3D Point at end of line
#
#      RESULT:
#          The contour will be updated
#

    def AddLine(self, inpoint):
        if not (isinstance(inpoint,Point3D) or isinstance(inpoint,KcsPoint3D.Point3D)):
           raise TypeError, GeoContour3D.__ErrorMessages[TypeError]
        point = Point3D(inpoint.X,inpoint.Y,inpoint.Z)
        segment = [point]
        self.Contour.append(segment)

# -----------------------------------------------------------------------------
#
#      METHOD:
#         AddArc
#
#      PURPOSE:
#          Add an arc segment to the contour
#
#      INPUT:
#          Parameters:
#          inpoint        Point3D       3D point at the end of the arc
#          inamplitude    vector3d      Amplitude vector at the midpoint of
#                                       the segment
#
#      RESULT:
#          The contour will be updated
#

    def AddArc(self, inpoint, inamplitude):
        if not (isinstance(inpoint,Point3D) or isinstance(inpoint,KcsPoint3D.Point3D)) or \
           not (isinstance(inamplitude,Vector3D) or isinstance(inamplitude,KcsVector3D.Vector3D)):
           raise TypeError, GeoContour3D.__ErrorMessages[TypeError]
        point = Point3D(inpoint.X,inpoint.Y,inpoint.Z)
        amplitude = Vector3D(inamplitude.X,inamplitude.Y,inamplitude.Z)
        segment = [point, amplitude]
        self.Contour.append(segment)

# -----------------------------------------------------------------------------
#
#      METHOD:
#         IsPoint
#
#      PURPOSE:
#          Checks if contour is a point
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          1 if contour is a point
#

    def IsPoint(self):
        if len(self.Contour)==1:
            return 1
        else:
            return 0

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetPoint
#
#      PURPOSE:
#          Set first point of contour
#
#      INPUT:
#          Parameters:
#          point     Point3D        3D point
#
#      RESULT:
#          None
#

    def SetPoint(self, startp):
        if not (isinstance(startp,Point3D) or isinstance(startp,KcsPoint3D.Point3D)):
           raise TypeError, GeoContour3D.__ErrorMessages[TypeError]
        point           = Point3D(startp.X,startp.Y,startp.Z)
        segment         = [point]
        self.Contour    = [segment]

# -----------------------------------------------------------------------------
