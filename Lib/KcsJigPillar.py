## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsJigPillar.py
#
#      PURPOSE:
#
#          To hold Jig pillars options.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
import string
import types
from KcsTransformation3D import Transformation3D

class Frames(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Frames  class',
                       ValueError: 'not supported value, see documentation of Frames class' }


   def __init__(self, panel):
        self.__Panel = panel


   def __repr__(self):
        return 'Panel: ' % (self.__Panel)


   def SetPanel(self, panel):
      if type(panel) != type(''):
         raise TypeError, Frames.__ErrorMessages[TypeError]
      self.__Panel = panel


   def GetPanel(self):
      return self.__Panel

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Panel = property (GetPanel, SetPanel, None, '')



#-----------------------------------------------------------------------
class ClosestJigPillar(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of ClosestJigPillar class',
                       ValueError: 'not supported value, see documentation of ClosestJigPillar class' }

   def __init__(self, frame, seam, panel):
        self.__Frame   = frame
        self.__Seam    = seam
        self.__Panel   = panel


   def __repr__(self):
      tup = (
            'ClosestJigPillar:',
            '   Frame      :' + str(self.__Frame),
            '   Seam       :' + str(self.__Seam),
            '   Panel      :' + str(self.__Panel))
      return string.join (tup, '\n')



   def SetFrame(self, frame):
      if type(frame) != type(''):
         raise TypeError, ClosestJigPillar.__ErrorMessages[TypeError]
      self.__Frame = frame

   def GetFrame(self):
      return self.__Frame



   def SetSeam(self, seam):
      if type(seam) != type(''):
         raise TypeError, ClosestJigPillar.__ErrorMessages[TypeError]
      self.__Seam = seam

   def GetSeam(self):
      return self.__Seam



   def SetPanel(self, panel):
      if type(panel) != type(''):
         raise TypeError, ClosestJigPillar.__ErrorMessages[TypeError]
      self.__Panel = panel


   def GetPanel(self):
      return self.__Panel


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Frame = property (GetFrame, SetFrame, None, '')
   Seam = property (GetSeam, SetSeam, None, '')
   Panel = property (GetPanel, SetPanel, None, '')


#-----------------------------------------------------------------------
class PinJig(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of PinJig class',
                       ValueError: 'not supported value, see documentation of PinJig class' }

   def __init__(self):
        self.__Panel =        ''
        self.__Jigs =         1
        self.__Heights =      1
        self.__Rulers =       1
        self.__Legends =      1
        self.__JigsOutside =  1
        self.__GridSizeX =    2
        self.__GridSizeY =    2
        self.__SeamPillars =  0
        self.__PlacementX =   0.0
        self.__PlacementY =   0.0
        self.__Rotate =       0.0
        self.__Matrix =       Transformation3D()


   def __repr__(self):
      tup = (
            '   PinJig        :',
            '   Panel         :' + str(self.__Panel),
            '   Jigs          :' + str(self.__Jigs),
            '   Heights       :' + str(self.__Heights),
            '   Rulers        :' + str(self.__Rulers),
            '   Legends       :' + str(self.__Legends),
            '   JigsOutside   :' + str(self.__JigsOutside),
            '   GridSizeX     :' + str(self.__GridSizeX),
            '   GridSizeY     :' + str(self.__GridSizeY),
            '   SeamPillars   :' + str(self.__SeamPillars),
            '   PlacementX    :' + str(self.__PlacementX),
            '   PlacementY    :' + str(self.__PlacementY),
            '   Rotate        :' + str(self.__Rotate),
            '   Matrix        :' + str(self.__Matrix))
      return string.join (tup, '\n')


   def SetPanel(self, panel):
      if type(panel) != type(''):
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Panel = panel

   def GetPanel(self):
      return self.__Panel


   def SetJigs(self, jigs):
      if type(jigs) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Jigs = jigs

   def GetJigs(self):
      return self.__Jigs


   def SetHeights(self, heights):
      if type(heights) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Heights = heights

   def GetHeights(self):
      return self.__Heights


   def SetRulers(self, rulers):
      if type(rulers) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Rulers = rulers

   def GetRulers(self):
      return self.__Rulers


   def SetLegends(self, legends):
      if type(legends) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Legends = legends

   def GetLegends(self):
      return self.__Legends


   def SetJigsOutside(self, jigoutside):
      if type(jigoutside) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__JigsOutside = jigoutside

   def GetJigsOutside(self):
      return self.__JigsOutside


   def SetGridSizeX(self, girdsizex):
      if type(girdsizex) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__GridSizeX = girdsizex

   def GetGridSizeX(self):
      return self.__GridSizeX


   def SetGridSizeY(self, girdsizey):
      if type(girdsizey) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__GridSizeY = girdsizey

   def GetGridSizeY(self):
      return self.__GridSizeY


   def SetSeamPillars(self, seampillars):
      if type(seampillars) != types.IntType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__SeamPillars = seampillars

   def GetSeamPillars(self):
      return self.__SeamPillars


   def SetPlacementX(self, placementx):
      if type(placementx) != types.FloatType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__PlacementX = placementx

   def GetPlacementX(self):
      return self.__PlacementX


   def SetPlacementY(self, placementy):
      if type(placementy) != types.FloatType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__PlacementY = placementy

   def GetPlacementY(self):
      return self.__PlacementY


   def SetRotate(self, rotate):
      if type(rotate) != types.FloatType:
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Rotate = rotate

   def GetRotate(self):
      return self.__Rotate


   def SetMatrix(self, matrix):
      if not (isinstance(matrix,Transformation3D)):
         raise TypeError, PinJig.__ErrorMessages[TypeError]
      self.__Matrix = matrix

   def GetMatrix(self):
      return self.__Matrix


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Panel = property (GetPanel, SetPanel, None, '')
   Jigs = property (GetJigs, SetJigs, None, '')
   Heights = property (GetHeights, SetHeights, None, '')
   Rulers = property (GetRulers, SetRulers, None, '')
   Legends = property (GetLegends, SetLegends, None, '')
   JigsOutside = property (GetJigsOutside, SetJigsOutside, None, '')
   GridSizeX = property (GetGridSizeX, SetGridSizeX, None, '')
   GridSizeY = property (GetGridSizeY, SetGridSizeY, None, '')
   SeamPillars = property (GetSeamPillars, SetSeamPillars, None, '')
   PlacementX = property (GetPlacementX, SetPlacementX, None, '')
   PlacementY = property (GetPlacementY, SetPlacementY, None, '')
   Rotate = property (GetRotate, SetRotate, None, '')
   Matrix = property (GetMatrix, SetMatrix, None, '')
