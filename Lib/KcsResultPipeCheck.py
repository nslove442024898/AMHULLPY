## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          ResultPipeCheck.py
#
#      PURPOSE:
#          The ResultPipeCheck class contains pipe productoion check information
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __PartId            Integer        Part Id number
#          __ConnNo            Integer        Connection number
#          __MsgNo             Integer        Message number
#          __MsgString         Integer        Message text
#
#      METHODS:
#          SetPartId                           sets part Id number
#          GetPartId                           gets part Id number
#          SetConnection                       sets connection number
#          GetConnection                       gets connection number
#          SetMessageNo                        sets message number
#          GetMessageNo                        gets message number
#          SetMessage                          sets message text
#          GetMessage                          gets message text


class ResultPipeCheck(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          PartId        integer        Part Id number
#          ConnNo        integer        Connection number
#          MsgNo         integer        Message number
#          MsgString     string         Message string

    def __init__(self, PartId = 0, ConnNo =0, MsgNo = 0, MsgString = ""):
        self.__PartId       = PartId
        self.__ConnNo       = ConnNo
        self.__MsgNo        = MsgNo
        self.__MsgString    = MsgString

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
        return "Part: " + str(self.__PartId) + " Conn: " + str(self.__ConnNo) + " Message: " + self.__MsgString

#
#      METHOD:
#          SetPartId
#
#      PURPOSE:
#          To set part Id number
#
#      INPUT:
#          Parameters:
#          PartId        Integer        part Id number

    def SetPartId(self, PartId):
        self.__PartId = PartId

#
#      METHOD:
#          GetPartId
#
#      PURPOSE:
#          To get part Id number
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Part Id number


    def GetPartId(self):
        return self.__PartId

#
#      METHOD:
#          SetConnection
#
#      PURPOSE:
#          To set connection number
#
#      INPUT:
#          Parameters:
#          ConnNo        Integer        connection number

    def SetConnection(self, ConnNo):
        self.__ConnNo = ConnNo

#
#      METHOD:
#          GetConnection
#
#      PURPOSE:
#          To get connection number
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Connection number


    def GetConnection(self):
        return self.__ConnNo


#
#      METHOD:
#          SetMessageNo
#
#      PURPOSE:
#          To set message number
#
#      INPUT:
#          Parameters:
#          MsgNo        Integer        message number

    def SetMessageNo(self, MsgNo):
        self.__MsgNo = MsgNo

#
#      METHOD:
#          GetMessageNo
#
#      PURPOSE:
#          To get message number
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Message number


    def GetMessageNo(self):
        return self.__MsgNo


#
#      METHOD:
#          SetMessage
#
#      PURPOSE:
#          To set message text
#
#      INPUT:
#          Parameters:
#          Msg        String        message text

    def SetMessage(self, Msg):
        self.__MsgString = Msg

#
#      METHOD:
#          GetMessage
#
#      PURPOSE:
#          To get message text
#
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          Message text


    def GetMessage(self):
        return self.__MsgString


#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    PartId = property (GetPartId , SetPartId)
    ConnNo = property (GetConnection , SetConnection)
    MsgNo =  property (GetMessageNo , SetMessageNo)
    MsgString = property (GetMessage , SetMessage)
