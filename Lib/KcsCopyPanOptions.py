## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsCopyPanOptions.py
#
#      PURPOSE:
#          The class holds information about a Copying Panel Options
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES

from KcsMovePanOptions import MovePanOptions
import types

class CopyPanOptions(MovePanOptions):
   'class holds information about Copying Panel Options'
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

   def __init__(self):
      'to create instance of the class'
      MovePanOptions.__init__(self)
      self.__Dictionary          = {}
      self.__BlockName           = ''

#      METHOD:
#           SetNameMapping
#
#      PURPOSE:
#          Sets Old Name and NewName Pairs

   def SetNameMapping(self, dict):
      'sets Dictionary Arguments'
      if type(dict) != types.DictionaryType:
         raise TypeError, CopyPanOptions.__ErrorMessages[TypeError]
      self.__Dictionary = dict
      for item in dict.keys():
         if type(item) != type("") or type(dict[item]) != type(""):
            raise TypeError, CopyPanOptions.__ErrorMessages[TypeError]


#-------------------------------------------------------------------

   def GetNameMapping(self):
      'gets Panels Names Dictionary'
      return   self.__Dictionary

#-------------------------------------------------------------------

#
#      METHOD:
#           SetBlockName
#
#      PURPOSE:
#          Sets Block Name

   def SetBlockName(self, name):
      if type(name) != types.StringType:
         raise TypeError, CopyPanOptions.__ErrorMessages[TypeError]
      self.__BlockName             = name

#-------------------------------------------------------------------

   def GetBlockName(self):
      'gets Block Name'
      return   self.__BlockName

#-------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   Dictionary    = property (GetNameMapping, SetNameMapping, None, 'Old Name and NewName Pairs')
   BlockName     = property (GetBlockName, SetBlockName, None, 'Block Name')

