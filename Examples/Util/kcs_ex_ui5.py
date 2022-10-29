## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui5.py
#
#      PURPOSE:
#
#          This program shows how to use kcs_ui.string_req().
#
import kcs_ui
import kcs_util

message = 'Please enter a string'
predef = 'This is the predefined string'
try:
   res = kcs_ui.string_req(message,predef)
   if res[0] == kcs_util.ok():
      print 'The entered string is:',res[1]
   else:
      print 'User interrupted'
except:
  print kcs_ui.error
