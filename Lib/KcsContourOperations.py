## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsContourOperations.py
#
#      PURPOSE:
#          The ContourOperations class holds information about two 2D dimensional
#          contours, which will be used to perfom operations on.

#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __contour1       Contour2D      First contour
#          __contour2       Contour2D      Second contour
#          __segments1      list           Segments list of first contour
#          __segments2      list           Segments list of second contour
try:
   import kcs_ic
   import kcs_ui
except:
   pass
import KcsVector2D
import KcsContour2D
from KcsContour2D import Contour2D
import KcsPoint2D
from KcsPoint2D import Point2D
import copy

ACCURACY = 1.0E-4


class BooleanOperations:
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          contour1       Contour2D      First contour
#          contour2       Contour2D      Second contour
   def __init__(self, contour1, contour2):
      if not (isinstance(contour1,Contour2D) or isinstance(contour1,KcsContour2D.Contour2D)) \
      or not (isinstance(contour2,Contour2D) or isinstance(contour2,KcsContour2D.Contour2D)):
         raise TypeError, 'Type Error'
      self.__contour1 = copy.deepcopy(contour1)
      self.__contour2 = copy.deepcopy(contour2)
      self.__segments1 = self.ConvertContour(contour1)
      self.__segments2 = self.ConvertContour(contour2)
#
#      METHOD:
#          ConvertContour
#
#      PURPOSE:
#          To convert contour segments to the following representation:
#           (start point, end point, center point, amplitude)
#
#      INPUT:
#          Parameters:
#          contour1       Contour2D      Contour to convert
   def ConvertContour(self, cont1):
      if not (isinstance(cont1,Contour2D) or isinstance(cont1,KcsContour2D.Contour2D)):
         raise TypeError, 'Type Error'
      Segments = []
      index = 0
      try:
         for seg in cont1.Contour:
            if index > 0:
               amplitude = 0
               point1 = seg[0]
               point2 = cont1.Contour[ index-1 ][0]
               if len(seg) > 1:
                  amplitude = seg[1]
               center =  cont1.GetCenterPoint(point2, point1, amplitude)
               if not point1 == point2:
                  Segments.append([point2, point1, center, amplitude])
            index += 1
      except Exception, e:
         kcs_ui.message_debug('Convert Contour: ' + str(e))
      return Segments
#
#      METHOD:
#          GetInsideSegments
#
#      PURPOSE:
#          To get all segments that are inside the other contour
#
#
#      INPUT:
#          Parameters:
#          segments       list   list of segments converted by ConvertContour
   def GetInsideSegments(self, segments):
       if not (type(segments)==type([]) or type(segments)==type(())):
         raise TypeError, 'Type Error'
       insideSegments = []
       try:
          for item in segments:
              res = self.IsOuterSegment(item)
              if res == 0:
                  insideSegments.append(item)
       except Exception,e:
          kcs_ui.message_debug("GetInsideSegments: " + str(e))
       return insideSegments
#
#      METHOD:
#          GetOuterSegments
#
#      PURPOSE:
#          To get all segments that are outside the other contour
#
#
#      INPUT:
#          Parameters:
#          segments       list   list of segments converted by ConvertContour
   def GetOuterSegments(self, segments):
       if not (type(segments)==type([]) or type(segments)==type(())):
         raise TypeError, 'Type Error'
       outerSegments = []
       try:
          for item in segments:
              res = self.IsOuterSegment(item)
              if res == 1:
                  outerSegments.append(item)
       except Exception,e:
          kcs_ui.message_debug("GetOuterSegments: "+ str(e))
       return outerSegments
#
#      METHOD:
#          GetConditionalSegments
#
#      PURPOSE:
#          To get all segments that are in both contours.
#
#
#      INPUT:
#          Parameters:
#          segments       list   list of segments converted by ConvertContour
   def GetConditionalSegments(self, segments):
       if not (type(segments)==type([]) or type(segments)==type(())):
         raise TypeError, 'Type Error'
       condSegments = []
       try:
          for item in segments:
              res = self.IsOuterSegment(item)
              if res == 2:
                 condSegments.append(item)
       except Exception,e:
          kcs_ui.message_debug("GetConditionalSegments: "+ str(e) )
       return condSegments
#
#      METHOD:
#          IsOuterSegment
#
#      PURPOSE:
#          To check if segment is an outer segment.
#
#
#      INPUT:
#          Parameters:
#          segment       list   segment converted by ConvertContour
   def IsOuterSegment(self, seg):
      if not (type(seg)==type([]) or type(seg)==type(())) or len(seg)!=4:
         raise TypeError, 'Type Error'
      try:
         res = 0
         oncont = 0
         index = 0
         while index < len(seg) - 1:
            res = self.IsOuterPoint(seg[index])
            if res == 1:
               return 1
            if res == 2:
               oncont += 1
            index += 1
         if oncont >= 3:
            return 2
      except Exception,e:
         kcs_ui.message_debug("IsOuterSegment: "+ str(e))
      return 0

#
#      METHOD:
#          IsOuterPoint
#
#      PURPOSE:
#          To check if point is an outer point.
#
#
#      INPUT:
#          Parameters:
#          point     Point2D    point
   def IsOuterPoint(self, point):
       try:
          if isinstance(point, Point2D) or isinstance(point, KcsPoint2D.Point2D):
              if self.__contour1.IsInside(point):
                  if not self.__contour1.IsPointOnContour(point):
                      return 0;
              if self.__contour2.IsInside(point):
                  if not self.__contour2.IsPointOnContour(point):
                      return 0;
              if self.__contour1.IsPointOnContour(point) and self.__contour2.IsPointOnContour(point):
                  return 2
              return 1;
          else:
             raise TypeError, 'Type Error'
       except Exception,e:
          kcs_ui.message_debug("IsOuterPoint: " + str(e))

#
#      METHOD:
#          ChooseNextSegment
#
#      PURPOSE:
#          To choose next segment used for adding contours.
#
#
#      INPUT:
#          Parameters:
#          segment       list   segment converted by ConvertContour
#          segments      list  list of priority segments converted by ConvertContour
#          conds         list  list of secondary segments converted by ConvertContour
   def ChooseNextSegment(self, seg, segments, conds):
       if not (type(segments)==type([]) or type(segments)==type(())) or \
          not (type(conds)==type([]) or type(conds)==type(())) or \
          not (type(seg)==type([]) or type(seg)==type(())) or \
          len(seg)!=4:
          raise TypeError, 'Type Error'
       try:
          for item in segments:
              if IsSamePoint(item[0], seg[1]):
                  if not IsSamePoint(item[1], seg[0]):
                     segments.remove(item)
                     return item
          for item in segments:
              if IsSamePoint(item[1], seg[1]):
                  segments.remove(item)
                  item = (item[1], item[0], item[2], -item[3])
                  return item
          for item in conds:
              if IsSamePoint(item[0], seg[1]):
                  if not IsSamePoint(item[1], seg[0]):
                     conds.remove(item)
                     return item
          for item in conds:
              if IsSamePoint(item[1], seg[1]):
                  conds.remove(item)
                  item = (item[1], item[0], item[2], -item[3])
                  return item
       except Exception,e:
         kcs_ui.message_debug("ChooseNextSegment: "+str(e))
#
#      METHOD:
#          DifferNextSegment
#
#      PURPOSE:
#          To choose next segment used for substracing contours.
#
#
#      INPUT:
#          Parameters:
#          segment       list   segment converted by ConvertContour
#          segments      list  list of priority segments converted by ConvertContour
#          conds         list  list of secondary segments converted by ConvertContour
   def DifferNextSegment(self, seg, segments, conds):
       if not (type(segments)==type([]) or type(segments)==type(())) or \
          not (type(conds)==type([]) or type(conds)==type(())) or \
          not (type(seg)==type([]) or type(seg)==type(())) or \
          len(seg)!=4:
          raise TypeError, 'Type Error'
       try:
          for item in segments:
              if IsSamePoint(item[0],seg[1]):
                  if not IsSamePoint(item[1], seg[0]):
                     segments.remove(item)
                     return item
                  else:
                     if not IsSamePoint(item[2],seg[2]):
                        segments.remove(item)
                        return item
          for item in segments:
              if IsSamePoint(item[1], seg[1]):
                  if not IsSamePoint(item[0], seg[0]):
                     segments.remove(item)
                     item = (item[1], item[0], item[2], -item[3])
                     return item
                  else:
                     if not IsSamePoint(item[2], seg[2]):
                        segments.remove(item)
                        item = (item[1], item[0], item[2], -item[3])
                        return item
          for item in conds:
              if IsSamePoint(item[0], seg[1]):
                  if not IsSamePoint(item[1], seg[0]):
                     conds.remove(item)
                     return item
                  else:
                     if IsSamePoint(item[2], seg[2]):
                        conds.remove(item)
                        return item
          for item in conds:
              if IsSamePoint(item[1], seg[1]):
                  if not IsSamePoint(item[0], seg[0]):
                        conds.remove(item)
                        item = (item[1], item[0], item[2], -item[3])
                        return item
                  else:
                     if not IsSamePoint(item[2], seg[2]):
                        conds.remove(item)
                        item = (item[1], item[0], item[2], -item[3])
                        return item
       except Exception,e:
          kcs_ui.message_debug("DifferNextSegment: "+ str(e))
       return None

#
#      METHOD:
#          CompositeContour
#
#      PURPOSE:
#          To add contours.
#
#
#      INPUT:
#          Parameters:
#          points         list  list of intersection points
   def CompositeContour(self, points):
       thisouter  = self.GetOuterSegments(self.__segments1)
       otherouter = self.GetOuterSegments(self.__segments2)
       thiscond   = self.GetConditionalSegments(self.__segments1)

       seg = thisouter[0]
       startpoint = seg[0]
       resCont = [seg]
       Contour = KcsContour2D.Contour2D(startpoint)
       Contour.AddArc(seg[1], seg[3])
       x = 0
       maxlen = len(self.__segments1) + len(self.__segments2)
       try:
          while not IsSamePoint(startpoint, seg[1]) and x < maxlen:
              if IsPointInPoints(seg[1], points):
                  temp = thisouter
                  thisouter = otherouter
                  otherouter = temp
                  out_len = len(thisouter)
                  nextseg = self.ChooseNextSegment(seg, thisouter, otherouter)
                  if not nextseg:
                     nextseg = self.ChooseNextSegment(seg, thisouter, thiscond)                
                                      
                  #when the next segment was not selected from thisouter
                  #switch the list back to initial state
                  if nextseg and out_len == len(thisouter):
                     temp = thisouter
                     thisouter = otherouter
                     otherouter = temp                    
                                      
                  resCont.append(nextseg)
              else:
                  nextseg = self.ChooseNextSegment(seg, thisouter, thiscond)
                  resCont.append(nextseg)
              seg = nextseg
              Contour.AddArc(seg[1], seg[3])
              x += 1
       except Exception,e:
          kcs_ui.message_debug("CompositeContour: "+ str(e))
       return Contour

#
#      METHOD:
#          ChooseDifStartPoint
#
#      PURPOSE:
#          To choose another start point when creating more than one contour.
#
#      INPUT:
#          Parameters:
#          usedouter     list  list of already used segments converted by ConvertContour
#          outersegemts  list  list of segments converted by ConvertContour
   def ChooseDifStartPoint(self,usedouter, outersegments):
      if not (type(usedouter)==type([]) or type(usedouter)==type(())) or \
         not (type(outersegments)==type([]) or type(outersegments)==type(())):
         raise TypeError, 'Type Error'
      res = 0
      try:
         if len(usedouter) == 0:
            return 0
         else:
            for item in outersegments:
               res = 0
               for used in usedouter:
                  if IsSamePoint(item[0], used[1]) or IsSamePoint(item[0], used[0]):
                     if IsSamePoint(item[1], used[1]) or IsSamePoint(item[1], used[1]):
                        res = 1
               if res == 0:
                  return item
      except Exception,e:
         kcs_ui.message_debug("ChooseDifStartPoint: " + str(e))
      return res
#
#      METHOD:
#          CommonContour
#
#      PURPOSE:
#          To multiply contours.
#
#      INPUT:
#          Parameters:
#          points         list  list of intersection points
   def CommonContour(self, points):
      insidesegments1 = self.GetInsideSegments(self.__segments1)
      insidesegments2 = self.GetInsideSegments(self.__segments2)
      condsegments = self.GetConditionalSegments(self.__segments1)
      allin = insidesegments1 + insidesegments2
      otherin = insidesegments2
      resCont = []
      usedinside = []
      res = 0
      y = 0
      maxlen = len(self.__segments1) + len(self.__segments2)
      try:
         while res != 1 and y < maxlen:
            y += 1
            res = self.ChooseDifStartPoint(usedinside, allin)
            if res == 0:
               if (len(insidesegments1)==0) and (len(insidesegments2)==0):
                  if len(condsegments):
                     seg = condsegments[0]
                  else:
                     res = 1
                     break
               elif len(insidesegments1):
                  seg = insidesegments1[0]
               else:
                  seg = insidesegments2[0]
            elif res == 1:
               break
            else:
               seg = res
            usedinside.append(seg)
            startpoint = seg[0]
            Contour = KcsContour2D.Contour2D(startpoint)
            Contour.AddArc(seg[1], seg[3])
            x = 0
            while (startpoint != seg[1] and x < maxlen):
               x += 1
               nextseg = self.DifferNextSegment(seg, allin, otherin)
               #nextseg = self.DifferNextSegment(seg, insidesegments1, otherin)

               if not nextseg:
                  nextseg = self.DifferNextSegment(seg, condsegments, allin)

               if nextseg:
                  seg = nextseg
                  usedinside.append(nextseg)
                  if not IsSamePoint(nextseg[0], nextseg[1]):
                     Contour.AddArc(seg[1], seg[3])
            resCont.append(Contour)
      except Exception,e:
         kcs_ui.message_debug("Common: "+str(e))
      return resCont
#
#      METHOD:
#          DifferContour
#
#      PURPOSE:
#          To substract contours.
#
#
#      INPUT:
#          Parameters:
#          points         list  list of intersection points
   def DifferContour(self, points):
       outersegments1 = self.GetOuterSegments(self.__segments1)
       outersegments2 = self.GetOuterSegments(self.__segments2)
       basicinside = self.GetInsideSegments(self.__segments2)
      
       #If there are no outer segments of the first contour
       #this contour lies inside the second one.
       #In such case the result is empty
       if len(outersegments1) == 0:
          return []
       
       basicouter = outersegments1
       condsegments = self.GetConditionalSegments(self.__segments1)

       #If there are no contours insiade the first contour
       #it means that there is no intersection between the two
       #contours only "common" segments.        
       if len(basicinside) == 0 and len(condsegments) ==0 :
          return [self.__contour1]
       
       usedouter = []
       resCont = []
       res = 0
       y = 0
       maxlen = len(self.__segments1) + len(self.__segments2)
       try:
          while res != 1 and y < maxlen:
             y += 1
             thisouter = outersegments1
             otherouter = outersegments2
             thiscond = condsegments
             
             res = self.ChooseDifStartPoint(usedouter, thisouter)
             
             if res == 0:
                seg = outersegments1[0]
             elif res == 1:
                break
             else:
                seg = res
             startpoint = seg[0]
             usedouter.append(seg)
             Contour = KcsContour2D.Contour2D(startpoint)
             Contour.AddArc(seg[1], seg[3])
             while not IsSamePoint(startpoint, seg[1]):
                 if IsPointInPoints(seg[1], points):
                     temp = thisouter
                     thisouter = otherouter
                     otherouter = temp
                     nextseg = self.DifferNextSegment(seg, basicinside, basicouter)
                     if not nextseg:
                        nextseg = self.DifferNextSegment(seg, basicouter, thiscond)
                     usedouter.append(nextseg)
                 else:
                     nextseg = self.DifferNextSegment(seg, basicinside, thiscond)
                     if not nextseg:
##                        nextseg = self.ChooseNextSegment(seg, thisouter, thiscond)
                        nextseg = self.DifferNextSegment(seg, basicouter, thiscond)
                        usedouter.append(nextseg)
                 seg = nextseg
                 if seg:
                    Contour.AddArc(seg[1], seg[3])
             resCont.append(Contour)
       except Exception,e:
          kcs_ui.message_debug("Differ Contour: "+ str(e))
       return resCont

   def GetSegments1(self): return self.__segments1
   def GetSegments2(self): return self.__segments2
   def GetContour1(self): return self.__contour1
   def GetContour2(self): return self.__contour2
   def SetContour1(self, value):
      if not (isinstance(value,Contour2D) or isinstance(value,KcsContour2D.Contour2D)):
         raise TypeError, 'Type Error'
      self.__contour1 = copy.deepcopy(value)
      self.__segments1 = self.ConvertContour(value)
   def SetContour2(self, value):
      if not (isinstance(value,Contour2D) or isinstance(value,KcsContour2D.Contour2D)):
         raise TypeError, 'Type Error'
      self.__contour2 = copy.deepcopy(value)
      self.__segments2 = self.ConvertContour(value)
   Contour1 = property(GetContour1,SetContour1, None, 'Contour1 - first contour')
   Contour2 = property(GetContour2,SetContour2, None, 'Contour2 - first contour')
   Segments1 = property(GetSegments1, None, None, 'Segments1 - segment list of first contour (start point, end point, center point, amplitude)')
   Segments2 = property(GetSegments2, None, None, 'Segments2 - segment list of second contour (start point, end point, center point, amplitude)')

def IsSamePoint(pointA,pointB):
   if not (isinstance(pointA, Point2D) or isinstance(pointA, KcsPoint2D.Point2D)) \
      or not (isinstance(pointB, Point2D) or isinstance(pointB, KcsPoint2D.Point2D)):
      raise TypeError, 'Type Error'
   if pointA.DistanceToPoint(pointB) < ACCURACY:
      return 1
   else:
      return 0

def IsPointInPoints(point, points):
   if not (isinstance(point, Point2D) or isinstance(point, KcsPoint2D.Point2D)):
      raise TypeError, 'Type Error'
   if type(points) <> type([]):
      raise TypeError, 'Type Error'
   for item in points:
      if not (isinstance(item, Point2D) or isinstance(item, KcsPoint2D.Point2D)):
         raise TypeError, 'Type Error'

   for item in points:
      if IsSamePoint(point, item):
         return 1

   return 0
