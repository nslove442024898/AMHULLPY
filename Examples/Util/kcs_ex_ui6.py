## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui6.py
#
#      PURPOSE:
#
#          This program shows how to use a number of kcs_ui functions.
#
import kcs_ui
import kcs_util
import KcsColour
import KcsPoint3D
import KcsStat_point3D_req

res = kcs_ui.int_req("Keyin integer")
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

res = kcs_ui.int_req("Keyin integer",999)
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

res = kcs_ui.real_req("Keyin real")
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

res = kcs_ui.real_req("Keyin real", 999.999)
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

res = kcs_ui.string_req("Keyin string")
if res[0] == kcs_util.ok():
   print 'Given value: ' + res[1]
else:
   print 'User interrupted'

res = kcs_ui.string_req("Keyin string", "predefined string")
if res[0] == kcs_util.ok():
   print 'Given value: ' + res[1]
else:
   print 'User interrupted'

pnt3D = KcsPoint3D.Point3D()
res = kcs_ui.point3D_req("Define 3D point",pnt3D)
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

init_stat = KcsStat_point3D_req.Stat_point3D_req()
init_stat.Helpdef = 1
init_stat.Helppnt = pnt3D
init_stat.Locktype = 2
init_stat.Lockpnt = pnt3D
init_stat.Lockvec = KcsPoint3D.Point3D(1.0,0.0,0.0)
init_stat.Initial3D = 4
init_stat.Initial2D = 3
res = kcs_ui.point3D_req("Define 3D point",init_stat,pnt3D)
if res[0] == kcs_util.ok():
   print 'Given value:', res[1]
else:
   print 'User interrupted'

kcs_ui.message_noconfirm("A non-confirmed message")

colour = KcsColour.Colour()
res = kcs_ui.colour_select("Colour selection", colour)
if res[0] == kcs_util.ok():
   print 'Given value: ' + res[1].Name()
else:
   print 'User interrupted'

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
