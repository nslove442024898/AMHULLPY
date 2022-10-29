## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsCommonProperties.py
#
#      PURPOSE:
#          The KcsCommonProperties class contains information about TDM properties
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __TypeCode1         Integer       Type code
#          __TypeCode2         Integer       Type code
#          __TypeCode3         Integer       Type code
#          __TypeCode4         Integer       Type code
#          __PlanningUnit      String        Planning unit
#          __CostCode          String        Cost code
#          __Alias1            String        Alias
#          __Alias2            String        Alias
#          __Alias3            String        Alias
#          __Alias4            String        Alias
#          __Description       String        Description
#          __Remarks           String        Remarks
#
#      METHODS:
#          SetTypeCode                       Sets type code
#          GetTypeCode                       Gets type code
#          SetPlanningUnit                   Sets planning unit
#          GetPlanningUnit                   Gets planning unit
#          SetCostCode                       Sets cost code
#          GetCostCode                       Gets cost code
#          SetAlias                          Sets alias
#          GetAlias                          Gets alias
#          SetDescription                    Sets description
#          GetDescription                    Gets description
#          SetRemarks                        Sets remarks
#          GetRemarks                        Gets remarks


import types
import string

ErrorMessages = { TypeError : 'not supported argument type, see documentation of KcsCommonProperties class',
                  ValueError : 'not supported argument value, see documentation of KcsCommonProperties class'}

class CommonProperties(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          None

    def __init__(self):
          self.__TypeCode1         = 0
          self.__TypeCode2         = -1
          self.__TypeCode3         = -1
          self.__TypeCode4         = -1
          self.__PlanningUnit      = ""
          self.__CostCode          = ""
          self.__Alias1            = ""
          self.__Alias2            = ""
          self.__Alias3            = ""
          self.__Alias4            = ""
          self.__Description       = ""
          self.__Remarks           = ""


#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
        tup = (
            "Type code1      :" + str(self.__TypeCode1),
            "Type code2      :" + str(self.__TypeCode2),
            "Type code3      :" + str(self.__TypeCode3),
            "Type code4      :" + str(self.__TypeCode4),
            "Planning unit   :" + str(self.__PlanningUnit),
            "Cost code       :" + str(self.__CostCode),
            "Alias1          :" + str(self.__Alias1),
            "Alias2          :" + str(self.__Alias2),
            "Alias3          :" + str(self.__Alias3),
            "Alias4          :" + str(self.__Alias4),
            "Description     :" + str(self.__Description),
            "Remarks         :" + str(self.__Remarks))
        return string.join (tup, '\n')


#
#      METHOD:
#          SetTypeCode
#
#      PURPOSE:
#          To set type code
#
#      INPUT:
#          Parameters:
#          No         Integer          Number
#          Code       Integer          type code

    def SetTypeCode(self, No, Code):
        if type(No) != types.IntType and type(No) != types.LongType and type(Code) != types.IntType and type(Code) != types.LongType:
            raise TypeError, ErrorMessages[TypeError]
        if No<0 or No>4:
            raise ValueError, ErrorMessages[ValueError]
        if No == 1:
            self.__TypeCode1 = Code
        elif No== 2:
            self.__TypeCode2 = Code
        elif No == 3:
            self.__TypeCode3 = Code
        else:
            self.__TypeCode4 = Code

#
#      METHOD:
#          GetTypeCode
#
#      PURPOSE:
#          To get type code
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Type code


    def GetTypeCode(self):
        return (self.__TypeCode1, self.__TypeCode2, self.__TypeCode3, self.__TypeCode4)



#
#      METHOD:
#          SetPlanningUnit
#
#      PURPOSE:
#          To set planning unit
#
#      INPUT:
#          Parameters:
#          PlanUnit       String              planning unit

    def SetPlanningUnit(self, PlanUnit):
            if type(PlanUnit) != type(""):
                raise TypeError, ErrorMessages[TypeError]
            self.__PlanningUnit = PlanUnit


#
#      METHOD:
#          GetPlanningUnit
#
#      PURPOSE:
#          To get planning unit
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Planning Unit


    def GetPlanningUnit(self):
        return self.__PlanningUnit


#
#      METHOD:
#          SetCostCode
#
#      PURPOSE:
#          To set cost code
#
#      INPUT:
#          Parameters:
#          Code       Integer              cost code

    def SetCostCode(self, Code):
            if type(Code) != type(""):
                raise TypeError, ErrorMessages[TypeError]
            self.__CostCode = Code


#
#      METHOD:
#          GetCostCode
#
#      PURPOSE:
#          To get cost code
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Cost code


    def GetCostCode(self):
        return self.__CostCode



#
#      METHOD:
#          SetAlias
#
#      PURPOSE:
#          To set alias
#
#      INPUT:
#          Parameters:
#          No           Integer             Number
#          Alias        String              Alias


    def SetAlias(self, No, Alias):
        if type(No) != types.IntType and type(No) != types.LongType or type(Alias) != types.StringType:
            raise TypeError, ErrorMessages[TypeError]
        if No<0 or No>4:
            raise ValueError, ErrorMessages[ValueError]
        if No == 1:
            self.__Alias1 = Alias
        elif No== 2:
            self.__Alias2 = Alias
        elif No == 3:
            self.__Alias3 = Alias
        else:
            self.__Alias4 = Alias


#
#      METHOD:
#          GetAlias
#
#      PURPOSE:
#          To get alias
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Alias


    def GetAlias(self):
        return (self.__Alias1, self.__Alias2, self.__Alias3, self.__Alias4)


#
#      METHOD:
#          SetDescription
#
#      PURPOSE:
#          To set description
#
#      INPUT:
#          Parameters:
#          desc       String              description

    def SetDescription(self, Desc):
            if type(Desc) != type(""):
                raise TypeError, ErrorMessages[TypeError]
            self.__Description = Desc


#
#      METHOD:
#          GetDescription
#
#      PURPOSE:
#          To get description
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Description


    def GetDescription(self):
        return self.__Description


#
#      METHOD:
#          SetRemarks
#
#      PURPOSE:
#          To set remarks
#
#      INPUT:
#          Parameters:
#          Remarks       String              Remarks

    def SetRemarks(self, rem):
            if type(rem) != type(""):
                raise TypeError, ErrorMessages[TypeError]
            self.__Remarks = rem


#
#      METHOD:
#          GetRemarks
#
#      PURPOSE:
#          To get remarks
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Remarks

    def GetRemarks(self):
        return self.__Remarks


#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    def getTypeCode1(self): return self.__TypeCode1
    def getTypeCode2(self): return self.__TypeCode2
    def getTypeCode3(self): return self.__TypeCode3
    def getTypeCode4(self): return self.__TypeCode4
    def setTypeCode1(self, value):
       if not type(value) in [types.IntType, types.LongType]:
          raise TypeError, ErrorMessages[TypeError]
       self.__TypeCode1 = value
    def setTypeCode2(self, value):
       if not type(value) in [types.IntType, types.LongType]:
          raise TypeError, ErrorMessages[TypeError]
       self.__TypeCode2 = value
    def setTypeCode3(self, value):
       if not type(value) in [types.IntType, types.LongType]:
          raise TypeError, ErrorMessages[TypeError]
       self.__TypeCode3 = value
    def setTypeCode4(self, value):
       if not type(value) in [types.IntType, types.LongType]:
          raise TypeError, ErrorMessages[TypeError]
       self.__TypeCode4 = value

    TypeCode1  =  property (getTypeCode1, setTypeCode1, None, '')
    TypeCode2  =  property (getTypeCode2, setTypeCode2, None, '')
    TypeCode3  =  property (getTypeCode3, setTypeCode3, None, '')
    TypeCode4  =  property (getTypeCode4, setTypeCode4, None, '')

    PlanningUnit = property (GetPlanningUnit, SetPlanningUnit, None, '')
    CostCode     = property (GetCostCode, SetCostCode, None, '')

    def getAlias1(self): return self.__Alias1
    def getAlias2(self): return self.__Alias2
    def getAlias3(self): return self.__Alias3
    def getAlias4(self): return self.__Alias4
    def setAlias1(self,value):
       if type(value)!=types.StringType:
          raise TypeError, ErrorMessages[TypeError]
       self.__Alias1 = value
    def setAlias2(self,value):
       if type(value)!=types.StringType:
          raise TypeError, ErrorMessages[TypeError]
       self.__Alias2 = value
    def setAlias3(self,value):
       if type(value)!=types.StringType:
          raise TypeError, ErrorMessages[TypeError]
       self.__Alias3 = value
    def setAlias4(self,value):
       if type(value)!=types.StringType:
          raise TypeError, ErrorMessages[TypeError]
       self.__Alias4 = value

    Alias1  =  property (getAlias1, setAlias1, None, '')
    Alias2  =  property (getAlias2, setAlias2, None, '')
    Alias3  =  property (getAlias3, setAlias3, None, '')
    Alias4  =  property (getAlias4, setAlias4, None, '')

    Description = property (GetDescription, SetDescription, None, 'Description')
    Remarks     = property (GetRemarks, SetRemarks, None, 'Remarks')
