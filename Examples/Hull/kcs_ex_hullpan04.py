## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hullpan04.py
#
#      PURPOSE:
#
#               This program presents kcs_hullpan: view_detail_new function.
#
#
#
#----------------------------------------------------------------------------------
import string
import CommonSample
import kcs_hullpan
import kcs_ui
import kcs_util
import KcsInterpretationObject


#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------

nViewHandle = 0
nElemHandle = 0
SymbolicView = KcsInterpretationObject.SymbolicView()

while 1:
   actions = (
      'Select Geometry',
      'Detail View Flange',
      'Detail View Seam',
      'Detail View Bracket',
      'Detail View Stiffener',
      'Symbolic View Recreate',
      'Symbolic View Modify'
      )

   (status, index) = kcs_ui.choice_select('Symbolic View','Operations on Symbolic Views', actions)
   if status == kcs_util.ok():
      if index == 1:
        [res, nElemHandle] = CommonSample.SelectGeometry("")
      elif index == 2:
         nViewHandle = kcs_hullpan.view_detail_new(2, nElemHandle)
      elif index == 3:
         nViewHandle = kcs_hullpan.view_detail_new(5, nElemHandle)
      elif index == 4:
         nViewHandle = kcs_hullpan.view_detail_new(4, nElemHandle)
      elif index == 5:
         nViewHandle = kcs_hullpan.view_detail_new(3, nElemHandle)
      elif index == 6:
         kcs_hullpan.view_symbolic_recreate(nViewHandle)
      elif index == 7:
         SymbolicView = kcs_hullpan.view_symbolic_modify(nViewHandle)
   else:
      print "User interrupted!"
      break;
#----------------------------------------------------------------------------------








