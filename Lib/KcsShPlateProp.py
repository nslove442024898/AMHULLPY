## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import string
import kcs_chm
from types import *

class ShPlateProp(object):
   """Shell Plate Properties
   This class is used together with kcs_chm.plate_prop_get and
   kcs_chm.plate_prop_set."""

   def __init__(self):
      self.__PartsList = None
      self.__GPS_1 = None
      self.__GPS_2 = None
      self.__GPS_3 = None
      self.__GPS_4 = None
      self.__SurfaceTreatment = None
      self.__Destination = None
      self.__Thickness = None
      self.__ThicknessOut = None
      self.__Quality = None
      self.__Posno = None
      self.__LaminateIn = None
      self.__LaminateOut = None
      self.__LongitudinalShrinkage = None
      self.__TransversalShrinkage = None
      self.__RawPlate = None

   def __repr__(self):
      tup = (
        'Shell Plate Properties:',
        'PartsList:\t\t\t' + str(self.__PartsList),
        'GPS_1:\t\t\t' + str(self.__GPS_1),
        'GPS_2:\t\t\t' + str(self.__GPS_2),
        'GPS_3:\t\t\t' + str(self.__GPS_3),
        'GPS_4:\t\t\t' + str(self.__GPS_4),
        'SurfaceTreatment:\t\t' + str(self.__SurfaceTreatment),
        'Destination:\t\t' + str(self.__Destination),

        'Thickness:\t\t' + str(self.__Thickness),
        'ThicknessOut:\t\t' + str(self.__ThicknessOut),
        'Quality:\t\t\t' + str(self.__Quality),
        'Posno:\t\t\t' + str(self.__Posno),
        'LaminateIn:\t\t' + str(self.__LaminateIn),
        'LaminateOut:\t\t' + str(self.__LaminateOut),

        'LongitudinalShrinkage:\t' + str(self.__LongitudinalShrinkage),
        'TransversalShrinkage \t' + str(self.__TransversalShrinkage),

        'RawPlate:\t\t' + str(self.__RawPlate))
      return string.join (tup, '\n')


   def SetPartsList(self, value):
      if type(value) == StringType:
         self.__PartsList = value

   def SetGPS_1(self, value):
      if type(value) == StringType:
         self.__GPS_1 = value

   def SetGPS_2(self, value):
      if type(value) == StringType:
         self.__GPS_2 = value

   def SetGPS_3(self, value):
      if type(value) == StringType:
         self.__GPS_3 = value

   def SetGPS_4(self, value):
      if type(value) == StringType:
         self.__GPS_4 = value

   def SetSurfaceTreatment(self, value):
      if type(value) == StringType:
         self.__SurfaceTreatment = value

   def SetDestination(self, value):
      if type(value) == StringType:
         self.__Destination = value

   def SetThickness(self, value):
      if type(value) in [FloatType,IntType]:
         self.__Thickness = value

   def SetThicknessOut(self, value):
      if type(value) in [FloatType,IntType]:
         self.__ThicknessOut = value

   def SetQuality(self, value):
      if type(value) in [StringType,IntType]:
         self.__Quality = value

   def SetPosno(self, value):
      if type(value) == IntType:
         self.__Posno = value

   def SetLaminateIn(self, value):
      if type(value) == IntType:
         self.__LaminateIn = value

   def SetLaminateOut(self, value):
      if type(value) == IntType:
         self.__LaminateOut = value

   def SetLongitudinalShrinkage(self, value):
      if type(value) in [FloatType,IntType]:
         self.__LongitudinalShrinkage = value

   def SetTransversalShrinkage(self, value):
      if type(value) in [FloatType,IntType]:
         self.__TransversalShrinkage = value

   def SetRawPlate(self, value):
      if type(value) == StringType:
         self.__RawPlate = value

   def GetPartsList(self):
      return self.__PartsList

   def GetGPS_1(self):
      return self.__GPS_1

   def GetGPS_2(self):
      return self.__GPS_2

   def GetGPS_3(self):
      return self.__GPS_3

   def GetGPS_4(self):
      return self.__GPS_4

   def GetSurfaceTreatment(self):
      return self.__SurfaceTreatment

   def GetDestination(self):
      return self.__Destination

   def GetThickness(self):
      return self.__Thickness

   def GetThicknessOut(self):
      return self.__ThicknessOut

   def GetQuality(self):
      return self.__Quality

   def GetPosno(self):
      return self.__Posno

   def GetLaminateIn(self):
      return self.__LaminateIn

   def GetLaminateOut(self):
      return self.__LaminateOut

   def GetLongitudinalShrinkage(self):
      return self.__LongitudinalShrinkage

   def GetTransversalShrinkage(self):
      return self.__TransversalShrinkage

   def GetRawPlate(self):
      return self.__RawPlate


   PartsList = property (GetPartsList , SetPartsList)
   GPS_1 = property (GetGPS_1 , SetGPS_1)
   GPS_2 = property (GetGPS_2 , SetGPS_2)
   GPS_3 = property (GetGPS_3 , SetGPS_3)
   GPS_4 = property (GetGPS_4 , SetGPS_4)
   SurfaceTreatment = property (GetSurfaceTreatment , SetSurfaceTreatment)
   Destination = property (GetDestination , SetDestination)

   Thickness = property (GetThickness , SetThickness)
   ThicknessOut = property (GetThicknessOut , SetThicknessOut)
   Quality = property (GetQuality , SetQuality)
   Posno = property (GetPosno , SetPosno)
   LaminateIn = property (GetLaminateIn , SetLaminateIn)
   LaminateOut = property (GetLaminateOut , SetLaminateOut)

   LongitudinalShrinkage = property (GetLongitudinalShrinkage , SetLongitudinalShrinkage)
   TransversalShrinkage = property (GetTransversalShrinkage , SetTransversalShrinkage)

   RawPlate = property (GetRawPlate , SetRawPlate)

if __name__ == "__main__":
   plt = ShPlateProp()
   print plt
