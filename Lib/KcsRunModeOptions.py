## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          RunModeOptions.py
#
#      PURPOSE:
#          The RunModeOptions class contains options
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __ConfirmGeneration          Integer        Confirm generation option
#          __TraceOn                    Integer        Trace on option
#
#      METHODS:
#          SetConfirmGeneration                        Set Confirm Generation
#          GetConfirmGeneration                        Get Confirm Generation
#          SetTraceOn                                  Set Trace on option
#          GetTraceOn                                  Get Trace on option


import string

ErrorMessages = { TypeError : 'not supported argument type, see documentation of RunModeOptions class',
                  ValueError : 'not supported argument value, see documentation of RunModeOptions class'}

class RunModeOptions(object):

# --------------------------------------------------------------------------
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
          self.__ConfirmGeneration   = None
          self.__TraceOn             = None

# --------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
        tup = (
            "Trace On           :" + str(self.__TraceOn),
            "Confirm Generation :" + str(self.__ConfirmGeneration))
        return string.join (tup, '\n')

# --------------------------------------------------------------------------
#
#      METHOD:
#          SetConfirmGeneration
#
#      PURPOSE:
#          To set Confirm Generation option
#
#      INPUT:
#          Parameters:
#          State       Integer               ( State=0 confirm off , State=1 confirm on)

    def SetConfirmGeneration(self, State = 1):
            if not isinstance(State,int) and State!=None:
                raise TypeError, ErrorMessages[TypeError]

            if State not in [0,1,None]:
                raise ValueError, ErrorMessages[ValueError]

            self.__ConfirmGeneration = State

# --------------------------------------------------------------------------
#
#      METHOD:
#          GetConfirmGeneration
#
#      PURPOSE:
#          To get Confirm Generation Option
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          State


    def GetConfirmGeneration(self):
        return self.__ConfirmGeneration


# --------------------------------------------------------------------------
#
#      METHOD:
#          SetTraceOn
#
#      PURPOSE:
#          To set Trace On option
#
#      INPUT:
#          Parameters:
#          State       Integer               ( State=0 Trace off , State=1 Trace on)

    def SetTraceOn(self, State = 1):

            if not isinstance(State,int) and State!=None:
                raise TypeError, ErrorMessages[TypeError]

            if State not in [0,1,None]:
                raise ValueError, ErrorMessages[ValueError]

            self.__TraceOn = State

# --------------------------------------------------------------------------
#
#      METHOD:
#          GetTraceOn
#
#      PURPOSE:
#          To get Trace On Option
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          State


    def GetTraceOn(self):
        return self.__TraceOn

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    ConfirmGeneration = property (GetConfirmGeneration , SetConfirmGeneration)
    TraceOn = property (GetTraceOn , SetTraceOn)
