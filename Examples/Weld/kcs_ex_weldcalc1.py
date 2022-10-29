## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_weldcalc1.py
#
#      PURPOSE:
#
#          weld calculation
#

import string
import kcs_assembly
import kcs_ui
import kcs_util
import kcs_weld
import KcsGeoContour3D
import KcsPoint3D
import KcsVector3D
import KcsWeldTable
import KcsWeldedJoint
import KcsWeld

OK = kcs_util.ok()
CANCEL  = kcs_util.cancel()

#try:
if 1:
   assembly = kcs_ui.string_req("Key in name of assembly :")
   if assembly[0] == OK:
#      try:
      if 1:
         state = kcs_assembly.assembly_exist(assembly[1])
         print state
         if (state==1):
              wstate = kcs_weld.weld_calculation( assembly[1], 0)
              print wstate
              if (wstate==1):
               kcs_ui.message_confirm("Weld calculation OK!" )

               weldTable = KcsWeldTable.WeldTable()
               weldprop = kcs_weld.weld_properties_get(assembly[1],weldTable)
               print weldTable

               print "TotalWeldLength = ", weldTable.GetTotalWeldLength()
               print ""
               nw = 0
               weldTable.SetWeldTableComment( "A2345678901234567890123456789012345678901234567890123456789012345678901234567890")
               print "Weld table comment: ", weldTable.GetWeldTableComment()
               njoints = weldTable.GetNumberWeldedJoints();
               for joint in range( 0, njoints, 1):
                  wj = weldTable.GetWeldedJoint( joint)
                  wj.SetJointComment( str( joint))
                  nwelds = wj.GetNumberWelds()
                  for weld in range( 0, nwelds ,1):
                     wld = wj.GetWeld( weld)
                     nw = nw + 1
                     wld.SetWeldComment( str( nw))
                     wld.SetStartSuspension( 50)
                     wld.SetEndSuspension( 75)
                     wj.SetWeld( weld, wld)

                  weldTable.SetWeldedJoint( joint, wj)
###               print "delete weld table"
###               wstate = kcs_weld.weld_delete( assembly[1]);
###               print wstate
               print weldTable
               weldprop = kcs_weld.weld_properties_set(assembly[1],weldTable)
         else:
            kcs_ui.message_confirm("Assembly " + string.upper(assembly[1]) + " does not exist ! " )
#      except:
#         kcs_ui.message_noconfirm("Assembly does not exist." )
#         print kcs_weld.error
   elif assembly[0] == CANCEL:
      a = 1
   else:
      kcs_ui.message_noconfirm("Invalid input parameter !" )
#except:
#    a = 3
