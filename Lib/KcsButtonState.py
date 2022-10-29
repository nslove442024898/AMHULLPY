## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsButtonState.py
#
#      PURPOSE:
#          The class holds information about button states during interactive operations
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#           __LockEnabled
#           __LockChecked
#           __OptionsEnabled
#
#      MEHTODS:
#           EnableLock
#           IsLockEnabled
#           SetCheckedLock
#           GetCheckedLock
#           EnableOptions
#           IsOptionsEnabled

import types
import string

class ButtonState(object):

   __ErrorMessages = {  TypeError : 'not supported argument type, see documentation of ButtonState class',
                        ValueError: 'not supported value type, see documentation of ButtonState class' }

   __LockButtonId = { None : 0, 'U' : 1, 'V' : 2 }
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
      self.__LockEnabled = 0
      self.__OptionsEnabled = 0
      self.__LockChecked = ButtonState.__LockButtonId[None]

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      'implements cmp(o1, o2) function'

      if not isinstance(other, ButtonState):
         return 1

      if self.__LockEnabled != other.__LockEnabled:
         return 1

      if self.__LockChecked != other.__LockChecked:
         return 1

      if self.__OptionsEnabled != other.__OptionsEnabled:
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

      if self.__LockEnabled:
         lockenabledstr = 'Enabled'
      else:
         lockenabledstr = 'Disabled'

      if self.__OptionsEnabled:
         optionsenabledstr = 'Enabled'
      else:
         optionsenabledstr = 'Disabled'

      tup = (
         'ButtonState:',
         '   Lock: ' + lockenabledstr,
         '   Checked lock: ' + str(self.GetCheckedLock()),
         '   Options: ' + optionsenabledstr,
         )
      return string.join(tup, '\n')

#
#      METHOD:
#          EnableLock
#
#      PURPOSE:
#          To set lock buttons enabled or disabled
#
#      ARGUMENTS:
#          enable           integer             lock buttons state:
#                                                     0 - disabled
#                                                  <> 0 - enabled
#
   def EnableLock(self, enable):
      'enables or disables lock buttons'

      if type(enable) != type(1):
         raise TypeError, self.__ErrorMessages[TypeError]
      if enable:
         self.__LockEnabled = 1
      else:
         self.__LockEnabled = 0

#
#      METHOD:
#          IsLockEnabled
#
#      PURPOSE:
#          returns state of lock buttons: 0 - disabled, 1 - enabled
#
   def IsLockEnabled(self):
      'returns state of lock buttons: 0 - disabled, 1 - enabled'
      return self.__LockEnabled

#
#      METHOD:
#          EnableOptions
#
#      PURPOSE:
#          To set Options button enabled or disabled
#
#      ARGUMENTS:
#          enable           integer             options button state:
#                                                     0 - disabled
#                                                  <> 0 - enabled
#
   def EnableOptions(self, enable):
      'enables or disables Options button'

      if type(enable) != type(1):
         raise TypeError, self.__ErrorMessages[TypeError]
      if enable:
         self.__OptionsEnabled = 1
      else:
         self.__OptionsEnabled = 0

#
#      METHOD:
#          IsOptionsEnabled
#
#      PURPOSE:
#          returns state of options button: 0 - disabled, 1 - enabled
#
   def IsOptionsEnabled(self):
      'returns state of Options button: 0 - disabled, 1 - enabled'

      return self.__OptionsEnabled

#
#      METHOD:
#          SetCheckedLock
#
#      PURPOSE:
#          Checks given lock button or resets selection
#
#      ARGUMENTS:
#          check               string or None                  lock button id to be checked:
#                                                                      'U'  -  U lock checked
#                                                                      'V'  -  V lock checked
#                                                                     None  -  No lock button checked

   def SetCheckedLock(self, check):
      'returns id of checked lock button'
      if check != None and type(check) != type(''):
         raise TypeError, self.__ErrorMessages[TypeError]

      if check in ButtonState.__LockButtonId.keys():
         self.__LockChecked = ButtonState.__LockButtonId[check]
      else:
         raise ValueError, self.__ErrorMessages[ValueError]


#
#      METHOD:
#          GetCheckedLock
#
#      PURPOSE:
#          Returns checked lock button
#
#      ARGUMENTS:
#          None
#
#      RESULTS:
#          [0]                 string or None                  checked lock button id:
#                                                                      'U'  -  U lock checked
#                                                                      'V'  -  V lock checked
#                                                                     None  -  No lock button checked

   def GetCheckedLock(self):
      'returns id of checked lock button'

      return ButtonState.__LockButtonId.keys()[ButtonState.__LockButtonId.values().index(self.__LockChecked)]


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   LockEnabled       = property (IsLockEnabled, EnableLock, None, 'LockEnabled - lock buttons state')
   OptionsEnabled    = property (IsOptionsEnabled, EnableOptions, None, 'OptionsEnabled - options button state')
   LockChecked       = property (GetCheckedLock, SetCheckedLock, None, 'LockChecked - check state of lock buttons')
