## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsEllipse2D.py
#
#      PURPOSE:
#          The Ellipse2D class holds information about a 2D ellipse. The
#          ellipse is defined from two points defining a rectangle
#          parallel to the coordinate axes.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Corner1        Point2D      The first corner point
#          Corner2        Point2D      The second corner point

import KcsPoint2D
from KcsPoint2D import Point2D
class Ellipse2D(object):

     __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Ellipse2D class',
                       ValueError: 'not supported value, see documentation of Ellipse2D class' }
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          p1        Point2D    First corner point
#          p2        Point2D    Second corner point

     def __init__(self, p1, p2):
        self.Corner1 = Point2D(p1.X,p1.Y)
        self.Corner2 = Point2D(p2.X,p2.Y)


#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Ellipse first corner: %s second corner: %s' % (self.Corner1, self.Corner2)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
     def GetCorner1(self): return self.__Corner1
     def SetCorner1(self,value):
        if not (isinstance(value,Point2D) or isinstance(value,KcsPoint2D.Point2D)):
           raise TypeError, Ellipse2D.__ErrorMessages[TypeError]
        self.__Corner1 = Point2D(value.X, value.Y)
     Corner1 = property (GetCorner1, SetCorner1, None, 'Corner1 - first ellipse corner point')

     def GetCorner2(self): return self.__Corner2
     def SetCorner2(self,value):
        if not (isinstance(value,Point2D) or isinstance(value,KcsPoint2D.Point2D)):
           raise TypeError, Ellipse2D.__ErrorMessages[TypeError]
        self.__Corner2 = Point2D(value.X, value.Y)
     Corner2 = property (GetCorner2, SetCorner2, None, 'Corner2 - second ellipse corner point')
