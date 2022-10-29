## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsDocumentReference.py
#
#      PURPOSE:
#          The class holds information about a element document reference
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import types
import string

class DocumentReference(object):
   'holds information about element document reference'

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of DocumentReference class',
                     ValueError: 'not supported value, see documentation of DocumentReference class' }

   ReferenceTypes = { 'unknown': -1, 'drawing' : 1, 'file' : 2, 'vitesse' : 3, 'document' : 4 }

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#
   def __init__(self):
      self.__Type             = DocumentReference.ReferenceTypes['file']
      self.__Document         = ''
      self.__Description      = ''
      self.__Purpose          = None
      self.__ReferenceFormat  = None

#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      'implements cmp(o1, o2) function'

      # if None object return not equal
      if not isinstance(other, DocumentReference):
         return 1

      if self.__Type != other.__Type:
         return 1
      if self.__Document != other.__Document:
         return 1
      if self.__Description != other.__Description:
         return 1
      if self.__Purpose != other.__Purpose:
         return 1
      if self.__ReferenceFormat != other.__ReferenceFormat:
         return 1
      return 0



#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
   def __repr__(self):
      'returns string representation of DocumentReference instance'

      tup = (
         'DocumentReference:',
         '   Type: ' + str(self.ReferenceTypes.keys()[self.ReferenceTypes.values().index(self.__Type)]),
         '   Document: ' + str(self.__Document),
         '   Description: ' + str(self.__Description),
         '   Purpose: ' + str(self.__Purpose),
         '   ReferenceFormat: ' + str(self.__ReferenceFormat)
         )
      return string.join(tup, '\n')

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         SetType
#
#      PURPOSE:
#          set document reference type
#
#      INPUT:
#          Parameters:
#          typestr        string         document reference type
#
#      RESULT:
#          document reference type will be updated
#

   def SetType(self, typestr):
      'sets document reference type'

      if type(typestr) != types.StringType:
         raise TypeError, DocumentReference.__ErrorMessages[TypeError]

      if typestr not in self.ReferenceTypes.keys():
         raise ValueError, DocumentReference.__ErrorMessages[ValueError]

      self.__Type = DocumentReference.ReferenceTypes[typestr]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetType
#
#      PURPOSE:
#          get document reference type
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         document reference type
#

   def GetType(self):
      'returns document reference type as string'
      return self.ReferenceTypes.keys()[self.ReferenceTypes.values().index(self.__Type)]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         SetDocument
#
#      PURPOSE:
#          set referenced document
#
#      INPUT:
#          Parameters:
#          document        string
#
#      RESULT:
#          referenced document will be updated
#

   def SetDocument(self, document):
      'sets referenced document string'
      if type(document) != types.StringType:
         raise TypeError, DocumentReference.__ErrorMessages[TypeError]

      self.__Document = document

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetDocument
#
#      PURPOSE:
#          get referenced document string
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         referenced document
#

   def GetDocument(self):
      return self.__Document

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         SetDescription
#
#      PURPOSE:
#          set document reference description
#
#      INPUT:
#          Parameters:
#          name        string
#
#      RESULT:
#          description will be updated
#

   def SetDescription(self, name):
      'sets document reference description string'
      if type(name) != types.StringType:
         raise TypeError, DocumentReference.__ErrorMessages[TypeError]

      self.__Description = name

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetDescription
#
#      PURPOSE:
#          get document reference description
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         description
#

   def GetDescription(self):
      return self.__Description

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         SetPurpose
#
#      PURPOSE:
#          set document reference purpose
#
#      INPUT:
#          Parameters:
#          purpose        integer or None if not set
#
#      RESULT:
#          purpose will be updated
#

   def SetPurpose(self, purpose):
      'sets document reference purpose'
      if type(purpose) != type(0) and purpose!=None:
         raise TypeError, DocumentReference.__ErrorMessages[TypeError]

      self.__Purpose = purpose

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#         GetPurpose
#
#      PURPOSE:
#          get document reference purpose
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          integer or None        purpose
#

   def GetPurpose(self):
      return self.__Purpose

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Type = property (GetType, SetType, None, "Type - document reference type")
   Document = property (GetDocument, SetDocument, None, "Document - referenced document string")
   Description = property (GetDescription, SetDescription, None, "Description - document reference description")
   Purpose = property (GetPurpose, SetPurpose, None, "Purpose - document reference purpose")
