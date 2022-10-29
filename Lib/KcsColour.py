## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsColour.py
#
#      PURPOSE:
#          The class holds information about a Colour.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          ColourString            string           The colour

import types
try:
   import kcs_ic
   SystemColourStrings = kcs_ic.colour_names_get()
except:
   SystemColourStrings = []

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Colour class',
                  ValueError: 'wrong colour name, see documentationo of Colour class' }
ColourStrings = ['White', 'Cyan', 'Blue', 'Magenta', 'Red', 'Yellow', 'Green', 'Black', 'Wheat', 'MediumAquamarine', 'NavyBlue',
                 'DarkOrchid', 'Firebrick', 'Orange', 'ForestGreen', 'DimGrey', 'UserColour1', 'UserColour2', 'UserColour3',
                 'UserColour4', 'UserColour5', 'UserColour6', 'UserColour7', 'UserColour8', 'UserColour9', 'UserColour10',
                 'UserColour11', 'UserColour12', 'UserColour13', 'UserColour14', 'UserColour15', 'UserColour16']


class Colour(object):

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
#          colour              The name of the colour
#                              Valid colours are:
#
#                                 "White"
#                                 "Cyan"
#                                 "Blue"
#                                 "Magenta"
#                                 "Red"
#                                 "Yellow"
#                                 "Green"
#                                 "Black"
#                                 "Wheat"
#                                 "MediumAquamarine"
#                                 "NavyBlue"
#                                 "DarkOrchid"
#                                 "Firebrick"
#                                 "Orange"
#                                 "ForestGreen"
#                                 "DimGrey"
#                                 "UserColour1"   (Default: "Tan")
#                                 "UserColour2"   (Default: "Aquamarine")
#                                 "UserColour3"   (Default: "SlateBlue")
#                                 "UserColour4"   (Default: "Violet")
#                                 "UserColour5"   (Default: "IndianRed")
#                                 "UserColour6"   (Default: "Gold")
#                                 "UserColour7"   (Default: "LimeGreen")
#                                 "UserColour8"   (Default: "Grey")
#                                 "UserColour9"   (Default: "Sienna")
#                                 "UserColour10"  (Default: "Turquoise")
#                                 "UserColour11"  (Default: "LightBlue")
#                                 "UserColour12"  (Default: "BlueViolet")
#                                 "UserColour13"  (Default: "Pink")
#                                 "UserColour14"  (Default: "Coral")
#                                 "UserColour15"  (Default: "SpringGreen")
#                                 "UserColour16"  (Default: "LightGrey")


   def __init__(self, colour = "Green"):
      self.ColourString = colour

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'ColourString: %s\n' % self.ColourString

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#        SetName
#
#      PURPOSE:
#          To set the name of the colour
#
#      INPUT:
#          Parameters:
#          colour                      string            Name of colour
#
#      RESULT:
#          The name of the colour will be set
#
   def SetName(self, colour):
      if type(colour) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]

      if  colour not in ColourStrings and colour not in SystemColourStrings:
         #check ignoring letter case
         found = 0
         for item in SystemColourStrings:
            if item.lower() == colour.lower():
               colour = item
               found = 1
               break
         if found == 0:
            raise ValueError, ErrorMessages[ValueError]

      self.__ColourString = colour

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#        GetName
#
#      PURPOSE:
#          To deliver the name of the colour
#
#      RESULT:
#          Returns:
#          string                The name of the colour
#

   def GetName(self):
      return self.__ColourString

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#        Name - obsolete
#
#      PURPOSE:
#          To deliver the name of the colour
#
#      RESULT:
#          Returns:
#          string                The name of the colour
#
   def Name(self):
      return (self.ColourString)


# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, Colour):
         raise TypeError, ErrorMessages[TypeError]

      if self.ColourString != other.ColourString:
         return 1
      else:
         return 0

# -----------------------------------------------------------------------------------------------------------------
#  Properties
# -----------------------------------------------------------------------------------------------------------------

   ColourString  = property (GetName, SetName, None, 'ColourString - the name of the colour')
