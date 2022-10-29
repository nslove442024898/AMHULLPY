## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsGaugedList.py
#
#      PURPOSE:
#          The class holds information about a list
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#
#          __GaugedYear        int
#          __GaugedMonth       int
#          __GaugedDay         int
#          __Diminution1       real
#          __Diminution2       real

import types
import copy
import string
ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class GaugedList:

#-------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#

   def __init__(self):
      self.__GaugedYear = 0
      self.__GaugedMonth = 0
      self.__GaugedDay = 0
      self.__Diminution1 = 0.0
      self.__Diminution2 = 0.0

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):

      tup = (
         '\nGauged list:',
            'GaugedYear : ' + str(self.__GaugedYear),
            'GaugedMonth : ' + str(self.__GaugedMonth),
            'GaugedDay : ' + str(self.__GaugedDay),
            'Diminution1 : ' + str(self.__Diminution1),
            'Diminution2 : ' + str(self.__Diminution2)
            )

      return string.join(tup, '\n')


#-------------------------------------------------------------------
#
#      METHOD:
#          setGaugedYear
#
#      PURPOSE:
#           set
#
#

   def setGaugedYear(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__GaugedYear = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setGaugedMonth
#
#      PURPOSE:
#           set
#
#

   def setGaugedMonth(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__GaugedMonth = value
#-------------------------------------------------------------------
#
#      METHOD:
#          setGaugedDay
#
#      PURPOSE:
#           set
#
#

   def setGaugedDay(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__GaugedDay = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setDiminution1
#
#      PURPOSE:
#           set
#
#

   def setDiminution1(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Diminution1 = value



#-------------------------------------------------------------------
#
#      METHOD:
#          setDiminution2
#
#      PURPOSE:
#           set
#
#

   def setDiminution2(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__Diminution2 = value



#-------------------------------------------------------------------
#
#      METHOD:
#          getGaugedYear
#
#      PURPOSE:
#           get
#
#

   def getGaugedYear(self):
      return self.__GaugedYear


#-------------------------------------------------------------------
#
#      METHOD:
#          getGaugedMonth
#
#      PURPOSE:
#           get
#
#
   def getGaugedMonth(self):
      return self.__GaugedMonth


#-------------------------------------------------------------------
#
#      METHOD:
#          getGaugedDay
#
#      PURPOSE:
#           get
#
#
   def getGaugedDay(self):
      return self.__GaugedDay


#-------------------------------------------------------------------
#
#      METHOD:
#          getDiminution1
#
#      PURPOSE:
#           get
#
#
   def getDiminution1(self):
      return self.__Diminution1


#-------------------------------------------------------------------
#
#      METHOD:
#          getDiminution2
#
#      PURPOSE:
#           get
#
#
   def getDiminution2(self):
      return self.__Diminution2



   def __del__(self):
      del self.__GaugedYear
      del self.__GaugedMonth
      del self.__GaugedDay
      del self.__Diminution1
      del self.__Diminution2
