## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#      NAME:
#          KcsTransformation2D.py
#
#      PURPOSE:
#          The transformation class is used to transform points and vectors
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __type         integer              Type of transformation matrix.
#                                              It is for internal use.
#                                                        0 =   Undefined transformation
#                                                        1 =   Identity transformation
#                                                        2 =   Transformation may also consist of
#                                                              translations.
#                                                        3 =   Transformation may also consist of
#                                                              rotations.
#                                                        4 =   Transformation may also consist of
#                                                              uniform scalings.
#                                                        5 =   Transformation may also consist of
#                                                              reflections.
#                                                        6 =   Transformation may also consist of
#                                                              general scalings.
#                                                        7 =   Transformation may also consist of
#                                                              skews (shears).
#                                                        8 =   Transformation may also consist of
#                                                              parallel projection.
#                                                        9 =   Transformation may also consist of
#                                                              central projection.
#
#          __matrix       list of reals        transformation matrix
#

import kcs_ic
from KcsVector2D import Vector2D
from KcsPoint2D import Point2D

import copy

class Transformation2D(object):

#-------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#          The matrix is initiated as unit matrix
#

   def __init__(self):
      self.__matrix = []
      for nRow in range(0, 3):
         Row = [0.0, 0.0, 0.0]
         self.__matrix.append(Row)
      self.IdentityTransf()
      self.__type = 1

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Transformation2D : %s %s %s %s %s %s %s %s %s' % (\
         self.__Get(0, 0), self.__Get(0, 1), self.__Get(0, 2),\
         self.__Get(1, 0), self.__Get(1, 1), self.__Get(1, 2),\
         self.__Get(2, 0), self.__Get(2, 1), self.__Get(2, 2))


#-------------------------------------------------------------------
#
#      METHOD:
#          __Set
#
#      PURPOSE:
#          Set matrix item
#
#      INPUT:
#          Parameters:
#           Row               integer              Row number
#           Col               integer              Column number
#           Value             real                 Item value
#
#      RESULT:
#          The matrix item will be updated
#

   def __Set(self, Row, Col, Value):
      newValue = 0.0 + Value
      if Row in range(0, 3) and Col in range(0, 3):
         (self.__matrix[Row])[Col] = newValue

#-------------------------------------------------------------------
#
#      METHOD:
#          __Get
#
#      PURPOSE:
#          Get matrix item
#
#      INPUT:
#          Parameters:
#           Row               integer              Row number
#           Col               integer              Column number
#
#      RESULT:
#          [0]                real                 Matrix item value
#

   def __Get(self, Row, Col):
      if Row in range(0, 3) and Col in range(0, 3):
         return (self.__matrix[Row])[Col]
      else:
         return 0.0

#-------------------------------------------------------------------
#
#      METHOD:
#          IdentityTransf
#
#      PURPOSE:
#           set identity matrix
#
#      INPUT:
#          Parameters:
#           None
#
#      RESULT:
#           None
#

   def IdentityTransf(self):
      for Row in range(0, 3):
         for Col in range(0, 3):
            if Row==Col:
               self.__Set(Row, Col, 1.0)
            else:
               self.__Set(Row, Col, 0.0)
      self.__type = 1


#-------------------------------------------------------------------
#
#      METHOD:
#          Translate
#
#      PURPOSE:
#           makes translation
#
#      INPUT:
#          Parameters:
#           vector2D             Vector2D              translation vector
#
#      RESULT:
#           None
#

   def Translate(self, vector):
      if vector.X!=0.0 or vector.Y!=0.0:
         M1 = Transformation2D()
         if kcs_ic.transf_translate_2d(M1, vector):
            self.Combine(M1)


#-------------------------------------------------------------------
#
#      METHOD:
#          Rotate
#
#      PURPOSE:
#           rotates about point
#
#      INPUT:
#          Parameters:
#           point             Point2D           rotation center point
#           angle             real              angle in radians
#
#      RESULT:
#           None
#

   def Rotate(self, center, angle):
      M1 = Transformation2D()
      if kcs_ic.transf_rotate_2d(M1, center, angle):
         self.Combine(M1)


#-------------------------------------------------------------------
#
#      METHOD:
#          Scale
#
#      PURPOSE:
#           performs uniform scaling
#
#      INPUT:
#          Parameters:
#           scale             real           scale factor
#
#      RESULT:
#           None
#

   def Scale(self, scale):
      if not scale==0.0:
         M1 = Transformation2D()
         if kcs_ic.transf_scale_2d(M1, scale):
            self.Combine(M1)

#-------------------------------------------------------------------
#
#      METHOD:
#          Reflect
#
#      PURPOSE:
#           adds reflect transformation
#
#      INPUT:
#          Parameters:
#           point             Point2D           Point in the reflection line
#           vector            Vector2D          Direction vector of the reflection line
#
#      RESULT:
#           None
#

   def Reflect(self, point, vector):
      M1 = Transformation2D()
      if kcs_ic.transf_reflect_2d(M1, point, vector):
         self.Combine(M1)


#-------------------------------------------------------------------
#
#      METHOD:
#          Combine
#
#      PURPOSE:
#           Combine the transformation (self) with another
#
#      INPUT:
#          Parameters:
#          tra          Transformation2D           The transformation to fetch information from
#
#      RESULT:
#           The transformation is updated
#

   def Combine(self, tra):
      M1 = copy.deepcopy(self)
      if kcs_ic.transf_combine_2d(M1, tra):
         self.__matrix  = copy.deepcopy(M1.__matrix)
         self.__type    = M1.__type

#-------------------------------------------------------------------
#
#      METHOD:
#          Invert
#
#      PURPOSE:
#           Inverts transformation matrix
#
#      INPUT:
#           None
#
#      RESULT:
#           The transformation is updated
#

   def Invert(self):
      M1 = copy.deepcopy(self);
      if kcs_ic.transf_invert_2d(M1):
         # copy result to self
         self.__matrix  = copy.deepcopy(M1.__matrix)
         self.__type    = M1.__type


#-------------------------------------------------------------------
#
#      METHOD:
#          GetByRow
#
#      PURPOSE:
#          A python array (in two dimensions) with values from the matrix will be returned
#
#      RESULT:
#          Parameters:
#          t     real           matrix type
#          M     real array     [[x11,x12,x13][x21,x22,x23][x31,x32,x33]]
#

   def GetByRow(self, t, M):
      t = self.__type
      for nRow in range(0, 3):
         for nCol in range(0, 3):
            M[nRow][nCol] = self.__Get(nRow, nCol)

#-------------------------------------------------------------------
#      METHOD:
#          __SetType
#
#      PURPOSE:
#          Set matrix type - for internal use only
#
#      INPUT:
#          Parameters:
#           Value             integer                 matrix type
#
#      RESULT:
#          The matrix type will be updated
#

   def __SetType(self, value):
      self.__type = value

#-------------------------------------------------------------------
#      METHOD:
#          __Decompose
#
#      PURPOSE:
#          Decompose matrix
#
#      INPUT:
#
#      RESULT:
#          tuple containing transformations (reflection, rotation, translation x, translation y, xyshear, scale x, scale y)
#

   def __Decompose(self):
      return kcs_ic.transf_decompose_2d(self)


#-------------------------------------------------------------------
#      METHOD:
#          GetScale
#
#      PURPOSE:
#          Returns scale as tuple: (scale x, scale y) or None if transformation matrix can not be decomposed
#
#      INPUT:
#
#      RESULT:
#          tuple containing scale values (scale x, scale y)
#            or
#          None
#

   def GetScale(self):
      rescode, result = kcs_ic.transf_decompose_2d(self)
      if rescode:
         return result[-2:]
      else:
         return None

#-------------------------------------------------------------------
#      METHOD:
#          GetXYShear
#
#      PURPOSE:
#          Returns XY shear or None if transformation matrix can not be decomposed
#
#      INPUT:
#
#      RESULT:
#          xy shear value
#            or
#          None
#

   def GetXYShear(self):
      rescode, result = kcs_ic.transf_decompose_2d(self)
      if rescode:
         return result[4]
      else:
         return None

#-------------------------------------------------------------------
#      METHOD:
#          GetTranslation
#
#      PURPOSE:
#          Returns translation as tuple: (translation x, translation y) or None if transformation matrix can not be decomposed
#
#      INPUT:
#
#      RESULT:
#          tuple containing translation values (translation x, translation y)
#            or
#          None
#

   def GetTranslation(self):
      rescode, result = kcs_ic.transf_decompose_2d(self)
      if rescode:
         return result[2:4]
      else:
         return None

#-------------------------------------------------------------------
#      METHOD:
#          GetRotation
#
#      PURPOSE:
#          Returns rotation or None if transformation matrix can not be decomposed
#
#      INPUT:
#
#      RESULT:
#          rotation
#            or
#          None
#

   def GetRotation(self):
      rescode, result = kcs_ic.transf_decompose_2d(self)
      if rescode:
         return result[1]
      else:
         return None

#-------------------------------------------------------------------
#      METHOD:
#          GetReflection
#
#      PURPOSE:
#          Returns reflection or None if transformation matrix can not be decomposed
#
#      INPUT:
#
#      RESULT:
#          reflection
#            or
#          None
#

   def GetReflection(self):
      rescode, result = kcs_ic.transf_decompose_2d(self)
      if rescode:
         return result[0]
      else:
         return None

#-------------------------------------------------------------------

   def GetType(self): return self.__type
   Type = property (GetType, None, None, 'type - type of matrix')

   def GetMatrix(self): return self.__matrix
   Matrix = property (GetMatrix, None, None, 'matrix')
