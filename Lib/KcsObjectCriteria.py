## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsObjectCriteria.py
#
#      PURPOSE:
#          The class holds information about an object
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __Name
#           __Code1
#           __Code2
#           __CreationDate
#           __Size
#
#      MEHTODS:
#           SetName
#           GetName
#           SetCode1
#           GetCode1
#           SetCode2
#           GetCode2
#           SetSize
#           GetSize
#           SetCreationDate
#           GetCreationDate


import types
import string
import copy

from KcsDateTime import DateTime

class ObjectCriteria(object):

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of ObjectCriteria class',
                     ValueError: 'not supported value type, see documentation of ObjectCriteria class' }

   __SignDefinition = { '=' : 1, '>' : 2, '>=' : 3, '<' : 4, '<=' : 5 }

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
      'creates instance of ObjectCriteria class'
      self.__Name = None
      self.__Code1 = None
      self.__Code2 = None
      self.__CreationDate = None
      self.__Size = None

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

      if not isinstance(other, ObjectCriteria):
         raise TypeError, self.__ErrorMessages[TypeError]

      if type(self.__Name) != type(other.__Name):
         return 1
      if type(self.__Name) != type(None) and string.lower(self.__Name) != string.lower(other.__Name):
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
      'returns string representation of ObjectCriteria instance'

      if self.__CreationDate == None:
         datestr = str(None)
      else:
         if type(self.__CreationDate[0]) == type(1):
            sign = ObjectCriteria.__SignDefinition.keys()[ObjectCriteria.__SignDefinition.values().index(self.__CreationDate[0])]
            date = self.__CreationDate[1]
            datestr = sign + ' ' + ( '%04d-%02d-%02d' % date.GetDate() )
         else:
            date1 = self.__CreationDate[0]
            date2 = self.__CreationDate[1]
            datestr = ( '%04d-%02d-%02d' % date1.GetDate() ) + ' - ' + ( '%04d-%02d-%02d' % date2.GetDate() )

      if self.__Size == None:
         sizestr = 'None'
      else:
         sizetup = self.GetSize()
         sizestr = sizetup[0] + ' ' + str(sizetup[1])

      tup = (
         'ObjectCriteria:',
         '   Name: ' + str(self.__Name),
         '   Code1: ' + str(self.__Code1),
         '   Code2: ' + str(self.__Code2),
         '   Creation date: ' + datestr,
         '   Size: ' + sizestr
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
#          name           string or None            object name
#
   def SetName(self, name):
      'sets name of object'
      if type(name) != type('') and type(name) != type(None):
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
#          code           integer or None             object code1
#
   def SetCode1(self, code):
      'sets code1 of object'
      if type(code) != type(1) and type(code) != type(None):
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
      if type(code) != type(1) and type(code) != type(None):
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
#          SetSize
#
#      PURPOSE:
#          To set size criteria
#
#      ARGUMENTS:
#          sign, size           string, integer             sign and size
#
   def SetSize(self, *args):
      'sets size criteria'
      if len(args)==1:
         if args[0] == None:
            self.__Size = None
         elif type(args[0]) == type(0):
            self.SetSize('=', args[0])
         else:
            raise TypeError, self.__ErrorMessages[TypeError]
      elif len(args) == 2:
         if type(args[0]) != type('') or type(args[1]) != type(0):
            raise TypeError, self.__ErrorMessages[TypeError]
         if args[0] not in ObjectCriteria.__SignDefinition.keys():
            raise ValueError, ObjectCriteria.__ErrorMessages[ValueError]
         self.__Size = (ObjectCriteria.__SignDefinition[args[0]], args[1])
      else:
         raise TypeError, self.__ErrorMessages[TypeError]

#
#      METHOD:
#          GetSize
#
#      PURPOSE:
#          Returns size of object as:
#              2. tuple of sign and size
#              3. None, if not set
#

   def GetSize(self):
      'returns creation date and time criteria'
      if self.__Size == None:
         return None
      else:
         sign = ObjectCriteria.__SignDefinition.keys()[ObjectCriteria.__SignDefinition.values().index(self.__Size[0])]
         return (sign, self.__Size[1])

#
#      METHOD:
#          SetCreationDate
#
#      PURPOSE:
#          To set creation date and time criteria
#
#      ARGUMENTS:
#          start, end     DateTime                 start and end creation dates
#            or
#          sign, date     string, DateTime         sign and creation date
#            or
#          None                                    creation date will not be used as criteria
#

   def SetCreationDate(self, *args):
      'sets creation date criteria, arguments: 1. start, end dates   2. sign, date   3. None'

      if len(args)==1:
         if args[0] == None:                                                    # None object
            self.__CreationDate = None
         elif isinstance(args[0], DateTime):
            self.SetCreationDate('=', args[0])
         else:
            raise TypeError, self.__ErrorMessages[TypeError]
      elif len(args)==2:
         if type(args[0]) == type('') and isinstance(args[1], DateTime):        # sign and date
            if args[0] not in ObjectCriteria.__SignDefinition.keys():
               raise ValueError, ObjectCriteria.__ErrorMessages[ValueError]
            else:
               self.__CreationDate = (ObjectCriteria.__SignDefinition[args[0]], copy.deepcopy(args[1]))
         elif isinstance(args[0], DateTime) and isinstance(args[1], DateTime):  # two dates
            if args[0] <= args[1]:
               self.__CreationDate = (copy.deepcopy(args[0]), copy.deepcopy(args[1]))
            else:
               self.__CreationDate = (copy.deepcopy(args[1]), copy.deepcopy(args[0]))
         else:
            raise TypeError, self.__ErrorMessages[TypeError]
      else:
         raise TypeError, self.__ErrorMessages[TypeError]

#
#      METHOD:
#          GetCreationDate
#
#      PURPOSE:
#          Returns creation date criteria as :
#              1. tuple of two dates
#              2. tuple of sign and single date
#              3. None
#

   def GetCreationDate(self):
      'returns creation date and time criteria'
      if self.__CreationDate == None:
         return None
      else:
         if type(self.__CreationDate[0]) == type(1):
            sign = ObjectCriteria.__SignDefinition.keys()[ObjectCriteria.__SignDefinition.values().index(self.__CreationDate[0])]
            return (sign, copy.deepcopy(self.__CreationDate[1]))
         else:
            return (copy.deepcopy(self.__CreationDate[0]), copy.deepcopy(self.__CreationDate[1]))


#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Name = property (GetName, SetName, None, 'Name')
   Code1 = property (GetCode1, SetCode1, None, 'Code1')
   Code2 = property (GetCode2, SetCode2, None, 'Code2')
   def SetSizeOnly(self, value):
      if value == None:
         self.__Size = None
      elif type(value) == type(0):
         self.SetSize('=', value)
      elif type(value) in [type([]), type(())] and len(value) == 2:
         if type(value[0]) != type('') or type(value[1]) != type(0):
            raise TypeError, self.__ErrorMessages[TypeError]
         if value[0] not in ObjectCriteria.__SignDefinition.keys():
            raise ValueError, ObjectCriteria.__ErrorMessages[ValueError]
         self.__Size = (ObjectCriteria.__SignDefinition[value[0]], value[1])
      else:
         raise TypeError, self.__ErrorMessages[TypeError]

   Size = property (GetSize, SetSizeOnly, None, 'Size')
   CreationDate = property (GetCreationDate, None, None, 'CreationDate')
