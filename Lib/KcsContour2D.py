## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsContour2D.py
#
#      PURPOSE:
#          The Contour2D class holds information about a 2D dimensional
#          contour. The contour is a list of segments. The segment is a
#          list of end coordinate and amplitude if applicable
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Contour        [segment]     list of segments
#          __Visible        integer       determines if contour is visible, 1 if visible otherwise 0
#          __Detectable     integer       determines if contour is detectable, 1 if visible otherwise 0
#          __Colour         Colour        colour of contour
#          __LineType       Linetype      linetype of contour
#          __Layer          Layer         layer of contour

try:
   import kcs_ic
   import kcs_draft
except:
   pass
import KcsPoint2D
from KcsPoint2D     import Point2D
from KcsVector2D     import Vector2D
import KcsColour
from KcsColour      import Colour
import KcsLinetype
from KcsLinetype    import Linetype
import KcsLayer
from KcsLayer       import Layer
import string
import types
func = {'IsClose':0,'IsInside':1,'Length':2,'Area':3,'Distance':4,'IsPointOnContour':5,'GetPointOnContour':6,'Direction':7}
ErrorMessages = { TypeError : 'not supported argument type, see documentation of Contour2D class',
                  ValueError: 'wrong points, see documentationo of Contour2D class' }

class Contour2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          startp        Point2D       2D start point of segment

    def __init__(self, startp = Point2D(0,0)):
        if not isinstance(startp, Point2D) and not isinstance(startp, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        point           = Point2D(startp.X,startp.Y)
        segment         = [point]
        self.Contour    = [segment]
        self.__Visible    = 1
        self.__Detectable = 1
        self.__Colour     = kcs_draft.colour_get(Colour())
        self.__LineType   = Linetype()
        self.__Layer      = Layer()

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
      tup = (
        'Contour2D:',
        '   segments:  ' + str(self.Contour),
        '   colour:    ' + str(self.__Colour),
        '   linetype:  ' + str(self.__LineType),
        '   layer:     ' + str(self.__Layer),
        '   visible:   ' + str(self.__Visible),
        '   detectable:' + str(self.__Detectable))
      return string.join (tup, '\n')

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

#
#      METHOD:
#         AddLine
#
#      PURPOSE:
#          Add a line (straight) segment to the contour
#
#      INPUT:
#          Parameters:
#          inpoint        Point2D       2D Point at end of line
#
#      RESULT:
#          The contour will be updated
#

    def AddLine(self, inpoint):
        if not isinstance(inpoint, Point2D) and not isinstance(inpoint, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        point = Point2D(inpoint.X,inpoint.Y)
        segment = [point]
        self.Contour.append(segment)

#
#      METHOD:
#         AddArc
#
#      PURPOSE:
#          Add an arc segment to the contour
#
#      INPUT:
#          Parameters:
#          inpoint        Point2D       2D point at the end of the arc
#          inamplitude    real          Amplitude at the midpoint of segment
#
#      RESULT:
#          The contour will be updated
#

    def AddArc(self, inpoint, inamplitude):
        if not isinstance(inpoint, Point2D) and not isinstance(inpoint, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        if not type(inamplitude) in [types.IntType, types.LongType, types.FloatType]:
           raise TypeError, ErrorMessages[TypeError]
        amplitude = inamplitude + 0.0
        point = Point2D(inpoint.X,inpoint.Y)
        segment = [point, amplitude]
        self.Contour.append(segment)

#
#      METHOD:
#         SetVisible
#
#      PURPOSE:
#          Sets contour visibility flag
#
#      INPUT:
#          Parameters:
#          visible        integer       if positive flag will be set to 1
#
#      RESULT:
#          The contour visible flag will be set
#

    def SetVisible(self, visible):
        if not isinstance(visible, int):
           raise TypeError, ErrorMessages[TypeError]
        if visible>0:
            self.__Visible = 1
        else:
            self.__Visible = 0

#
#      METHOD:
#         IsVisible
#
#      PURPOSE:
#          Gets contour visibility flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The contour visibility flag will be returned
#

    def IsVisible(self):
        return self.__Visible

#
#      METHOD:
#         SetDetectable
#
#      PURPOSE:
#          Sets contour detectable flag
#
#      INPUT:
#          Parameters:
#          detectable        integer       if positive flag will be set to 1
#
#      RESULT:
#          The contour detectable flag will be set
#

    def SetDetectable(self, detectable):
        if not isinstance(detectable, int):
           raise TypeError, ErrorMessages[TypeError]
        if detectable>0:
            self.__Detectable = 1
        else:
            self.__Detectable = 0

#
#      METHOD:
#         IsDetectable
#
#      PURPOSE:
#          Gets contour detectable flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The contour detectable flag will be returned
#

    def IsDetectable(self):
        return self.__Detectable

#
#      METHOD:
#         SetColour
#
#      PURPOSE:
#          Sets contour colour
#
#      INPUT:
#          Parameters:
#          colour        Colour       new colour
#
#      RESULT:
#          The contour colour will be set
#

    def SetColour(self, colour):
        if not isinstance(colour, Colour) and not isinstance(colour, KcsColour.Colour):
           raise TypeError, ErrorMessages[TypeError]
        self.__Colour = colour

#
#      METHOD:
#         GetColour
#
#      PURPOSE:
#          Gets contour colour
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The contour colour will be returned
#

    def GetColour(self):
        return self.__Colour

#
#      METHOD:
#         SetLineType
#
#      PURPOSE:
#          Sets contour linetype
#
#      INPUT:
#          Parameters:
#          linetype        Linetype       new linetype
#
#      RESULT:
#          The contour linetype will be set
#

    def SetLineType(self, linetype):
        if not isinstance(linetype, Linetype) and not isinstance(linetype, KcsLinetype.Linetype):
           raise TypeError, ErrorMessages[TypeError]
        self.__LineType = linetype

#
#      METHOD:
#         GetLineType
#
#      PURPOSE:
#          Gets contour linetype
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The contour linetype will be returned
#

    def GetLineType(self):
        return self.__LineType

#
#      METHOD:
#         SetLayer
#
#      PURPOSE:
#          Sets contour layer
#
#      INPUT:
#          Parameters:
#          layer        Layer       new layer
#
#      RESULT:
#          The contour layer will be set
#

    def SetLayer(self, layer):
       if not isinstance(layer, Layer) and not isinstance(layer, KcsLayer.Layer):
          raise TypeError, ErrorMessages[TypeError]
       self.__Layer = layer

#
#      METHOD:
#         GetLayer
#
#      PURPOSE:
#          Gets contour layer
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The contour layer will be returned
#

    def GetLayer(self):
       return self.__Layer


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

#
#      METHOD:
#         SetPoint
#
#      PURPOSE:
#          Set first point of contour
#
#      INPUT:
#          Parameters:
#          point     Point2D        2D point
#
#      RESULT:
#          None
#

    def SetPoint(self, startp):
        if not isinstance(startp, Point2D) and not isinstance(startp, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        point           = Point2D(startp.X,startp.Y)
        segment         = [point]
        self.Contour    = [segment]

#
#      METHOD:
#         IsClosed
#
#      PURPOSE:
#         Check whether the contour is closed or not
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Res               int              1 = Contour is closed
#                                             0 = Contour is not closed

    def IsClosed(self):
        return kcs_draft.geocontour_function(func['IsClose'],self)

#
#      METHOD:
#         IsInside
#
#      PURPOSE:
#         Check whether the contour is closed or not
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Res              int                 1 = The point is inside the contour
#                                               0 = The point is outside the contour.
#                                                   If the contour is not closed then this function returns 0

    def IsInside(self, extPnt):
        if not isinstance(extPnt, Point2D) and not isinstance(extPnt, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        return kcs_draft.geocontour_function(func['IsInside'],self,extPnt)

#
#      METHOD:
#         Length
#
#      PURPOSE:
#          Get the length of contour
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Length             real            The length of contour
#

    def Length(self):
        return kcs_draft.geocontour_function(func['Length'],self)

#
#      METHOD:
#         Area
#
#      PURPOSE:
#          Get the area of contour
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Area             real            The area of contour
#

    def Area(self):
        return kcs_draft.geocontour_function(func['Area'],self)

#
#      METHOD:
#         Distance
#
#      PURPOSE:
#          Get the distace of a point from the start point of the Contour
#
#      INPUT:
#          Parameters:
#          pnt              Point2D         The Point whose distance from the start point of the contourn is to be calculated
#
#      RESULT:
#          Dist             real            The distance of given point pnt from the start point
#

    def Distance(self,pnt):
        if not isinstance(pnt, Point2D) and not isinstance(pnt, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        return kcs_draft.geocontour_function(func['Distance'],self,pnt)

#
#      METHOD:
#         IsPointOnContour
#
#      PURPOSE:
#          Check whether the given point is on contour or not
#
#      INPUT:
#          Parameters:
#          pnt              Point2D         The Point which is tobe checked
#
#      RESULT:
#          Res              int             1 == The Point is on Contour
#                                           0 == The Point is not on Contour

    def IsPointOnContour(self,pnt):
        if not isinstance(pnt, Point2D) and not isinstance(pnt, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        return kcs_draft.geocontour_function(func['IsPointOnContour'],self,pnt)

#
#      METHOD:
#         GetPointOnContour
#
#      PURPOSE:
#          Get a point on contour which is nearest to the given point
#
#      INPUT:
#          Parameters:
#          pnt              Point2D         The referecen point
#
#      RESULT:
#          Res              Poinit2D        The Point on contour nearest to given point pnt

    def GetPointOnContour(self,pnt):
        if not isinstance(pnt, Point2D) and not isinstance(pnt, KcsPoint2D.Point2D):
           raise TypeError, ErrorMessages[TypeError]
        return kcs_draft.geocontour_function(func['GetPointOnContour'],self,pnt)

#
#      METHOD:
#          Direction
#
#      PURPOSE:
#          Get the direction of the contour
#
#      INPUT:
#          Parameters:
#           None
#
#      RESULT:
#          Res               int        1 = if contour is clockwise
#                                      -1 = if contour in anticlockwise

    def Direction(self):
        return kcs_draft.geocontour_function(func['Direction'],self,Point2D())
#
#      METHOD:
#          GetCenterPoint
#
#      PURPOSE:
#          Get the cener point of a segment given by star,
#          end point and amplitude
#
#      INPUT:
#          Parameters:
#           start           Point2D         Starting point of the segment
#           end             Point2D         Ending point of the segment
#           amp             real            The amplitude of a segment
#
#      RESULT:
#          Res               Point2D        The segments center point
#
    def GetCenterPoint(self, start, end, amp):
        import math
        if not (isinstance(start, Point2D) or isinstance(start, KcsPoint2D.Point2D)) or \
           not (isinstance(end, Point2D) or isinstance(end, KcsPoint2D.Point2D)):
           raise TypeError, ErrorMessages[TypeError]
        if not type(amp) in [types.IntType, types.LongType, types.FloatType]:
           raise TypeError, ErrorMessages[TypeError]
        res = Point2D(0,0)
        if start.X != end.X:
           resX = (end.X - start.X)/2 + start.X
        else:
           resX = start.X
        if start.Y != end.Y:
           resY = (end.Y - start.Y)/2 + start.Y
        else:
           resY = start.Y
        res.SetCoordinates(resX, resY)
        if amp == 0:
            return res
        vect = Vector2D(0,0)
        vect.SetFromPoints(res, end)
        vect.SetLength(amp)
        #if amp < 0:
        #    vect.Rotate((math.pi/2))
        #else:
        vect.Rotate(-(math.pi/2))
        center = Point2D(res.X + vect.X, res.Y + vect.Y)
        return center
#
#      METHOD:
#          __add__
#
#      PURPOSE:
#          The addition operator
#
#      INPUT:
#          Parameters:
#           other               Contour2d       The contour that is to be added
#
#      RESULT:
#           Res                 Contour2d       New instance of Contour2D representing
#                                               the sum of self and other
#
    def __add__(self, other):
        if not isinstance(other, Contour2D) and not isinstance(other, KcsContour2D.Contour2D):
            if type(other) == type([]) and len(other) == 1:
                if not isinstance(other[0], Contour2D) and not isinstance(other[0], KcsContour2D.Contour2D):
                    raise TypeError, ErrorMessages[TypeError]
            else:
                raise TypeError, ErrorMessages[TypeError]
        import KcsContourOperations
        newcontour1 = self
        newcontour2 = other
        if not newcontour1.IsClosed() or not newcontour2.IsClosed():
            raise TypeError, ErrorMessages[TypeError]

        #Get intersections         
        (newcontour1, newcontour2, points) = newcontour1.__intersect(newcontour2)
        #if contours are not intersecting two cases are possible
        #1. contour A is completely outside contour B
        #2. contour A is completely isside contour B
        if len(points) == 0:
           if self.IsInside(other.Contour[0][0]):
              return [self]
           else:
              if other.IsInside(self.Contour[0][0]):
                 return [other]
              else:
                 return [self, other]

        booloper = KcsContourOperations.BooleanOperations(newcontour1, newcontour2)
        return [booloper.CompositeContour(points)]
#
#      METHOD:
#          __mul__
#
#      PURPOSE:
#          The multiplication operator
#
#      INPUT:
#          Parameters:
#           other               Contour2d       The contour that is to be multiplicated
#
#      RESULT:
#           Res                 Contour2d       New instance of Contour2D representing
#                                               the common part of self and other
#
    def __mul__(self, other):
        if not isinstance(other, Contour2D) and not isinstance(other, KcsContour2D.Contour2D):
            if type(other) == type([]) and len(other) == 1:
                if not isinstance(other[0], Contour2D) and not isinstance(other[0], KcsContour2D.Contour2D):
                    raise TypeError, ErrorMessages[TypeError]
            else:
                raise TypeError, ErrorMessages[TypeError]
        import KcsContourOperations
        newcontour1 = self
        newcontour2 = other
        if not newcontour1.IsClosed() or not newcontour2.IsClosed():
            raise TypeError, ErrorMessages[TypeError]
        #Get intersections         
        (newcontour1, newcontour2, points) = newcontour1.__intersect(newcontour2)
        booloper = KcsContourOperations.BooleanOperations(newcontour1, newcontour2)
        list = booloper.CommonContour(points)
        reslist = []
        for item in list:
            if item.IsClosed():
                reslist.append( item )
        return reslist
#
#      METHOD:
#          __sub__
#
#      PURPOSE:
#          The substract operator
#
#      INPUT:
#          Parameters:
#           other               Contour2d       The contour that is to be substracted
#
#      RESULT:
#           Res                 Contour2d       New instance of Contour2D representing
#                                               the difference of self and other
#
    def __sub__(self, other):
        if not isinstance(other, Contour2D) and not isinstance(other, KcsContour2D.Contour2D):
            if type(other) == type([]) and len(other) == 1:
                if not isinstance(other[0], Contour2D) and not isinstance(other[0], KcsContour2D.Contour2D):
                    raise TypeError, ErrorMessages[TypeError]
            else:
                raise TypeError, ErrorMessages[TypeError]
        import KcsContourOperations

        newcontour1 = self
        newcontour2 = other
        
        if not newcontour1.IsClosed() or not newcontour2.IsClosed():
            raise TypeError, ErrorMessages[TypeError]
                
        (newcontour1, newcontour2, points) = newcontour1.__intersect(newcontour2)
        #if contours are not intersecting two cases are possible
        #1. contour A is completely outside contour B
        #2. contour A is completely isside contour B
        if len(points) == 0:
           if self.IsInside(other.Contour[0][0]):
              return [self, other]
           else:
              if other.IsInside(self.Contour[0][0]):
                 return []
              else:
                 return [self]
            
        booloper = KcsContourOperations.BooleanOperations(newcontour1, newcontour2)
        list = booloper.DifferContour(points)
        reslist = []
        for item in list:
            if item.IsClosed():
                reslist.append( item )
        return reslist

#
#  For some Boolean operation contour have to be decomposed 
#  This method checks if the contour intersects itself in such case
#  a new vertex is added in the intersection.
#
    def __processcontour(self):
      in_contour = self
      (points, segments1, segments2) = kcs_ic.intersection_points_get(in_contour, in_contour)
      listNo = 0
      SpPoints = points
      newcontour = self
      while len(points) > 0:
         ip = points.pop()
         seg1 = segments1.pop()
         seg2 = segments2.pop()
         contour_len = len(newcontour.Contour);
         newcontour = kcs_ic.contour_split(newcontour, ip, seg1, ip, -seg1)

         (ps, s1, s2) = kcs_ic.intersection_points_get(newcontour, newcontour)         
         #if segments count have changed the list of segments ids must be
         #updated
         if contour_len < len(newcontour.Contour):
            for seg in range(len(segments1)):
               segments1[seg] >= s1[seg]

      
      return newcontour

#
#  Intersect contours
#
#  RESULT:
#     tuple with two contours and list of points
#     contours are splited in points of intersection
#
    def __intersect(self, other):
      #Prepare the contours for the operation
      newcontour1 = self.__processcontour()
      newcontour2 = other.__processcontour()

      (points, segments1, segments2) = kcs_ic.intersection_points_get(newcontour1, newcontour2)
      res_points=[]
      for point in points:
         res_points.append(point)

      processed_ip = []
      while len(points) > 0:
         ip = points.pop()
         seg1 = segments1.pop()
         seg2 = segments2.pop()

         newcontour1 = kcs_ic.contour_split(newcontour1, ip, seg1, ip, -seg1)
         newcontour2 = kcs_ic.contour_split(newcontour2, ip, seg2, ip, -seg2)
         (points, segments1, segments2) = kcs_ic.intersection_points_get(newcontour1, newcontour2)
         #remove processed intersections from the list
         processed_ip.append(ip)
         for pt in processed_ip:
            for ppt in points:
               if ppt.DistanceToPoint(pt) < 1e-8:
                  previous = points.index(ppt)
                  break
            points.pop(previous)
            segments1.pop(previous)
            segments2.pop(previous)          
      return (newcontour1, newcontour2, res_points)

      
#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

    Visible    = property (IsVisible, SetVisible, None, 'Visible - contour visibility flag')
    Detectable = property (IsDetectable, SetDetectable, None, 'Detectable - contour detectable flag')
    Colour     = property (GetColour, SetColour, None, 'Colour - contour colour')
    LineType   = property (GetLineType, SetLineType, None, 'LineType - ')
    Layer      = property (GetLayer, SetLayer, None, 'Layer - ')
