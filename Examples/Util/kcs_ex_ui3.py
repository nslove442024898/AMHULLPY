## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui3.py
#
#      PURPOSE:
#
#          This program shows how to use kcs_ui.choice_select()
#
import kcs_ui
import kcs_util
import KcsStringlist

t1 = "Example of \"choice_select\""
t2 = "Available choices"
t4 = "Choice no. 1"
slist = KcsStringlist.Stringlist(t4)
t5 = "Choice no. 2"
slist.AddString(t5)
t6 = "Choice no. 3"
slist.AddString(t6)
try:
   res = kcs_ui.choice_select(t1,t2,slist)
   if res[0] == kcs_util.ok():
      print 'Your selection: Choice no',res[1]
   elif res[0] == kcs_util.cancel():
      print 'You pressed CANCEL'
   else:
      print 'User interrupted'
except:
  print kcs_ui.error
