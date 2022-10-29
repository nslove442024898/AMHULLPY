## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsSymbol.py
#
#      PURPOSE:
#          The Symbol class holds information about a symbol.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __SymbolId          integer       symbol number
#          __FontId            integer       font number
#          __Visible           integer       determines if symbol is visible, 1 if visible otherwise 0
#          __Detectable        integer       determines if symbol is detectable, 1 if visible otherwise 0
#          __Colour            Colour        colour of symbol
#          __LineType          Linetype      linetype of symbol
#          __Layer             Layer         layer of symbol
#          __Position          Point2D       position of symbol
#          __Height            real          height of symbol:
#                                            > 0.0  height of symbol space, no deformation (width ignored)
#                                            < 0.0  height of symbol (absolute value)
#          __Width             real          width of symbol (relevant if height < 0.0):
#                                            <= 0.0  no deformation (width follows height proportionally)
#                                            >  0.0  width of symbol
#          __Rotation          real          rotation of symbol
#          __Reflection        integer       reflection of symbol

import math
import string
import KcsPoint2D
from KcsPoint2D     import Point2D
from KcsColour      import Colour
from KcsLinetype    import Linetype
from KcsLayer       import Layer
import kcs_draft

class Symbol(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          font        integer       font id
#          symbol      integer       symbol id

    def __init__(self, fontid=21, symbolid=1):
        self.__SymbolId       = symbolid
        self.__FontId         = fontid
        self.__Visible        = 1
        self.__Detectable     = 1
        self.__Colour         = kcs_draft.colour_get(Colour())
        self.__LineType       = Linetype()
        self.__Layer          = Layer()
        self.__Position       = Point2D(0, 0)
        self.__Height         = 1.0
        self.__Height         = kcs_draft.symbol_height_get()
        self.__Width          = -1.0
        self.__Rotation       = 0.0
        self.__Rotation       = kcs_draft.symbol_rotation_get()
        self.__Reflection     = 0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):


      if self.__Reflection == 0:
         reflectionMsg = 'None'
      elif self.__Reflection == 1:
         reflectionMsg = 'Reflection: in U axis'
      elif self.__Reflection == 2:
         reflectionMsg = 'Reflection: in V axis',
      else :
         reflectionMsg = ''


      tup = (
        'Symbol:'
        '   SymbolId:  ' + str(self.__SymbolId ),
        '   FontId:    ' + str(self.__FontId ),
        '   Colour:    ' + str(self.__Colour),
        '   LineType:  ' + str(self.__LineType),
        '   Layer:     ' + str(self.__Layer),
        '   Position:  ' + str(self.__Position ),
        '   Height:    ' + str(self.__Height ),
        '   Width:     ' + str(self.__Width ),
        '   Rotation:  ' + str(self.__Rotation ),
        '   Reflection:' + str(reflectionMsg),
        '   Visible:   ' + str(self.__Visible ),
        '   Detectable:' + str(self.__Detectable ))
      return string.join (tup, '\n')

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

    def __cmp__(self, other):

       if not isinstance(other, Symbol):
          return 1

       if self.__SymbolId != other.__SymbolId:
          return 1

       if self.__FontId != other.__FontId:
          return 1

       if self.__Colour != other.__Colour:
          return 1

       if self.__Layer != other.__Layer:
          return 1

       if self.__LineType != other.__LineType:
          return 1

       if self.__Position != other.__Position:
          return 1

       if self.__Height != other.__Height:
          return 1

       if self.__Width != other.__Width:
          return 1

       if self.__Rotation != other.__Rotation:
          return 1

       if self.__Reflection != other.__Reflection:
          return 1

       if self.__Visible != other.__Visible:
          return 1

       if self.__Detectable != other.__Detectable:
          return 1

       return 0

#
#
#      METHOD:
#         SetFontId
#
#      PURPOSE:
#          Set font id
#
#      INPUT:
#          Parameters:
#          fontid        integer       font
#
#      RESULT:
#          The font id will be set
#

    def SetFontId(self, fontid):
        self.__FontId = fontid

#
#      METHOD:
#         GetFontId
#
#      PURPOSE:
#          Get font id
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The font id will be returned
#

    def GetFontId(self):
        return self.__FontId

#
#      METHOD:
#         SetSymbolId
#
#      PURPOSE:
#          Set symbol id
#
#      INPUT:
#          Parameters:
#          symbolid        integer       symbol id
#
#      RESULT:
#          The symbol id will be set
#

    def SetSymbolId(self, symbolid):
        self.__SymbolId = symbolid

#
#      METHOD:
#         GetSymbolId
#
#      PURPOSE:
#          Get symbol id
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol id will be returned
#

    def GetSymbolId(self):
        return self.__SymbolId

#
#      METHOD:
#         SetVisible
#
#      PURPOSE:
#          Sets symbol visibility flag
#
#      INPUT:
#          Parameters:
#          visible        integer       if positive flag will be set to 1
#
#      RESULT:
#          The symbol visible flag will be set
#

    def SetVisible(self, visible):
        if visible>0:
            self.__Visible = 1
        else:
            self.__Visible = 0

#
#      METHOD:
#         IsVisible
#
#      PURPOSE:
#          Gets symbol visibility flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol visibility flag will be returned
#

    def IsVisible(self):
        return self.__Visible

#
#      METHOD:
#         SetDetectable
#
#      PURPOSE:
#          Sets symbol detectable flag
#
#      INPUT:
#          Parameters:
#          detectable        integer       if positive flag will be set to 1
#
#      RESULT:
#          The symbol detectable flag will be set
#

    def SetDetectable(self, detectable):
        if detectable>0:
            self.__Detectable = 1
        else:
            self.__Detectable = 0

#
#      METHOD:
#         IsDetectable
#
#      PURPOSE:
#          Gets symbol detectable flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol detectable flag will be returned
#

    def IsDetectable(self):
        return self.__Detectable

#
#      METHOD:
#         SetColour
#
#      PURPOSE:
#          Sets symbol colour
#
#      INPUT:
#          Parameters:
#          colour        Colour       new colour
#
#      RESULT:
#          The symbol colour will be set
#

    def SetColour(self, colour):
        self.__Colour = Colour(colour.ColourString)

#
#      METHOD:
#         GetColour
#
#      PURPOSE:
#          Gets symbol colour
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol colour will be returned
#

    def GetColour(self):
        return self.__Colour

#
#      METHOD:
#         SetLineType
#
#      PURPOSE:
#          Sets symbol linetype
#
#      INPUT:
#          Parameters:
#          linetype        Linetype       new linetype
#
#      RESULT:
#          The symbol linetype will be set
#

    def SetLineType(self, linetype):
        self.__LineType = Linetype(linetype.LinetypeString)

#
#      METHOD:
#         GetLineType
#
#      PURPOSE:
#          Gets symbol linetype
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol linetype will be returned
#

    def GetLineType(self):
        return self.__LineType

#
#      METHOD:
#         SetLayer
#
#      PURPOSE:
#          Sets symbol layer
#
#      INPUT:
#          Parameters:
#          layer        Layer       new layer
#
#      RESULT:
#          The symbol layer will be set
#

    def SetLayer(self, layer):
        self.__Layer = Layer(layer.LayerId)

#
#      METHOD:
#         GetLayer
#
#      PURPOSE:
#          Gets symbol layer
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol layer will be returned
#

    def GetLayer(self):
        return self.__Layer

#
#      METHOD:
#         SetPosition
#
#      PURPOSE:
#          Sets symbol position
#
#      INPUT:
#          Parameters:
#          position        Point2D       new symbol position
#
#      RESULT:
#          The symbol position will be set
#

    def SetPosition(self, position):
        if not isinstance(position,Point2D) and not isinstance(position, KcsPoint2D.Point2D):
            return None
        self.__Position = Point2D(position.X, position.Y)

#
#      METHOD:
#         GetPosition
#
#      PURPOSE:
#          Gets symbol position
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol position will be returned
#

    def GetPosition(self):
        return self.__Position

#
#      METHOD:
#         SetHeight
#         NOTE! Obsolete. Use method SetSpaceHeight instead!
#
#      PURPOSE:
#          Sets height of symbol space (no deformation, width will follow height proportionally)
#
#      INPUT:
#          Parameters:
#          height        real       new symbol space height
#
#      RESULT:
#          The symbol space height will be set
#

    def SetHeight(self, height):
        if math.fabs(height)!=0:
            self.__Height = math.fabs(height)
            self.__Width = -1.0
#
#      METHOD:
#         SetSpaceHeight
#
#      PURPOSE:
#          Sets height of symbol space (no deformation, width will follow height proportionally)
#
#      INPUT:
#          Parameters:
#          height        real       new symbol space height
#
#      RESULT:
#          The symbol space height will be set
#

    def SetSpaceHeight(self, height):
        if math.fabs(height)!=0:
            self.__Height = math.fabs(height)
            self.__Width = -1.0

#
#      METHOD:
#         SetTrueHeight
#
#      PURPOSE:
#          Sets true height of symbol (no deformation, width will follow height proportionally)
#
#      INPUT:
#          Parameters:
#          height        real       new true symbol height
#
#      RESULT:
#          The true symbol height will be set
#

    def SetTrueHeight(self, height):
        if math.fabs(height)!=0:
            self.__Height = -1.0 * math.fabs(height)
            self.__Width = -1.0

#
#      METHOD:
#         SetTrueHeigthAndWidth
#
#      PURPOSE:
#          Sets true height and width of symbol (symbol will be deformed)
#
#      INPUT:
#          Parameters:
#          height        real       new true symbol height
#          width         real       new true symbol width
#
#      RESULT:
#          The true symbol height and width will be set
#

    def SetTrueHeightAndWidth(self, height, width):
        if math.fabs(height)!=0 and math.fabs(width)!=0:
            self.__Height = -1.0 * math.fabs(height)
            self.__Width = math.fabs(width)

#
#      METHOD:
#         GetHeight
#
#      PURPOSE:
#          Gets height attribute of symbol
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The value of symbol height attribute will be returned:
#             > 0.0  height of symbol space, no deformation (width ignored)
#             < 0.0  height of symbol (absolute value)
#

    def GetHeight(self):
        return self.__Height

#
#      METHOD:
#         GetWidth
#
#      PURPOSE:
#          Gets width attribute of symbol
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The value of symbol width attribute will be returned:
#             <= 0.0  no deformation (width follows height proportionally)
#             >  0.0  width of symbol
#

    def GetWidth(self):
        return self.__Width

#
#      METHOD:
#         SetRotation
#
#      PURPOSE:
#          Sets symbol rotation
#
#      INPUT:
#          Parameters:
#          rotation        real       new symbol rotation
#
#      RESULT:
#          The symbol rotation will be set
#

    def SetRotation(self, rotation):
        self.__Rotation = (rotation % 360) + 0.0

#
#      METHOD:
#         GetRotation
#
#      PURPOSE:
#          Gets symbol rotation
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol rotation will be returned
#

    def GetRotation(self):
        return self.__Rotation

#
#      METHOD:
#         SetReflectionInUAxis
#
#      PURPOSE:
#          Sets symbol reflection in U axis
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol reflection in U axis will be set
#

    def SetReflectionInUAxis(self):
        self.__Reflection = 1

#
#      METHOD:
#         IsReflectedInUAxis
#
#      PURPOSE:
#          Checks symbol reflection in U axis
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          1 if symbol is reflected in U axis, otherwise 0
#

    def IsReflectedInUAxis(self):
        if self.__Reflection == 1:
            return 1
        else:
            return 0

#
#      METHOD:
#         SetReflectionInVAxis
#
#      PURPOSE:
#          Sets symbol reflection in V axis
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol reflection in V axis will be set
#

    def SetReflectionInVAxis(self):
        self.__Reflection = 2

#
#      METHOD:
#         IsReflectedInVAxis
#
#      PURPOSE:
#          Checks symbol reflection in V axis
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          1 if symbol is reflected in V axis, otherwise 0
#

    def IsReflectedInVAxis(self):
        if self.__Reflection == 2:
            return 1
        else:
            return 0

#
#      METHOD:
#         SetNoReflection
#
#      PURPOSE:
#          Clears symbol reflection
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The symbol reflection will be cleared
#

    def SetNoReflection(self):
        self.__Reflection = 0

#
#      METHOD:
#         IsReflected
#
#      PURPOSE:
#          Checks symbol reflection
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          1 if symbol is reflected, otherwise 0
#

    def IsReflected(self):
        if self.__Reflection != 0:
            return 1
        else:
            return 0

#-----------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    SymbolId    = property (GetSymbolId , SetSymbolId)
    FontId      = property (GetFontId , SetFontId)
    Visible     = property (IsVisible , SetVisible)
    Detectable  = property (IsDetectable , SetDetectable)
    SymColour   = property (GetColour , SetColour)
    SymLineType = property (GetLineType , SetLineType)
    SymLayer    = property (GetLayer , SetLayer)
    Position    = property (GetPosition , SetPosition)
    Height      = property (GetHeight)
    Width       = property (GetWidth)
    Rotation    = property (GetRotation , SetRotation)
    def GetReflection(self): return self.__Reflection
    def SetReflection(self,value):
        if not isinstance(value,int) or not value in [0,1,2]:
            return None
        self.__Reflection = value
    Reflection  = property (GetReflection , SetReflection)
