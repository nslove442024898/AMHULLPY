## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import string
import kcs_chm
from types import *

def pType(index):
   IpType = ['CUTTING_PLANE','FRAME_PLANE','BUTTOCK_PLANE','WATERLINE_PLANE']
   if index in [kcs_chm.kcsCUTTING_PLANE,
                   kcs_chm.kcsFRAME_PLANE,
                   kcs_chm.kcsBUTTOCK_PLANE,
                   kcs_chm.kcsWATERLINE_PLANE]:
      return IpType[index]
   else:
      return str(index)
def iType(index):
   IiType = {kcs_chm.kcsCUTTING_PLANE:'CUTTING_PLANE',
         kcs_chm.kcsX_AXIS:'X_AXIS',
         kcs_chm.kcsY_AXIS:'Y_AXIS',
         kcs_chm.kcsZ_AXIS:'Z_AXIS',
         kcs_chm.kcsPERPENDICULAR:'PERPENDICULAR',
         kcs_chm.kcsPERP_WHOLE:'PERP_WHOLE'}
   if index in [kcs_chm.kcsCUTTING_PLANE,
                   kcs_chm.kcsPERPENDICULAR,
                   kcs_chm.kcsPERP_WHOLE,
                   kcs_chm.kcsX_AXIS,
                   kcs_chm.kcsY_AXIS,
                   kcs_chm.kcsZ_AXIS]:
      return IiType[index]
   else:
      return str(index)

class ShProfData(object):
   """Data for profile type and parameters.
   Type         See the hull modeling documentation for possible types.
                Must be an integer.

   Parameters   Maximum number of parameters is 6.
                Can be integers or floating points."""

   def __init__(self):
      self.__Type = None
      self.__Parameters = None

   def __repr__(self):
      tup = (
        '\tType:       \t' + str(self.__Type),
        '\tParameters:\t' + str(self.__Parameters))
      return string.join (tup, '\n')

   def SetType(self, value):
      if value in kcs_chm.kcsPROFILE_TYPES:
         self.__Type = value

   def SetParameter(self, value):
      if type(value) in [FloatType,IntType]:
         if self.__Parameters:
            if len(self.__Parameters) < 7:
               self.__Parameters.append(value)
         else:
            self.__Parameters = []
            self.__Parameters.append(value)

   def GetType(self):
      return self.__Type

   def GetParameter(self, value):
      if type(value) != IntType:
         return None
      if self.__Parameters:
         if value < len(self.__Parameters):
            return self.__Parameters[value]
      else:
         return self.__Parameters

   Type = property(GetType, SetType)
   def GetParameters(self): return self.__Parameters
   def SetParameters(self,value):
      if type(value)!=ListType:
         return None
      list = []
      for p in value:
         if type(p) not in [FloatType,IntType]:
            return None
         list.append(p)
      self.__Parameters = list
   Parameters = property (GetParameters, SetParameters)

class ShEndCut(object):
   """Shell stiffener end cut data."""
   def __init__(self):
      self.__CalcWebAngle = None
      self.__CalcFrom = None
      self.__Type = None
      self.__Parameters = None

   def __repr__(self):
      tup = (
        '\t\tCalcWebAngle:\t' + str(self.__CalcWebAngle),
        '\t\tCalcFrom:    \t' + pType(self.__CalcFrom),
        '\t\tType:         \t' + str(self.__Type),
        '\t\tParameters:  \t' + str(self.__Parameters))
      return string.join (tup, '\n')

   def SetType(self, value):
      if type(value) == StringType:
         self.__Type = value

   def SetCalcWebAngle(self, value):
      if value:
         self.__CalcWebAngle = 1
      else:
         self.__CalcWebAngle = 0

   def SetCalcFrom(self, value):
      if value in [kcs_chm.kcsCUTTING_PLANE,
                   kcs_chm.kcsFRAME_PLANE,
                   kcs_chm.kcsBUTTOCK_PLANE,
                   kcs_chm.kcsWATERLINE_PLANE]:
         self.__CalcFrom = value

   def SetParameter(self, value):
      if type(value) in [FloatType,IntType]:
         if self.__Parameters:
            if len(self.__Parameters) < 7:
               self.__Parameters.append(value)
         else:
            self.__Parameters = []
            self.__Parameters.append(value)

   def GetType(self):
      return self.__Type

   def GetCalcWebAngle(self):
      return self.__CalcWebAngle

   def GetCalcFrom(self):
      return self.__CalcFrom

   def GetParameter(self, value):
      if type(value) != IntType:
         return None
      if self.__Parameters:
         if value < len(self.__Parameters):
            return self.__Parameters[value]
      else:
         return self.__Parameters

   Type = property(GetType, SetType)
   CalcWebAngle = property(GetCalcWebAngle , SetCalcWebAngle)
   CalcFrom = property(GetCalcFrom , SetCalcFrom)
   def GetParameters(self): return self.__Parameters
   def SetParameters(self,value):
      if type(value)!=ListType:
         return None
      list = []
      for p in value:
         if type(p) not in [FloatType,IntType]:
            return None
         list.append(p)
      self.__Parameters = list
   Parameters = property(GetParameters , SetParameters)

class ShEndDef(object):
   """Shell stiffener end definition data."""
   def __init__(self):
      self.__Connection = None
      self.__Excess = None
      self.__Offset = None
      self.__OffsetFrom = None
      self.__EndCut = ShEndCut()
      self.__WebBevel = None
      self.__FlaBevel = None
      self.__InclAngle = None
      self.__InclAngleType = None

   def __repr__(self):
      tup = (
        '\tConnection:   \t' + str(self.__Connection),
        '\tExcess:       \t' + str(self.__Excess),
        '\tOffset:       \t' + str(self.__Offset),
        '\tOffsetFrom:   \t' + pType(self.__OffsetFrom),
        '\tEndCut:\n'+str(self.__EndCut),
        '\tWebBevel:     \t' + str(self.__WebBevel),
        '\tFlaBevel:     \t' + str(self.__FlaBevel),
        '\tInclAngle:    \t' + str(self.__InclAngle),
        '\tInclAngleType:\t' + iType(self.__InclAngleType))
      return string.join (tup, '\n')

   def SetConnection(self, value):
      if type(value) == IntType:
         self.__Connection = value

   def SetExcess(self, value):
      if type(value) in [FloatType,IntType]:
         self.__Excess = value

   def SetOffset(self, value):
      if type(value) in [FloatType,IntType]:
         self.__Offset = value

   def SetOffsetFrom(self, value):
      if value in [kcs_chm.kcsCUTTING_PLANE,
                   kcs_chm.kcsFRAME_PLANE,
                   kcs_chm.kcsBUTTOCK_PLANE,
                   kcs_chm.kcsWATERLINE_PLANE]:
         self.__OffsetFrom = value

   def SetWebBevel(self, value):
      if type(value) in [FloatType,IntType]:
         self.__WebBevel = value

   def SetFlaBevel(self, value):
      if type(value) in [FloatType,IntType]:
         self.__FlaBevel = value

   def SetInclAngle(self, value):
      if type(value) in [FloatType,IntType]:
         self.__InclAngle = value

   def SetInclAngleType(self, value):
      if value in [kcs_chm.kcsCUTTING_PLANE,
                   kcs_chm.kcsPERPENDICULAR,
                   kcs_chm.kcsPERP_WHOLE,
                   kcs_chm.kcsX_AXIS,
                   kcs_chm.kcsY_AXIS,
                   kcs_chm.kcsZ_AXIS]:
         self.__InclAngleType = value

   def GetEndCut(self):
      return self.__EndCut

   def GetConnection(self):
      return self.__Connection

   def GetExcess(self):
      return self.__Excess

   def GetOffset(self):
      return self.__Offset

   def GetOffsetFrom(self):
      return self.__OffsetFrom

   def GetWebBevel(self):
      return self.__WebBevel

   def GetFlaBevel(self):
      return self.__FlaBevel

   def GetInclAngle(self):
      return self.__InclAngle

   def GetInclAngleType(self):
      return self.__InclAngleType

   Connection = property (GetConnection, SetConnection)
   Excess = property (GetExcess , SetExcess)
   Offset = property (GetOffset , SetOffset)
   OffsetFrom = property (GetOffsetFrom , SetOffsetFrom)
   EndCut = property (GetEndCut)
   WebBevel = property (GetWebBevel , SetWebBevel)
   FlaBevel = property (GetFlaBevel , SetFlaBevel)
   InclAngle = property (GetInclAngle , SetInclAngle)
   InclAngleType = property (GetInclAngleType , SetInclAngleType)

class ShStiffProp(object):
   """Shell stiffener properties
   This class is used together with kcs_chm.stiffener_prop_get and
   kcs_chm.stiffener_prop_set."""
   def __init__(self):
      self.__DummyInterval = None
      self.__GPS_1 = None
      self.__GPS_2 = None
      self.__GPS_3 = None
      self.__GPS_4 = None
      self.__SurfaceTreatment = None
      self.__Destination = None
      self.__UseStiffenerData = None
      self.__Posno = None
      self.__PosnoPrefix = None
      self.__PosnoSuffix = None
      self.__Profile = ShProfData()
      self.__Quality = None
      self.__End = [ShEndDef(),ShEndDef()]
      self.__TraceBevel = None
      self.__Shrinkage = None
      self.__FilletWeldDepth = None
      self.__Perpendicular = None

   def __repr__(self):
      tup = (
        'Shell Stiffener Properties:',
        'Dummy Interval:  \t' + str(self.__DummyInterval),
        'Destination:     \t' + str(self.__Destination),
        'FilletWeldDepth: \t' + str(self.__FilletWeldDepth),
        'GPS_1:           \t' + str(self.__GPS_1),
        'GPS_2:           \t' + str(self.__GPS_2),
        'GPS_3:           \t' + str(self.__GPS_3),
        'GPS_4:           \t' + str(self.__GPS_4),
        'Perpendicular:   \t' + str(self.__Perpendicular),
        'Posno:           \t' + str(self.__Posno),
        'PosnoPrefix:     \t' + str(self.__PosnoPrefix),
        'PosnoSuffix:     \t' + str(self.__PosnoSuffix),
        'Shrinkage:       \t' + str(self.__Shrinkage),
        'SurfaceTreatment:\t' + str(self.__SurfaceTreatment),
        'TraceBevel:      \t' + str(self.__TraceBevel),
        'UseStiffenerData:\t' + str(self.__UseStiffenerData),
        'Quality:         \t' + str(self.__Quality),
        'Profile:\n'+str(self.__Profile),
        'End[0]:\n'+str(self.__End[0]),
        'End[1]:\n'+str(self.__End[1]))
      return string.join (tup, '\n')


   def SetDummyInterval(self, value):
      if value == kcs_chm.kcsDUMMY_INTERVAL:
         self.__DummyInterval = value
      else:
         self.__DummyInterval = 0

   def SetDestination(self, value):
      if type(value) == StringType:
         self.__Destination = value

   def SetFilletWeldDepth(self, value):
      if type(value) in [FloatType,IntType]:
         self.__FilletWeldDepth = value

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

   def SetPerpendicular(self, value):
      if value:
         self.__Perpendicular = 1
         self.__End[0].SetInclAngleType(kcs_chm.kcsPERP_WHOLE)
         self.__End[1].SetInclAngleType(kcs_chm.kcsPERP_WHOLE)
      else:
         self.__Perpendicular = 0

   def SetPosno(self, value):
      if type(value) == IntType:
         self.__Posno = value

   def SetPosnoPrefix(self, value):
      if type(value) == StringType:
         self.__PosnoPrefix = value

   def SetPosnoSuffix(self, value):
      if type(value) == StringType:
         self.__PosnoSuffix = value

   def SetShrinkage(self, value):
      if type(value) in [FloatType,IntType]:
         self.__Shrinkage = value

   def SetSurfaceTreatment(self, value):
      if type(value) == StringType:
         self.__SurfaceTreatment = value

   def SetTraceBevel(self, value):
      if type(value) in [FloatType,IntType]:
         self.__TraceBevel = value

   def SetUseStiffenerData(self, value):
      if value:
         self.__UseStiffenerData = 1
      else:
         self.__UseStiffenerData = 0

   def SetQuality(self, value):
      if type(value) in [StringType,IntType]:
         self.__Quality = value

   def SetProfileType(self, value):
      self.__Profile.SetType(value)

   def SetProfileParameter(self, value):
      self.__Profile.SetParameter(value)

   def GetEnd1(self):
      return self.__End[0]

   def GetEnd2(self):
      return self.__End[1]

   def GetDummyInterval(self):
      return self.__DummyInterval

   def GetDestination(self):
      return self.__Destination

   def GetFilletWeldDepth(self):
      return self.__FilletWeldDepth

   def GetGPS_1(self):
      return self.__GPS_1

   def GetGPS_2(self):
      return self.__GPS_2

   def GetGPS_3(self):
      return self.__GPS_3

   def GetGPS_4(self):
      return self.__GPS_4

   def GetPerpendicular(self):
      return self.__Perpendicular

   def GetPosno(self):
      return self.__Posno

   def GetPosnoPrefix(self):
      return self.__PosnoPrefix

   def GetPosnoSuffix(self):
      return self.__PosnoSuffix

   def GetShrinkage(self):
      return self.__Shrinkage

   def GetSurfaceTreatment(self):
      return self.__SurfaceTreatment

   def GetTraceBevel(self):
      return self.__TraceBevel

   def GetUseStiffenerData(self):
      return self.__UseStiffenerData

   def GetQuality(self):
      return self.__Quality

   def GetProfileType(self):
      return self.__Profile.GetType()

   def GetProfileParameter(self, value):
      return self.__Profile.GetParameter(value)

   DummyInterval = property (GetDummyInterval , SetDummyInterval)
   GPS_1 = property (GetGPS_1 , SetGPS_1)
   GPS_2 = property (GetGPS_2 , SetGPS_2)
   GPS_3 = property (GetGPS_3 , SetGPS_3)
   GPS_4 = property (GetGPS_4 , SetGPS_4)
   SurfaceTreatment = property (GetSurfaceTreatment , SetSurfaceTreatment)
   Destination = property (GetDestination , SetDestination)
   UseStiffenerData = property (GetUseStiffenerData , SetUseStiffenerData)
   Posno = property (GetPosno , SetPosno)
   PosnoPrefix = property (GetPosnoPrefix , SetPosnoPrefix)
   PosnoSuffix = property (GetPosnoSuffix , SetPosnoSuffix)
   def GetProfile(self): return self.__Profile
   Profile = property (GetProfile)
   Quality = property (GetQuality , SetQuality)
   def GetEnd(self): return self.__End
   End = property (GetEnd)
   TraceBevel = property (GetTraceBevel , SetTraceBevel)
   Shrinkage = property (GetShrinkage , SetShrinkage)
   FilletWeldDepth = property (GetFilletWeldDepth , SetFilletWeldDepth)
   Perpendicular = property (GetPerpendicular )

if __name__ == "__main__":
   sti = ShStiffProp()
   sti.SetProfileType(10)
   sti.SetProfileParameter(220)
   sti.SetProfileParameter(17)
   print sti

