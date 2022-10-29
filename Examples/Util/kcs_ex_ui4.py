## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui4.py
#
#      PURPOSE:
#
#          This program shows how to use kcs_ui.string_select().
#
import kcs_ui
import kcs_util
import KcsStringlist

t1 = "Example of \"string_select\""
t2 = "List of strings"
t3 = "Please select a string"
t4 = "String 1"
slist = KcsStringlist.Stringlist(t4)
t5 = "String 2"
slist.AddString(t5)
t6 = "String 3"
slist.AddString(t6)
try:
   res = kcs_ui.string_select(t1,t2,t3,slist)
   if res[0] == kcs_util.ok():
      print 'Your selection:',slist.StrList[res[1]-1]
   else:
      print 'User interrupted'
except:
  print kcs_ui.error
