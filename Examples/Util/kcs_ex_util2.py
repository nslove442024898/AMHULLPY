## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_util2.py
#
#      PURPOSE:
#
#          This program shows how the utility functions can be used to
#          check the user response from a Vitesse UI function
#
import kcs_ui
import kcs_util
import KcsStringlist

s1 = "Example of \"choice_select\""
s2 = "Available choices"
s4 = "Choice no. 1"
slist = KcsStringlist.Stringlist(s4)
s5 = "Choice no. 2"
slist.AddString(s5)
s6 = "Choice no. 3"
slist.AddString(s6)
try:
   res = kcs_ui.choice_select(s1,s2,slist)
   if res[0] == kcs_util.ok():
      print 'Your selection: Choice no',res[1]
   elif res[0] == kcs_util.cancel():
      print 'You pressed CANCEL or REJECT'
   elif res[0] == kcs_util.options():
      print 'You pressed OPTIONS'
   elif res[0] == kcs_util.quit():
      print 'You pressed EF (QUIT)'
   elif res[0] == kcs_util.operation_complete():
      print 'You pressed OPERATION COMPLETE'
   else:
      print 'You pressed some other interrupting button'
except:
  print kcs_ui.error

try:
   res = kcs_ui.answer_req("Example of \"answer_req\"", "Will You answer this\ntwo-line question?")
   if res == kcs_util.yes():
      print 'You answered YES'
   elif res == kcs_util.no():
      print 'You answered NO'
   elif res == kcs_util.cancel():
      print 'You pressed CANCEL or REJECT'
   elif res == kcs_util.options():
      print 'You pressed OPTIONS'
   elif res == kcs_util.quit():
      print 'You pressed EF (QUIT)'
   else:
      print 'You pressed some other interrupting button'
except:
  print kcs_ui.error
