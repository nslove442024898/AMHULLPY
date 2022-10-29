## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsWeld.py
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

from KcsGeoContour3D import GeoContour3D
from KcsPoint3D import Point3D
from KcsVector3D import Vector3D

class Weld:
   """Class holds information about Weld object"""

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of Weld class',
                       IndexError: 'not supported index value, see documentation of Weld class',
                       ValueError: 'not supported value, see documentation of Weld class' }

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
           WeldName          string            Weld name
           WeldComment       string            Weld comment
           WeldLength        real              Weld length
           LegLength         real              Weld leg length
           Layers            int               Number of weld layers
           Position          string            Weld position
           TestProcedure     string            Test procedure
           Process           string            Process
           StandardProcess   string            Standard process
           StartSuspension   real              Start suspension
           EndSuspension     real              End suspension
           ConnectionAngle   real              Connection angle
           RotationAngle     real              Rotation angle
           InclinationAngle  real              Inclination angle
           TorchVector       Vector3D          Torch vector
           BevelPart1        real              Bevelcode part 1
           BevelPart2        real              Bevelcode part 2
           ThicknessPart1    real              Thickness part 1
           ThicknessPart2    real              Thickness part 2
           QualityPart1      string            Quality part 1
           QualityPart2      string            Quality part 2
           Geometry          GeoContour3D      Weld geometry
"""

      self.__WeldName            = ''
      self.__WeldComment         = ''
      self.__WeldLength          = 0.0
      self.__LegLength           = 0.0
      self.__Layers              = 1
      self.__Position            = ''
      self.__TestProcedure       = ''
      self.__Process             = ''
      self.__StandardProcess     = ''
      self.__StartSuspension     = 0.0
      self.__EndSuspension       = 0.0
      self.__ConnectionAngle     = 0.0
      self.__RotationAngle       = 0.0
      self.__InclinationAngle    = 0.0
      self.__TorchVector         = Vector3D( 0.0, 0.0, 0.0)
      self.__BevelPart1          = 0
      self.__BevelPart2          = 0
      self.__ThicknessPart1      = 0.0
      self.__ThicknessPart2      = 0.0
      self.__QualityPart1        = ''
      self.__QualityPart2        = ''
      self.__Geometry            = GeoContour3D()


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
         'Weld:',
         '   Name: ' + self.__WeldName,
         '   WeldComment: ' + self.__WeldComment,
         '   WeldLength: ' + str(self.__WeldLength),
         '   LegLength: ' + str(self.__LegLength),
         '   Layers: ' + str(self.__Layers),
         '   Position: ' + self.__Position,
         '   TestProcedure: ' + self.__TestProcedure,
         '   Process: ' + self.__Process,
         '   StandardProcess: ' + self.__StandardProcess,
         '   StartSuspension: ' + str(self.__StartSuspension),
         '   EndSuspension: ' + str(self.__EndSuspension),
         '   ConnectionAngle: ' + str(self.__ConnectionAngle),
         '   RotationAngle: ' + str(self.__RotationAngle),
         '   InclinationAngle: ' + str(self.__InclinationAngle),
         '   TorchVector : ' + str(self.__TorchVector),
         '   BevelPart1: ' + str(self.__BevelPart1),
         '   BevelPart2: ' + str(self.__BevelPart2),
         '   ThicknessPart1: ' + str(self.__ThicknessPart1),
         '   ThicknessPart2: ' + str(self.__ThicknessPart2),
         '   QualityPart1: ' + self.__QualityPart1,
         '   QualityPart2: ' + self.__QualityPart2,
         '   Geometry: ' + str(self.__Geometry))

      return string.join(tup, '\n')

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldName
#
#      PURPOSE:
#          set weld name
#
#      INPUT:
#          Parameters:
#          joint       int         joint number
#          weld        int         weld number
#
#      RESULT:
#          weld name will be updated
#

   def SetWeldName(self, joint, weld):
      'sets weld name'

      weldname = 'J-' + str( joint) + '/W-' + str( weld)
      self.__WeldName = weldname

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldName
#
#      PURPOSE:
#          get weld name
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld name
#

   def GetWeldName(self):
      'returns name of weld object'
      return self.__WeldName

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldComment
#
#      PURPOSE:
#          set weld comment
#
#      INPUT:
#          Parameters:
#          comment        string         weld comment
#
#      RESULT:
#          weld comment will be updated
#

   def SetWeldComment(self, comment):
      'sets weld comment'

      self.__WeldComment = comment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldComment
#
#      PURPOSE:
#          get weld comment
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld comment
#

   def GetWeldComment(self):
      'returns comment of weld object'
      return self.__WeldComment

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetWeldLength
#
#      PURPOSE:
#          set weld length
#
#      INPUT:
#          Parameters:
#          name        real         weldlength
#
#      RESULT:
#          weld length will be updated
#

   def SetWeldLength(self, weldlength):
      'sets weld length'

      if type(weldlength) != types.FloatType and type(weldlength) != types.IntType and type(weldlength) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__WeldLength = weldlength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetWeldLength
#
#      PURPOSE:
#          get weld length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         weldlength
#

   def GetWeldLength(self):
      'returns weld length'
      return self.__WeldLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetLegLength
#
#      PURPOSE:
#          set weld leg length
#
#      INPUT:
#          Parameters:
#          name        real         weld leglength
#
#      RESULT:
#          weld leglength will be updated
#

   def SetLegLength(self, leglength):
      'sets weld leg length'

      if type(leglength) != types.FloatType and type(leglength) != types.IntType and type(leglength) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__LegLength = leglength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetLegLength
#
#      PURPOSE:
#          get weld leg length
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         weld leg length
#

   def GetLegLength(self):
      'returns weld leg length'
      return self.__LegLength

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetLayers
#
#      PURPOSE:
#          set number of weld layers
#
#      INPUT:
#          Parameters:
#          name        int         number of weld Layers
#
#      RESULT:
#          weld layers will be updated
#

   def SetLayers(self, layers):
      'sets number of weld layers'

      if type(layers) != types.IntType and type(layers) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__Layers = layers

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetLayers
#
#      PURPOSE:
#          get number of weld layers
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          int         number of weldlayers
#

   def GetLayers(self):
      'returns weld leg length'
      return self.__Layers

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetPosition
#
#      PURPOSE:
#          set weld position
#
#      INPUT:
#          Parameters:
#          name        string         weld position
#
#      RESULT:
#          weld position will be updated
#

   def SetPosition(self, position):
      'sets weld position'

      if type(position) != types.StringType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__Position = position

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetPosition
#
#      PURPOSE:
#          get weld position
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld position
#

   def GetPosition(self):
      'returns weld position'
      return self.__Position

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetTestProcedure
#
#      PURPOSE:
#          set weld testprocedure
#
#      INPUT:
#          Parameters:
#          name        string         weld testprocedure
#
#      RESULT:
#          weld testprocedure will be updated
#

   def SetTestProcedure(self, testprocedure):
      'sets weld testprocedure'

      if type(testprocedure) != types.StringType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__TestProcedure = testprocedure

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetTestProcedure
#
#      PURPOSE:
#          get weld testprocedure
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld testprocedure
#

   def GetTestProcedure(self):
      'returns weld testprocedure'
      return self.__TestProcedure

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetProcess
#
#      PURPOSE:
#          set weld process
#
#      INPUT:
#          Parameters:
#          name        string         weld process
#
#      RESULT:
#          weld process will be updated
#

   def SetProcess(self, process):
      'sets weld process'

      if type(process) != types.StringType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__Process = process

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetProcess
#
#      PURPOSE:
#          get weld process
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld process
#

   def GetProcess(self):
      'returns weld process'
      return self.__Process

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetStandardProcess
#
#      PURPOSE:
#          set weld standard process
#
#      INPUT:
#          Parameters:
#          name        string         weld standard process
#
#      RESULT:
#          weld standard process will be updated
#

   def SetStandardProcess(self, standardprocess):
      'sets weld standard process'

      if type(standardprocess) != types.StringType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__StandardProcess = standardprocess

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetStandardProcess
#
#      PURPOSE:
#          get weld standard process
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          string         weld standard process
#

   def GetStandardProcess(self):
      'returns weld standard process'
      return self.__StandardProcess

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetStartSuspension
#
#      PURPOSE:
#          set start suspension
#
#      INPUT:
#          Parameters:
#          startsuspension        real         start suspension
#
#      RESULT:
#          start suspension will be updated
#

   def SetStartSuspension(self, startsuspension):
      'sets start suspension'

      if type(startsuspension) != types.FloatType and type(startsuspension) != types.IntType and type(startsuspension) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__StartSuspension = startsuspension

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetStartSuspension
#
#      PURPOSE:
#          get start suspension
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         start suspension
#

   def GetStartSuspension(self):
      'returns start suspension'
      return self.__StartSuspension

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetEndSuspension
#
#      PURPOSE:
#          set start suspension
#
#      INPUT:
#          Parameters:
#          EndSuspension        real         end suspension
#
#      RESULT:
#          end suspension will be updated
#

   def SetEndSuspension(self, endsuspension):
      'sets end suspension'

      if type(endsuspension) != types.FloatType and type(endsuspension) != types.IntType and type(endsuspension) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__EndSuspension = endsuspension

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetEndSuspension
#
#      PURPOSE:
#          get end suspension
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         end suspension
#

   def GetEndSuspension(self):
      'returns start suspension'
      return self.__EndSuspension

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetConnectionAngle
#
#      PURPOSE:
#          set connection angle
#
#      INPUT:
#          Parameters:
#          connectionangle        real         connection angle
#
#      RESULT:
#          connection angle will be updated
#

   def SetConnectionAngle(self, connectionangle):
      'sets connection angle'

      if type(connectionangle) != types.FloatType and type(connectionangle) != types.IntType and type(connectionangle) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__ConnectionAngle = connectionangle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetConnectionAngle
#
#      PURPOSE:
#          get connection angle
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         connection angle
#

   def GetConnectionAngle(self):
      'returns connection angle'
      return self.__ConnectionAngle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetRotationAngle
#
#      PURPOSE:
#          set rotation angle
#
#      INPUT:
#          Parameters:
#          rotationangle        real         rotation angle
#
#      RESULT:
#          rotation angle will be updated
#

   def SetRotationAngle(self, rotationangle):
      'sets rotation angle'

      if type(rotationangle) != types.FloatType and type(rotationangle) != types.IntType and type(rotationangle) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__RotationAngle = rotationangle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetRotationAngle
#
#      PURPOSE:
#          get rotation angle
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         rotation angle
#

   def GetRotationAngle(self):
      'returns rotation angle'
      return self.__RotationAngle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetInclinationAngle
#
#      PURPOSE:
#          set inclination angle
#
#      INPUT:
#          Parameters:
#          inclinationangle        real         inclination angle
#
#      RESULT:
#          inclination angle will be updated
#

   def SetInclinationAngle(self, inclinationangle):
      'sets inclination angle'

      if type(inclinationangle) != types.FloatType and type(inclinationangle) != types.IntType and type(inclinationangle) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      self.__InclinationAngle = inclinationangle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetInclinationAngle
#
#      PURPOSE:
#          get inclination angle
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          real         inclination angle
#

   def GetInclinationAngle(self):
      'returns inclination angle'
      return self.__InclinationAngle

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetTorchVector
#
#      PURPOSE:
#          set torch vector
#
#      INPUT:
#          Parameters:
#          torchvector        Vector3D         torch vector
#
#      RESULT:
#          torch vector will be updated
#

   def SetTorchVector(self, torchvector):
      'sets torch vector'

      self.__TorchVector = torchvector

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetTorchVector
#
#      PURPOSE:
#          get torch vector
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          Vector3D         torch vector
#

   def GetTorchVector(self):
      'returns torch vector'
      return self.__TorchVector

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetBevelCode
#
#      PURPOSE:
#          set bevel code for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#          name        real         bevelcode for part <part>
#
#      RESULT:
#          weld bevelcode will be updated for the given part
#

   def SetBevelCode(self, part, bevelcode):
      'sets bevel code'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if type(bevelcode) != types.FloatType and type(bevelcode) != types.IntType and type(bevelcode) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      if part == 1:
         self.__BevelPart1 = bevelcode
      else:
         self.__BevelPart2 = bevelcode

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetBevelCode
#
#      PURPOSE:
#          get bevelcode for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#
#      RESULT:
#          real         bevel code for part <part>
#

   def GetBevelCode(self,part):
      'returns bevel code'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if part == 1:
         return self.__BevelPart1
      else:
         return self.__BevelPart2

# -----------------------------------------------------------------------------
#
#      METHOD:
#         SetThickness
#
#      PURPOSE:
#          set thickness for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#          name        real         thickness for part <part>
#
#      RESULT:
#          weld thickness will be updated for the given part
#

   def SetThickness(self, part, thickness):
      'sets thickness'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if type(thickness) != types.FloatType and type(thickness) != types.IntType and type(thickness) != types.LongType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      if part == 1:
         self.__ThicknessPart1 = thickness
      else:
         self.__ThicknessPart2 = thickness

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetThickness
#
#      PURPOSE:
#          get thickness for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#
#      RESULT:
#          real         thickness for part <part>
#

   def GetThickness(self,part):
      'returns thickness'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if part == 1:
         return self.__ThicknessPart1
      else:
         return self.__ThicknessPart2

# ----------------------------------------------------------------------------
#
#      METHOD:
#         SetQuality
#
#      PURPOSE:
#          set quality for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#          name        string       quality for part <part>
#
#      RESULT:
#          weld quality will be updated for the given part
#

   def SetQuality(self, part, quality):
      'sets quality'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if type(quality) != types.StringType:
         raise TypeError, Weld.__ErrorMessages[TypeError]

      if part == 1:
         self.__QualityPart1 = quality
      else:
         self.__QualityPart2 = quality

# ----------------------------------------------------------------------------
#
#      METHOD:
#         GetQuality
#
#      PURPOSE:
#          get quality for the given part
#
#      INPUT:
#          Parameters:
#          name        int          part (1 or 2)
#
#      RESULT:
#          string        quality for part <part>
#

   def GetQuality(self,part):
      'returns quality'

      if not 1 <= part <= 2:
         raise IndexError, Weld.__ErrorMessages[IndexError]

      if part == 1:
         return self.__QualityPart1
      else:
         return self.__QualityPart2

#-----------------------------------------------------------------------------
#
#      METHOD:
#         SetPoint
#
#      PURPOSE:
#          Set first point of contour
#
#      INPUT:
#          Parameters:
#          point     Point3D        3D point
#
#      RESULT:
#          None
#
   def SetPoint(self, *args):
      """sets start point of the contour"""

      if len(args)==1:
         if not isinstance(args[0], Point3D):
            raise TypeError, Weld.__ErrorMessages[TypeError]

         apply( self.__Geometry.SetPoint, args)
      else:
         raise TypeError, Weld.__ErrorMessages[TypeError]

# -----------------------------------------------------------------------------
#
#      METHOD:
#         AddArc
#
#      PURPOSE:
#          Add an arc segment to the contour
#
#      INPUT:
#          Parameters:
#          point     Point3D        3D point
#          amplitude Vector3D       amplitude vector
#
#      RESULT:
#          None
#
   def AddArc(self, *args):
      """adds an arc segment to the contour"""

      if len(args)==2:
         if not isinstance(args[0], Point3D):
            raise TypeError, Weld.__ErrorMessages[TypeError]

         apply( self.__Geometry.AddArc, args)
      else:
         raise TypeError, Weld.__ErrorMessages[TypeError]

# -----------------------------------------------------------------------------
#
#      METHOD:
#         AddLine
#
#      PURPOSE:
#          Add a line (straight) segment to the contour
#
#      INPUT:
#          Parameters:
#          point     Point3D        3D point
#
#      RESULT:
#          None
#
   def AddLine(self, *args):
      """adds a line segment to the contour"""

      if len(args)==1:
         if not isinstance(args[0], Point3D):
            raise TypeError, Weld.__ErrorMessages[TypeError]

         apply( self.__Geometry.AddLine, args)
      else:
         raise TypeError, Weld.__ErrorMessages[TypeError]

# -----------------------------------------------------------------------------
#
#      METHOD:
#         GetNoSegments
#
#      PURPOSE:
#          get number of segments in the contour
#
#      INPUT:
#          Parameters:
#            None
#
#      RESULT:
#          integer         number of segments
#
   def GetNoSegments(self):
      """returns the number of segments in the contour"""

      nseg = len( self.__Geometry.Contour)
      if nseg > 0:
         return ( nseg -1)
      else:
         return ( 0)

# -----------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   WeldName = property (GetWeldName, None, None, 'WeldName')
   WeldComment = property (GetWeldComment, SetWeldComment, None, 'WeldComment')
   WeldLength = property (GetWeldLength, SetWeldLength, None, 'WeldLength')
   LegLength = property (GetLegLength, SetLegLength, None, 'LegLength')
   Layers = property (GetLayers, SetLayers, None, 'Layers')
   Position = property (GetPosition, SetPosition, None, 'Position')
   TestProcedure = property (GetTestProcedure, SetTestProcedure, None, 'TestProcedure')
   Process = property (GetProcess, SetProcess, None, 'Process')
   StandardProcess = property (GetStandardProcess, SetStandardProcess, None, 'StandardProcess')
   StartSuspension = property (GetStartSuspension, SetStartSuspension, None, 'StartSuspension')
   EndSuspension = property (GetEndSuspension, SetEndSuspension, None, 'EndSuspension')
   ConnectionAngle = property (GetConnectionAngle, SetConnectionAngle, None, 'ConnectionAngle')
   RotationAngle = property (GetRotationAngle, SetRotationAngle, None, 'RotationAngle')
   InclinationAngle = property (GetInclinationAngle, SetInclinationAngle, None, 'InclinationAngle')
   TorchVector = property (GetTorchVector, SetTorchVector, None, 'TorchVector')
