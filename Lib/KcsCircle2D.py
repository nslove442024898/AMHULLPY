## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsCircle2D.py
#
#      PURPOSE:
#          The Circle2D class holds information about a 2D circle. The circle
#          consists of a centre point and a radius
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Centre         Point2D       The centre point
#          Radius         real          The radius

import math
import types
from KcsPoint2D import Point2D
import KcsVector2D

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Point2D class' }
#ParamLimit = { ParamLimit : "Parameter contains invalid value" }
PointError = "The point is inside the circle"
CircleError = "One circle is inside other, So no tangent can exist"

class Circle2D(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          inpoint         the centre point
#          rad             The radius of the circle

     def __init__(self, inpoint, rad):
        if not isinstance(inpoint, Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.Centre  = Point2D(inpoint.X,inpoint.Y)
        self.Radius = rad

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'My Circle Centre: %s Radius: %s' % (self.Centre, self.Radius)

#
#      METHOD:
#          TangentAtPoint
#
#      PURPOSE:
#          Calculate the tangent point and line segment on circle form the external point.
#
#      INPUT:
#          Parameters:
#          pntExt              Point2D       The external point
#          pntOnCircle         Point2D       The point on circle
#
#      RESULT:
#          Returns:
#          vector           	KcsVector2D     The vector representing the tangent from
#	  point pntExt to the circle at point pntOnCircle

     def HasPoint(self, pnt):
        """
        This public method of class KCSCircle2D checks whether the point pnt is inside the Circle2D or not.
        If the point is inside the Circle2D it returns 1 which means success otherwise it returns 0.
        """
        if not isinstance(pnt,Point2D):
           raise TypeError, ErrorMessages[TypeError]
        u = pnt.X - self.Centre.X
        v = pnt.Y - self.Centre.Y
        sqr_uv = u*u + v*v
        diff = math.sqrt(sqr_uv) - self.Radius
        if diff < -0.0003:
           return 1
        else:
           return 0

     def IsPointOnCircle(self, pnt):
        """
        This public method of class KCSCircle2D checks whether the point pnt is on the Circle2D or not with the precision of 0.0003
        If the point is on the Circle2D it returns 1 which means success otherwise it retuns 0.
        """
        if not isinstance(pnt,Point2D):
           raise TypeError, ErrorMessages[TypeError]
        if self.HasPoint(pnt)== 0:
           u = pnt.X - self.Centre.X
           v = pnt.Y - self.Centre.Y
           sqr_uv = u*u + v*v
           diff = math.sqrt(sqr_uv) - self.Radius
           if diff < 0.0003:
              return 1
           else:
              return 0
        else:
           return 0

     def __GetTangentPointsForExternalPoint(self, pntExt):
        """
        This private method of class KCSCircle2D returns the 2 possible tangent points for the external point pntExt
        which should lie outside the Circle2D.
        If the point pntExt lies inside the circle this function return 0 which indicates error
        else if point pntExt lies on the circle the function returns the same point as tangent point.
        This method is called from function GetTangentPoints
        """
        if not isinstance(pntExt,Point2D):
           raise TypeError, ErrorMessages[TypeError]
        u = pntExt.X - self.Centre.X
        v = pntExt.Y - self.Centre.Y
        sqr_uv = (u*u) + (v*v)
        if self.HasPoint(pntExt) == 1:
           return 0
        if self.IsPointOnCircle(pntExt) == 1:
           return pntExt
        else:
#          Assign start point of tangent
           pt1X = pntExt.X
           pt1Y = pntExt.Y
#          Compute the two possible tangent points
           sqrad = self.Radius * self.Radius
           tp1 = Point2D(0,0)
           tp2 = Point2D(0,0)
           if math.fabs(v) < 0.0003:
              tp1.X = sqrad/u
              tp1.Y = math.sqrt(sqrad-(tp1.X*tp1.X))
              tp2.X = tp1.X
              tp2.Y = -tp1.Y
           else:
              temp = self.Radius * v * math.sqrt(sqr_uv - sqrad)
              tp1.X = (u * sqrad + temp)/sqr_uv
              tp1.Y = (sqrad - (u * tp1.X))/v
              tp2.X = ((u * sqrad) - temp)/sqr_uv
              tp2.Y = (sqrad - (u * tp2.X))/v
           tp1.X = tp1.X + self.Centre.X
           tp1.Y = tp1.Y + self.Centre.Y
           tp2.X = tp2.X + self.Centre.X
           tp2.Y = tp2.Y + self.Centre.Y
           pntList = [tp1,tp2]
           return pntList

     def GetTangentPoints(self, tngPnt1=0, tngPnt2=0,cle=0):
        """
        This public function returns a list of 2 KCSPoint2D which are possible tangent points for a point tngPnt1 lying outside the Circle2D.
        If user has specified the tngPnt2 and cle that means that user wants to get tangent to this circle which
        is also a tangent to circle cle. And tngPnt1 is a approximate tangent point to self and tngPnt2 is approximate tangent point to cle.
        So in that case this function returns 2 points where first point is tangential to self and second point is tangential to cle
        and both these points are lying on the tangent to both the circles
        """
        if tngPnt2 == 0:
            pntList = self.__GetTangentPointsForExternalPoint(tngPnt1)
            return pntList
        else:
           if not isinstance(cle,Circle2D) or not isinstance(tngPnt1,Point2D) or not isinstance(tngPnt2,Point2D):
              raise TypeError, ErrorMessages[TypeError]
#          Calculate some constants.
           dh = cle.Centre.X - self.Centre.X
           dk = cle.Centre.Y - self.Centre.Y
           rDiff = self.Radius - cle.Radius
           rSum = self.Radius + cle.Radius
           h = math.sqrt(dh*dh + dk*dk)

#          Check if one circle is totally inside the other.
#          In this case, no tangent can be constructed.
           if (h-math.fabs(rDiff)) < 0.0003:
              raise CircleError
#          Transform the identification points, so that first arc
#          centre coinsides with origo, and second arc centre
#          is on the x-axis (H,0).

#          Translate the identification points
           u1 = tngPnt1.X - self.Centre.X
           v1 = tngPnt1.Y - self.Centre.Y
           u2 = tngPnt2.X - self.Centre.X
           v2 = tngPnt2.Y - self.Centre.Y

#          Find the rotation angle
           angle = math.asin(dk/h)
           if dh < 0.0:
              angle = math.pi - angle

#          Rotate the identification points
           angle = -angle
           vec1 = KcsVector2D.Vector2D(0.0,0.0)
           vec1.X = u1
           vec1.Y = v1
           vec1.Rotate(angle)
           u1 = vec1.X
           v1 = vec1.Y
           vec1.X = u2
           vec1.Y = v2
           vec1.Rotate(angle)
           u2 = vec1.X
           v2 = vec1.Y
           angle = -angle

#--------------------------------------------------------------------
#          CASE 1.  Imagine the tangent as a transmission chain;
#          the circles will then have the same rotation direction.
#--------------------------------------------------------------------

           if ((v1*v2) > 0.0) or ((h-rSum)< 0.0003):
#             Horizontal tangent
              if math.fabs(rDiff) < 0.003:
                 x1 = 0.0
                 y1 = self.Radius
                 x2 = h
                 y2 = self.Radius
#             Non-horizontal tangent
              else:
                 x1 = self.Radius * (rDiff/h)
                 y1 = math.sqrt(self.Radius*self.Radius - x1*x1)
                 x2 = cle.Radius*(rDiff/h)
                 y2 = math.sqrt(cle.Radius*cle.Radius - x2*x2)
                 x2 = x2 + h
              if v1 < 0.0:
                 y1 = -y1
                 y2 = -y2
#------------------------------------------------------------------------
#       CASE 2.  Imagine the tangent as a transmission chain;
#       the circles will then have the opposite rotation direction.
#------------------------------------------------------------------------
           else:
              x1 = self.Radius * (rSum/h)
              y1 = math.sqrt(self.Radius*self.Radius - x1*x1)
              x2 = -cle.Radius*(rSum/h)
              y2 = -math.sqrt(cle.Radius*cle.Radius - x2*x2)
              x2 = x2 + h
              if v1 < 0.0:
                 y1 = -y1
                 y2 = -y2
#--------------------------------------------------------------------
#          TRANSFORM BACK TO ORIGINAL COORDINATES
#---------------------------------------------------------------------
#          Rotate back
           vec1.X = x1
           vec1.Y = y1
           vec1.Rotate(angle)
           x1 = vec1.X
           y1 = vec1.Y
           vec1.X = x2
           vec1.Y = y2
           vec1.Rotate(angle)
           x2 = vec1.X
           y2 = vec1.Y

#          Translate back
           tp1 = Point2D(0,0)
           tp2 = Point2D(0,0)
           tp1.X = x1 + self.Centre.X
           tp1.Y = y1 + self.Centre.Y
           tp2.X = x2 + self.Centre.X
           tp2.Y = y2 + self.Centre.Y
           pntList = [tp1,tp2]
           return pntList

     def TangentAtPoint(self, pntExt, pntRef):
        """
        This public method returns a vector which is a tangent to this Circle2D thru point pntExt and the approximate point
        pntRef selected by the user
        """
        if not isinstance(pntExt,Point2D) or not isinstance(pntRef,Point2D):
           raise TypeError, ErrorMessages[TypeError]
        vect = KcsVector2D.Vector2D(0.0,0.0)
        # Translate given point and identification point
        # so that arc centre coinsides with origin
        pntList = self.GetTangentPoints(pntExt)
        if type(pntList) == type(0):
           raise PointError
        if type(pntList) == type(pntExt):
           vect.SetFromPoints(self.Centre,pntExt)
           vect.SetToUnitVector()	
           vect.Rotate(math.pi/2)
           return vect
        else:
           if type(pntList) == type([]):
              dist1 = (pntRef.X-pntList[0].X)*(pntRef.X-pntList[0].X) + (pntRef.Y - pntList[0].Y)*(pntRef.Y - pntList[0].Y)
              dist2 = (pntRef.X-pntList[1].X)*(pntRef.X-pntList[1].X) + (pntRef.Y - pntList[1].Y)*(pntRef.Y - pntList[1].Y)
              if dist1 < dist2:
                 x1 = pntList[0].X
                 y1 = pntList[0].Y
              else:
                 x1 = pntList[1].X
                 y1 = pntList[1].Y
              vect.X =  x1 - pntExt.X
              vect.Y =  y1 - pntExt.Y
              vect.SetToUnitVector()
              return vect

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

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

     def getCentre(self): return self.__Centre
     def setCentre(self, point):
        if not isinstance(point, Point2D):
           raise TypeError, ErrorMessages[TypeError]
        self.__Centre = Point2D(point.X, point.Y)
     Centre  = property (getCentre, setCentre, None, 'Centre - circle centre point')

     def getRadius(self): return self.__Radius
     def setRadius(self, value):
        if not type(value) in (types.IntType, types.LongType, types.FloatType):
           raise TypeError, ErrorMessages[TypeError]
        self.__Radius = value
     Radius  = property (getRadius, setRadius, None, 'Radius - circle radius')
