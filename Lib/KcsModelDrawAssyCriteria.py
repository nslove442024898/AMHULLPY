## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsModelDrawAssyCriteria.py
#
#      PURPOSE:
#          The class holds information about a Assembly model to be draw
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __Name                  string            Assembly name
#          __Recursive             integer           1 - draw whole assembly recursively
#                                                    0 - draw only parts directly belonging to the chosen level
#          __Criteria              dictionary        criteria keys
#

import types
import string

ErrorMessages = { TypeError : 'not supported argument type, see documentation of ModelDrawAssyCriteria class',
                  ValueError: 'not supported model type, see documentation of ModelDrawAssyCriteria class' }

class ModelDrawAssyCriteria(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#
   def __init__(self, name = ""):
      self.__Name = name
      self.__Recursive = 1
      self.__Criteria = { 'PlanePanel' : 1, 'CurvedPanel' : 1, 'Pipe' : 1, 'Equipment' : 1,
                        'Cableway' : 1, 'Structure' : 1, 'PlacedVolume' : 1, 'Ventilation' : 1 }

#
#      METHOD:
#          SetAssemblyName
#
#      PURPOSE:
#          set assembly name
#
#      INPUT:
#          Parameters:
#           name        string            assembly name
#

   def SetAssemblyName(self, name):
      if type(name) != types.StringType:
         raise TypeError, ErrorMessages[TypeError]
      self.__Name = name

#
#      METHOD:
#          GetAssemblyName
#
#      PURPOSE:
#          gets assembly name
#
#      INPUT:
#          Parameters:
#              None
#
#      RETURNS:
#           Assembly name
#

   def GetAssemblyName(self):
      return self.__Name

#
#      METHOD:
#          IsRecursive
#
#      PURPOSE:
#          Returns:
#              1 if recursive mode is selected
#              0 if parts mode is selected
#
#      INPUT:
#          Parameters:
#              None
#

   def IsRecursive(self):
      if self.__Recursive:
         return 1
      else:
         return 0

#
#      METHOD:
#          SetRecursive
#
#      PURPOSE:
#          Set mode to:
#              1 - recursive mode
#              0 - parts mode
#
#      INPUT:
#          Parameters:
#              mode     integer     defines mode:
#                                      1 - recursive mode
#                                      0 - parts mode
#

   def SetRecursive(self, mode):
      if mode:
         self.__Recursive = 1
      else:
         self.__Recursive = 0

#
#      METHOD:
#          EnableModelType
#
#      PURPOSE:
#          This method should be use to set/clear flag for specified kind of model
#
#      INPUT:
#          Parameters:
#              type      string        model type
#              value     integer       value for that type:
#                                         0     - type not selected
#                                         <>0   - type selected
#
   def EnableModelType(self, modeltype, value):
      if modeltype not in self.__Criteria.keys():
         raise ValueError, ErrorMessages[ValueError]

      if type(value) != types.IntType and type(value) != types.LongType:
         raise TypeError, ErrorMessages[TypeError]

      self.__Criteria[modeltype] = value

#
#      METHOD:
#          IsModelTypeEnabled
#
#      PURPOSE:
#          Checks if specified model type is enabled
#
#      INPUT:
#          Parameters:
#              type      string        model type
#
#      RESULT:
#        0        -  model type not enabled
#        <>0      -  model type enabled
#
   def IsModelTypeEnabled(self, key):
      if key not in self.__Criteria.keys():
         raise ValueError, ErrorMessages[ValueError]
      if self.__Criteria[key]!=0:
         return 1
      else:
         return 0


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

      if not isinstance(other,ModelDrawAssyCriteria):
         raise TypeError, ErrorMessages[TypeError]

      if self.__Name != other.__Name:
         return 1
      if self.__Recursive != other.__Recursive:
         return 1
      for key in self.__Criteria.keys():
         if self.__Criteria[key] != other.__Criteria[key]:
            return 1
      return 0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
   def __repr__(self):
      tup = (
         'ModelDrawAssyCriteria:',
         '   name     : ' + str (self.__Name),
         '   recursive: ' + str (self.__Recursive),
         '   criteria : ' + str (self.__Criteria))
      return string.join (tup, '\n')

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Name = property (GetAssemblyName, SetAssemblyName, None, 'Name')
   Recursive = property (IsRecursive, SetRecursive, None, 'Recursive')
   def GetCriteria(self): return self.__Criteria
   Criteria = property (GetCriteria, None, None, 'Criteria')
