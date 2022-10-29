## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      MODULE NAME:
#          KcsSketchDimensioning.py
#
#      PURPOSE:
#          The KcsSketchDimensioning module is used with trig_hull_endcut_dim trigger
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
#
#      CLASS NAME:
#         DimensionSet
#
#      PURPOSE:
#          The DimensionSet class holds dimension data returned from trig_hull_endcut_dim trigger
#
#      ATTRIBUTES:
#          private:
#           __Elements    list              list of dimensions
#
#      METHODS:
#        AddLinearDim                       Adds linear dimension to the set
#        AddAngleDim                        Adds angle dimension to the set
#        AddRadiusDim                       Adds radius dimension to the set
#        AddCustomDim                       Adds custom dimension to the set
import string
import KcsRline2D
import KcsPoint2D
import KcsVector2D
import KcsRectangle2D
from KcsRline2D import Rline2D
from KcsPoint2D import Point2D
from KcsVector2D import Vector2D


class DimensionSet:

   ErrorMessages = { TypeError : 'not supported argument type, see documentation of DimensionSet class' }
# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
# -----------------------------------------------------------------------------------------------------------------

   def __init__(self):
      self.__LinearDim  = []
      self.__AngleDim   = []
      self.__RadiusDim  = []
      self.__CustomDim  = []

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddLinearDim
#
#      PURPOSE:
#          To add linear dimension to the set
#
#      INPUT:
#          Parameters:
#           measurePoint1                 First end of a measure. Instance of Point2D
#           measurePoint2                 Second end of a measure. Instance of Point2D
#           direction                     Direction vector along the witness lines. Instance of Vector2D
#           linePoint                     A point locating the projection line. Instance of Point2D
#           text                          Measure text
#
# -----------------------------------------------------------------------------------------------------------------

   def AddLinearDim(self, measurePoint1, measurePoint2, direction, linePoint, text):
      if ( isinstance(measurePoint1, KcsPoint2D.Point2D) or isinstance(measurePoint1, Point2D) ) and\
         ( isinstance(measurePoint2, KcsPoint2D.Point2D) or isinstance(measurePoint2, Point2D) ) and\
         ( isinstance(direction, KcsVector2D.Vector2D)   or isinstance(direction, Vector2D) )    and\
         ( isinstance(linePoint, KcsPoint2D.Point2D)     or isinstance(linePoint, Point2D) )     and\
         isinstance(text, str):
            self.__LinearDim.append( [ measurePoint1, measurePoint2, direction, linePoint, text ] )
      else:
        raise TypeError, DimensionSet.ErrorMessages[TypeError]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddAngleDim
#
#      PURPOSE:
#          To add angle dimension to the set
#
#      INPUT:
#          Parameters:
#           firstLine                     First leg (line) of a measure. Instance of Rline2D
#           secondLine                    Second leg (line) of a measure. Instance of Rline2D
#           drawFirst                     Flag for drawing first leg.  1 - draw, 0 - not draw
#           drawSecond                    Flag for drawing second leg. 1 - draw, 0 - not draw
#           linePoint                     A point locating the dimensioning arc. Instance of Point2D
#           textPoint                     A point locating the measure text. Instance of Point2D
#           text                          Measure text
#
# -----------------------------------------------------------------------------------------------------------------

   def AddAngleDim(self, firstLine, secondLine, linePoint, textPoint, text, drawFirst = 1, drawSecond = 1, drawDegree = 0):
      if ( isinstance(firstLine, KcsRline2D.Rline2D)  or isinstance(firstLine, Rline2D) )  and\
         ( isinstance(secondLine, KcsRline2D.Rline2D) or isinstance(secondLine, Rline2D) ) and\
         ( isinstance(drawFirst, int)  or isinstance(drawFirst, long)  or isinstance(drawFirst, float) )  and\
         ( isinstance(drawSecond, int) or isinstance(drawSecond, long) or isinstance(drawSecond, float) ) and\
         ( isinstance(drawDegree, int) or isinstance(drawDegree, long) or isinstance(drawDegree, float) ) and\
         ( isinstance(linePoint, KcsPoint2D.Point2D)  or isinstance(linePoint, Point2D))   and\
         ( isinstance(textPoint, KcsPoint2D.Point2D)  or isinstance(textPoint, Point2D))   and\
         isinstance(text, str):
            self.__AngleDim.append( [ firstLine, secondLine, linePoint, textPoint, text, drawFirst, drawSecond, drawDegree ] )
      else:
        raise TypeError, DimensionSet.ErrorMessages[TypeError]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddRadiusDim
#
#      PURPOSE:
#          To add radius dimension to the set
#
#      INPUT:
#          Parameters:
#           textPoint                     A point locating the measure text. Instance of Point2D
#           text                          Measure text
#
# -----------------------------------------------------------------------------------------------------------------

   def AddRadiusDim(self, textPoint, text):
      if ( isinstance(textPoint, KcsPoint2D.Point2D)  or isinstance(textPoint, Point2D))   and\
         isinstance(text, str):
            self.__RadiusDim.append( [ textPoint, text ] )
      else:
        raise TypeError, DimensionSet.ErrorMessages[TypeError]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddCustomDim
#
#      PURPOSE:
#          To add radius dimension to the set
#
#      INPUT:
#          Parameters:
#           textPoint                     A point locating the measure text. Instance of Point2D
#           text                          Measure text
#
# -----------------------------------------------------------------------------------------------------------------

   def AddCustomDim(self, textPoint, text):
      if ( isinstance(textPoint, KcsPoint2D.Point2D)  or isinstance(textPoint, Point2D))   and\
         isinstance(text, str):
            self.__CustomDim.append( [ textPoint, text ] )
      else:
        raise TypeError, DimensionSet.ErrorMessages[TypeError]

#-----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          Reset
#
#      PURPOSE:
#          To remove all elements from highlight set
#
#      INPUT:
#          Parameters:
#           None
# -----------------------------------------------------------------------------------------------------------------

   def Reset(self):
      self.__LinearDim  = []
      self.__AngleDim   = []
      self.__RadiusDim  = []
      self.__CustomDim  = []

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
# -----------------------------------------------------------------------------------------------------------------

   def __repr__(self):
      tup = (
         "Linear dimensions  : " + str(self.__LinearDim),
         "Angle dimensions   : " + str(self.__AngleDim),
         "Radius dimensions  : " + str(self.__RadiusDim),
         "Custom dimensions  : " + str(self.__CustomDim),
         )
      return string.join (tup,'\n')

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
#
#      CLASS NAME:
#          ProfileSketch
#
#      PURPOSE:
#          The ProfileSketch class is designed for storing profile settings
#          used by trig_hull_endcut_dim trigger to position endcut dimensions on the sketch
#
#      ATTRIBUTES:
#          private:
#           __ProfileType         integer           profile type
#           __ProfileParams       list              list of profile parameterss (six float values)
#           __EndcutType          integer           endcut type
#           __EndcutCode          integer           endcut code
#           __EndcutParams        list              list of endcut parameters (nine float values)
#           __EndcutRectangle     Rectangle2D       limiting rectangle for endcut dimensions
#           __FlangeCutRectangle  Rectangle2D       limiting rectangle for flange cut dimensions
#
#      METHODS:
#        GetProfileType                        Gets profile type
#        GetProfileParams                      Gets profile parameters
#        GetEndcutType                         Gets endcut type
#        GetEndcutCode                         Gets endcut code
#        GetEndcutParams                       Gets endcut parameters
#        GetEndcutRectangle                    Gets limiting rectangle for endcut
#        GetFlangeCutRectangle                 Gets limiting rectangle for flange cut

class ProfileSketch:

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
# -----------------------------------------------------------------------------------------------------------------

   def __init__(self):
      self.__ProfileType  = 0
      self.__ProfileParams = []
      self.__EndcutType = 0
      self.__EndcutCode = 0
      self.__EndcutParams = []
      self.__EndcutRectangle = None
      self.__FlangeCutRectangle = None
      self.__Excess = 0
      self.__SketchExcess = 0
      self.__BevelGapWeb = 0
      self.__BevelGapFlange = 0

   def GetProfileType(self):
      return self.__ProfileType

   def GetProfileParams(self):
      return self.__ProfileParams

   def GetEndcutType(self):
      return self.__EndcutType

   def GetEndcutCode(self):
      return self.__EndcutCode

   def GetEndcutParams(self):
      return self.__EndcutParams

   def GetEndcutRectangle(self):
      return self.__EndcutRectangle

   def GetFlangeCutRectangle(self):
      return self.__FlangeCutRectangle

   def GetExcess(self):
      return self.__Excess

   def GetSketchExcess(self):
      return self.__SketchExcess

   def GetBevelGapWeb(self):
      return self.__BevelGapWeb

   def GetBevelGapFlange(self):
      return self.__BevelGapFlange

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
# -----------------------------------------------------------------------------------------------------------------

   def __repr__(self):
      tup = (
         "Profile type         : " + str(self.__ProfileType),
         "Profile parameters   : " + str(self.__ProfileParams),
         "Endcut type          : " + str(self.__EndcutType),
         "Endcut code          : " + str(self.__EndcutCode),
         "Endcut parameters    : " + str(self.__EndcutParams),
         "Endcut rectangle     : " + str(self.__EndcutRectangle),
         "Flange cut rectangle : " + str(self.__FlangeCutRectangle),
         "Flange bevel gap     : " + str(self.__BevelGapFlange),
         "Web bevel gap        : " + str(self.__BevelGapWeb),
         "Excess               : " + str(self.__Excess),
         "Excess on sketch     : " + str(self.__SketchExcess),
         )
      return string.join (tup,'\n')
