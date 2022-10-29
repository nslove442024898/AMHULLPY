## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsWeldedJoint.py
#
#      PURPOSE:
#          The class holds information about a Weld
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES
import types
import string
import copy

from KcsWeld import Weld

class WeldedJoint(object):
   """Class holds information about Welded Joint object"""

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Welded Joint class',
                       IndexError: 'not supported index value, see documentation of Welded Joint class',
                       ValueError: 'not supported value, see documentation of Welded Joint class' }

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
           JointName          string            Welded joint name
           JointComment       string            Joint comment
           WeldType           string            Weld type
           JointLength        real              Joint length
           SuspensionLength   real              Suspension length
           ConnectionLength   real              Connection length
           Assembly1          string            Assembly name for first part
           Assembly2          string            Assembly name for second part
           PartName1          string            Part name for first part
           PartName2          string            Part name for second part
           ExtPartName1       string            Extended part name for 1st part
           ExtPartName2       string            Extended part name for 2nd part
           PartType1          integer           Part type for first part
           PartType2          integer           Part type for second part
           ManualFlag         integer           Manual flag
           Welds              Weld              Weld data
"""

      self.__JointName           = ''
      self.__JointComment        = ''
      self.__WeldType            = 'undefined'
      self.__JointLength         = 0.0
      self.__SuspensionLength    = 0.0
      self.__ConnectionLength    = 0.0
      self.__Assembly1           = ''
      self.__Assembly2           = ''
      self.__PartName1           = ''
      self.__PartName2           = ''
      self.__ExtPartName1        = ''
      self.__ExtPartName2        = ''
      self.__PartType1           = 0
      self.__PartType2           = 0
      self.__ManualFlag          = 0
      self.__Welds               = []


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
         'Welded Joint:',
         '   JointName: ' + self.__JointName,
         '   JointComment: ' + self.__JointComment,
         '   WeldType: ' + self.__WeldType,
         '   JointLength: ' + str(self.__JointLength),
         '   SuspensionLength: ' + str(self.__SuspensionLength),
         '   ConnectionLength: ' + str(self.__ConnectionLength),
         '   Assembly1: ' + self.__Assembly1,
         '   Assembly2: ' + self.__Assembly2,
         '   PartName1: ' + self.__PartName1,
         '   PartName2: ' + self.__PartName2,
         '   ExtPartName1: ' + self.__ExtPartName1,
         '   ExtPartName2: ' + self.__ExtPartName2,
         '   PartType1: ' + str(self.__PartType1),
         '   PartType2: ' + str(self.__PartType2),
         '   ManualFlag: ' + str(self.__ManualFlag),
         ' ',
         '   Welds: ' + str(self.__Welds))

      return string.join(tup, '\n')

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetJointName
#
#      PURPOSE:
#          set welded joint name
#
#      INPUT:
#          Parameters:
#          joint        integer         number of welded joint
#
#      RESULT:
#          welded joint name will be updated
#

   def SetJointName(self, joint):
      'sets welded joint name'

      jointname = 'J-' + str( joint)
      self.__JointName = jointname

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetJointName
#
#      PURPOSE:
#          get welded joint name
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         welded joint name
#

   def GetJointName(self):
      'returns name of welded joint object'
      return self.__JointName

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetJointComment
#
#      PURPOSE:
#          set welded joint comment
#
#      INPUT:
#          Parameters:
#          comment        string         welded joint comment
#
#      RESULT:
#          welded joint comment will be updated
#

   def SetJointComment(self, comment):
      'sets welded joint comment'

      self.__JointComment = comment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetJointComment
#
#      PURPOSE:
#          get welded joint comment
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         welded joint comment
#

   def GetJointComment(self):
      'returns comment of welded joint object'
      return self.__JointComment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldType
#
#      PURPOSE:
#          set weld type
#
#      INPUT:
#          Parameters:
#          wtype        string         weld type
#
#      RESULT:
#          weld type will be updated
#

   def SetWeldType(self, wtype):
      'sets weld type'

      if type(wtype) != types.StringType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      self.__WeldType = wtype

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldType
#
#      PURPOSE:
#          get weld type
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld type
#

   def GetWeldType(self):
      'returns weld type'
      return self.__WeldType

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetJointLength
#
#      PURPOSE:
#          set joint weld length
#
#      INPUT:
#          Parameters:
#          jointlength        real         joint length
#
#      RESULT:
#          joint length will be updated
#

   def SetJointLength(self, jointlength):
      'sets joint length'

      if type(jointlength) != types.FloatType and type(jointlength) != types.IntType and type(jointlength) != types.LongType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      self.__JointLength = jointlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetJointLength
#
#      PURPOSE:
#          get joint length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         jointlength
#

   def GetJointLength(self):
      'returns joint length'
      return self.__JointLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetSuspensionLength
#
#      PURPOSE:
#          set suspension length
#
#      INPUT:
#          Parameters:
#          suspensionlength        real         suspension length
#
#      RESULT:
#          suspension length will be updated
#

   def SetSuspensionLength(self, suspensionlength):
      'sets suspension length'

      if type(suspensionlength) != types.FloatType and type(suspensionlength) != types.IntType and type(suspensionlength) != types.LongType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      self.__SuspensionLength = suspensionlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetSuspensionLength
#
#      PURPOSE:
#          get suspension length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         suspensionlength
#

   def GetSuspensionLength(self):
      'returns suspension length'
      return self.__SuspensionLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetConnectionLength
#
#      PURPOSE:
#          set connection length
#
#      INPUT:
#          Parameters:
#          connectionlength        real         connection length
#
#      RESULT:
#          connection length will be updated
#

   def SetConnectionLength(self, connectionlength):
      'sets connection length'

      if type(connectionlength) != types.FloatType and type(connectionlength) != types.IntType and type(connectionlength) != types.LongType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      self.__ConnectionLength = connectionlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetConnectionLength
#
#      PURPOSE:
#          get connection length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         connectionlength
#

   def GetConnectionLength(self):
      'returns connection length'
      return self.__ConnectionLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetAssemblyName
#
#      PURPOSE:
#          set assembly name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#          assembly    string       assembly name
#
#      RESULT:
#          assembly name will be updated for the given part
#

   def SetAssemblyName(self, part, assembly):
      'sets assembly name'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if type(assembly) != types.StringType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      if part == 1:
         self.__Assembly1 = assembly
      else:
         self.__Assembly2 = assembly

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetAssemblyName
#
#      PURPOSE:
#          get assembly name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#
#      RESULT:
#          string         assembly for part <part>
#

   def GetAssemblyName(self,part):
      'returns assembly'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if part == 1:
         return self.__Assembly1
      else:
         return self.__Assembly2

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetPartName
#
#      PURPOSE:
#          set part name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#          name        string       part name
#
#      RESULT:
#          part name will be updated for the given part
#

   def SetPartName(self, part, name):
      'sets part name'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if type(name) != types.StringType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      if part == 1:
         self.__PartName1 = name
      else:
         self.__PartName2 = name

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetPartName
#
#      PURPOSE:
#          get name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#
#      RESULT:
#          string         name for part <part>
#

   def GetPartName(self,part):
      'returns name'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if part == 1:
         return self.__PartName1
      else:
         return self.__PartName2

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetExtendedPartName
#
#      PURPOSE:
#          set extended part name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#          name        string       extended part name
#
#      RESULT:
#          Extended part name will be updated for the given part
#

   def SetExtendedPartName(self, part, name):
      'sets extended part name'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if type(name) != types.StringType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      if part == 1:
         self.__ExtPartName1 = name
      else:
         self.__ExtPartName2 = name

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetExtendedPartName
#
#      PURPOSE:
#          get extended part name for the given part
#
#      INPUT:
#          Parameters:
#          part        int          part (1 or 2)
#
#      RESULT:
#          string         Extended part name for part <part>
#

   def GetExtendedPartName(self,part):
      'returns name'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if part == 1:
         return self.__ExtPartName1
      else:
         return self.__ExtPartName2

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetPartType
#
#      PURPOSE:
#          set part type
#
#      INPUT:
#          Parameters:
#              part           integer        part (1 or 2)
#              intype         integer        part type
#
#      RESULT:
#          part type will be update for the given part
#

   def SetPartType(self, part, intype):
      'sets part type'

      if type(intype) != types.IntType and type(intype) != types.LongType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]
      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if part == 1:
         self.__PartType1 = intype
      else:
         self.__PartType2 = intype

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetManualFlag
#
#      PURPOSE:
#          set manual flag
#
#      INPUT:
#          Parameters:
#          manualflag        integer         manual flag
#
#      RESULT:
#          manual flag will be updated
#

   def SetManualFlag(self, manualflag):
      'sets manual flag'

      if type(manualflag) != types.IntType and type(manualflag) != types.LongType:
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      self.__ManualFlag = manualflag

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetManualFlag
#
#      PURPOSE:
#          get manual flag
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          integer         manual flag
#

   def GetManualFlag(self):
      'returns joint length'
      return self.__ManualFlag

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetPartType
#
#      PURPOSE:
#          get type for the given part
#
#      INPUT:
#          Parameters:
#          part           integer        part (1 or 2)
#
#      RESULT:
#          integer         type for part <part>
#

   def GetPartType(self,part):
      'returns type'

      if not 1 <= part <= 2:
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      if part == 1:
         return self.__PartType1
      else:
         return self.__PartType2

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetNumberWelds
#
#      PURPOSE:
#          get the number of welds
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          int            number of welds
#

   def GetNumberWelds(self):
      'returns number of welds in the given joint object'
      return len(self.__Welds)

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeld
#
#      PURPOSE:
#          set the weld to the welded joint
#
#      INPUT:
#          Parameters:
#          weld        int           the current weld
#          inweld      Weld          the weld
#
#      RESULT:
#          the weld will be added
#

   def SetWeld(self, weld, inweld):
      'sets weld'

      if not isinstance(inweld, Weld):
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]
      if not 0 <= weld < len(self.__Welds):
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      self.__Welds[weld] = copy.deepcopy( inweld)

# -----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeld
#
#      PURPOSE:
#          get the given weld
#
#      INPUT:
#          Parameters:
#          weld       int          the current weld
#
#      RESULT:
#          Parameters:
#

   def GetWeld(self,weld):
      'returns the given weld'

      if not 0 <= weld < len(self.__Welds):
         raise IndexError, WeldedJoint.__ErrorMessages[IndexError]

      currentweld = copy.deepcopy( self.__Welds[weld])

      return currentweld

# ----------------------------------------------------------------------------
#
#      METHOD:
#         AddWeld
#
#      PURPOSE:
#          add weld to the welded joint
#
#      INPUT:
#          Parameters:
#          weld        Weld          The weld
#
#      RESULT:
#          the weld will be added
#

   def AddWeld(self, inweld):
      'adds weld'

      if not isinstance(inweld, Weld):
         raise TypeError, WeldedJoint.__ErrorMessages[TypeError]

      weld = copy.deepcopy( inweld)
      self.__Welds.append(weld)

# ----------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   JointName = property (GetJointName, SetJointName, None, 'JointName')
   JointComment = property (GetJointComment, SetJointComment, None, 'JointComment')
   WeldType = property (GetWeldType, SetWeldType, None, 'WeldType')
   JointLength = property (GetJointLength, SetJointLength, None, 'JointLength')
   SuspensionLength = property (GetSuspensionLength, SetSuspensionLength, None, 'SuspensionLength')
   ConnectionLength = property (GetConnectionLength, SetConnectionLength, None, 'ConnectionLength')
   ManualFlag = property (GetManualFlag, SetManualFlag, None, 'ManualFlag')

