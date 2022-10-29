## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsDiminutionList.py
#
#      PURPOSE:
#          The class holds information about a list
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#
#          __CalcMode                   int
#          __OriginalThickness1         real
#          __OriginalThickness2         real
#          __ThicknessPredictionPattern int
#          __ListOfGaugeds[]            GaugedList
#
import types
import copy
import string
from KcsGaugedList import GaugedList

ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class DiminutionList:

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
      self.__CalcMode = 0
      self.__OriginalThickness1 = 0.0
      self.__OriginalThickness2 = 0.0
      self.__ThicknessPredictionPattern = 0
      self.__DiminutionCalcYear = 0
      self.__DiminutionCalcMonth = 0
      self.__DiminutionCalcDay = 0
      self.__ListOfGaugeds = []

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):

      tup = (
         'Diminution list:',
         'CalcMode : ' +  str(self.__CalcMode),
         'OriginalThickness1 : ' + str(self.__OriginalThickness1),
         'OriginalThickness2 : ' + str(self.__OriginalThickness2),
         'ThicknessPredictionPattern : ' + str(self.__ThicknessPredictionPattern),
         'DiminutionCalcYear : ' + str(self.__DiminutionCalcYear),
         'DiminutionCalcMonth : ' + str(self.__DiminutionCalcMonth),
         'DiminutionCalcDay : ' + str(self.__DiminutionCalcDay),
         'ListOfGaugeds : ' + str(self.__ListOfGaugeds))
      return string.join(tup, '\n')

#-------------------------------------------------------------------
#
#      METHOD:
#          getDiminutionCalcYear
#
#      PURPOSE:
#           get
#
#

   def getDiminutionCalcYear(self):
      return self.__DiminutionCalcYear


#-------------------------------------------------------------------
#
#      METHOD:
#          getDiminutionCalcMonth
#
#      PURPOSE:
#           get
#
#      INPUT:
#          Parameters:
#          gauged       int

   def getDiminutionCalcMonth(self):
      return self.__DiminutionCalcMonth


#-------------------------------------------------------------------
#
#      METHOD:
#          getDiminutionCalcDay
#
#      PURPOSE:
#           get
#
#      INPUT:
#          Parameters:
#          gauged       int

   def getDiminutionCalcDay(self):
      return self.__DiminutionCalcDay


#-------------------------------------------------------------------
#
#      METHOD:
#          getThicknessPredictionPattern
#
#      PURPOSE:
#           get
#
#

   def getThicknessPredictionPattern(self):
      return self.__ThicknessPredictionPattern


#-------------------------------------------------------------------
#
#      METHOD:
#          getOriginalThickness1
#
#      PURPOSE:
#           get
#
#

   def getOriginalThickness1(self):
      return self.__OriginalThickness1


#-------------------------------------------------------------------
#
#      METHOD:
#          getOriginalThickness2
#
#      PURPOSE:
#           get
#
#

   def getOriginalThickness2(self):
      return self.__OriginalThickness2



#-------------------------------------------------------------------
#
#      METHOD:
#          setDiminutionCalcYear
#
#      PURPOSE:
#           set
#
#
   def setDiminutionCalcYear(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DiminutionCalcYear = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setDiminutionCalcMonth
#
#      PURPOSE:
#           set
#
#
   def setDiminutionCalcMonth(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DiminutionCalcMonth = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setDiminutionCalcDay
#
#      PURPOSE:
#           set
#
#
   def setDiminutionCalcDay(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DiminutionCalcDay = value



#-------------------------------------------------------------------
#
#      METHOD:
#          getListOfGauged
#
#      PURPOSE:
#           get
#
#      INPUT:
#          Parameters:
#          gauged       int

   def getListOfGauged(self, gauged):
      if not 0 <= gauged < len(self.__ListOfGaugeds):
         raise IndexError, ErrorMessages[IndexError]

      listofgauged = copy.deepcopy( self.__ListOfGaugeds[gauged])
      return listofgauged

#-------------------------------------------------------------------
#
#      METHOD:
#          getCalcMode
#
#      PURPOSE:
#           get
#
#
   def getCalcMode(self):
      return self.__CalcMode


#-------------------------------------------------------------------
#
#      METHOD:
#          setThicknessPredictionPattern
#
#      PURPOSE:
#           set
#
#
   def setThicknessPredictionPattern(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__ThicknessPredictionPattern = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setOriginalThickness1
#
#      PURPOSE:
#           set
#
#
   def setOriginalThickness1(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__OriginalThickness1 = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setOriginalThickness2
#
#      PURPOSE:
#           set
#
#
   def setOriginalThickness2(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__OriginalThickness2 = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setCalcMode
#
#      PURPOSE:
#           set
#
#
   def setCalcMode(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__CalcMode = value


# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetNumberListOfGauged
#
#      PURPOSE:
#          get the number of gauged data
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          int            number of gauged data
#

   def GetNumberListOfGauged(self):
      return len(self.__ListOfGaugeds)




# ----------------------------------------------------------------------------
#
#      METHOD:
#         AddListOfGauged
#
#      PURPOSE:
#          add gauged data
#
#      INPUT:
#          Parameters:
#          GaugedList
#
#      RESULT:
#          the welded joint will be added
#

   def AddListOfGauged(self, inlistofgauged):
      if not isinstance(inlistofgauged, GaugedList):
         raise TypeError, self.__ErrorMessages[TypeError]
      listofgauged = copy.deepcopy(inlistofgauged)
      self.__ListOfGaugeds.append(listofgauged)


   def __del__(self):
      del self.__CalcMode
      del self.__OriginalThickness1
      del self.__OriginalThickness2
      del self.__ThicknessPredictionPattern
      del self.__DiminutionCalcYear
      del self.__DiminutionCalcMonth
      del self.__DiminutionCalcDay
      del self.__ListOfGaugeds
