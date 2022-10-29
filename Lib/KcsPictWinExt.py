## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPictWinExt.py
#
#      PURPOSE:
#          The class holds information about picture element window extension.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          PictWinExtString            string

import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of PictWinExt class',
                  ValueError: 'wrong PictWinExt name, see documentationo of PictWinExt class' }
PictWinExtStrings = ['Small', 'Big', 'Infinite']

class PictWinExt(object):

# -----------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          extension           The named extension level
#                              Valid extensions are:
#
#                                 "Small"
#                                 "Big"
#                                 "Infinite"

   def __init__(self, extension = "Small"):
      if type(extension) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]
      if extension not in PictWinExtStrings:
         raise ValueError, ErrorMessages[ValueError]
      self.PictWinExtString = extension

# -----------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'PictWinExtString: %s\n' % self.PictWinExtString

# -----------------------------------------------------------------------------
#
#      METHOD:
#        SetExtension
#
#      PURPOSE:
#          To set the extension level
#
#      INPUT:
#          Parameters:
#          extension                    string
#
#      RESULT:
#          The named extension level will be set
#
   def SetExtension(self, extension):
      if type(extension) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]
      if extension not in PictWinExtStrings:
         raise ValueError, ErrorMessages[ValueError]
      self.PictWinExtString = extension

# -----------------------------------------------------------------------------
#
#      METHOD:
#        Extension
#
#      PURPOSE:
#          To deliver the named extension level
#
#      RESULT:
#          Returns:
#          string                The named picture extension level
#
   def Extension(self):
      return (self.PictWinExtString)


# -----------------------------------------------------------------------------
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

      if not isinstance(other,PictWinExt):
         raise TypeError, ErrorMessages[TypeError]

      if self.PictWinExtString == other.PictWinExtString:
         return 0
      elif self.PictWinExtString == 'Small':
         return -1
      elif self.PictWinExtString == 'Big' and other.PictWinExtString == 'Infinite':
         return -1
      else:
         return 1

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   ExtString = property (Extension, SetExtension, None, '')
