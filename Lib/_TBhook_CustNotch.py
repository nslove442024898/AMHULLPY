## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_CustNotch - Customizing of Notches
#
#  If this script is found in the PYTHONPATH it can be used to
#  create customer defined Notches
#

import string
import kcs_util
import math

ok = kcs_util.success()
not_ok = kcs_util.failure()

#------------------------------------------------------------------------------
#  NotchList - the list of Vitesse Notch types to select from
#
#  The NotchList must contain the types of Vitesse Notches used.
#  This as a means of doublecheck. The order of the Notch
#  types is irrelevant.
#
#  !! Please make sure that the list of Notch names end with an empty string
#     as this is used as the signal to terminate the reading of names !!
#------------------------------------------------------------------------------

NotchList = (
  "NOTA",
  "NOTB",
  "HOS",
  ""
)


NotchData = []


#-----------------------------------------------------------------------------
#  Interface methods - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def getNotchName(NotchNo):
  try:
    return NotchList[NotchNo]
  except:
    return None

def getNotchSegment(SegNo):
  try:
    return NotchData[SegNo]
  except:
    return None

#-----------------------------------------------------------------------------
#
#     Function setNotchContour -
#
#     The Notch definition function adding Notch segments to the NotchData list.
#     The function should define a Notch contour in the UV co-ordinate system
#     whose origin will be the reference point of the Notch. Up to 8 number of
#     Notch parameters are allowed.
#
#     The breakpoints of the Notchcontour should be defined as a number of
#     segments (R, U, V), where R is equal to 0.0 for a line segment, positive
#     for a counterclock radius and negative for a clockwise radius.
#
#     The Notch code should be implemented with an exception handling mechanism so
#     that a failure to run the code will always be signalled by the return code.
#
#     The return code should heve one of the following predefined values
#
#        = 0 OK
#        = 1 Unrecognized Notch type
#        = 2 Wrong number of parameters
#        = 3 Unreasonable parameter values
#        = 4 Notch geometry could not be generated
#
#-----------------------------------------------------------------------------

def setNotchContour(NotchName, NPar, Par1, Par2, Par3, Par4, Par5, Par6, Par7, Par8):

  global NotchData
  NotchData = []


#----------------------------------------------------
#  Notch Type NOTA
#---------------------------------------------------

  if NotchName == "NOTA":

     try:
#
#  Check parameters
#
        if NPar != 2:
           NotchRes = 3
        else:
#
#  Start contour
#
           U = -Par2/2.0
           V =  -500.0
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)
#
#  Following breakpoints
#
           U = -Par2/2.0
           V = Par1
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)

           U = Par2/2.0
           V = Par1
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)

#
#  Endpoint
#
           U = Par2/2.0
           V = -500
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)
#
#  Success result code
#
           NotchRes = 0

     except:
        NotchRes = 4

#----------------------------------------------------
#  Notchtype NOTB
#----------------------------------------------------
  elif NotchName == "NOTB":
     try:
#
#  Check parameters
#
        if NPar != 2:
           NotchRes = 2
        else:


           U = -500
           V = Par2
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)

           U = Par1
           V = Par2
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)

           U = Par1
           V = -500
           Segment = ( 0.0, U, V)
           NotchData.append( Segment)
#
#  Success result code
#
           NotchRes = 0
#
#  Failure generating Notch
#
     except:
        NotchRes = 4

#----------------------------------------------------
#  Notchtype HOL
#---------------------------------------------------
  elif NotchName == "HOL":
     if NPar != 1:
        NotchRes = 2
#
# Test case, not implemented
#
     else:
        NotchRes = 4

  else:
     NotchRes = 1

#----------------------------------------------------
#  Return Code from Notch defining function
#---------------------------------------------------

  return NotchRes
