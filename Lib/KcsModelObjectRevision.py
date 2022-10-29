## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsModelObjectRevision.py
#
#      PURPOSE:
#          The class holds information about a revision
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __revisionName      string              revision name.
#          __revisionRemark    string              revision remark
#          __createdBy         string              created by
#          __createdDate       string              created date
#          __modifiedBy        string              modified by
#          __modifiedDate      string              modified date

import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation',
                  ValueError : 'not supported argument value, see documentation'}

class ModelObjectRevision(object):

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
      self.__revisionName = ''
      self.__revisionRemark = ''
      self.__createdBy = ''
      self.__createdDate = ''
      self.__modifiedBy = ''
      self.__modifiedDate = ''

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'ModelObjectRevision : %s %s %s %s %s %s' % (
      self.getRevisionName(), self.getRevisionRemark(), self.getCreatedBy(),
      self.getCreatedDate(), self.getModifiedBy(), self.getModifiedDate() )


#-------------------------------------------------------------------
#
#      METHOD:
#          __Set
#
#      PURPOSE:
#
#
#      INPUT:
#
#      RESULT:
#
#

   def __Set(self, revisionName, revisionRemark, createdBy, createdDate, modifiedBy, modifiedDate):
      if type(revisionName) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__revisionName = revisionName
      if type(revisionRemark) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__revisionRemark = revisionRemark
      if type(createdBy) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__createdBy = createdBy
      if type(createdDate) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__createdDate = createdDate
      if type(modifiedBy) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__modifiedBy = modifiedBy
      if type(modifiedDate) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__modifiedDate = modifiedDate

#-------------------------------------------------------------------
#
#      METHOD:
#          __Get
#
#      PURPOSE:
#          Get revision info
#
#

   def Get(self):
      return '%s %s %s %s %s %s' % (
      self.getRevisionName(), self.getRevisionRemark(), self.getCreatedBy(),
      self.getCreatedDate(), self.getModifiedBy(), self.getModifiedDate() )


#-------------------------------------------------------------------
#
#      METHOD:
#          getRevisionName
#
#      PURPOSE:
#           get
#
#
   def getRevisionName(self):
      return self.__revisionName


#-------------------------------------------------------------------
#
#      METHOD:
#          getRevisionRemark
#
#      PURPOSE:
#           get
#
#

   def getRevisionRemark(self):
      return self.__revisionRemark


#-------------------------------------------------------------------
#
#      METHOD:
#          getCreatedBy
#
#      PURPOSE:
#           get
#
#

   def getCreatedBy(self):
      return self.__createdBy


#-------------------------------------------------------------------
#
#      METHOD:
#          getCreatedDate
#
#      PURPOSE:
#           get
#
#

   def getCreatedDate(self):
      return self.__createdDate


#-------------------------------------------------------------------
#
#      METHOD:
#          getModifiedBy
#
#      PURPOSE:
#           get
#
#

   def getModifiedBy(self):
      return self.__modifiedBy


#-------------------------------------------------------------------
#
#      METHOD:
#          getModifiedDate
#
#      PURPOSE:
#           get
#
#

   def getModifiedDate(self):
      return self.__modifiedDate


#-------------------------------------------------------------------
#
#      METHOD:
#          setRevisionName
#
#      PURPOSE:
#           set
#
#

   def setRevisionName(self, value):
      if type(value) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__revisionName = value


#-------------------------------------------------------------------
#
#      METHOD:
#          setRevisionRemark
#
#      PURPOSE:
#           set
#
#

   def setRevisionRemark(self, value):
      if type(value) != types.StringType:
         raise TypeError, self.__ErrorMessages[TypeError]
      self.__revisionRemark = value

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   revisionName = property (getRevisionName,setRevisionName, None, 'revisionName')
   revisionRemark = property (getRevisionRemark,setRevisionRemark, None, 'revisionRemark')
   createdBy = property (getCreatedBy, None, None, 'createdBy')
   createdDate = property (getCreatedDate, None, None, 'createdDate')
   modifiedBy = property (getModifiedBy, None, None, 'modifiedBy')
   modifiedDate = property (getModifiedDate, None, None, 'modifiedDate')
