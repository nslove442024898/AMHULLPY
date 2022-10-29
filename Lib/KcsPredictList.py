## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsPredictList_py.py
#
#      PURPOSE:
#          The class holds information about a list
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#
#          __DiminutionCalcYear           int
#          __DiminutionCalcMonth          int
#          __DiminutionCalcDay            int
#          __PredictedDiminution          real
#
import types
import string
import copy

ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class PredictionList:

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

      self.__DiminutionCalcYear = 0
      self.__DiminutionCalcMonth = 0
      self.__DiminutionCalcDay = 0
      self.__PredictedDiminution = 0.0
      self.__OriginalThickness1 = 0.0
      self.__OriginalThickness2 = 0.0

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):

      tup = (
         'Prediction list:',
         'DiminutionCalcYear : ' + str(self.__DiminutionCalcYear),
         'DiminutionCalcMonth : ' + str(self.__DiminutionCalcMonth),
         'DiminutionCalcDay : ' + str(self.__DiminutionCalcDay),
         'PredictedDiminution : ' + str(self.__PredictedDiminution),
         'OriginalThickness1 : ' + str(self.__OriginalThickness1),
         'OriginalThickness2 : ' + str(self.__OriginalThickness2)

          )
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
#          getPredictedDiminution
#
#      PURPOSE:
#           get
#
#
   def getPredictedDiminution(self):
      return self.__PredictedDiminution


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
#          setOriginalThickness1
#
#      PURPOSE:
#           set
#
#
   def setOriginalThickness1(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__OriginalThickness1= value


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
      self.__OriginalThickness2= value


#-------------------------------------------------------------------
#
#      METHOD:
#          setPredictedDiminution
#
#      PURPOSE:
#           set
#
#
   def setPredictedDiminution(self, value):
      if type(value) != types.FloatType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__PredictedDiminution = value
