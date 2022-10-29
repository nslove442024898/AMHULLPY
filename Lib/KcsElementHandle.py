## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsElementHandle.py
#
#      PURPOSE:
#          The ElementHandle class holds information about a element handle.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __handle            integer        element handle

import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of ElementHandle class',
                         ValueError: 'not supported value, see documentation of ElementHandle class' }

class ElementHandle(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#           None


   def __init__(self):
      self.__handle = -1

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'handle: %d' % self.__handle


#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          Defines compare operator

   def __cmp__(self, other):
      if not isinstance(other, ElementHandle) and type(other) != type(1):
         return -1

      if type(other) == types.IntType:
         handle = other
      else:
         handle = other.__handle

      if self.__handle > handle:
         return 1
      elif self.__handle < handle:
         return -1
      else:
         return 0
		
#
#     New style from Python version 2.2
#

#
#      METHOD:
#         SetHandle
#
#      PURPOSE:
#          Sets element handle.

   def SetHandle(self, value):
	  if type(value) != types.IntType:	
	     raise TypeError, ErrorMessages[TypeError]
	  self.__handle	= value

#
#      METHOD:
#         GetHandle
#
#      PURPOSE:
#          Returns element handle.

   def GetHandle(self):
	  return self.__handle
	
   handle = property(GetHandle,SetHandle, None, 'handle - element handle')
		
