## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          ResultPipeStructConn.py
#
#      PURPOSE:
#          The ResultPipeStructConn class contains information about structure connected to pipe part
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __StructName            String        Name of structure
#          __AliasName             String        Alias string
#
#      METHODS:
#          SetStruct                           Sets structure name
#          GetStruct                           Gets structure name
#          SetAlias                            Sets alias string
#          GetAlias                            Gets alias string

import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of ResultPipeStructConn class'}

class ResultPipeStructConn(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          StructName       string        Structure name
#          AliasName        string        Structure alias name

    def __init__(self, StructName = "", AliasName = ""):
        if type(StructName) != type("") or type(AliasName) != type(""):
            raise TypeError, ErrorMessages[TypeError]

        self.__StructName       = StructName
        self.__AliasName        = AliasName

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
        return "[Structure] " + self.__StructName + " [Alias] " + self.__AliasName

#
#      METHOD:
#          SetStruct
#
#      PURPOSE:
#          To set structure name
#
#      INPUT:
#          Parameters:
#          StructName        String        Structure name

    def SetStruct(self, StructName):
        if type(StructName) != type(""):
            raise TypeError, ErrorMessages[TypeError]

        self.__StructName = StructName

#
#      METHOD:
#          GetStruct
#
#      PURPOSE:
#          To get structure name
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Structure name


    def GetStruct(self):
        return self.__StructName

#
#      METHOD:
#          SetAlias
#
#      PURPOSE:
#          To set alias string
#
#      INPUT:
#          Parameters:
#          AliasName        String        Alias string

    def SetAlias(self, AliasName):
        if type(AliasName) != type(""):
            raise TypeError, ErrorMessages[TypeError]
        self.__AliasName = AliasName

#
#      METHOD:
#          GetAlias
#
#      PURPOSE:
#          To get alias string
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Alias string


    def GetAlias(self):
        return self.__AliasName

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    StructName       = property (GetStruct , SetStruct)
    AliasName        = property (GetAlias , SetAlias)
