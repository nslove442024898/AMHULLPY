## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_util3.py
#
#      PURPOSE:
#
#          This program shows how the utility functions can be used to
#          return proper values from a trigger function. It also shows
#          how to check which application that is current so we can
#          perform different actions in different applications.
#
#          Please note that a trigger Vitesse script needs to be named
#          properly so this is not a valid example.
#
import kcs_util

def pre(*args):
   if kcs_util.drafting():
#
#     We are running Drafting so this function is allowed.
#
      return kcs_util.trigger_ok()
   else:
#
# Other applications are not allowed to invoke this function.
#
      return kcs_util.trigger_abort()
