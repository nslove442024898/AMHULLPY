## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsModel.py
#
#      PURPOSE:
#          The class holds information about a Model
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          Type                  string            Model type
#                                                  Valid types are:
#                                                     "plane panel"
#                                                     "hull curve"
#                                                     "pipe"
#                                                     "pipe spool"
#                                                     "equipment"
#                                                     "cable way"
#                                                     "cable"
#                                                     "penetration"
#                                                     "struct"
#                                                     "placed volume"
#                                                     "longitudinal"
#                                                     "transversal"
#                                                     "ventilation"
#                                                     "subsurface"
#                                                     "lines fairing curve"
#                                                     "accommodation"
#                                                     "curved panel"
#                                                     "assembly"
#                                                     "curved plate"
#                                                     "plane"
#                                                     "curved stiffener"
#                                                     "space general"
#                                                     "room"
#                                                     "weld table"
#          Name                  string            Name of the model
#          PartType              string            Model part type
#                                                  Valid part types are:
#                                                     "panel"
#                                                     "boundary"
#                                                     "hole"
#                                                     "bracket"
#                                                     "plate"
#                                                     "notch"
#                                                     "seam"
#                                                     "stiffener"
#                                                     "flange"
#                                                     "pillar"
#                                                     "bead"
#                                                     "cutout"
#                                                     "excess"
#                                                     "hole/notch/cutout"
#                                                     "point"
#                                                     "curve"
#                                                     "welded joint"
#                                                     "tubi"
#                                                     "unknown"
#          PartId                integer           Part ID
#          SubPartType           string            Model subpart type
#                                                  Valid subpart types are:
#                                                     ""
#                                                     "limit"
#                                                     "crossmark"
#          SubPartId             integer           Subpart ID
#          ReflCode              integer           Reflection code (relevant for hull)
#                                                  Valid codes are:
#                                                     0 = not reflected
#                                                     1 = reflected
#                                                     2 = both parts

import types
import string


class Model(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Model class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          type                    Model type
#          name                    Name of the model
#          part_type               Model part type
#          part_id                 Part ID
#          subpart_type            Model subpart type
#          subpart_id              Subpart ID
#          refl_code               Reflection code
#
   def __init__(self, type = "", name = ""):
      self.Type = type
      self.Name = name
      self.PartType = ""
      self.PartId = 0
      self.SubPartType = ""
      self.SubPartId = 0
      self.ReflCode = 0


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

      if not isinstance(other, Model):
         raise TypeError, Model.__ErrorMessages[TypeError]

      if string.lower(self.Type) != string.lower(other.Type):
         return 1
      if string.lower(self.Name) != string.lower(other.Name):
         return 1
      if string.lower(self.PartType) != string.lower(other.PartType):
         return 1
      if self.PartId != other.PartId:
         return 1
      if string.lower(self.SubPartType) != string.lower(other.SubPartType):
         return 1
      if self.SubPartId != other.SubPartId:
         return 1
      if self.ReflCode != other.ReflCode:
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
      'returns string representation of Model instance'

      tup = (
         'Model:',
         '   Type: ' + self.Type,
         '   Name: ' + self.Name,
         '   PartType: ' + self.PartType,
         '   PartId: ' + str(self.PartId),
         '   SubPartType: ' + self.SubPartType,
         '   SubPartId: ' + str(self.SubPartId),
         '   ReflCode: ' + str(self.ReflCode),
         )
      return string.join(tup, '\n')

#
#      METHOD:
#        SetType
#
#      PURPOSE:
#          To set the model type
#
#      INPUT:
#          Parameters:
#          type                  string            Model type
#
#      RESULT:
#          The model type will be set
#
   def SetType(self, modeltype):
      if type(modeltype) != types.StringType:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__Type = modeltype


#
#      METHOD:
#        GetType
#
#      PURPOSE:
#          To deliver the model type
#
#      RESULT:
#          Returns:
#          string                The model type
#
   def GetType(self):
      return (self.__Type)


#
#      METHOD:
#        SetName
#
#      PURPOSE:
#          To set the model name
#
#      INPUT:
#          Parameters:
#          name                  string            Model name
#
#      RESULT:
#          The model name will be set
#
   def SetName(self, name):
      if type(name) != types.StringType:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__Name = name


#
#      METHOD:
#        GetName
#
#      PURPOSE:
#          To deliver the model name
#
#      RESULT:
#          Returns:
#          string                The model name
#
   def GetName(self):
      return (self.__Name)


#
#      METHOD:
#        SetPartType
#
#      PURPOSE:
#          To set the model part type
#
#      INPUT:
#          Parameters:
#          parttype                  string                The model part type
#
#      RESULT:
#          The model part type will be set
#
   def SetPartType(self, parttype):
      if type(parttype) != types.StringType:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__PartType = parttype

#
#      METHOD:
#        GetPartType
#
#      PURPOSE:
#          To deliver the model part type
#
#      RESULT:
#          Returns:
#          string                The model part type
#
   def GetPartType(self):
      return (self.__PartType)

#
#      METHOD:
#        SetPartId
#
#      PURPOSE:
#          To set the model part ID
#
#      INPUT:
#          Parameters:
#          id                  integer                The model part ID
#
#      RESULT:
#          The model part ID will be set
#
   def SetPartId(self, id):
      if type(id) not in [types.IntType, types.LongType]:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__PartId = id


#
#      METHOD:
#        GetPartId
#
#      PURPOSE:
#          To deliver the model part ID
#
#      RESULT:
#          Returns:
#          integer                The model part ID
#
   def GetPartId(self):
      return (self.__PartId)

#
#      METHOD:
#        SetSubPartType
#
#      PURPOSE:
#          To set the model subpart type
#
#      INPUT:
#          Parameters:
#          subparttype                  string                The model subpart type
#
#      RESULT:
#          The model subpart type will be set
#
   def SetSubPartType(self, subparttype):
      if type(subparttype) != types.StringType:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__SubPartType = subparttype

#
#      METHOD:
#        GetSubPartType
#
#      PURPOSE:
#          To deliver the model subpart type
#
#      RESULT:
#          Returns:
#          string                The model subpart type
#
   def GetSubPartType(self):
      return (self.__SubPartType)

#
#      METHOD:
#        SetSubPartId
#
#      PURPOSE:
#          To set the model subpart ID
#
#      INPUT:
#          Parameters:
#          id                  integer                The model subpart ID
#
#      RESULT:
#          The model subpart ID will be set
#
   def SetSubPartId(self, id):
      if type(id) not in [types.IntType, types.LongType]:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__SubPartId = id

#
#      METHOD:
#        GetSubPartId
#
#      PURPOSE:
#          To deliver the model subpart ID
#
#      RESULT:
#          Returns:
#          integer                The model subpart ID
#
   def GetSubPartId(self):
      return (self.__SubPartId)


#
#      METHOD:
#        SetReflCode
#
#      PURPOSE:
#          To set the reflection code
#
#      INPUT:
#          Parameters:
#          reflcode        integer                The reflection code
#
   def SetReflCode(self, reflcode):
      if type(reflcode) != types.IntType:
         raise TypeError, Model.__ErrorMessages[TypeError]
      self.__ReflCode = reflcode


#
#      METHOD:
#        GetReflCode
#
#      PURPOSE:
#          To deliver the reflection code
#
#      RESULT:
#          Returns:
#          integer                The reflection code
#
   def GetReflCode(self):
      return (self.__ReflCode)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Type = property (GetType, SetType, None, 'Type')
   Name = property (GetName, SetName, None, 'Name')
   PartType = property (GetPartType, SetPartType, None, 'PartType')
   PartId = property (GetPartId, SetPartId, None, 'PartId')
   SubPartType = property (GetSubPartType, SetSubPartType, None, 'SubPartType')
   SubPartId = property (GetSubPartId, SetSubPartId, None, 'SubPartId')
   ReflCode = property (GetReflCode, SetReflCode,None, 'ReflCode')
