## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsLinetype.py
#
#      PURPOSE:
#          The class holds information about a line type.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          LinetypeString           string           The line type

import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Linetype class',
                  ValueError: 'wrong linetype name, see documentationo of Linetype class' }

# -----------------------------------------------------------------------------------------------------------------
# function returns dictionary with all line type names:  { 'system name' : 'alias name', ... }
# -----------------------------------------------------------------------------------------------------------------
def GetLinetypes():
   try:
      import kcs_ic
      return kcs_ic.linetypes_get()
   except:
      return  {'Solid': 'Solid'}
# -----------------------------------------------------------------------------------------------------------------
# function returns line type alias name for given system name
# -----------------------------------------------------------------------------------------------------------------
def GetAliasName(name):
   if type(name) != type(''):
      raise TypeError, ErrorMessages[TypeError]
   dict = GetLinetypes()
   if name in dict.keys():
      return dict[name]
   if name in dict.values():
      return name
   return ''

# -----------------------------------------------------------------------------------------------------------------
# function returns line type system name for given alias name
# -----------------------------------------------------------------------------------------------------------------
def GetSystemName(name):
   if type(name) != type(''):
      raise TypeError, ErrorMessages[TypeError]
   dict = GetLinetypes()
   if name in dict.values():
      return dict.keys()[dict.values().index(name)]
   if name in dict.keys():
      return name
   return ''


class Linetype(object):

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
#          linetype              The name of the line type. It can be system name as well as alias name

   def __init__(self, linetype = "Solid"):
      if type(linetype) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]
      if linetype not in GetLinetypes().keys() and linetype not in GetLinetypes().values():
         raise ValueError, ErrorMessages[ValueError]
      self.LinetypeString = linetype


#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'LinetypeString: %s\n' % self.LinetypeString

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#        SetName
#
#      PURPOSE:
#          To set the name of the line type
#
#      INPUT:
#          Parameters:
#          name                 string            Name of linetype
#
#      RESULT:
#          The name of the line type will be set
#

   def SetName(self, name):
      if type(name) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]
      elif name not in GetLinetypes().keys() and name not in GetLinetypes().values():
         raise ValueError, ErrorMessages[ValueError]
      self.__LinetypeString = name

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#        Name
#
#      PURPOSE:
#          To deliver the name of the line type
#
#      RESULT:
#          Returns:
#          string                The name of the line type
#
   def Name(self):
      return (self.__LinetypeString)


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

      if not isinstance(other,Linetype):
         raise TypeError, ErrorMessages[TypeError]

      # find system names and compare
      name1 = GetSystemName(self.LinetypeString)
      name2 = GetSystemName(other.LinetypeString)
      if name1 != '' and name2 != '':
         if name1 != name2:
            return 1
         else:
            return 0

      # if names not found just compare given strings
      if self.LinetypeString != other.LinetypeString:
         return 1
      else:
         return 0

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   LinetypeString = property (Name, SetName, None, 'LinetypeString - system or alias name of line type')
