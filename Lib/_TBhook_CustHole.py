## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_CustHole - Customizing of Holes
#
#  If this script is found in the PYTHONPATH it can be used to
#  create customer defined Holes
#

import string
import math


#------------------------------------------------------------------------------
#  HoleList - the list of Vitesse hole types to select from
#
#  The HoleList must contain the types of Vitesse holes used.
#  This as a means of doublecheck. The order of the hole
#  types is irrelevant.
#
#  !! Please make sure that the list of hole names end with an empty string
#     as this is used as the signal to terminate the reading of names !!
#------------------------------------------------------------------------------

HoleList = (
  "FH",
  "HOL",
  "HOS",
  ""
)


HoleData = []


#-----------------------------------------------------------------------------
#  Interface methods - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def getHoleName(HoleNo):
  try:
    return HoleList[HoleNo]
  except:
    return None

def getHoleSegment(SegNo):
  try:
    return HoleData[SegNo]
  except:
    return None

#-----------------------------------------------------------------------------
#
#     Function setHoleContour -
#
#     The Hole definition function adding hole segments to the HoleData list.
#     The function should define a hole contour in the UV co-ordinate system
#     whose origin will be the reference point of the hole. Up to 8 number of
#     hole parameters are allowed.
#
#     The breakpoints of the holecontour should be defined as a number of
#     segments (R, U, V), where R is equal to 0.0 for a line segment, positive
#     for a counterclock radius and negative for a clockwise radius.
#
#     The hole code should be implemented with an exception handling mechanism so
#     that a failure to run the code will always be signalled by the return code.
#
#     The return code should heve one of the following predefined values
#
#        = 0 OK
#        = 1 Unrecognized hole type
#        = 2 Wrong number of parameters
#        = 3 Unreasonable parameter values
#        = 4 Hole geometry could not be generated
#
#-----------------------------------------------------------------------------

def setHoleContour(HoleName, NPar, Par1, Par2, Par3, Par4, Par5, Par6, Par7, Par8):

  global HoleData
  HoleData = []


#----------------------------------------------------
#  Hole Type FH
#---------------------------------------------------

  if HoleName == "FH":

     try:
#
#  Check parameters
#
        if NPar != 2:
           HoleRes = 3
        elif Par2 > ( Par1 / 2.0 ):
           HoleRes = 2
        else:
#
#  Start contour
#
           Segment = ( 0.0, 0.0, 0.0)
           HoleData.append( Segment)
#
#  Following breakpoints
#
           U = math.sqrt( (Par1-Par2)*(Par1-Par2) - Par2*Par2)
           V = 0.0
           SaveU = U
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           V = (Par1 * Par2) / (Par1 - Par2)
           U = math.sqrt(Par1*Par1 - V*V)
           Segment = ( Par2, U, V)
           HoleData.append( Segment)

           U = -U
           Segment = ( Par1, U, V)
           HoleData.append( Segment)

           U = -SaveU
           Segment = ( Par2, U, 0.0)
           HoleData.append( Segment)
#
#  Endpoint
#
           Segment = ( 0.0, 0.0, 0.0)
           HoleData.append( Segment)
           HoleRes = 0

     except:
        HoleRes = 4

#----------------------------------------------------
#  Holetype HOS
#----------------------------------------------------
  elif HoleName == "HOS":
     try:
#
#  Check parameters
#
        if NPar != 4:
           HoleRes = 2
        else:

           R = Par2 / 2.0 - Par3 / 2.0
           U = ( Par2 / 2.0)
           V = -(Par1 / 2.0 - R)
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           V = Par1 / 2.0 - R
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           U = Par3 / 2.0
           V = Par1 / 2.0
           Segment = ( R, U, V)
           HoleData.append( Segment)

           V = V - Par4
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           U = - U
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           V = Par1 / 2.0
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           U = -( Par2 / 2.0)
           V = Par1 / 2.0 - R
           Segment = ( R, U, V)
           HoleData.append( Segment)

           U = -( Par2 / 2.0)
           V = -(Par1 / 2.0 - R)
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           U = -( Par3 / 2.0)
           V = -( Par1 / 2.0)
           Segment = ( R, U, V)
           HoleData.append( Segment)

           V = V + Par4
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           U = U + Par3
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)

           V = V - Par4
           Segment = ( 0.0, U, V)
           HoleData.append( Segment)
#
#  Last segment, whose endpoint should be the same as the startpoint
#  of the contour
#
           U = ( Par2 / 2.0)
           V = -(Par1 / 2.0 - R)
           Segment = ( R, U, V)
           HoleData.append( Segment)
#
#  Success result code
#
           HoleRes = 0
#
#  Failure generating hole
#
     except:
        HoleRes = 4

#----------------------------------------------------
#  Holetype HOL
#---------------------------------------------------
  elif HoleName == "HOL":
     if NPar != 1:
        HoleRes = 2
#
# Test case, not implemented
#
     else:
        HoleRes = 4

  else:
     HoleRes = 1

#----------------------------------------------------
#  Return Code from Hole defining function
#---------------------------------------------------

  return HoleRes
