## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsText.py
#
#      PURPOSE:
#          The Text class holds information about a text.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __Visible           integer       determines if text is visible, 1 if visible otherwise 0
#          __Detectable        integer       determines if text is detectable, 1 if visible otherwise 0
#          __Colour            Colour        colour of text
#          __LineType          Linetype      linetype of text
#          __Layer             Layer         layer of text
#          __Position          Point2D       position of text
#          __Height            real          height of text
#          __Rotation          real          rotation of text
#          __Aspect            real          aspect of text
#          __Slanting          real          slanting of text
#          __Font              string        font of text
#          __String            string        string
#          __Bold              integer
#          __Italic            integer
#          __Underline         integer
#          __Strikeout         integer

import math
import string
import kcs_draft
from KcsPoint2D     import Point2D
from KcsColour      import Colour
from KcsLinetype    import Linetype
from KcsLayer       import Layer

import kcs_ic

class Text(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          text        string       text string


   def __init__(self, text=''):
      self.__String         = text
      self.__Visible        = 1
      self.__Detectable     = 1
      self.__Colour         = Colour()
      kcs_draft.colour_get(self.__Colour)
      self.__LineType       = Linetype()
      kcs_draft.linetype_get(self.__LineType)
      self.__Layer          = Layer(kcs_draft.layer_get())
      self.__Position       = Point2D(0, 0)
      self.__Height         = kcs_draft.text_height_get()
      self.__Rotation       = kcs_draft.text_rotation_get()
      self.__Aspect         = kcs_draft.text_aspect_get()
      self.__Slanting       = kcs_draft.text_slant_get()
      self.__Bold           = kcs_draft.text_bold_get()
      self.__Italic         = kcs_draft.text_italic_get()
      self.__Underline      = kcs_draft.text_underline_get()
      self.__Strikeout      = kcs_draft.text_strikeout_get()
      self.__Font           = 'TBSystemFont0'
      fontId = kcs_draft.text_ascii_font_get()
      try:
         self.__Font        = kcs_ic.font_name_get(fontId)
      except:
         print kcs_ic.error

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      tup = (
         'Text:',
         '   String:    ' + str(self.__String ),
         '   Colour:    ' + str(self.__Colour),
         '   LineType:  ' + str(self.__LineType),
         '   Layer:     ' + str(self.__Layer),
         '   Font:      ' + str(self.__Font ),
         '   Position:  ' + str(self.__Position ),
         '   Height:    ' + str(self.__Height ),
         '   Rotation:  ' + str(self.__Rotation ),
         '   Aspect:    ' + str(self.__Aspect ),
         '   Slanting:  ' + str(self.__Slanting ),
         '   Visible:   ' + str(self.__Visible ),
         '   Detectable:' + str(self.__Detectable ),
         '   Bold:      ' + str(self.__Bold ),
         '   Italic:    ' + str(self.__Italic ),
         '   Underline: ' + str(self.__Underline ),
         '   Strikeout: ' + str(self.__Strikeout ))
      return string.join (tup, '\n')

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      try:

         if not isinstance(other, Text):
            return 1

         if self.__String != other.__String:
            return 1

         if self.__Colour != other.__Colour:
            return 1

         if self.__LineType != other.__LineType:
            return 1

         if self.__Layer != other.__Layer:
            return 1

         if self.__Font != other.__Font:
            return 1

         if self.__Position != other.__Position:
            return 1

         if self.__Height != other.__Height:
            return 1

         if self.__Rotation != other.__Rotation:
            return 1

         if self.__Aspect != other.__Aspect:
            return 1

         if self.__Slanting != other.__Slanting:
            return 1

         if self.__Visible != other.__Visible:
            return 1

         if self.__Detectable != other.__Detectable:
            return 1

         if self.__Bold != other.__Bold:
            return 1

         if self.__Italic != other.__Italic:
            return 1

         if self.__Underline != other.__Underline:
            return 1

         if self.__Strikeout != other.__Strikeout:
            return 1

         return 0
      except:
         return 0
#
#      METHOD:
#         SetString
#
#      PURPOSE:
#          Sets text string
#
#      INPUT:
#          Parameters:
#          text        string       new text string
#
#      RESULT:
#          The text string will be set
#

   def SetString(self, text):
      self.__String = text

#
#      METHOD:
#         GetString
#
#      PURPOSE:
#          Gets text string
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text string will be returned
#

   def GetString(self):
      return self.__String

#
#      METHOD:
#         SetVisible
#
#      PURPOSE:
#          Sets text visibility flag
#
#      INPUT:
#          Parameters:
#          visible        integer       if positive flag will be set to 1
#
#      RESULT:
#          The text visible flag will be set
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
#          Gets text visibility flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text visibility flag will be returned
#

   def IsVisible(self):
      return self.__Visible

#
#      METHOD:
#         SetDetectable
#
#      PURPOSE:
#          Sets text detectable flag
#
#      INPUT:
#          Parameters:
#          detectable        integer       if positive flag will be set to 1
#
#      RESULT:
#          The text detectable flag will be set
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
#          Gets text detectable flag
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text detectable flag will be returned
#

   def IsDetectable(self):
      return self.__Detectable

#
#      METHOD:
#         SetColour
#
#      PURPOSE:
#          Sets text colour
#
#      INPUT:
#          Parameters:
#          colour        Colour       new colour
#
#      RESULT:
#          The text colour will be set
#

   def SetColour(self, colour):
      self.__Colour = Colour(colour.ColourString)

#
#      METHOD:
#         GetColour
#
#      PURPOSE:
#          Gets text colour
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text colour will be returned
#

   def GetColour(self):
      return self.__Colour

#
#      METHOD:
#         SetLineType
#
#      PURPOSE:
#          Sets text linetype
#
#      INPUT:
#          Parameters:
#          linetype        Linetype       new linetype
#
#      RESULT:
#          The text linetype will be set
#

   def SetLineType(self, linetype):
      self.__LineType = Linetype(linetype.LinetypeString)

#
#      METHOD:
#         GetLineType
#
#      PURPOSE:
#          Gets text linetype
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text linetype will be returned
#

   def GetLineType(self):
      return self.__LineType

#
#      METHOD:
#         SetLayer
#
#      PURPOSE:
#          Sets text layer
#
#      INPUT:
#          Parameters:
#          layer        Layer       new layer
#
#      RESULT:
#          The text layer will be set
#

   def SetLayer(self, layer):
      self.__Layer = Layer(layer.LayerId)

#
#      METHOD:
#         GetLayer
#
#      PURPOSE:
#          Gets text layer
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text layer will be returned
#

   def GetLayer(self):
      return self.__Layer

#
#      METHOD:
#         SetPosition
#
#      PURPOSE:
#          Sets text position
#
#      INPUT:
#          Parameters:
#          position        Point2D       new text position
#
#      RESULT:
#          The text position will be set
#

   def SetPosition(self, position):
      self.__Position = Point2D(position.X, position.Y)

#
#      METHOD:
#         GetPosition
#
#      PURPOSE:
#          Gets text position
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text position will be returned
#

   def GetPosition(self):
      return self.__Position

#
#      METHOD:
#         SetHeight
#
#      PURPOSE:
#          Sets text height
#
#      INPUT:
#          Parameters:
#          height        real       new text height
#
#      RESULT:
#          The text height will be set
#

   def SetHeight(self, height):
      if math.fabs(height)!=0:
         self.__Height = math.fabs(height)

#
#      METHOD:
#         GetHeight
#
#      PURPOSE:
#          Gets text height
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text height will be returned
#

   def GetHeight(self):
      return self.__Height

#
#      METHOD:
#         SetRotation
#
#      PURPOSE:
#          Sets text rotation
#
#      INPUT:
#          Parameters:
#          rotation        real       new text rotation
#
#      RESULT:
#          The text rotation will be set
#

   def SetRotation(self, rotation):
      self.__Rotation = (rotation % 360) + 0.0

#
#      METHOD:
#         GetRotation
#
#      PURPOSE:
#          Gets text rotation
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text rotation will be returned
#

   def GetRotation(self):
      return self.__Rotation

#
#      METHOD:
#         SetAspect
#
#      PURPOSE:
#          Sets text aspect
#
#      INPUT:
#          Parameters:
#          aspect        real       new text aspect
#
#      RESULT:
#          The text rotation will be set
#

   def SetAspect(self, aspect):
      self.__Aspect = aspect + 0.0

#
#      METHOD:
#         GetAspect
#
#      PURPOSE:
#          Gets text aspect
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text aspect will be returned
#

   def GetAspect(self):
      return self.__Aspect

#
#      METHOD:
#         SetSlanting
#
#      PURPOSE:
#          Sets text slanting
#
#      INPUT:
#          Parameters:
#          slanting        real       new text slanting
#
#      RESULT:
#          The text slanting will be set
#

   def SetSlanting(self, slanting):
      if slanting>=0 and slanting<=180:
         self.__Slanting = slanting + 0.0

#
#      METHOD:
#         GetSlanting
#
#      PURPOSE:
#          Gets text slanting
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text slanting will be returned
#

   def GetSlanting(self):
      return self.__Slanting

#
#      METHOD:
#         SetFont
#
#      PURPOSE:
#          Sets text font
#
#      INPUT:
#          Parameters:
#          font        string       new text font
#
#      RESULT:
#          The text font will be set
#

   def SetFont(self, font):
      self.__Font = font

#
#      METHOD:
#         GetFont
#
#      PURPOSE:
#          Gets text font
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The text font will be returned
#

   def GetFont(self):
      return self.__Font

   def SetBold(self, bold):
      self.__Bold = bold
   def GetBold(self):
      return self.__Bold

   def SetItalic(self, italic):
      self.__Italic = italic
   def GetItalic(self):
      return self.__Italic

   def SetUnderline(self, underline):
      self.__Underline = underline
   def GetUnderline(self):
      return self.__Underline

   def SetStrikeout(self, strikeout):
      self.__Strikeout = strikeout
   def GetStrikeout(self):
      return self.__Strikeout

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   String         = property ( GetString, SetString)
   Visible        = property ( IsVisible, SetVisible)
   Detectable     = property ( IsDetectable, SetDetectable)
   TextColour     = property ( GetColour, SetColour)
   TextLineType   = property ( GetLineType, SetLineType)
   TextLayer      = property ( GetLayer, SetLayer)
   Position       = property ( GetPosition, SetPosition)
   Height         = property ( GetHeight, SetHeight)
   Rotation       = property ( GetRotation, SetRotation)
   Aspect         = property ( GetAspect, SetAspect)
   Slanting       = property ( GetSlanting, SetSlanting)
   Font           = property ( GetFont, SetFont)
   Bold           = property ( GetBold, SetBold)
   Italic         = property ( GetItalic, SetItalic)
   Underline      = property ( GetUnderline, SetUnderline)
   Strikeout      = property ( GetStrikeout, SetStrikeout)
