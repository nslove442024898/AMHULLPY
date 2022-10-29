## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsWeldTable.py
#
#      PURPOSE:
#          The class holds information about a Weld Table
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES
import types
import string
import copy

from KcsWeldedJoint import WeldedJoint

class WeldTable(object):
   """Class holds information about Weld Table object"""

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Weld Table class',
                       IndexError: 'not supported index value, see documentation of Weld Table class',
                       ValueError: 'not supported value, see documentation of Weld Table class' }

# ----------------------------------------------------------------------------
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
      """to create instance of the class

ATTRIBUTES:
           WeldTableName           string           Weld table name
           WeldTableComment        string           The weld table comment
           WeldTableStatus         string           The weld table status
           TotalWeldLength         real             The total weld length
           TotalSuspensionLength   real             The total suspension length
           TotalConnectionLength   real             The total connection length
           WeldedJoints            Welded joint     Welded joint data
"""

      self.__WeldTableName          = ''
      self.__WeldTableComment       = ''
      self.__WeldTableStatus        = ''
      self.__TotalWeldLength        = 0.0
      self.__TotalSuspensionLength  = 0.0
      self.__TotalConnectionLength  = 0.0
      self.__WeldedJoints           = []


# ----------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
   def __repr__(self):
      'returns string representation of Weld object'

      tup = (
         'Weld Table:',
         '   Name: ' + self.__WeldTableName,
         '   Comment: ' + self.__WeldTableComment,
         '   Status: ' + self.__WeldTableStatus,
         '   Total weld length: ' + str(self.__TotalWeldLength),
         '   Total suspension length: ' + str(self.__TotalSuspensionLength),
         '   Total connection length: ' + str(self.__TotalConnectionLength),
         ' ',
         '   Welded Joints: ' + str(self.__WeldedJoints))

      return string.join(tup, '\n')

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldTableName
#
#      PURPOSE:
#          set weld table name
#
#      INPUT:
#          Parameters:
#          wtname        string         name of weld table
#
#      RESULT:
#          weld table name will be updated
#

   def SetWeldTableName(self, wtname):
      'sets weld table name'

      self.__WeldTableName = wtname

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldTableName
#
#      PURPOSE:
#          get weld table name
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld table name
#

   def GetWeldTableName(self):
      'returns name of weld table object'
      return self.__WeldTableName

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldTableComment
#
#      PURPOSE:
#          set weld table comment
#
#      INPUT:
#          Parameters:
#          wtcomment        string         comment of weld table
#
#      RESULT:
#          weld table comment will be updated
#

   def SetWeldTableComment(self, wtcomment):
      'sets weld table comment'

      self.__WeldTableComment = wtcomment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldTableComment
#
#      PURPOSE:
#          get weld table comment
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld table comment
#

   def GetWeldTableComment(self):
      'returns comment of weld table object'
      return self.__WeldTableComment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldTableStatus
#
#      PURPOSE:
#          set weld table status
#
#      INPUT:
#          Parameters:
#          wtstatus        string         status of weld table
#
#      RESULT:
#          weld table status will be updated
#

   def SetWeldTableStatus(self, wtstatus):
      'sets weld table status'

      self.__WeldTableStatus = wtstatus

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldTableStatus
#
#      PURPOSE:
#          get weld table status
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld table status
#

   def GetWeldTableStatus(self):
      'returns status of weld table object'
      return self.__WeldTableStatus

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetTotalWeldLength
#
#      PURPOSE:
#          set total weld length
#
#      INPUT:
#          Parameters:
#          name        real         totalweldlength
#
#      RESULT:
#          total weld length will be updated
#

   def SetTotalWeldLength(self, totalweldlength):
      'sets total weld length'

      if type(totalweldlength) != types.FloatType and type(totalweldlength) != types.IntType and type(totalweldlength) != types.LongType:
         raise TypeError, WeldTable.__ErrorMessages[TypeError]

      self.__TotalWeldLength = totalweldlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetTotalWeldLength
#
#      PURPOSE:
#          get total weld length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         totalweldlength
#

   def GetTotalWeldLength(self):
      'returns weld length'
      return self.__TotalWeldLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetTotalSuspensionLength
#
#      PURPOSE:
#          set total suspension length
#
#      INPUT:
#          Parameters:
#          totalsuspensionlength        real         total suspension length
#
#      RESULT:
#          total suspension length will be updated
#

   def SetTotalSuspensionLength(self, totalsuspensionlength):
      'sets total suspension length'

      if type(totalsuspensionlength) != types.FloatType and type(totalsuspensionlength) != types.IntType and type(totalsuspensionlength) != types.LongType:
         raise TypeError, WeldTable.__ErrorMessages[TypeError]

      self.__TotalSuspensionLength = totalsuspensionlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetTotalSuspensionLength
#
#      PURPOSE:
#          get total suspension length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         totalsuspensionlength
#

   def GetTotalSuspensionLength(self):
      'returns suspension length'
      return self.__TotalSuspensionLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetTotalConnectionLength
#
#      PURPOSE:
#          set total connection length
#
#      INPUT:
#          Parameters:
#          totalconnectionlength        real         total connection length
#
#      RESULT:
#          total connection length will be updated
#

   def SetTotalConnectionLength(self, totalconnectionlength):
      'sets total connection length'

      if type(totalconnectionlength) != types.FloatType and type(totalconnectionlength) != types.IntType and type(totalconnectionlength) != types.LongType:
         raise TypeError, WeldTable.__ErrorMessages[TypeError]

      self.__TotalConnectionLength = totalconnectionlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetTotalConnectionLength
#
#      PURPOSE:
#          get total connection length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         totalconnectionlength
#

   def GetTotalConnectionLength(self):
      'returns connection length'
      return self.__TotalConnectionLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldedJoint
#
#      PURPOSE:
#          set the given welded joint in the weld table
#
#      INPUT:
#          Parameters:
#          joint               int                  the current joint
#          welded joint        WeldedJoint          the welded joint
#
#      RESULT:
#          the welded joint will be updated
#

   def SetWeldedJoint(self, joint, inweldedjoint):
      'sets welded joint'

      if not isinstance(inweldedjoint, WeldedJoint):
         raise TypeError, WeldTable.__ErrorMessages[TypeError]
      if not 0 <= joint < len(self.__WeldedJoints):
         raise IndexError, WeldTable.__ErrorMessages[IndexError]

      self.__WeldedJoints[joint] = copy.deepcopy( inweldedjoint)

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldedJoint
#
#      PURPOSE:
#          get the given joint
#
#      INPUT:
#          Parameters:
#          joint       int          the current joint
#
#      RESULT:
#          Parameters:
#

   def GetWeldedJoint(self,joint):
      'returns the given welded joint'

      if not 0 <= joint < len(self.__WeldedJoints):
         raise IndexError, WeldTable.__ErrorMessages[IndexError]

      weldedjoint = copy.deepcopy( self.__WeldedJoints[joint])

      return weldedjoint

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetNumberWeldedJoints
#
#      PURPOSE:
#          get the number of welded joints
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          int            number of joints
#

   def GetNumberWeldedJoints(self):
      'returns number of welded joints in the weld table object'
      return len(self.__WeldedJoints)

# ----------------------------------------------------------------------------
#
#      METHOD:
#         AddWeldedJoint
#
#      PURPOSE:
#          add welded joint to the weld table
#
#      INPUT:
#          Parameters:
#          welded joint        WeldedJoint          The welded joint
#
#      RESULT:
#          the welded joint will be added
#

   def AddWeldedJoint(self, inweldedjoint):
      'adds welded joint'

      if not isinstance(inweldedjoint, WeldedJoint):
         raise TypeError, WeldTable.__ErrorMessages[TypeError]
      weldedjoint = copy.deepcopy( inweldedjoint)
      self.__WeldedJoints.append(weldedjoint)

# -----------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   WeldTableName = property (GetWeldTableName, SetWeldTableName, None, 'WeldTableName')
   WeldTableComment = property (GetWeldTableComment, SetWeldTableComment, None, 'WeldTableComment')
   WeldTableStatus = property (GetWeldTableStatus, SetWeldTableStatus, None, 'WeldTableStatus')
   TotalWeldLength = property (GetTotalWeldLength, SetTotalWeldLength, None, 'TotalWeldLength')
   TotalSuspensionLength = property (GetTotalSuspensionLength, SetTotalSuspensionLength, None, 'TotalSuspensionLength')
   TotalConnectionLength = property (GetTotalConnectionLength, SetTotalConnectionLength, None, 'TotalConnectionLength')
