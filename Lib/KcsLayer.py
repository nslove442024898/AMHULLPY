## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsLayer.py
#
#      PURPOSE:
#          The Layer class holds information about a layer.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __LayerId          integer       layer id


import types
try:
   import kcs_ic
except:
   pass

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Layer class' }

class Layer(object):
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
#          layerid        integer       layer id

   def __init__(self, layerid=1):
      if type(layerid) != types.IntType:
         raise TypeError, ErrorMessages[TypeError]
      self.__LayerId = layerid

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Layer: %s\n' % self.__LayerId

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         SetLayer
#
#      PURPOSE:
#          Set layer id
#
#      INPUT:
#          Parameters:
#          layer        integer       layer id
#
#      RESULT:
#          The layer id will be set
#

   def SetLayer(self, layerid):
      if type(layerid) != types.IntType:
         raise TypeError, ErrorMessages[TypeError]
      self.__LayerId = layerid

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetLayer
#
#      PURPOSE:
#          Get layer id
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The layer id will be returned
#

   def GetLayer(self):
      return self.__LayerId

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetDescription
#
#      PURPOSE:
#          Get layer desription
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          The layer desription will be returned
#

   def GetDescription(self):
      desc = ''
      try:
         desc = kcs_ic.layer_desc_get(self.__LayerId)
      except:
         print kcs_ui.error
      return desc

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

      if not isinstance(other,Layer):
         raise TypeError, ErrorMessages[TypeError]

      if self.__LayerId < other.__LayerId:
         return -1
      elif self.__LayerId > other.__LayerId:
         return 1
      else:
         return 0

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   LayerId = property (GetLayer, SetLayer, None, 'LayerId - layer id')
