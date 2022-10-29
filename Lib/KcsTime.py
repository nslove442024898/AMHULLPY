## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsTime.py
#
#      PURPOSE:
#          The class holds information about a time
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __Hour            integer        hour
#           __Minute          integer        minute
#           __Second          integer        second
#           __Hundredths      integer        hundredths of second
#
#      METHODS:
#           __init__
#           __cmp__
#           __repr__
#           SetTime
#           GetTime


import types
import time


class Time(object):
   'holds information about time'

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Time class',
                       ValueError: 'not supported value type, see documentation of Time class' }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#              hour, min, sec, hund - integers
#

   def __init__(self, hour=0, min=0, sec=0, hund=0):
      'parameters: hour, minute, second, hundredths'
      self.__Hour, self.__Minute, self.__Second, self.__Hundredths = 0, 0, 0, 0
      self.SetTime(hour, min, sec, hund)

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function
#
#      PARAMETERS:
#              other        Time or None
#

   def __cmp__(self, other):
      'compares two Time objects'

      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other, self.__class__):
         raise TypeError, Time.__ErrorMessages[TypeError]

      if self.__Hour < other.__Hour:
         return -1
      elif self.__Hour > other.__Hour:
         return -1

      if self.__Minute < other.__Minute:
         return -1
      elif self.__Minute > other.__Minute:
         return 1

      if self.__Second < other.__Second:
         return -1
      elif self.__Second > other.__Second:
         return 1

      if self.__Hundredths < other.__Hundredths:
         return -1
      elif self.__Hundredths > other.__Hundredths:
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
      'prints time in format: hh:mm:ss'
      return 'Time: %02d:%02d:%02d.%02d' % (self.__Hour, self.__Minute, self.__Second, self.__Hundredths)

#
#      METHOD:
#          SetTime
#
#      PURPOSE:
#          To set time
#
#      PARAMETERS:
#              hour, min, sec, hund             integers         values: hour, minute, second, hundredths
#              or
#              time                             Time             another Time instance

   def SetTime(self, *args):
      'set time:     1. SetTime(h, m, s, hund)   2. SetTime(AnotherTimeInstance)'
      if len(args)==4:
         if type(args[0])==type(0) and type(args[1])==type(0) and type(args[2])==type(0) and type(args[3])==type(0):
            (self.__Hour, self.__Minute, self.__Second, self.__Hundredths) = args
         else:
            raise ValueError, Time.__ErrorMessages[ValueError]
      elif len(args)==1:
         self.__Hour          = (args[0]).__Hour
         self.__Minute        = (args[0]).__Minute
         self.__Second        = (args[0]).__Second
         self.__Hundredths   = (args[0]).__Hundredths
      else:
         raise TypeError, Time.__ErrorMessages[TypeError]

#
#      METHOD:
#          GetTime
#
#      PURPOSE:
#          Returns time as tuple (hour, minute, second, hundredths)
#
   def GetTime(self):
      'returns time as tuple: (hour, minute, second, hundredths)'
      return (self.__Hour, self.__Minute, self.__Second, self.__Hundredths)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   def GetHour(self): return self.__Hour
   def SetHour(self,value):
      if not type(value)==type(0):
         raise TypeError, Time.__ErrorMessages[TypeError]
      self.__Hour = value
   Hour = property (GetHour, SetHour, None, 'Hour - hour from Time object')

   def GetMinute(self): return self.__Minute
   def SetMinute(self,value):
      if not type(value)==type(0):
         raise TypeError, Time.__ErrorMessages[TypeError]
      self.__Minute = value
   Minute = property (GetMinute, SetMinute, None, 'Minute - minute from Time object')

   def GetSecond(self): return self.__Second
   def SetSecond(self,value):
      if not type(value)==type(0):
         raise TypeError, Time.__ErrorMessages[TypeError]
      self.__Second = value
   Second = property (GetSecond, SetSecond, None, 'Second - second from Time object')

   def GetHundredths(self): return self.__Hundredths
   def SetHundredths(self,value):
      if not type(value)==type(0):
         raise TypeError, Time.__ErrorMessages[TypeError]
      self.__Hundredths = value
   Hundredths = property (GetHundredths, SetHundredths, None, 'Hundredths - hundredth of second from Time object')

#
#-----------------------------------------------------------------------------
#  Self test
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
   time = Time()
   time.Hour = 13
   time.Minute = 8
   time.Second = time.Hour + 3
   time.Hundredths = 99
   print time
