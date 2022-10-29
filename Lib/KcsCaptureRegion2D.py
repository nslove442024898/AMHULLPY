## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsCaptureRegion2D.py
#
#      PURPOSE:
#          The CaptureRegion2D class holds information about a 2D capture region.
#          The region is defined with Contour2D, Inside/Outside flag, Cut/NoCut flag.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __Contour             Contour2D defining region
#           __Inside              integer, 1 if Inside selected, 0 if Outside
#           __Rect                integer, 1 if internal member Contour contains rectangle
#           __Infinite            integer, 1 if region is infinite, otherwise 0
#           __Cut                 integer, 1 if Cut selected, 0 if NoCut

from KcsPoint2D import Point2D
from KcsContour2D import Contour2D
from KcsRectangle2D import Rectangle2D
import string
import copy

class CaptureRegion2D(object):

    __ErrorMessages = {  TypeError : 'not supported argument type, see documentation of CaptureRegion2D class',
                        ValueError: 'not supported value type, see documentation of CaptureRegion2D class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#           None
#
    def __init__(self):
        self.__Cut = 0
        self.__Inside = 1
        self.__Rect = 0
        self.__Contour = Contour2D(Point2D(0, 0))
        self.__Infinite = 1

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
      tup = (
        'CaptureRegion2D',
        '   Contour: ' + str( self.__Contour ),
        '   Inside:  ' + str( self.__Inside ),
        '   Cut:     ' + str( self.__Cut ),
        '   Rect:    ' + str( self.__Rect ),
        '   Infinite:' + str( self.__Infinite ))
      return string.join (tup, '\n')

#
#      METHOD:
#         SetRectangle
#
#      PURPOSE:
#          Sets the region based on given rectangle
#
#      INPUT:
#          Parameters:
#          Rectangle        Rectangle2D       2D rectangle
#
#      RESULT:
#          The contour will be updated
#

    def SetRectangle(self, Rectangle):
        if not isinstance(Rectangle,Rectangle2D):
           raise ValueError, self.__ErrorMessages[TypeError]
        self.__Rect = 1
        self.__Contour = Contour2D(Point2D(Rectangle.Corner1.X, Rectangle.Corner1.Y))
        self.__Contour.AddLine(Point2D(Rectangle.Corner1.X, Rectangle.Corner2.Y))
        self.__Contour.AddLine(Point2D(Rectangle.Corner2.X, Rectangle.Corner2.Y))
        self.__Contour.AddLine(Point2D(Rectangle.Corner2.X, Rectangle.Corner1.Y))
        self.__Contour.AddLine(Point2D(Rectangle.Corner1.X, Rectangle.Corner1.Y)) # close contour
        self.__Infinite = 0

#
#      METHOD:
#         SetContour
#
#      PURPOSE:
#          Sets the region based on given countur
#
#      INPUT:
#          Parameters:
#          Contour        Contour2D       2D contour
#
#      RESULT:
#          The contour will be updated
#

    def SetContour(self, Contour):
        if not isinstance(Contour,Contour2D):
           raise ValueError, self.__ErrorMessages[TypeError]
        self.__Rect = 0
        self.__Contour = copy.deepcopy(Contour)
        self.__Infinite = 0


#
#      METHOD:
#         SetInside
#
#      PURPOSE:
#          Sets the Inside on 1
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The Inside will be set to 1
#

    def SetInside(self):
        self.__Inside = 1

#
#      METHOD:
#         SetOutside
#
#      PURPOSE:
#          Sets the Inside on 0
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The Inside will be set to 0
#

    def SetOutside(self):
        self.__Inside = 0

#
#      METHOD:
#         SetCut
#
#      PURPOSE:
#          Sets the Cut on 1
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The Cut will be set to 1
#

    def SetCut(self):
        self.__Cut = 1

#
#      METHOD:
#         SetNoCut
#
#      PURPOSE:
#          Sets the Cut on 0
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The Cut will be set to 0
#

    def SetNoCut(self):
        self.__Cut = 0

#
#      METHOD:
#         SetBoundaryInfinite
#
#      PURPOSE:
#          Sets the Infinite flag to 1
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The Cut will be set to 0
#

    def SetBoundaryInfinite(self):
        self.__Infinite = 1


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    def getCut(self): return self.__Cut
    def setCut(self, value):
       if not type(value)==type(0) or value<0:
          raise ValueError, self.__ErrorMessages[TypeError]
       if value>0:
          self.__Cut = 1
       else:
          self.__Cut = 0
    Cut     = property (getCut, setCut, None, 'Cut - flag for include(1)/not include(0) geometry intersecting the capture region')

    def getInside(self): return self.__Inside
    def setInside(self, value):
       if not type(value)==type(0) or value<0:
          raise ValueError, self.__ErrorMessages[TypeError]
       if value>0:
          self.__Inside = 1
       else:
          self.__Inside = 0
    Inside  = property (getInside, setInside, None, 'Inside - flag for include objects inside/outside of contour')

    def getInfinite(self): return self.__Infinite
    def setInfinite(self, value):
       if not type(value)==type(0) or value<0:
          raise ValueError, self.__ErrorMessages[TypeError]
       if value>0:
          self.__Infinite = 1
       else:
          self.__Infinite = 0
    Infinite = property (getInfinite, setInfinite, None, 'Infinite - flag for infinite region')

    def getRect(self): return self.__Rect
    Rect = property (getRect, None, None, 'Rect - contour type flag, set by SetRectangle and SetContour')

    def getContour(self): return self.__Contour
    Contour = property (getContour, None, None, 'Contour - capture region contour, set by SetRectangle and SetContour')
