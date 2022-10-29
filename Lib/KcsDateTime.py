## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsDateTime.py
#
#      PURPOSE:
#          The class holds information about date and time
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           see: class Date, class Time
#
#      METHODS:
#           __init__
#           __cmp__
#           __repr__
#           see: class Date, class Time

import types
import time

from KcsDate import Date
from KcsTime import Time

class DateTime(Date, Time):
   'class holds information about date and time'

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of DateTime class',
                       ValueError: 'not supported value type, see documentation of DateTime class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#              day, month, year, hour, minute, second     integers
#

   def __init__(self, year=2000, month=1, day=1, hour=0, minute=0, second=0, hund=0):
      'creates instance of DateTime class, parameters: year, month, day, hour, minute, second, hundredths'

      Date.__init__(self)
      Time.__init__(self)
      self.SetDate(year, month, day)
      self.SetTime(hour, minute, second, hund)

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      'compares two DateTime objects'

      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, self.__class__):
         raise TypeError, DateTime.__ErrorMessages[TypeError]

      result = Date.__cmp__(self, other)
      if result != 0:
         return result
      else:
         return Time.__cmp__(self, other)

      return 0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
   def __repr__(self):
      'prints date and time in format: yyyy-mm-dd hh:mm:ss.hh'
      return 'Date and time: %04d-%02d-%02d %02d:%02d:%02d.%02d' % (self.GetDate() + self.GetTime())

#
#      METHOD:
#          SetDateTime
#
#      PURPOSE:
#          To set date and time
#
#      PARAMETERS:
#              year, month, day, hour, min, sec, hund     integers         values: year, month, day, hour, minute, second, hundredths
#
#              or
#
#              datetime                                   DateTime         another DateTime instance

   def SetDateTime(self, *args):
      'set date and time:     1. SetDateTime(y, mon, day, h, m, s, hund)   2. SetDateTime(AnotherDateTimeInstance)'
      if len(args)==7:
         for item in args:
            if type(item) != type(0):
               raise TypeError, DateTime.__ErrorMessages[TypeError]
         apply(self.SetDate, args[:3])
         apply(self.SetTime, args[-4:])
      elif len(args)==1:
         apply(self.SetDate, args[0].GetDate())
         apply(self.SetTime, args[0].GetTime())
      else:
         raise TypeError, DateTime.__ErrorMessages[TypeError]

#
#      METHOD:
#          GetDateTime
#
#      PURPOSE:
#          Returns date and time as tuple (year, month, day, hour, minute, second, hundredths)
#
   def GetDateTime(self):
      'returns date and time as tuple: (year, month, day, hour, minute, second, hundredths)'
      return self.GetDate() + self.GetTime()

#
#-----------------------------------------------------------------------------
#  Self test
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
   date = DateTime()
   date.Second = 56
   date.Day = 31
   date.Year = 1998
   date.Month = date.Month + 3
   print date
