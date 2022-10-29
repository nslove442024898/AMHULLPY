## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsTMList.py
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
#          __DateOfBuildYear            int
#          __DateOfBuildMonth           int
#          __DateOfBuildDay             int
#          __ListOfDiminution[]         DiminutionList
#
import types
import copy
import string
from KcsDiminutionList import DiminutionList

ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class TMList:

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
      self.__DateOfBuildYear = 0
      self.__DateOfBuildMonth = 0
      self.__DateOfBuildDay = 0
      self.__ListOfDiminution = []



#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):

      tup = (
         'TM list:',
         'NoOfData : ' +  str(self.__NoOfData),
         'DateOfBuildYear : ' + str(self.__DateOfBuildYear),
         'DateOfBuildMonth : ' + str(self.__DateOfBuildMonth),
         'DateOfBuildDay : ' + str(self.__DateOfBuildDay),
         'ListOfDiminution : ' + str(self.__ListOfDiminution))
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
#          getDateOfBuildYear
#
#      PURPOSE:
#           get
#
#

   def getDateOfBuildYear(self):
      return self.__DateOfBuildYear
#-------------------------------------------------------------------
#
#      METHOD:
#          getDateOfBuildMonth
#
#      PURPOSE:
#           get
#
#

   def getDateOfBuildMonth(self):
      return self.__DateOfBuildMonth
#-------------------------------------------------------------------
#
#      METHOD:
#          getDateOfBuildDay
#
#      PURPOSE:
#           get
#
#

   def getDateOfBuildDay(self):
      return self.__DateOfBuildDay


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
#          setDateOfBuildYear
#
#      PURPOSE:
#           set
#
#
   def setDateOfBuildYear(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DateOfBuildYear = value

#-------------------------------------------------------------------
#
#      METHOD:
#          setDateOfBuildMonth
#
#      PURPOSE:
#           set
#
#
   def setDateOfBuildMonth(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DateOfBuildMonth = value

#-------------------------------------------------------------------
#
#      METHOD:
#          setDateOfBuildDay
#
#      PURPOSE:
#           set
#
#
   def setDateOfBuildDay(self, value):
      if type(value) != types.IntType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__DateOfBuildDay = value



#-------------------------------------------------------------------
#
#      METHOD:
#          getListOfDiminution
#
#      PURPOSE:
#           get
#
#      INPUT:
#          Parameters:
#          diminution       int

   def getListOfDiminution(self, diminution):
      if not 0 <= diminution < len(self.__ListOfDiminution):
         #print "len(self.__ListOfDiminution): " + str(len(self.__ListOfDiminution))
         raise IndexError, ErrorMessages[IndexError]

      listofdiminution = copy.deepcopy( self.__ListOfDiminution[diminution])
      return listofdiminution

# ----------------------------------------------------------------------------
#
#      METHOD:
#         AddListOfDiminution
#
#      PURPOSE:
#          add diminution data
#
#      INPUT:
#          Parameters:
#          DiminutionList
#
#      RESULT:
#
#

   def AddListOfDiminution(self, inlistofdiminution):
      if not isinstance(inlistofdiminution, DiminutionList):
         raise TypeError, self.__ErrorMessages[TypeError]
      listofdiminution = copy.deepcopy(inlistofdiminution)
      self.__ListOfDiminution.append(listofdiminution)


   def __del__(self):
      del self.__NoOfData
      del self.__DateOfBuildYear
      del self.__DateOfBuildMonth
      del self.__DateOfBuildDay
      del self.__ListOfDiminution
