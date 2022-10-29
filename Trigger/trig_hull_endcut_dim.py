## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#---------------------------------------------------------------------------------------------------
#  trig_hull_endcut_dim - Endcut dimensioning on profile sketch
#---------------------------------------------------------------------------------------------------
#
#  This trigger is fired by Hull Profile Cutting Interface (sf609d.exe)
#  and Hull Profile Interface (sf628d.exe) while creation of profile sketches.
#  It enables customisation of endcut and flange dimensioning regarding to
#  the type of endcut drawn.
#
#  KcsSketchDimensioning module was created only for trig_hull_endcut_dim
#  trigger with classes:
#         ProfileSketch  - input data for the trigger
#         DimensionSet   - output data returned by the trigger
#
#  The functionality is currently handled by the 'pre' trigger.
#  Input:
#         first argument   - ProfileSketch class instance with sketch data
#  Output:
#         trigger result   - kcs_util.trigger_ok() or kcs_util.trigger_abort()
#         webEndcutDS      - DimensionSet instance with web dimensioning
#         flaEndcutDS      - DimensionSet instance with flange dimensioning
#
#  Refer to KcsSketchDimensioning class and documentation for further details.
#
#---------------------------------------------------------------------------------------------------
import KcsPoint2D
import KcsVector2D
import KcsRline2D
import math
import KcsSketchDimensioning
import kcs_util

ABOUT_ZERO    = 0.00001       # zero accurancy
MIN_DIMENSION = 1             # minimal dimension to show
GAP           = 10            # distance from limiting rectangle
                              #    - no dimension will appeare closer than 'GAP' to rectangle
                              #    GAP 0 means that dimensions will be just on the boundary of rectangle
GAP_TEXT      = 10            # gap left for text above a projection line of a dimension
SHIFT_TYPE    = 8*GAP_TEXT    # shift used to move endcut type text
SHIFT_RADIUS  = 15            # shift used to move a bit radius text


VECTOR_H      = KcsVector2D.Vector2D(1,0) # witness lines vector - horizontal
VECTOR_V      = KcsVector2D.Vector2D(0,1) # witness lines vector - vertical

#---------------------------------------------------------------------------------------------------
#                                            END CUT 116
#---------------------------------------------------------------------------------------------------
def Endcut116(flangeWidth, a, b, fR1, strR1, fR2, strR2, degAlfa1, degAlfa3, fExcess, fSketchExcess, fBevelWeb, xleft,
              ylow, yflangelow, profHeight):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180

   webEndcutDS.AddCustomDim(KcsPoint2D.Point2D(xleft-2*SHIFT_TYPE,ylow), 'Endcut type 116')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b,b)
   if b>5:
      point2.Move(10,0)
   else:
      point2.Move(-fSketchExcess,0)
   point3 = KcsPoint2D.Point2D(-fSketchExcess-GAP,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(a-fR1,b+fR1+SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+fR2+SHIFT_RADIUS,profHeight-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #KS10
   if b>5:
      point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+5+SHIFT_RADIUS,b+SHIFT_RADIUS)
      webEndcutDS.AddRadiusDim(point1, 'KS10')

   #angle 1
   if degAlfa1 > MIN_DIMENSION and degAlfa1 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight-fSketchExcess,profHeight)
      add_angle(degAlfa1, pointC, 180, 1, 1, 1, webEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 65
#---------------------------------------------------------------------------------------------------
def Endcut65(flangeWidth, a, b, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, fExcess, fSketchExcess, fBevelWeb, xleft,
              ylow, yflangelow, profHeight):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180

   webEndcutDS.AddCustomDim(KcsPoint2D.Point2D(xleft-2*SHIFT_TYPE,ylow), 'Endcut type 65')

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   if fR1>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(fR1+SHIFT_RADIUS,SHIFT_RADIUS)
      webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   if fR2>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+1/math.tan(radAlfa2)*(profHeight-b)/2+SHIFT_RADIUS,
                                  b+SHIFT_RADIUS)
      webEndcutDS.AddRadiusDim(point1, strR2)

   #angle 1
   if degAlfa1 > MIN_DIMENSION and degAlfa1 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
      add_angle(degAlfa1, pointC, 0, 1, 1, 1, webEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 119
#---------------------------------------------------------------------------------------------------
def Endcut119(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa3, fExcess, fSketchExcess,
              fBevelWeb, xleft, ylow, yflangelow, profHeight, fWebThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 119')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   # c
   if c>b:
      point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
      point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*c-fSketchExcess,c)
      point3 = KcsPoint2D.Point2D(xleft-3*GAP_TEXT,c/2)
      webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(c))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #angle 3
   if degAlfa3 > MIN_DIMENSION and degAlfa3 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*c+1/math.tan(radAlfa3)*(profHeight-c), profHeight)
      add_angle(degAlfa3, pointC, 180, 1, 0, 1, webEndcutDS)

   #-------------flange sketch--------------
   #angle 2
   if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-fWebThickness), flangeWidth)
      add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 120
#---------------------------------------------------------------------------------------------------
def Endcut120(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, fExcess, fSketchExcess,
              fBevelWeb, xleft, ylow, yhigh, yflangelow, xflangeleft, profHeight, fWebThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-3*GAP_TEXT), 'Endcut type 120')

   #a
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight-fSketchExcess,profHeight)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+a,profHeight)
   point3 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+a/2,yhigh)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(fR1+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+a+SHIFT_RADIUS,b-fR2)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #KS10
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+5+SHIFT_RADIUS,b-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, 'KS10')

   #angle 1
   if degAlfa1 > MIN_DIMENSION and degAlfa1 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b, b)
      add_angle(degAlfa1, pointC, 0, 0, 1, 1, webEndcutDS)

   #-------------flange sketch--------------

   # c
   point1 = KcsPoint2D.Point2D(-fExcess,0)
   point2 = KcsPoint2D.Point2D(-fExcess,c)
   point3 = KcsPoint2D.Point2D(xflangeleft,c/2)

   flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #angle 2
   if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-c), flangeWidth)
      add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 162
#---------------------------------------------------------------------------------------------------
def Endcut162(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa3, degAlfa4, fExcess,
              fSketchExcess, fBevelWeb, xleft,
              ylow, yhigh, yflangelow, xflangeleft, profHeight, fWebThickness, fFlangeWing, fFlangeThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 162')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)-fSketchExcess,profHeight)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)+b,profHeight)
   point3 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)+b/2,yhigh+2*GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(b+fExcess-fBevelWeb))

   #R1
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*2*fR2+fR1,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*2*fR2+fR2/2+SHIFT_RADIUS,2*fR2)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #-------------flange sketch--------------

   if c<>0 and c<flangeWidth:
      #c
      if fFlangeWing>c:
         if degAlfa2 <> 0:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*c -1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
         else:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
      else:
         point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
         point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing) - fExcess,c-fFlangeWing)
      point3 = KcsPoint2D.Point2D(xflangeleft,-fFlangeWing)
      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      #angle 2
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         # arc center
         if fFlangeWing>c:
            if degAlfa2 <> 0:
               pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-fFlangeWing), flangeWidth-fFlangeWing)
         else:
            pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing)+1/math.tan(radAlfa2)*(flangeWidth-c), flangeWidth-fFlangeWing)
         add_angle(degAlfa2, pointC, 180, 1, 0, 1, flaEndcutDS)
   else: #c=0
      #angle 4
      if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(flangeWidth-fFlangeWing)-fExcess, flangeWidth-fFlangeWing)
         add_angle(degAlfa4, pointC, -180, 1, 0, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 40
#---------------------------------------------------------------------------------------------------
def Endcut40(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa3, degAlfa4, fExcess,
              fSketchExcess, fBevelWeb, xleft,
              ylow, yhigh, yflangelow, xflangeleft, profHeight, fWebThickness, fFlangeWing, fFlangeThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 40')

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft, b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(fR1+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #angle2
   if degAlfa1 > MIN_DIMENSION and degAlfa1 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(-fSketchExcess, 0)
      add_angle(degAlfa1, pointC, 180, 1, 1, 1, webEndcutDS)

   #-------------flange sketch--------------

   #c
   if c<>0 and c<flangeWidth:
      #c
      if fFlangeWing>c:
         if degAlfa2 <> 0:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*c -1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
         else:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
      else:
         point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
         point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing) - fExcess,c-fFlangeWing)
      point3 = KcsPoint2D.Point2D(xflangeleft,-fFlangeWing)
      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         # arc center
         if fFlangeWing>c:
            if degAlfa2 <> 0:
               pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-fFlangeWing), flangeWidth-fFlangeWing)
         else:
            pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing)+1/math.tan(radAlfa2)*(flangeWidth-c), flangeWidth-fFlangeWing)
         add_angle(degAlfa2, pointC, 180, 1, 0, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 39
#---------------------------------------------------------------------------------------------------
def Endcut39(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa3, degAlfa4,
              fExcess, fSketchExcess, fBevelWeb, xleft,
              ylow, yhigh, yflangelow, xflangeleft, profHeight, fWebThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   #R2 = 1000* d + R
   R = fR2 % 1000
   d = (fR2 - R)/1000
   fR2=R
   strR2=translate_radius(fR2)

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 39')

   # a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(b-1/math.tan(radAlfa3)*fR2)+1/math.tan(radAlfa3)*d,b+math.sin(radAlfa3)*d-1/math.tan(radAlfa3)*fR2-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #-------------flange sketch--------------
   if c<>0 and c<flangeWidth:
      #c
      point1 = KcsPoint2D.Point2D(-fExcess,(fWebThickness-c)/2)
      point2 = KcsPoint2D.Point2D(-fExcess,(fWebThickness+c)/2)
      point3 = KcsPoint2D.Point2D(xflangeleft,fWebThickness/2)

      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         #angle 2
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-c)/2,(fWebThickness+flangeWidth)/2)
         add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 145
#---------------------------------------------------------------------------------------------------
def Endcut145(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa3, degAlfa4,
              fExcess, fSketchExcess, fBevelWeb, xleft,
              ylow, yhigh, yflangelow, xflangeleft, profHeight, fWebThickness):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 145')

   # a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------

   if c<>0 and c<flangeWidth:
      #c
      point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(c-fWebThickness)/2-fExcess,(fWebThickness-c)/2)
      point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(fWebThickness+c)/2-fExcess,(fWebThickness+c)/2)
      point3 = KcsPoint2D.Point2D(xflangeleft,fWebThickness/2)

      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      #angle 2
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-c)/2+1/math.tan(radAlfa4)*(c+fWebThickness)/2,(fWebThickness+flangeWidth)/2)
         add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   else: #c=0
      if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
         #angle 4
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(flangeWidth+fWebThickness)/2-fExcess, (flangeWidth+fWebThickness)/2)
         add_angle(degAlfa4, pointC, 0, 0, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
#                                            END CUT 25
#---------------------------------------------------------------------------------------------------
def Endcut25(flangeWidth, b, c, fR1, strR1, degAlfa1, degAlfa3, fExcess, fSketchExcess,
             fBevelWeb, fBevelFlange,
             xleft, ylow, xflangeleft, yflangelow, yflangehigh):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 25')

   #b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b -fSketchExcess+ fBevelWeb,b-10)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(fR1+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #excess
   if fExcess-fBevelWeb>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
      point2 = KcsPoint2D.Point2D(fR1,0)
      point3 = KcsPoint2D.Point2D((point1.X+point2.X)/2,ylow-GAP_TEXT)
      fDim = fR1 + fExcess - fBevelWeb
      webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3, strRound(fDim) )

   #-------------flange sketch--------------

   #c
   point1 = KcsPoint2D.Point2D(-fExcess,0)
   point2 = KcsPoint2D.Point2D(-fExcess,c)
   point3 = KcsPoint2D.Point2D(xflangeleft,c/2)
   flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

   #angle 3
   if degAlfa3 > MIN_DIMENSION and degAlfa3 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa3)*(flangeWidth-c), flangeWidth)
      add_angle(degAlfa3, pointC, 0, 0, 1, 1, flaEndcutDS)

      #excess
      if abs(fBevelFlange)>ABOUT_ZERO and abs(fExcess)>ABOUT_ZERO:
         point1 = KcsPoint2D.Point2D(-fExcess,0)
         point2 = KcsPoint2D.Point2D(0,0)
         point3 = KcsPoint2D.Point2D((point1.X+point2.X)/2+30,yflangelow-2*GAP_TEXT)
         fDim = fExcess-fBevelWeb
         flaEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3, strRound(fDim) )

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 129
#---------------------------------------------------------------------------------------------------
def Endcut129(flangeWidth, fWebThickness, a, b, c, strR1, degAlfa1, degAlfa2, degAlfa3,
              fExcess, fSketchExcess, fBevelWeb, fBevelFlange, xleft,ylow, xflangeleft, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa3 = degAlfa3*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 129')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   radAlfa1 = degAlfa1*math.pi/180
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b - fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------
   #c
   radAlfa2 = degAlfa2*math.pi/180
   fAlfa2X = 1/math.tan(radAlfa2)*(c-fWebThickness)  # horizontal dist change at C & Alfa2
   point1 = KcsPoint2D.Point2D(0, 0)
   point2 = KcsPoint2D.Point2D(fAlfa2X -fExcess, c)
   point3 = KcsPoint2D.Point2D(xflangeleft,c/2)
   flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

   #angle 3
   if degAlfa3 > MIN_DIMENSION and degAlfa3 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(fAlfa2X+1/math.tan(radAlfa3)*(flangeWidth-c), flangeWidth)
      add_angle(degAlfa3, pointC, 0, 0, 1, 1, flaEndcutDS)

   # excess & bevel gap
   if abs(fExcess)>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(fAlfa2X, c)
      point2 = KcsPoint2D.Point2D(fAlfa2X -fExcess, c)
      point3 = KcsPoint2D.Point2D(fAlfa2X + (-fExcess )/2, 2*c)
      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(fExcess - fBevelFlange))

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 44
#---------------------------------------------------------------------------------------------------
def Endcut44(flangeWidth, fWebThickness, a, b, c, strR1, degAlfa1, degAlfa2, degAlfa4,
             fExcess, fSketchExcess, fBevelWeb, fBevelFlange, xleft, ylow, xflangeleft, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 44')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(min(xleft,-fSketchExcess-GAP),b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------
   if c<>0 and c<flangeWidth:
      #c
      point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(c-fWebThickness)/2-fExcess,(fWebThickness-c)/2)
      point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(fWebThickness+c)/2-fExcess,(fWebThickness+c)/2)
      point3 = KcsPoint2D.Point2D(xflangeleft,fWebThickness/2)
      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      #angle 2
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-c)/2+1/math.tan(radAlfa4)*(c+fWebThickness)/2,(fWebThickness+flangeWidth)/2)
         add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   else: #c=0
      if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
         #angle 4
         #arc center
         pointC = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(c-fWebThickness)/2-fExcess,(fWebThickness-c)/2)
         add_angle(degAlfa4, pointC, 0, 0, 0, 1, flaEndcutDS)

   #excess
   if fExcess-fBevelFlange>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(c-fWebThickness)/2-fExcess,(fWebThickness-c)/2)
      point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(c-fWebThickness)/2,(fWebThickness-c)/2)
      point3 = KcsPoint2D.Point2D((point1.X + point2.X)/2,yflangelow-3*GAP_TEXT)
      flaEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3, strRound(fExcess - fBevelFlange) )

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 83
#---------------------------------------------------------------------------------------------------
def Endcut83(flangeWidth, fWebThickness, fFlangeThickness, profHeight,
             b, c, strR1, strR2, degAlfa1, degAlfa2, degAlfa3,
             fExcess, fSketchExcess, fBevelWeb, fBevelFlange, xleft, xflangeleft, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 83')

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa3 = degAlfa3*math.pi/180

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(min(xleft,-fSketchExcess-GAP),b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #R1
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+1/math.tan(radAlfa3)*(profHeight-b)/2,b)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+1/math.tan(radAlfa3)*(profHeight-b),profHeight-fFlangeThickness-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #-------------flange sketch--------------
   if c<>0 and c<flangeWidth:
      #c
      point1 = KcsPoint2D.Point2D(-fExcess,(fWebThickness-c)/2)
      point2 = KcsPoint2D.Point2D(-fExcess,(fWebThickness+c)/2)
      point3 = KcsPoint2D.Point2D(min(xflangeleft,-fExcess-GAP),fWebThickness/2)

      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         #angle 2
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-c)/2,(fWebThickness+flangeWidth)/2)
         add_angle(degAlfa2, pointC, 0, 0, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 139
#---------------------------------------------------------------------------------------------------
def Endcut139( fFlangeThickness, profHeight, flangeWidth, fFlangeWing,
              a, b, c, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa4,
              fExcess, fSketchExcess, fBevelWeb, fBevelFlange, ylow, yhigh, xflangeleft, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   #R2 = 1000* d + R
   R = fR2 % 1000
   d = (fR2 - R)/1000
   fR2=R
   strR2=translate_radius(fR2)

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 139')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)-fSketchExcess,profHeight + 2*GAP_TEXT)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)+b,profHeight)
   point3 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+b/2,yhigh+20)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_V,point3,strRound(b+fExcess-fBevelWeb))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*profHeight+b,profHeight-fFlangeThickness-2*SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #-------------flange sketch--------------
   if c<>0 and c<flangeWidth:
      #c
      if fFlangeWing>c:
         if degAlfa2 <> 0:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*c -1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa2)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
         else:
            point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
            point2 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(fFlangeWing-c) - fExcess,c-fFlangeWing)
      else:
         point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*fFlangeWing - fExcess,-fFlangeWing)
         point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing) - fExcess,c-fFlangeWing)
      point3 = KcsPoint2D.Point2D(xflangeleft,-fFlangeWing)
      flaEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(c))
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         # arc center
         if fFlangeWing>c:
            if degAlfa2 <> 0:
               pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(flangeWidth-fFlangeWing), flangeWidth-fFlangeWing)
         else:
            pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c-fFlangeWing)+1/math.tan(radAlfa2)*(flangeWidth-c), flangeWidth-fFlangeWing)
         add_angle(degAlfa2, pointC, 180, 1, 0, 1, flaEndcutDS)
   else: #c=0
      if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
         #angle 4
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(flangeWidth-fFlangeWing)-fExcess, flangeWidth-fFlangeWing)
         add_angle(degAlfa4, pointC, 0, 0, 1, 1, flaEndcutDS)


   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 164
#---------------------------------------------------------------------------------------------------
def Endcut164( fFlangeThickness, profHeight, flangeWidth, fFlangeWing,
               a, b, c, strR1, degAlfa1, degAlfa2, degAlfa4,
               fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
               ylow, yhigh, xflangeleft, yflangelow):
   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa2 = degAlfa2*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 164')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   radAlfa1 = degAlfa1*math.pi/180
   if abs(90-degAlfa1)>MIN_DIMENSION:
      # leave gap for snip
      point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)-fSketchExcess,
                                  yhigh+GAP)
   else:
      point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)-fSketchExcess,
                                  profHeight - fFlangeThickness)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)+b,profHeight)
   point3 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(profHeight-fFlangeThickness)+b/2,yhigh+20)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(b+fExcess-fBevelWeb))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------
   if c<>0 and c<flangeWidth:
      #c
      if flangeWidth-c < fFlangeWing:
         point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa4)*(flangeWidth-fFlangeWing)-fExcess,flangeWidth-fFlangeWing)
         point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*(c+fFlangeWing-flangeWidth)-fExcess,flangeWidth-c-fFlangeWing)
         point3 = KcsPoint2D.Point2D(xflangeleft,flangeWidth-c-fFlangeWing)
      else:
         point1 = KcsPoint2D.Point2D(-1/math.tan(radAlfa2)*(flangeWidth-c-fFlangeWing)-fExcess,flangeWidth-c-fFlangeWing)
         point2 = KcsPoint2D.Point2D(point1.X-1/math.tan(radAlfa4)*(c),point1.Y+c)
         point3 = KcsPoint2D.Point2D(xflangeleft,flangeWidth-c-fFlangeWing)
      flaEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(c))

      #angle 2
      if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa2)*(fFlangeWing),-fFlangeWing)
         add_angle(degAlfa2, pointC, -degAlfa2, 1, 0, 1, flaEndcutDS)

   else: #c=0
      #angle 4
      if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
         #arc center
         pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*fFlangeWing-fExcess, -fFlangeWing)
         add_angle(degAlfa4, pointC, -degAlfa4, 1, 0, 1, flaEndcutDS)
   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 188
#---------------------------------------------------------------------------------------------------
def Endcut188(profHeight, a, b, c, strR1, fR1, degAlfa4,
              fExcess, fSketchExcess, fBevelWeb,  xleft, yhigh, yflangelow ):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 188')

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,profHeight)
   point2 = KcsPoint2D.Point2D(a,profHeight)
   point3 = KcsPoint2D.Point2D(a/2,yhigh)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess - fBevelWeb))

   # b (twice)
   if b == 0:
      b=fR1
   if b >= fR1:
      point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
      point2 = KcsPoint2D.Point2D(-fSketchExcess,b)
      point3 = KcsPoint2D.Point2D(xleft,b/2)
      webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))
      point1 = KcsPoint2D.Point2D(-fSketchExcess,profHeight-b)
      point2 = KcsPoint2D.Point2D(-fSketchExcess,profHeight)
      point3 = KcsPoint2D.Point2D(xleft,profHeight-b/2)
      webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #R1 (twice)
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,fR1)
   webEndcutDS.AddRadiusDim(point1, strR1)
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,profHeight-fR1)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------
   #angle
   if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(- fExcess, 0)
      add_angle(degAlfa4, pointC, 0, 0, 0, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 190
#---------------------------------------------------------------------------------------------------
def Endcut190( flangeWidth, a, b, c, strR1, fR1, degAlfa1, degAlfa2, degAlfa4,
               fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
               xleft, ylow, xflangeleft, yflangelow):
   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180
   radAlfa4 = degAlfa4*math.pi/180

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-SHIFT_TYPE), 'Endcut type 190')

   #b
   if b==0:
      b=fR1
   if b<>0:
      point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
      point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b-fSketchExcess,b)
      point3 = KcsPoint2D.Point2D(min(xleft, -GAP-fSketchExcess),b/2)
      webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #a
   if b<>0:
      point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
      point2 = KcsPoint2D.Point2D(a,0)
      point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
      webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   if fR1<>0:
      # R1
      point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,b+SHIFT_RADIUS)
      webEndcutDS.AddRadiusDim(point1, strR1)

   #-------------flange sketch--------------
   if degAlfa2 <> 0 and degAlfa2 <> 90:
      #c
      point1 = KcsPoint2D.Point2D(-fExcess,0)
      point3 = KcsPoint2D.Point2D(min(xflangeleft,-fExcess-GAP)-GAP_TEXT,0)
      point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*c -fExcess,c)
      flaEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(c))

   #angle 2
   if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa4)*c+1/math.tan(radAlfa2)*(flangeWidth-c), flangeWidth)
      add_angle(degAlfa2, pointC, 0, 1, 1, 1, flaEndcutDS)

   #angle 4
   if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
      #arc center
      pointC = KcsPoint2D.Point2D(-fExcess, 0)
      add_angle(degAlfa4, pointC, 0, 1, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS


#---------------------------------------------------------------------------------------------------
#                                            END CUT 175
#---------------------------------------------------------------------------------------------------
def Endcut175( flangeWidth, profHeight, fWebThickness, a, b, c, strR1, fR2, strR2, degAlfa4,
               fExcess, fSketchExcess, fBevelWeb,
               xleft, ylow, yhigh, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa4 = degAlfa4*math.pi/180

   #R2 = 1000* d + R
   R = fR2 % 1000
   d = (fR2 - R)/1000
   fR2=R

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 175')

   #a
   point1 = KcsPoint2D.Point2D(0,profHeight)
   point2 = KcsPoint2D.Point2D(a,profHeight)
   point3 = KcsPoint2D.Point2D(a/2,yhigh)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a))

   # b
   point1 = KcsPoint2D.Point2D(0,profHeight-b)
   point2 = KcsPoint2D.Point2D(0,profHeight)
   point3 = KcsPoint2D.Point2D(xleft,profHeight-b/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(b))

   #c
   point1 = KcsPoint2D.Point2D(-fSketchExcess, fWebThickness)
   point2 = KcsPoint2D.Point2D(c,0)
   point3 = KcsPoint2D.Point2D(c/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(c+fExcess-fBevelWeb))

   #R1
   point1 = KcsPoint2D.Point2D(SHIFT_RADIUS,profHeight-b-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(-fExcess+a+d+fR2+SHIFT_RADIUS,profHeight-fWebThickness-fR2-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #-------------flange sketch--------------
   #angle 4
   if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(-fExcess+ math.cos(radAlfa4)*(flangeWidth+fWebThickness)/2, (flangeWidth+fWebThickness)/2)
      add_angle(degAlfa4, pointC, 0, 1, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 181
#---------------------------------------------------------------------------------------------------
def Endcut181( flangeWidth, profHeight, fWebThickness, a, b, c, strR1, fR2, strR2, degAlfa4,
               fExcess, fSketchExcess, fBevelWeb,
               xleft, ylow, yhigh, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   flaEndcutDS.AddCustomDim(KcsPoint2D.Point2D(GAP_TEXT,yflangelow-4*GAP_TEXT), 'Endcut type 181')

   radAlfa4 = degAlfa4*math.pi/180

   #R2 = 1000* d + R
   R = fR2 % 1000
   d = (fR2 - R)/1000
   fR2=R

   #a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,profHeight)
   point2 = KcsPoint2D.Point2D(a,profHeight)
   point3 = KcsPoint2D.Point2D(a/2,yhigh)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(-fSketchExcess,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #c
   point1 = KcsPoint2D.Point2D(-fSketchExcess,profHeight-c)
   point2 = KcsPoint2D.Point2D(-fSketchExcess,profHeight)
   point3 = KcsPoint2D.Point2D(xleft,profHeight-c/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(c))

   #R1 (twice)
   point1 = KcsPoint2D.Point2D(SHIFT_RADIUS,b+SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)
   point1 = KcsPoint2D.Point2D(SHIFT_RADIUS,profHeight-c-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(a-d/2,profHeight-c-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #angle 4
   if degAlfa4 > MIN_DIMENSION and degAlfa4 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(-fExcess + 1/math.tan(radAlfa4)*((flangeWidth+fWebThickness)/2), (flangeWidth+fWebThickness)/2)
      add_angle(degAlfa4, pointC, 0, 1, 1, 1, flaEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 69
#---------------------------------------------------------------------------------------------------
def Endcut69(  profHeight, a, b, c, strR1, strR2, degAlfa1, degAlfa2,
               fExcess, fSketchExcess, fBevelWeb,
               xleft, ylow, yhigh, yflangelow):

   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180

   webEndcutDS.AddCustomDim(KcsPoint2D.Point2D(-2*SHIFT_TYPE,-4*GAP_TEXT), 'Endcut type 69')

   # a
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(a,0)
   point3 = KcsPoint2D.Point2D(a/2,ylow-GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(a+fExcess-fBevelWeb))

   # b
   point1 = KcsPoint2D.Point2D(-fSketchExcess,0)
   point2 = KcsPoint2D.Point2D(-fSketchExcess + 1/math.tan(radAlfa1)*b,b)
   point3 = KcsPoint2D.Point2D(xleft,b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #c
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b,b)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+c,b)
   point3 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+c/2,yhigh-2*GAP_TEXT)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3,strRound(c))

   #R1
   point1 = KcsPoint2D.Point2D(a+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #R2
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+SHIFT_RADIUS,b-SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR2)

   #angle 2
   if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*b+c+1/math.tan(radAlfa2)*(profHeight-b),profHeight)
      add_angle(degAlfa2, pointC, 180, 1, 0, 1, webEndcutDS)

   return webEndcutDS, flaEndcutDS

#---------------------------------------------------------------------------------------------------
#                                            END CUT 114
#---------------------------------------------------------------------------------------------------
def Endcut114(  profHeight, b, c, fR1, strR1, degAlfa1, degAlfa2,
               fExcess, fSketchExcess,  fBevelWeb,
               xleft, ylow, yhigh, yflangelow):
   #output data
   webEndcutDS     = KcsSketchDimensioning.DimensionSet()
   flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

   webEndcutDS.AddCustomDim(KcsPoint2D.Point2D(-2*SHIFT_TYPE,-4*GAP_TEXT), 'Endcut type 114')

   radAlfa1 = degAlfa1*math.pi/180
   radAlfa2 = degAlfa2*math.pi/180

   if c==0:
      c=(profHeight-b)/2

   # b
   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*c-fSketchExcess,c)
   point2 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(b+c)-fSketchExcess,b+c)
   point3 = KcsPoint2D.Point2D(xleft,c+b/2)
   webEndcutDS.AddLinearDim(point2,point1,VECTOR_H,point3,strRound(b))

   #c
   #calculate x positions
   y1 = math.sin(math.pi/2 - radAlfa2) * fR1
   x2 = fR1 - math.cos(math.pi/2 - radAlfa2)*fR1

   # bottom x
   xb = (1/math.tan(radAlfa1)*c) + (1/math.tan(radAlfa2)*(c-y1)) + x2

   # top x
   xt = (1/math.tan(radAlfa1)*(b+c)) + (1/math.tan(radAlfa2)*((profHeight-b-c)-y1)) + x2

   point1 = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*c-fExcess,c)
   point2 = KcsPoint2D.Point2D(xb,0)
   point3 = KcsPoint2D.Point2D(xleft,c/2)
   webEndcutDS.AddLinearDim(point1,point2,VECTOR_H,point3,strRound(c))

   #R1 (in two positions)
   point1 = KcsPoint2D.Point2D(xb+SHIFT_RADIUS,SHIFT_RADIUS)
   webEndcutDS.AddRadiusDim(point1, strR1)
   point1 = KcsPoint2D.Point2D(xt-3*SHIFT_RADIUS,profHeight-SHIFT_RADIUS-GAP)
   webEndcutDS.AddRadiusDim(point1, strR1)

   #angle 2
   if degAlfa2 > MIN_DIMENSION and degAlfa2 <> 90:
      # arc center
      pointC = KcsPoint2D.Point2D(1/math.tan(radAlfa1)*(b+c),b+c)
      add_angle(degAlfa2, pointC, 0, 1, 0, 1, webEndcutDS)

   #excess
   if fExcess-fBevelWeb>ABOUT_ZERO:
      point1 = KcsPoint2D.Point2D(-fExcess,0)
      point2 = KcsPoint2D.Point2D(xb,0)
      point3 = KcsPoint2D.Point2D((point1.X+point2.X)/2,ylow-GAP_TEXT)
      fDim = fR1 + fExcess - fBevelWeb
      webEndcutDS.AddLinearDim(point2,point1,VECTOR_V,point3, strRound(fDim) )

   return webEndcutDS, flaEndcutDS
#---------------------------------------------------------------------------------------------------
# Pre method for trigger
#---------------------------------------------------------------------------------------------------
def pre(*args):

   try:
      if len(args)<1:
         raise ValueError, "Not enough arguments"

      profileSketch = args[0]
      if profileSketch == None:
         raise ValueError, "Not valid arguments"

      #input data
      aryEndcut    = profileSketch.GetEndcutParams()
      aryProfile   = profileSketch.GetProfileParams()

      if len(aryEndcut)<9:
         raise ValueError, "Not enough endcut parameters"
      if len(aryProfile)<6:
         raise ValueError, "Not enough profile parameters"

      nEndcutType  = profileSketch.GetEndcutType()

      rectWeb      = profileSketch.GetEndcutRectangle()
      rectFlange   = profileSketch.GetFlangeCutRectangle()

      fExcess      = profileSketch.GetExcess()
      fSketchExcess = profileSketch.GetSketchExcess()
      fBevelWeb    = profileSketch.GetBevelGapWeb()
      fBevelFlange = profileSketch.GetBevelGapFlange()

      #output data
      webEndcutDS     = KcsSketchDimensioning.DimensionSet()
      flaEndcutDS     = KcsSketchDimensioning.DimensionSet()

      #calculating point to show the measures outside the rectangle

      ylow=rectWeb[0].Y-GAP
      yhigh=rectWeb[1].Y+GAP
      xleft=rectWeb[0].X-GAP
      xright=rectWeb[1].X+GAP
      xflangeleft=rectFlange[0].X-GAP
      xflangeright=rectFlange[1].X+GAP
      yflangelow=rectFlange[0].Y-GAP
      yflangehigh=rectFlange[1].Y+GAP

      #profile height
      profHeight = aryProfile[0]
      # if nEndcutType==44 or nEndcutType==83 or nEndcutType==175 or nEndcutType==181:
      fWebThickness = aryProfile[2]

      #flange
      flangeWidth = aryProfile[1]
      flangeHalf = flangeWidth/2.0
      if nEndcutType==139 or nEndcutType==164 or nEndcutType==83 or nEndcutType==162 or nEndcutType==40:
         fFlangeThickness = aryProfile[3]
         fFlangeWing = aryProfile[4]

      #endcut parameters
      a = aryEndcut[0]
      b = aryEndcut[1]
      c = aryEndcut[2]
      strR1 = translate_radius(aryEndcut[3])
      strR2 = translate_radius(aryEndcut[4])

      if aryEndcut[3]<0:
         fR1=(-1)*aryEndcut[3]
      else:
         fR1=aryEndcut[3]

      if aryEndcut[4]<0:
         fR2=(-1)*aryEndcut[4]
      else:
         fR2=aryEndcut[4]

      degAlfa1 = aryEndcut[5]
      degAlfa2 = aryEndcut[6]
      degAlfa3 = aryEndcut[7]
      degAlfa4 = aryEndcut[8]

      #-----------------------------FLAT BARS--------------------------------------------

      if nEndcutType == 69:
         webEndcutDS, flaEndcutDS = Endcut69( profHeight, a, b, c, strR1, strR2, degAlfa1, degAlfa2,
                                              fExcess, fSketchExcess, fBevelWeb,
                                              xleft, ylow, yhigh, yflangelow)
      elif nEndcutType == 65:
         webEndcutDS, flaEndcutDS = Endcut65(flangeWidth, a, b, fR1, strR1, fR2, strR2, degAlfa1,
                                             degAlfa2, fExcess, fSketchExcess, fBevelWeb, xleft,
                                             ylow, yflangelow, profHeight)
      elif nEndcutType == 114:
         webEndcutDS, flaEndcutDS = Endcut114( profHeight, b, c, fR1, strR1, degAlfa1, degAlfa2,
                                               fExcess, fSketchExcess, fBevelWeb,
                                               xleft, ylow, yhigh, yflangelow)
      elif nEndcutType == 116:
         webEndcutDS, flaEndcutDS = Endcut116 (flangeWidth, a, b, fR1, strR1, fR2, strR2, degAlfa1,
                                               degAlfa3, fExcess, fSketchExcess, fBevelWeb, xleft, ylow, yflangelow,
                                               profHeight)

      #-----------------------------BULBS AND L BARS------------------------------------

      elif nEndcutType == 25:
         webEndcutDS, flaEndcutDS = Endcut25 (flangeWidth, b, c, fR1, strR1, degAlfa1, degAlfa3,
                                              fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                              xleft, ylow, xflangeleft, yflangelow, yflangehigh)
      elif nEndcutType == 119:
         webEndcutDS, flaEndcutDS = Endcut119(flangeWidth, a, b, c, fR1, strR1, fR2, strR2,
                                              degAlfa1, degAlfa2, degAlfa3,fExcess, fSketchExcess, fBevelWeb, xleft,
                                              ylow, yflangelow, profHeight, fWebThickness)

      elif nEndcutType == 120:
         webEndcutDS, flaEndcutDS = Endcut120(flangeWidth, a, b, c, fR1, strR1, fR2, strR2,
                                              degAlfa1, degAlfa2, fExcess, fSketchExcess, fBevelWeb, xleft,
                                              ylow, yhigh, yflangelow, xflangeleft, profHeight,
                                              fWebThickness)
      elif nEndcutType == 129:
         webEndcutDS, flaEndcutDS = Endcut129(flangeWidth, fWebThickness,
                                              a, b, c, strR1, degAlfa1, degAlfa2, degAlfa3,
                                              fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                              xleft, ylow, xflangeleft, yflangelow)

      #-----------------------------ASYMMETRICAL T BARS----------------------------------

      elif nEndcutType == 40:
         webEndcutDS, flaEndcutDS = Endcut40(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1,
                                             degAlfa2, degAlfa3, degAlfa4, fExcess, fSketchExcess, fBevelWeb, xleft,
                                             ylow, yhigh, yflangelow, xflangeleft, profHeight,
                                             fWebThickness, fFlangeWing, fFlangeThickness)
      elif nEndcutType == 139:
         webEndcutDS, flaEndcutDS = Endcut139( fFlangeThickness, profHeight, flangeWidth, fFlangeWing,
                                               a, b, c, strR1, fR2, strR2, degAlfa1, degAlfa2, degAlfa4,
                                               fExcess, fSketchExcess, fBevelWeb, fBevelFlange, ylow, yhigh, xflangeleft, yflangelow)
      elif nEndcutType == 162:
         webEndcutDS, flaEndcutDS = Endcut162(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1,
                                              degAlfa2, degAlfa3, degAlfa4, fExcess, fSketchExcess, fBevelWeb, xleft,
                                              ylow, yhigh, yflangelow, xflangeleft, profHeight,
                                              fWebThickness, fFlangeWing, fFlangeThickness)
      elif nEndcutType == 164:
         webEndcutDS, flaEndcutDS = Endcut164( fFlangeThickness, profHeight, flangeWidth, fFlangeWing,
                                               a, b, c, strR1, degAlfa1, degAlfa2, degAlfa4,
                                               fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                               ylow, yhigh, xflangeleft, yflangelow)

      #-----------------------------  T BARS---------------------------------------------

      elif nEndcutType == 39:
         webEndcutDS, flaEndcutDS = Endcut39(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1,
                                             degAlfa2, degAlfa3, degAlfa4, fExcess, fSketchExcess, fBevelWeb, xleft,
                                             ylow, yhigh, yflangelow, xflangeleft, profHeight,
                                             fWebThickness)
      elif nEndcutType == 44:
         webEndcutDS, flaEndcutDS = Endcut44(flangeWidth, fWebThickness, a, b, c, strR1, degAlfa1, degAlfa2, degAlfa4,
                                             fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                             xleft, ylow, xflangeleft, yflangelow)
      elif nEndcutType == 83:
         webEndcutDS, flaEndcutDS = Endcut83(flangeWidth, fWebThickness, fFlangeThickness, profHeight,
                                             b, c, strR1, strR2, degAlfa1, degAlfa2, degAlfa3,
                                             fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                             xleft, xflangeleft, yflangelow)
      elif nEndcutType == 145:
         webEndcutDS, flaEndcutDS = Endcut145(flangeWidth, a, b, c, fR1, strR1, fR2, strR2, degAlfa1,
                                             degAlfa2, degAlfa3, degAlfa4, fExcess, fSketchExcess, fBevelWeb, xleft,
                                             ylow, yhigh, yflangelow, xflangeleft, profHeight,
                                             fWebThickness)

      #-----------------------------  I BARS---------------------------------------------

      elif nEndcutType == 175:
         webEndcutDS, flaEndcutDS = Endcut175( flangeWidth, profHeight, fWebThickness,
                                               a, b, c, strR1, fR2, strR2, degAlfa4,
                                               fExcess, fSketchExcess, fBevelWeb,
                                               xleft, ylow, yhigh, yflangelow)
      elif nEndcutType == 181:
         webEndcutDS, flaEndcutDS = Endcut181( flangeWidth, profHeight, fWebThickness, a, b, c, strR1, fR2, strR2,
                                               degAlfa4, fExcess, fSketchExcess, fBevelWeb,
                                               xleft, ylow, yhigh, yflangelow)

      #-----------------------------  U BARS---------------------------------------------

      elif nEndcutType == 188:
         webEndcutDS, flaEndcutDS = Endcut188( profHeight, a, b, c, strR1, fR1, degAlfa4,
                                               fExcess, fSketchExcess, fBevelWeb, xleft, yhigh, yflangelow )

      elif nEndcutType == 190:
         webEndcutDS, flaEndcutDS = Endcut190( flangeWidth, a, b, c, strR1, fR1, degAlfa1, degAlfa2, degAlfa4,
                                               fExcess, fSketchExcess, fBevelWeb, fBevelFlange,
                                               xleft, ylow, xflangeleft, yflangelow)

      #-----------------------------END OF ENDCUTS------------------------------------------
      else:
         return kcs_util.trigger_abort()

      return [kcs_util.trigger_ok(), webEndcutDS, flaEndcutDS ]


   except  Exception, e:
      print "Failed ", e
      return kcs_util.trigger_abort()

#---------------------------------------------------------------------------------------------------
# Post method for trigger
#---------------------------------------------------------------------------------------------------
def post(*args):
   return kcs_util.trigger_ok()

#---------------------------------------------------------------------------------------------------
# Auxiliary methods
#---------------------------------------------------------------------------------------------------
def strRound(fVal):
   'Translate floating point numbers into strings'
   'Not generate ".0" if it has no fraction part'
   hasFraction = abs(fVal - int(fVal))>ABOUT_ZERO
   if not hasFraction:
      return str(int(fVal))
   else:
      return str(fVal)

#---------------------------------------------------------------------------------------------------
def translate_radius(fRadius):
   'Translate radius value into string with KS or R'
   if fRadius<0:
      fRadius=(-1)*fRadius
      strRadius='KS'+strRound(fRadius)
   else:
      fRadius = fRadius % 1000
      strRadius='R'+strRound(fRadius)
   return strRadius


#---------------------------------------------------------------------------------------------------
#
# Adding angle to endcut dimensioning set
#
# input:
#
# degAlfa
#   - angle to be added (in degrees)
#
# pointC
#   - centre point of angle
#
# degAngle1
#   - angle of first arm of angle, degrees are counted counterclockcwise
#     from the line y=poinC.y directed right from the poincC;
#     negative value is possible
#
# show_first_arcus_arm
#  -  0 do not show
#     1 show line
#
# show_second_arcus_arm
#  -  0 do not show
#     1 show line
#
# show_degree
#  -  0 do not show
#     1 show line
#
# DS
#     dimensionig set
#
#---------------------------------------------------------------------------------------------------
def add_angle(degAlfa, pointC, degAngle1, show_first_arcus_arm, show_second_arcus_arm, show_degree, DS):

   SHIFT_ANGLE   = 55            # shift used to move angle line and text from arc center
   SCALE_LEG     = 1.1           # scale used with SHIFT_ANGLE to calculate angle leg length
   ANGLE_INSIDE = 55             # above this value angle text will be placed inside angle
   ANGLE_IN = 0.6                # scale for placing angle text inside angle
   ANGLE_OUT = 1.2 * SCALE_LEG   # scale for placing angle text outside angle

   TEXT_LENGTH = 28
   TEXT_HEIGHT = 7


   radAlfa = degAlfa*math.pi/180

   if degAngle1<0:
      degAngle1=360 + degAngle1
   radAngle1=degAngle1*math.pi/180


   #first arcus arm end point
   point1 = KcsPoint2D.Point2D(pointC.X + math.cos(radAngle1)*SCALE_LEG*SHIFT_ANGLE,
                               pointC.Y + math.sin(radAngle1)*SCALE_LEG*SHIFT_ANGLE)

   #second arcus arm end point
   point2 = KcsPoint2D.Point2D(pointC.X + math.cos(radAngle1+radAlfa)*SCALE_LEG*SHIFT_ANGLE,
                               pointC.Y + math.sin(radAngle1+radAlfa)*SCALE_LEG*SHIFT_ANGLE)

   #arcus line point (SHIFT_ANGLE from arc center)
   point3 = KcsPoint2D.Point2D(pointC.X + math.cos(radAngle1+radAlfa/2)*SHIFT_ANGLE,
                               pointC.Y + math.sin(radAngle1+radAlfa/2)*SHIFT_ANGLE)

   #arcus text point (SCALE_LEG*SHIFT_ANGLE from arc center)
   if degAlfa>ANGLE_INSIDE:
      distRadius = ANGLE_IN * SHIFT_ANGLE
      distRadiusValueY=0
      distRadiusValueX=0
      if degAngle1 + degAlfa/2 <45 or degAngle1 + degAlfa/2> 315:
         distRadiusValueY= - TEXT_HEIGHT/2
         distRadiusValueX= - TEXT_LENGTH*2/5
      elif degAngle1 + degAlfa/2 < 135:
         distRadiusValueX= - TEXT_LENGTH/2
      elif degAngle1 + degAlfa/2 < 225:
         distRadiusValueX= - TEXT_LENGTH/2
         distRadiusValueY= - TEXT_HEIGHT/2
      else:# degAngle1 + degAlfa/2 < 315:
         distRadiusValueX= - TEXT_LENGTH/2
         distRadiusValueY= - TEXT_HEIGHT

   else:
      distRadius = ANGLE_OUT * SHIFT_ANGLE
      distRadiusValueY=0
      distRadiusValueX=0
      if degAngle1 + degAlfa/2 <45 or degAngle1 + degAlfa/2> 315:
         distRadiusValueY= - TEXT_HEIGHT/2
      elif degAngle1 + degAlfa/2 < 135:
         distRadiusValueX= - TEXT_LENGTH/2
      elif degAngle1 + degAlfa/2 < 225:
         distRadiusValueX= - TEXT_LENGTH
         distRadiusValueY= - TEXT_HEIGHT/2
      else:# degAngle1 + degAlfa/2 < 315:
         distRadiusValueX= - TEXT_LENGTH/2
         distRadiusValueY= - TEXT_HEIGHT

   point4 = KcsPoint2D.Point2D(pointC.X + math.cos(radAngle1+radAlfa/2)*distRadius+distRadiusValueX,
                               pointC.Y + math.sin(radAngle1+radAlfa/2)*distRadius+distRadiusValueY)

   line1 = KcsRline2D.Rline2D(pointC, point1)
   line2 = KcsRline2D.Rline2D(pointC, point2)

   DS.AddAngleDim(line1, line2, point3, point4, strRound(degAlfa),
                  show_first_arcus_arm, show_second_arcus_arm, show_degree)

   return
#---------------------------------------------------------------------------------------------------
