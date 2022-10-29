## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsDate.py
#
#      PURPOSE:
#          The class holds information about a date
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __Year
#           __Month
#           __Day
#
#      METHODS:
#           __init__
#           __cmp__
#           __repr__
#           SetDate
#           GetDate

import types
import time

class Date(object):
   'class holds information about date'

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Date class',
                       ValueError: 'not supported value type, see documentation of Date class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#              day, month, year     integers
#

   def __init__(self, year=2000, month=1, day=1):
      'creates instance of Date class, parameters: year, month, day'

      self.__Year, self.__Month, self.__Day = 2000, 1, 1
      self.SetDate(year, month, day)

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      'compares two Date objects'

      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, self.__class__):
         raise TypeError, Date.__ErrorMessages[TypeError]

      if self.__Year < other.__Year:
         return -1
      elif self.__Year > other.__Year:
         return 1

      if self.__Month < other.__Month:
         return -1
      elif self.__Month > other.__Month:
         return 1

      if self.__Day < other.__Day:
         return -1
      elif self.__Day > other.__Day:
         return 1

      return 0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
#      PARAMETERS:
#
   def __repr__(self):
      'prints date in format: yyyy-mm-dd'
      return 'Date: %04d-%02d-%02d' % (self.__Year, self.__Month, self.__Day)

#
#      METHOD:
#          SetDate
#
#      PURPOSE:
#          To set date
#
   def SetDate(self, *args):
      'sets date:    1. SetDate(year, month, day)  2. SetDate(AnotherDateInstance)'

      if len(args)==3:
         self.__Year, self.__Month, self.__Day = time.localtime(time.mktime((args[0], args[1], args[2], 0, 0, 0, 0, 0, 0)))[0:3]
      elif len(args)==1:
         self.__Year  = (args[0]).__Year
         self.__Month = (args[0]).__Month
         self.__Day   = (args[0]).__Day
      else:
         raise TypeError, Date.__ErrorMessages[TypeError]

#
#      METHOD:
#          GetDate
#
#      PURPOSE:
#          Returns date as tuple (year, month, day)
#
   def GetDate(self):
      'returns date as tuple: (year, month, day)'
      return (self.__Year, self.__Month, self.__Day)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetYear(self): return self.__Year
   def SetYear(self,value):
      if not type(value)==type(2000):
         raise TypeError, Date.__ErrorMessages[TypeError]
      self.__Year = value
   Year = property (GetYear, SetYear, None, 'Year - year from Date object')

   def GetMonth(self): return self.__Month
   def SetMonth(self,value):
      if not type(value)==type(12):
         raise TypeError, Date.__ErrorMessages[TypeError]
      self.__Month = value
   Month = property (GetMonth, SetMonth, None, 'Month - month from Date object')

   def GetDay(self): return self.__Day
   def SetDay(self,value):
      if not type(value)==type(20):
         raise TypeError, Date.__ErrorMessages[TypeError]
      self.__Day = value
   Day = property (GetDay, SetDay, None, 'Day - day from Date object')
