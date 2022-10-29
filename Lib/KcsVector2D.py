## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsVector2D.py
#
#      PURPOSE:
#          The Vector2D class holds information about a 2D vector
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          X              real          The X value
#          Y              real          The Y value

from KcsPoint2D import Point2D
import math
class Vector2D:

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          X              real          The X component of the vector
#          Y              real          The Y component of the vector
#
     def __init__(self, x=-32000.0, y=-32000.0):
        self.X = x + 0.0
        self.Y = y + 0.0

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return '[X Y:%s,%s]' % (self.X, self.Y)

#
#      METHOD:
#          __add__
#
#      PURPOSE:
#          Add another vector to the vector
#
#      INPUT:
#          Parameters:
#          vec            Vector2D      Vector to add to self
#
#      RESULT:
#          The vector will be updated
#

     def __add__(self, vec):
        self.X = vec.X + self.X
        self.Y = vec.Y + self.Y

#
#      METHOD:
#          __sub__
#
#      PURPOSE:
#          Subtract another vector from the vector
#
#      INPUT:
#          Parameters:
#          vec            Vector2D      Vector to subtract from self
#
#      RESULT:
#          The vector will be updated
#

     def __sub__(self, vec):
        self.X = self.X - vec.X
        self.Y = self.Y - vec.Y


#
#      METHOD:
#          BlankProduct
#
#      PURPOSE:
#          Scale the vector length (blank_product)
#
#      INPUT:
#          Parameters:
#          sc              real          The scale factor
#
#      RESULT:
#          The vector will be updated
#

     def BlankProduct(self, sc):
        self.X = self.X * sc
        self.Y = self.Y * sc


#
#      METHOD:
#          CompareVector
#
#      PURPOSE:
#          The two vectors self and vec are compared
#          If only the direction is supposed to be compared use unit_vector first.
#
#      INPUT:
#          Parameters:
#          vec            Vector2D      The vector to compare with
#          tolerance      real          The tolerance factor for vector comparison
#
#      RESULT:
#          Returns:
#          Integer        1 = The vectors are equal.
#                         0 = The vectors are not equal

     def CompareVector(self, vec, tolerance):
        xx= math.sqrt((self.X-vec.X)*(self.X-vec.X) + (self.Y-vec.Y)*(self.Y-vec.Y))
        if xx < tolerance:
           return 1
        else:
           return 0


#
#      METHOD:
#          DotProduct
#
#      PURPOSE:
#          Get the dot product (scalar product)
#          between self and other vector
#
#          reference XB202
#
#      INPUT:
#          Parameters:
#          vec          Vector2D           The vector to calculate dot product with
#
#      RESULT:
#          Returns:
#          Real           The dot product

     def DotProduct(self, vec):
        return (self.X * vec.X + self.Y * vec.Y)


#
#      METHOD:
#          LargestComponentAxis
#
#      PURPOSE:
#          Get the coordinate axis, corresponding to the largest component in vector
#
#      RESULT:
#          Returns:
#          String         X or Y

     def LargestComponentAxis(self):
        if self.X < self.Y:
           return ('Y')
        else:
           return ('X')


#
#      METHOD:
#          Length
#
#      PURPOSE:
#          get the length of the vector
#
#      RESULT:
#          Returns:
#          Real           The length of vector

     def Length(self):
        return (math.sqrt(self.X*self.X + self.Y*self.Y))



#
#      METHOD:
#          Rotate
#
#      PURPOSE:
#          Rotate vector by giving an angle in radians
#
#          reference XB206
#
#      INPUT:
#          Parameters:
#          angle        real      The rotation angle.
#                                 A positive value is counterclockwise rotation
#
#      RESULT:
#          The vector will be updated
#


     def Rotate(self, angle):
        x = math.cos(angle)*self.X - math.sin(angle)*self.Y
        y = math.sin(angle)*self.X + math.cos(angle)*self.Y
        self.X = x
        self.Y = y


#
#      METHOD:
#          Round
#
#      PURPOSE:
#          The vector component values are rounded to given number of decimals
#
#      INPUT:
#          Parameters:
#          decimals      real    Number of decimals
#
#      RESULT:
#          The vector will be updated
#
#

     def Round(self, decimals):
        self.X =int(self.X * math.pow(10, decimals)+0.5) / math.pow(10, decimals)
        self.Y =int(self.Y * math.pow(10, decimals)+0.5) / math.pow(10, decimals)


#
#      METHOD:
#          ScalarComponentOnVector
#
#      PURPOSE:
#          Scalar component
#          normal scalar projection of self on the unrestricted line with direction vec
#
#          reference XB214
#
#      INPUT:
#          Parameters:
#          vec       Vector2D        The direction vector of the line
#
#
#      RESULT:
#          Returns:
#          Real           The scalar projection


     def ScalarComponentOnVector(self, vec):
        L1 = vec.Length()
        if L1 < 1.0E-15:
           return(0)
        else:
           return((self.X*vec.X + self.Y*vec.Y)/L1)

#
#      METHOD:
#          SetComponents
#
#      PURPOSE:
#          Set the vector from given vector components
#
#      INPUT:
#          Parameters:
#          x            real              The x - value
#          y            real              The y - value
#
#      RESULT:
#          The vector will be updated
#

     def SetComponents(self, x, y):
        self.X = x + 0.0
        self.Y = y + 0.0



#
#      METHOD:
#          SetFromPoints
#
#      PURPOSE:
#          Update the vector to be a vector from point p1 towards point p2
#
#
#      INPUT:
#          Parameters:
#          p1             Point2D       Start point (Point which the vector is directed from)
#          p2             Point2D       End point (Point which the vector is directed towards)
#
#      RESULT:
#          The vector will be updated
#

     def SetFromPoints(self, p1, p2):
        self.X = p2.X - p1.X
        self.Y = p2.Y - p1.Y


#
#      METHOD:
#          SetFromVector
#
#      PURPOSE:
#          Update the vector with values from another vector (copy)
#
#      INPUT:
#          Parameters:
#          vec         Vector2D      Vector to copy values from
#
#      RESULT:
#          The vector will be updated
#

     def SetFromVector(self, vec):
        self.X = vec.X
        self.Y = vec.Y


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
#          vec1            Vector2D      Vector to be subtracted with vec2
#          vec2            Vector2D      Vector
#
#      RESULT:
#          The vector will be updated
#

     def SetFromVectorDifference(self, vec1, vec2):
        self.X = vec1.X - vec2.X
        self.Y = vec1.Y - vec2.Y



#
#      METHOD:
#          SetFromVectorSum
#
#      PURPOSE:
#          Update the vector to be the sum of two vectors
#
#      INPUT:
#          Parameters:
#          vec1         vector2D        The first vector
#          vec2         vector2D        The second vector
#
#      RESULT:
#          The vector will be updated
#

     def SetFromVectorSum(self, vec1, vec2):
        self.X = vec1.X + vec2.X
        self.Y = vec1.Y + vec2.Y


#
#      METHOD:
#          SetLength
#
#      PURPOSE:
#          Update the vector to have a certain length
#
#      INPUT:
#          Parameters:
#          length       real          The new length of the vector
#
#      RESULT:
#          The vector will be updated
#

     def SetLength(self, length):
        self.SetToUnitVector()
        self.X = self.X * length
        self.Y = self.Y * length


#
#      METHOD:
#          SetToUnitvector
#
#      PURPOSE:
#          Update the length of vector to 1 (one)
#
#      INPUT:
#          none
#
#
#      RESULT:
#          The vector will be updated
#

     def SetToUnitVector(self):
        length = self.Length()
        if length >= 1.0E-15:
           self.X = self.X/length
           self.Y = self.Y/length
