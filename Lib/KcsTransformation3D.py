## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsTransformation3D.py
#
#      PURPOSE:
#          The transformation matrix class is used to transform points and vectors
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          type         integer     Type of transformation matrix.
#                                   The following codes may be used:
#                                   0  Unknown type of transformation matrix.
#                                   1  Transformation matrix does not contain
#                                      general scaling or projection.
#                                   2  Transformation matrix contains general scaling.
#                                   3  Transformation matrix contains projection.
#
#          matrix11       real      element(1,1) in the transformation matrix
#          .              .
#          matrix44       real      element(4,4) in the transformation matrix


import math

class Transformation3D:
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
        self.type = 1
        self.matrix11 = 1.0
        self.matrix12 = 0.0
        self.matrix13 = 0.0
        self.matrix14 = 0.0
        self.matrix21 = 0.0
        self.matrix22 = 1.0
        self.matrix23 = 0.0
        self.matrix24 = 0.0
        self.matrix31 = 0.0
        self.matrix32 = 0.0
        self.matrix33 = 1.0
        self.matrix34 = 0.0
        self.matrix41 = 0.0
        self.matrix42 = 0.0
        self.matrix43 = 0.0
        self.matrix44 = 1.0

#-------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
        return 'Matrix type %s by row : %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' %  (self.type, self.matrix11, self.matrix12, self.matrix13, self.matrix14, self.matrix21, self.matrix22, self.matrix23, self.matrix24,\
        self.matrix31, self.matrix32, self.matrix33, self.matrix34, self.matrix41, self.matrix42, self.matrix43, self.matrix44)

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __cmp__
#
#      PURPOSE:
#          implements cmp(o1, o2) function

     def __cmp__(self, other):
        try:
           if not isinstance(other, self.__class__):
              return 1

           for row in range(0, 4):
              for col in range(0, 4):
                 if self.__Get(row, col) != other.__Get(row, col):
                    return 1

           if self.type != other.type:
              return 1
        except Exception, e:
           print e
           return 1

        return 0


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
        if Row in range(0, 4) and Col in range(0, 4):
           M = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
           type = 0
           self.GetByRow(type, M)
           (M[Row])[Col] = newValue
           self.SetByRow(type, M)

#-------------------------------------------------------------------
#
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
        self.type = value

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
        if Row in range(0, 4) and Col in range(0, 4):
           M = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
           type = 0
           self.GetByRow(type, M)
           return (M[Row])[Col]
        else:
           return 0.0


#-------------------------------------------------------------------
#
#      METHOD:
#          Combine
#
#      PURPOSE:
#          Combine the transformation (self) with another
#
#          reference XA740(self, tra, self)
#
#      INPUT:
#          Parameters:
#          tra          Transformation 3D    The transformation to fetch information from
#
#      RESULT:
#          The transformation is updated
#
#

     def Combine(self, tra):
        M1  =[[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
        M2  =[[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
        Mout=[[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
        t1 = 0
        t2 = 0
        self.GetByRow(t1, M1)
        tra.GetByRow(t2, M2)
        for i in range (0, 4, 1):
          for j in range (0, 4, 1):
             sum=0.0
             for k in range (0, 4, 1):
                 sum=sum+M1[i][k]*M2[k][j]
             Mout[i][j]=sum
        if self.type > tra.type:
          tout = self.type
        else:
          tout = tra.type
        self.SetByRow(tout, Mout)

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
#          M     real array     [[x11,x12,x13,x14][x21,x22,x23,x24][...][...x44]]
#

     def GetByRow(self, t, M):
         t = self.type
         M[0][0]=self.matrix11
         M[0][1]=self.matrix12
         M[0][2]=self.matrix13
         M[0][3]=self.matrix14
         M[1][0]=self.matrix21
         M[1][1]=self.matrix22
         M[1][2]=self.matrix23
         M[1][3]=self.matrix24
         M[2][0]=self.matrix31
         M[2][1]=self.matrix32
         M[2][2]=self.matrix33
         M[2][3]=self.matrix34
         M[3][0]=self.matrix41
         M[3][1]=self.matrix42
         M[3][2]=self.matrix43
         M[3][3]=self.matrix44

#-------------------------------------------------------------------
#
#      METHOD:
#          Invert
#
#      PURPOSE:
#          Invert the transformation (self)
#
#          reference XA739
#
#      RESULT:
#          The transformation is updated
#

     def Invert(self):
        M  =[[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
        t = 0
        self.GetByRow(t, M)
        self.matrix11 = M[0][0]
        self.matrix21 = M[0][1]
        self.matrix31 = M[0][2]
        self.matrix12 = M[1][0]
        self.matrix22 = M[1][1]
        self.matrix32 = M[1][2]
        self.matrix13 = M[2][0]
        self.matrix23 = M[2][1]
        self.matrix33 = M[2][2]
        self.matrix14 = 0.0
        self.matrix24 = 0.0
        self.matrix34 = 0.0
        self.matrix41 = (-M[3][0]*M[0][0]-M[3][1]*M[0][1]-M[3][2]*M[0][2])/M[3][3]
        self.matrix42 = (-M[3][0]*M[1][0]-M[3][1]*M[1][1]-M[3][2]*M[1][2])/M[3][3]
        self.matrix43 = (-M[3][0]*M[2][0]-M[3][1]*M[2][1]-M[3][2]*M[2][2])/M[3][3]
        self.matrix44 = 1.0/M[3][3]

#-------------------------------------------------------------------
#
#      METHOD:
#          ReflectX
#
#      PURPOSE:
#          Reflect the (self) matrix in the X axis
#
#          reference XA732
#
#      RESULT:
#          The transformation is updated
#

     def ReflectX(self):
        T  = Transformation3D()
        T.matrix11 = -1.0
        self.Combine(T)

#-------------------------------------------------------------------
#
#      METHOD:
#          ReflectY
#
#      PURPOSE:
#          Reflect the matrix (self) in the y axis
#
#          reference XA732
#
#      RESULT:
#          The transformation is updated
#

     def ReflectY(self):
        T  = Transformation3D()
        T.matrix22 = -1.0
        self.Combine(T)

#-------------------------------------------------------------------
#
#      METHOD:
#          ReflectZ
#
#      PURPOSE:
#          Reflect the matrix (self) in the z axis
#
#          reference XA732
#
#      RESULT:
#          The transformation is updated
#

     def ReflectZ(self):
        T  = Transformation3D()
        T.matrix33 = -1.0
        self.Combine(T)

#-------------------------------------------------------------------
#
#      METHOD:
#          Rotate
#
#      PURPOSE:
#          Add a rotation to the transformation (self)
#
#      INPUT:
#          Parameters:
#          point     Point3D      This point is on the axis to rotate arround
#          axis      Vector3D     A vector of class which togeter with point
#                                 determines the rotation axis
#          angle     real         The angle, in radians, of rotation.
#                                 Countercloskwise rotation seen from the end point
#                                 of the vector 'axis' is considered positive
#
#          reference XA738
#
#      RESULT:
#          The transformation is updated
#

     def Rotate(self, point, axis, angle):
        from KcsVector3D import Vector3D
        w_vec = Vector3D(axis.X, axis.Y, axis.Z)
        w_vec.SetToUnitVector()
#
#       calculate vector perpendicular to rotation axis
#
        u_vec = Vector3D(0.0, 0.0, 0.0)
        if abs(w_vec.X) + abs(w_vec.Y) > 1.0E-15:
           u_vec.X = w_vec.Y
           u_vec.Y = -w_vec.X
        else:
           u_vec.Y = -w_vec.Z
           u_vec.Z = w_vec.Y
#
#       calculate the third vector
#
        v_vec = Vector3D(0.0, 0.0, 0.0)
        v_vec.SetFromCrossProduct(w_vec, u_vec)
#
#       create a transformation matrix from uvw-xyz
#
        T2 = Transformation3D()
        T2.SetFromPointAndTwoVectors(point, u_vec, v_vec)
#
#       create a transformation matrix for rotation
#
        T3 = Transformation3D()
        T3.matrix11 = math.cos(angle)
        T3.matrix12 = math.sin(angle)
        T3.matrix21 = -1*math.sin(angle)
        T3.matrix22 = math.cos(angle)
#
#       Transformation xyz-uvw
#       Rotation
#       Transformation uvw-xyz
#
        T3.Combine(T2)
        T2.Invert()
        T2.Combine(T3)
#
#       combine self with the result of rotation
#
        self.Combine(T2)

#-------------------------------------------------------------------
#
#      METHOD:
#          SetByRow
#
#      PURPOSE:
#          Initate transformation (matrix with a 2-dimension array)
#
#      INPUT:
#          Parameters:
#          t     real           matrix type
#          M     real array     [[x11,x12,x13,x14][x21,x22,x23,x24][...][...x44]]
#
#      RESULT:
#          The transformation is updated
#
#

     def SetByRow(self, t, M):
         self.type = t
         self.matrix11=M[0][0] + 0.0
         self.matrix12=M[0][1] + 0.0
         self.matrix13=M[0][2] + 0.0
         self.matrix14=M[0][3] + 0.0
         self.matrix21=M[1][0] + 0.0
         self.matrix22=M[1][1] + 0.0
         self.matrix23=M[1][2] + 0.0
         self.matrix24=M[1][3] + 0.0
         self.matrix31=M[2][0] + 0.0
         self.matrix32=M[2][1] + 0.0
         self.matrix33=M[2][2] + 0.0
         self.matrix34=M[2][3] + 0.0
         self.matrix41=M[3][0] + 0.0
         self.matrix42=M[3][1] + 0.0
         self.matrix43=M[3][2] + 0.0
         self.matrix44=M[3][3] + 0.0

#-------------------------------------------------------------------
#
#      METHOD:
#          SetByRowFromArray
#
#      PURPOSE:
#          Initate transformation (from array)
#
#      INPUT:
#          Parameters:
#          t     real           matrix type
#          M     real array     [x11,x12,x13,x14,x21,x22,x23,x24,...x44]
#
#      RESULT:
#          The transformation is updated
#
#

     def SetByRowFromArray(self, t, M):
         self.type = t
         self.matrix11=M[0] + 0.0
         self.matrix12=M[1] + 0.0
         self.matrix13=M[2] + 0.0
         self.matrix14=M[3] + 0.0
         self.matrix21=M[4] + 0.0
         self.matrix22=M[5] + 0.0
         self.matrix23=M[6] + 0.0
         self.matrix24=M[7] + 0.0
         self.matrix31=M[8] + 0.0
         self.matrix32=M[9] + 0.0
         self.matrix33=M[10] + 0.0
         self.matrix34=M[11] + 0.0
         self.matrix41=M[12] + 0.0
         self.matrix42=M[13] + 0.0
         self.matrix43=M[14] + 0.0
         self.matrix44=M[15] + 0.0

#-------------------------------------------------------------------
#
#      METHOD:
#          SetFromPointAndTwoVectors
#
#      PURPOSE:
#          Initate matrix by a point and two vectors
#
#          reference XA730D
#
#      INPUT:
#          Parameters:
#          p0         Point3D     Origo for matrix
#          U          Vector3D    U vector for matrix
#          V          Vector3D    V vector for matrix
#
#      RESULT:
#          The transformation is updated
#
#

     def SetFromPointAndTwoVectors(self, p0, U, V):
        from KcsVector3D import Vector3D
        self.type=1

#       update U - vector

        length = U.Length()
        self.matrix11=U.X/length
        self.matrix12=U.Y/length
        self.matrix13=U.Z/length
        self.matrix14=0.0

#       update V - vector

        length = V.Length()
        self.matrix21=V.X/length
        self.matrix22=V.Y/length
        self.matrix23=V.Z/length
        self.matrix24=0.0

#       update W - vector by calculation cross product of U and V

        W = Vector3D()
        W.SetFromCrossProduct(U,V)
        length = W.Length()
        self.matrix31=W.X/length
        self.matrix32=W.Y/length
        self.matrix33=W.Z/length
        self.matrix34=0.0

#       update the origo

        self.matrix41=p0.X
        self.matrix42=p0.Y
        self.matrix43=p0.Z
        self.matrix44=1.0

#-------------------------------------------------------------------
#
#      METHOD:
#          SetFromPointAndThreeVectors
#
#      PURPOSE:
#          Initate matrix by a point and three vectors
#
#      INPUT:
#          Parameters:
#          p0       Point3D        Origo for matrix
#          uvec     Vector3D       U vector for matrix
#          vvec     Vector3D       V vector for matrix
#          wvec     Vector3D       W vector for matrix
#
#      RESULT:
#          The transformation is updated
#
#

     def SetFromPointAndThreeVectors(self,p0,uvec,vvec,wvec):
        self.type = 1
        self.matrix11= uvec.X
        self.matrix12= uvec.Y
        self.matrix13= uvec.Z
        self.matrix14= 0.0
        self.matrix21= vvec.X
        self.matrix22= vvec.Y
        self.matrix23= vvec.Z
        self.matrix24= 0.0
        self.matrix31= wvec.X
        self.matrix32= wvec.Y
        self.matrix33= wvec.Z
        self.matrix34= 0.0
        self.matrix41= p0.X
        self.matrix42= p0.Y
        self.matrix43= p0.Z
        self.matrix44= 1.0

#-------------------------------------------------------------------
#
#      METHOD:
#          SetFromTransformation
#
#      PURPOSE:
#          Update the transformation with values from another (copy)
#
#      INPUT:
#          Parameters:
#          tra        Transformation3D     The transformation to copy from
#
#      RESULT:
#          The transformation (self)is updated
#
#

     def SetFromTransformation(self, tra):
        self.type = tra.type
        self.matrix11 = tra.matrix11
        self.matrix12 = tra.matrix12
        self.matrix13 = tra.matrix13
        self.matrix14 = tra.matrix14
        self.matrix21 = tra.matrix21
        self.matrix22 = tra.matrix22
        self.matrix23 = tra.matrix23
        self.matrix24 = tra.matrix24
        self.matrix31 = tra.matrix31
        self.matrix32 = tra.matrix32
        self.matrix33 = tra.matrix33
        self.matrix34 = tra.matrix34
        self.matrix41 = tra.matrix41
        self.matrix42 = tra.matrix42
        self.matrix43 = tra.matrix43
        self.matrix44 = tra.matrix44

#-------------------------------------------------------------------
#
#      METHOD:
#          Translate
#
#      PURPOSE:
#          Add a translation to the transformation (self) by giving a vector defining how origo
#          will be moved
#
#      INPUT:
#          Parameters:
#          transvec   Vector3D   Translation vector
#
#          reference XA731

     def Translate(self, transvec):
        T = Transformation3D()
        T.matrix41 = transvec.X
        T.matrix42 = transvec.Y
        T.matrix43 = transvec.Z
        self.Combine(T)
