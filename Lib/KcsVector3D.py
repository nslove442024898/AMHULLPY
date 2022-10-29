## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsVector3D.py
#
#      PURPOSE:
#          The vector3D class holds information about a 3D vector
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          X          real          The X component
#          Y          real          The Y component
#          Z          real          The Z component

from KcsPoint3D     import Point3D
import KcsLine3D
import KcsPlane3D
import KcsTransformation3D
import math
import types

ErrorMessages = { TypeError : 'not supported argument type, see documentation of Vector3D class',
                  IndexError: 'not valid index, valid values of index for Vector3D class are: 0, 1, 2' }

class Vector3D:
#------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          x              real          The X component of the vector
#          y              real          The Y component of the vector
#          z              real          The Z component of the vector
#

   def __init__(self, x=-32000.0, y=-32000.0, z=-32000.0):
      if (type(x)!=types.IntType and type(x) != types.LongType and type(x) != types.FloatType) or\
         (type(y)!=types.IntType and type(y) != types.LongType and type(y) != types.FloatType) or\
         (type(z)!=types.IntType and type(z) != types.LongType and type(z) != types.FloatType):
         raise TypeError, ErrorMessages[TypeError]
      self.X = x + 0.0
      self.Y = y + 0.0
      self.Z = z + 0.0

#------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return '[X Y Z:%s,%s,%s]' % (self.X, self.Y, self.Z)

#------------------------------------------------------------------
#
#      METHOD:
#          __add__
#
#      PURPOSE:
#          Add the parameters with values from another vector
#
#      INPUT:
#          Parameters:
#          vec            Vector3D      Vector to add to self

   def __add__(self, vec):
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      return Vector3D(vec.X + self.X, vec.Y + self.Y, vec.Z + self.Z)

#------------------------------------------------------------------
#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

   def __cmp__(self, other):
      # if None object return not equal
      if type(other)==types.NoneType:
         return 1

      if not isinstance(other,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      if self.X != other.X or self.Y != other.Y or self.Z != other.Z:
         return 1
      else:
         return 0

#------------------------------------------------------------------
#
#      METHOD:
#          __nonzero__
#
#      PURPOSE:
#          Called to implement truth value testing

   def __nonzero__ (self):

      if self.X == 0.0 and self.Y == 0.0 and self.Z == 0.0:
         return 0
      else:
         return 1

#------------------------------------------------------------------
#
#      METHOD:
#          __getitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __getitem__(self, index):
      if type(index) != types.IntType and type(index) != types.LongType:
         raise TypeError, ErrorMessages[TypeError]

      if index==0:
         return self.X
      elif index==1:
         return self.Y
      elif index==2:
         return self.Z
      else:
         raise IndexError, ErrorMessages[IndexError]

#------------------------------------------------------------------
#
#      METHOD:
#          __setitem__
#
#      PURPOSE:
#          implements sequential datatype protocol

   def __setitem__(self, index, value):
      if (type(index) != types.IntType and type(index) != types.LongType) or \
         (type(value) != types.IntType and type(value) != types.LongType and type(value) != types.FloatType):
         raise TypeError, ErrorMessages[TypeError]
      if index==0:
         self.X = value + 0.0
      elif index==1:
         self.Y = value + 0.0
      elif index==2:
         self.Z = value + 0.0
      else:
         raise IndexError, ErrorMessages[IndexError]

#------------------------------------------------------------------
#
#      METHOD:
#          __setattr__
#
#      PURPOSE:
#          implements self.name = value function

   def __setattr__(self, name, value):
      if (name=='X' or name=='Y' or name=='Z') and (type(value) != types.IntType and type(value) != types.LongType and type(value) != types.FloatType):
         raise TypeError, ErrorMessages[TypeError]
      self.__dict__[name] = value

#------------------------------------------------------------------
#
#      METHOD:
#          __sub__
#
#      PURPOSE:
#          Subtract the parameters with values from another vector
#
#      INPUT:
#          Parameters:v
#          vec            vector3D      Vector to subtract from self

   def __sub__(self, vec):
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      return Vector3D(self.X - vec.X, self.Y - vec.Y, self.Z - vec.Z)

#------------------------------------------------------------------
#
#      METHOD:
#          AngleToVector
#
#      PURPOSE:
#          Calculate the angle between self and a vector, in radians
#
#          reference XB013
#
#      INPUT:
#          Parameters:
#          vec           Vector3D   Vector to calculate angle to
#
#      RESULT:
#          Returns:
#          Real           The angle
#                         If any of the vectors is the zero vector, the
#                         resulting angle will be PI/2.
#

   def AngleToVector(self, vec):
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      len1 = self.Length()
      len2 = vec.Length()
      if len1 < 1.0E-15:
         return(math.asin(1))
      elif len2 < 1.0E-15:
         return(math.asin(1))
      else:
         xx = self.DotProduct(vec)
         if (xx/(len1*len2)) > 1.0:
            return (math.acos(1))
         elif (xx/(len1*len2)) < -1.0:
            return (math.acos(-1))
         else:
            return(math.acos(xx/(len1*len2)))


#------------------------------------------------------------------
#
#      METHOD:
#          AngleToVectorWithSign
#
#      PURPOSE:
#          Calculate the angle between self and a vector with sign, in radians
#
#          reference XB014
#
#      INPUT:
#          Parameters:
#          vec         Vector3D     Vector to calculate angle to
#          nvec        vector3D     A vector defining the positive side of the
#                                   plane defined by the vectors self and vec.
#                                   nvec needs not to be a perpendicular to plane
#
#
#      RESULT:
#          Returns:
#          Real        real   The angle (with sign)
#                             If any of the vectors is the zero vector, the
#                             resulting angle will be PI/2.
#

   def AngleToVectorWithSign(self, vec, nvec):
      if not isinstance(vec,Vector3D) or not isinstance(nvec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      if self.Length() < 1.0E-15:
         return(math.asin(1))
      elif vec.Length() < 1.0E-15:
         return(math.asin(1))
      elif nvec.Length() < 1.0E-15:
         return(math.asin(1))
      else:
         angle = self.AngleToVector(vec)
         if (nvec.BoxProduct(self,vec)) < 0.0:
            return(-1.0*angle)
         else:
            return(angle)


#------------------------------------------------------------------
#
#      METHOD:
#          BlankProduct
#
#      PURPOSE:
#          Scale the vector length,  blank_product
#
#      INPUT:
#          Parameters:
#          sc              The scale factor
#
#      RESULT:
#          The vector will be updated
#

   def BlankProduct(self, sc):
      if type(sc)!=types.IntType and type(sc)!=types.LongType and type(sc)!=types.FloatType:
         raise TypeError, ErrorMessages[TypeError]
      self.X = self.X * sc
      self.Y = self.Y * sc
      self.Z = self.Z * sc


#------------------------------------------------------------------
#
#      METHOD:
#          BoxProduct
#
#      PURPOSE:
#          Calculate the box product between self and two other vectors
#          Box product = self * (vec1 x vec2).
#          The box product is:
#          - positive if the system (self,vec1,vec2) is right handed
#          - negative if system is left handed
#
#          reference XB008
#
#      INPUT:
#          Parameters:
#          vec1     Vector3D         First vector in the box product
#          vec2     Vector3D         Second vector in the box product
#
#      RESULT:
#          Returns:
#          real         The resulting box product

   def BoxProduct(self, vec1, vec2):
      if not isinstance(vec1,Vector3D) or not isinstance(vec2,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      vect = Vector3D()
      vect.SetFromCrossProduct(vec1, vec2)
      return(self.DotProduct(vect))


#------------------------------------------------------------------
#
#      METHOD:
#          CompareVector
#
#      PURPOSE:
#          The two vectors self and vec are compared
#          If only the direction is supposed to becompared use unit_vector first.
#
#      INPUT:
#          Parameters:
#          vec           Vector3D    The vector to compare with
#          tolerance     real        The tolerance factor for vector comparsion
#
#      RESULT:
#          Returns:
#          Integer        1 = The vectors are equal.
#                         0 = The vectors are not equal

   def CompareVector(self, vec, tolerance):
      if type(tolerance)!=types.IntType and type(tolerance)!=types.LongType and type(tolerance)!=types.FloatType:
         raise TypeError, ErrorMessages[TypeError]
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      xx= math.sqrt((self.X-vec.X)*(self.X-vec.X) + (self.Y-vec.Y)*(self.Y-vec.Y) + (self.Z-vec.Z)*(self.Z-vec.Z))
      if xx < tolerance:
         return 1
      else:
         return 0


#------------------------------------------------------------------
#
#      METHOD:
#          DotProduct
#
#      PURPOSE:
#          Calculate, and return, the dot product (scalar product)
#          between self and other vector
#
#          reference XB007
#
#      INPUT:
#          Parameters:
#          vec       Vector3D          The vector to calculate dot product with
#
#      RESULT:
#          Returns:
#          Real           The dot product

   def DotProduct(self, vec):
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      return (self.X * vec.X + self.Y * vec.Y + self.Z * vec.Z)


#------------------------------------------------------------------
#
#      METHOD:
#          AbsoluteLargestComponentAxis
#
#      PURPOSE:
#          Get the largest component in vector
#
#      RESULT:
#          Returns:
#          String         X, Y or Z

   def AbsoluteLargestComponentAxis(self):
      MaxValue = math.fabs(self.X)
      Index = 0
      if MaxValue < math.fabs(self.Y):
         MaxValue = math.fabs(self.Y)
         Index = 1
      if MaxValue < math.fabs(self.Z):
         Index = 2
      return (Index)


#------------------------------------------------------------------
#
#      METHOD:
#          Length
#
#      PURPOSE:
#          Calculate the length of the vector
#
#      RESULT:
#          Returns:
#          Real           The length of vector

   def Length(self):
      return (math.sqrt(self.X*self.X + self.Y*self.Y + self.Z*self.Z))


#------------------------------------------------------------------
#
#      METHOD:
#          ProjectOnLine
#
#      PURPOSE:
#          Normal projection of the vector (self) on a line of type Line3D
#
#          reference XB016
#
#      INPUT:
#          Parameters:
#          projline     Line3D         The line
#
#      RESULT:
#          The vector is updated
#          If the line vector is the zero vector, self is not updated
#

   def ProjectOnLine(self, projline):
      from KcsLine3D import Line3D
      if not (isinstance(projline,Line3D) or isinstance(projline,KcsLine3D.Line3D)):
         raise TypeError, ErrorMessages[TypeError]
      self.ProjectOnVector(projline.Direction)


#------------------------------------------------------------------
#
#      METHOD:
#          ProjectOnVector
#
#      PURPOSE:
#          Normal projection of the vector (self) on a vector of type Vector3D
#
#          reference XB016
#
#      INPUT:
#          Parameters:
#          projvec     Vector3D         The vector to project on
#
#      RESULT:
#          The vector is updated
#          If the projection vector is the zero vector, self is not updated
#

   def ProjectOnVector(self, projvec):
      if not isinstance(projvec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      LL = projvec.X*projvec.X + projvec.Y*projvec.Y + projvec.Z*projvec.Z
      if (LL > 1.0E-15):
         LL = (self.X*projvec.X + self.Y*projvec.Y + self.Z*projvec.Z) / LL
         self.X = projvec.X * LL
         self.Y = projvec.Y * LL
         self.Z = projvec.Z * LL

#------------------------------------------------------------------
#
#      METHOD:
#          ProjectOnPlane
#
#      PURPOSE:
#          Project the vector on a plane, self will be updated with the result
#
#          reference XB018
#
#      INPUT:
#          Parameters:
#          projplane      Plane3D        The plane
#
#      RESULT:
#          The vector is updated
#          If the plane normal is the zero vector, self is not updated
#
#

   def ProjectOnPlane(self, projplane):
      from KcsPlane3D import Plane3D
      if not (isinstance(projplane,Plane3D) or isinstance(projplane,KcsPlane3D.Plane3D)):
         raise TypeError, ErrorMessages[TypeError]

      nvec = Vector3D()
      nvec.SetFromVector(projplane.Normal)
      len = nvec.Length()
      if len >= 1.0E-15:
         sc = self.DotProduct(nvec) / (len * len)
         self.X = self.X - sc*nvec.X
         self.Y = self.Y - sc*nvec.Y
         self.Z = self.Z - sc*nvec.Z


#------------------------------------------------------------------
#
#      METHOD:
#          Rotate
#
#      PURPOSE:
#          Rotate the vector by giving an angle in radians referring
#          to another vector
#
#          reference XB012
#
#      INPUT:
#          Parameters:
#          angle          Counterclockwise rotation seen from the end point
#                         of the vector rvec
#          rvec           Reference vector.
#
#      RESULT:
#          The vector is updated.
#          If length of rvec is zero the self
#          vector will be a blank product of self and cos(angle)
#

   def Rotate(self, angle, rvec):
      if not isinstance(rvec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]
      if type(angle)!= types.IntType and type(angle) != types.LongType and type(angle) != types.FloatType:
         raise TypeError, ErrorMessages[TypeError]

      c1 = math.cos(angle)
      if rvec.Length() >= 1.0E-15:
         urvec = Vector3D(rvec.X, rvec.Y, rvec.Z)
         urvec.SetToUnitVector()
         c2 = (1.0 - c1) * self.DotProduct(urvec)
         c3 = math.sin(angle)
         x = c1*self.X + c2*urvec.X + c3*(urvec.Y*self.Z - urvec.Z*self.Y)
         y = c1*self.Y + c2*urvec.Y + c3*(urvec.Z*self.X - urvec.X*self.Z)
         z = c1*self.Z + c2*urvec.Z + c3*(urvec.X*self.Y - urvec.Y*self.X)
         self.X = x
         self.Y = y
         self.Z = z
      else:
         self.BlankProduct(c1)


#------------------------------------------------------------------
#
#      METHOD:
#          Round
#
#      PURPOSE:
#          The vector component values are rounded to given number of decimals
#
#      INPUT:
#          Parameters:
#          decimals       Number of decimals
#
#      RESULT:
#          The vector is updated
#
#

   def Round(self, decimals):
      if type(decimals) != types.IntType:
         raise TypeError, ErrorMessages[TypeError]

      self.X =int(self.X * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
      self.Y =int(self.Y * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
      self.Z =int(self.Z * math.pow(10, decimals)+0.5) / math.pow(10, decimals)


#------------------------------------------------------------------
#
#      METHOD:
#          ScalarComponentOnLine
#
#      PURPOSE:
#          normal scalar projection of self on a line
#
#          reference XB015
#
#      INPUT:
#          Parameters:
#          projline     Line3D      The line to project on
#
#      RESULT:
#          Returns:
#          The scalar component of the vector (with sign) on the line
#
#

   def ScalarComponentOnLine(self, projline):
      from KcsLine3D import Line3D
      if not (isinstance(projline,Line3D) or isinstance(projline,KcsLine3D.Line3D)):
         raise TypeError, ErrorMessages[TypeError]

      len = projline.Direction.Length()
      if len < 1.0E-15:
         return(0)
      else:
         return((self.DotProduct(projline.Direction))/len)


#------------------------------------------------------------------
#
#      METHOD:
#          SetComponents
#
#      PURPOSE:
#          Update the vector components
#
#      INPUT:
#          Parameters:
#          x          real    The x - value
#          y          real    The y - value
#          z          real    The z - value
#
#      RESULT:
#          The vector is updated


   def SetComponents(self, x, y, z):
      if (type(x)!=types.IntType and type(x) != types.LongType and type(x) != types.FloatType) or\
         (type(y)!=types.IntType and type(y) != types.LongType and type(y) != types.FloatType) or\
         (type(z)!=types.IntType and type(z) != types.LongType and type(z) != types.FloatType):
         raise TypeError, ErrorMessages[TypeError]
      self.X = x + 0.0
      self.Y = y + 0.0
      self.Z = z + 0.0


#------------------------------------------------------------------
#
#      METHOD:
#          SetFromCrossProduct
#
#      PURPOSE:
#          Update the vector to be a cross product of two vectors
#
#          reference xb006
#
#      INPUT:
#          Parameters:
#          vec1          Vector3D    First vector in the cross product
#          vec2          Vector3D    Second vector in the cross product
#
#      RESULT:
#          The vector is updated


   def SetFromCrossProduct(self, vec1, vec2):
      if not isinstance(vec1,Vector3D) or not isinstance(vec2,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      self.X = vec1.Y*vec2.Z - vec1.Z*vec2.Y
      self.Y = vec1.Z*vec2.X - vec1.X*vec2.Z
      self.Z = vec1.X*vec2.Y - vec1.Y*vec2.X


#------------------------------------------------------------------
#
#      METHOD:
#          SetFromPoints
#
#      PURPOSE:
#          Update the vector to be a vector from point p1 towards p2
#
#      INPUT:
#          Parameters:
#          p1         Point3D   Start point
#          p2         Point3D   End point
#
#      RESULT:
#          The vector will be updated
#

   def SetFromPoints(self, p1, p2):
      if not isinstance(p1,Point3D) or not isinstance(p2,Point3D):
         raise TypeError, ErrorMessages[TypeError]

      self.X = p2.X - p1.X
      self.Y = p2.Y - p1.Y
      self.Z = p2.Z - p1.Z


#------------------------------------------------------------------
#
#      METHOD:
#          SetFromVector
#
#      PURPOSE:
#          Update the parameters with values from another vector (copy)
#
#      INPUT:
#          Parameters:
#          vec       Vector3D   Vector to copy values from
#
#      RESULT:
#          The vector will be updated
#

   def SetFromVector(self, vec):
      if not isinstance(vec,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      self.X = vec.X
      self.Y = vec.Y
      self.Z = vec.Z


#------------------------------------------------------------------
#
#      METHOD:
#          SetFromVectorDifference
#
#      PURPOSE:
#          Update the vector to be the difference of two vectors
#          self = vec1 - vec2
#
#      INPUT:
#          Parameters:
#          vec1      Vector3D        Vector to be subtracted with V
#          vec2      Vector3D        Vector
#
#      RESULT:
#          The vector is updated


   def SetFromVectorDifference(self, vec1, vec2):
      if not isinstance(vec1,Vector3D) or not isinstance(vec2,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      self.X = vec1.X - vec2.X
      self.Y = vec1.Y - vec2.Y
      self.Z = vec1.Z - vec2.Z


#------------------------------------------------------------------
#
#      METHOD:
#          SetFromVectorSum
#
#      PURPOSE:
#          Update the vector to be the sum of two vectors
#
#      INPUT:
#          Parameters:
#          vec1         Vector3D        The first vector
#          vec2         Vector3D        The second vector
#
#      RESULT:
#          The vector is updated
#

   def SetFromVectorSum(self, vec1, vec2):
      if not isinstance(vec1,Vector3D) or not isinstance(vec2,Vector3D):
         raise TypeError, ErrorMessages[TypeError]

      self.X = vec1.X + vec2.X
      self.Y = vec1.Y + vec2.Y
      self.Z = vec1.Z + vec2.Z

#------------------------------------------------------------------
#
#      METHOD:
#          SetLength
#
#      PURPOSE:
#          Update the vector to have a certain length
#
#      INPUT:
#          Parameters:
#          length       real              The new length of vector
#
#      RESULT:
#          The vector will be updated
#
#

   def SetLength(self, length):
      if (type(length)!=types.IntType and type(length) != types.LongType and type(length) != types.FloatType):
         raise TypeError, ErrorMessages[TypeError]

      self.SetToUnitVector()
      self.BlankProduct(length)

#------------------------------------------------------------------
#
#      METHOD:
#          SetToUnitVector
#
#      PURPOSE:
#          Update the length of vector to 1
#
#      RESULT:
#          The vector is updated
#
#

   def SetToUnitVector(self):
      len = self.Length()
      if len >= 1.0E-15:
         self.X = self.X/len
         self.Y = self.Y/len
         self.Z = self.Z/len

#------------------------------------------------------------------
#
#      METHOD:
#          Transform
#
#      PURPOSE:
#          Transform the vector using a matrix,
#          self will be updated with the result
#
#          reference XA751
#
#      INPUT:
#          Parameters:
#          tra         Transformation3D         Transformation
#
#      RESULT:
#          The vector is updated
#
#
#

   def Transform(self, tra):
      from KcsTransformation3D import Transformation3D
      if not (isinstance(tra,Transformation3D) or isinstance(tra,KcsTransformation3D.Transformation3D)):
         raise TypeError, ErrorMessages[TypeError]

      X = self.X*tra.matrix11 + self.Y*tra.matrix21 + self.Z*tra.matrix31
      Y = self.X*tra.matrix12 + self.Y*tra.matrix22 + self.Z*tra.matrix32
      Z = self.X*tra.matrix13 + self.Y*tra.matrix23 + self.Z*tra.matrix33
      self.X = X
      self.Y = Y
      self.Z = Z
