## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsObject.py
#
#      PURPOSE:
#          The class holds information about an database object
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __Name
#           __Code1
#           __Code2
#           __DateTime
#           __Size
#
#      MEHTODS:
#           SetName
#           GetName
#           SetCode1
#           GetCode1
#           SetCode2
#           GetCode2
#           __SetSize
#           GetSize
#           SetDate
#           GetDate


import types
import string
import copy

from KcsDateTime import DateTime

class Object(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Object class',
                     ValueError: 'not supported value type, see documentation of Object class' }

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
      'creates instance of Object class'
      self.__Name = ''
      self.__Code1 = 0
      self.__Code2 = 0
      self.__DateTime = DateTime()
      self.__Size = 0

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      'implements cmp(o1, o2) function'

      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, Object):
         raise TypeError, self.__ErrorMessages[TypeError]

      if string.lower(self.__Name) != string.lower(other.__Name):
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
      'returns string representation of Object instance'

      tup = (
         'Object:',
         '   Name: ' + self.__Name,
         '   Code1: ' + str(self.__Code1),
         '   Code2: ' + str(self.__Code2),
         '   ' + str(self.__DateTime),
         '   Size: ' + str(self.__Size)
         )
      return string.join(tup, '\n')

#
#      METHOD:
#          SetName
#
#      PURPOSE:
#          To set object's name
#
#      ARGUMENTS:
#          name           string             object name
#
   def SetName(self, name):
      'sets name of object'

      if type(name) != type(''):
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Name = name

#
#      METHOD:
#          GetName
#
#      PURPOSE:
#          Returns name of object
#
   def GetName(self):
      'returns name of object'
      return self.__Name

#
#      METHOD:
#          SetCode1
#
#      PURPOSE:
#          To set object's code1
#
#      ARGUMENTS:
#          code           integer             object code1
#
   def SetCode1(self, code):
      'sets code1 of object'
      if type(code) != type(1):
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Code1 = code

#
#      METHOD:
#          GetCode1
#
#      PURPOSE:
#          Returns code1 of object
#
   def GetCode1(self):
      'returns code1 of object'
      print 'in'
      print 'code', self.__Code1
      return self.__Code1

#
#      METHOD:
#          SetCode2
#
#      PURPOSE:
#          To set object's code2
#
#      ARGUMENTS:
#          code           integer             object code2
#
   def SetCode2(self, code):
      'sets code1 of object'
      if type(code) != type(1):
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Code2 = code

#
#      METHOD:
#          GetCode2
#
#      PURPOSE:
#          Returns code1 of object
#
   def GetCode2(self):
      'returns code1 of object'
      return self.__Code2

#
#      METHOD:
#          __SetSize
#
#      PURPOSE:
#          To set object's size
#
#      ARGUMENTS:
#          size           integer             object size
#
   def __SetSize(self, size):
      'sets size of object'
      if type(size) != type(1):
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Size = size

#
#      METHOD:
#          GetSize
#
#      PURPOSE:
#          Returns size of object
#
   def GetSize(self):
      'returns size of object'
      return self.__Size

#
#      METHOD:
#          SetCreationDate
#
#      PURPOSE:
#          To set object's creation date and time
#
#      ARGUMENTS:
#          date           DateTime     date of creation object
#
   def SetCreationDate(self, date):
      'sets creation date and time of object'
      if not isinstance(date, DateTime):
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DateTime = copy.deepcopy(date)

#
#      METHOD:
#          GetCreationDate
#
#      PURPOSE:
#          Returns creation date and time of object
#
   def GetCreationDate(self):
      'returns creation date and time of object'
      return copy.deepcopy(self.__DateTime)

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Name = property (GetName, SetName, None, 'Name')
   Code1 = property (GetCode1, SetCode1, None, 'Code1')
   Code2 = property (GetCode2, SetCode2, None, 'Code2')
   CreationDate = property (GetCreationDate, SetCreationDate, None, 'DateTime')
   Size = property (GetSize, None, None, 'Size')
