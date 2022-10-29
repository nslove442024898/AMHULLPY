## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsTMResult.py
#
#      PURPOSE:
#          The class holds information about a list
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#
#          __NoOfData                   int
#          __ListOfPredict[]            PredictList
#
import types
import copy
import string
from KcsPredictList import PredictionList

ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class TMResult:

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
      self.__NoOfData = 0
      self.__ListOfPrediction = []



#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):

      tup = (
         'TMResult:',
         'NoOfData' +  str(self.__NoOfData),
         'ListOfPrediction' + str(self.__ListOfPrediction))
      return string.join(tup, '\n')

#-------------------------------------------------------------------
#
#      METHOD:
#          getNoOfData
#
#      PURPOSE:
#           get
#
#

   def getNoOfData(self):
      return self.__NoOfData


#-------------------------------------------------------------------
#
#      METHOD:
#          setNoOfData
#
#      PURPOSE:
#           set
#
#
   def setNoOfData(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__NoOfData = value


#-------------------------------------------------------------------
#
#      METHOD:
#          getListOfPredicted
#
#      PURPOSE:
#           get
#
#      INPUT:
#          Parameters:
#          diminution       int

   def getListOfPredicted(self, predicted):
      if not 0 <= predicted < len(self.__ListOfPrediction):
         raise IndexError, ErrorMessages[IndexError]

      listofpredicted = copy.deepcopy( self.__ListOfPrediction[predicted])
      return listofpredicted

# ----------------------------------------------------------------------------
#
#      METHOD:
#         AddListOfPredicted
#
#      PURPOSE:
#          add predicted data
#
#      INPUT:
#          Parameters:
#          ListOfPredicted
#
#      RESULT:
#
#

   def AddListOfPredicted(self, inlistofpredicted):
      if not isinstance(inlistofpredicted, PredictionList):
         raise TypeError, self.__ErrorMessages[TypeError]
      inlistofpredicted = copy.deepcopy(inlistofpredicted)
      self.__ListOfPrediction.append(inlistofpredicted)
