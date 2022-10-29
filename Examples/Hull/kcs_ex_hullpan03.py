## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hullpan03.py
#
#      PURPOSE:
#
#               This program presents kcs_hullpan:  panel(s) function.
#
#
#
#----------------------------------------------------------------------------------
import string
import kcs_ui
import kcs_util
import kcs_hullpan
import CommonSample
import KcsPoint3D
import KcsVector3D
import KcsPlane3D

#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
isPanelActive = ''
hullpanname = ''
hulltype = ''
location = ''
model = ''

while 1:
   actions = (
      'Panel: ' +hullpanname+ 'Type: ' +hulltype,
      'Activated: ' +isPanelActive,
      'Remove Seam',
      'Group Delete',
      'Group Divide',
      'Split Stiffener by Model',
      'Split Stiffener by Plane'
      )

   (status, index) = kcs_ui.choice_select('Panels','Operations on the Panels', actions)
   if status == kcs_util.ok():
      if index == 1:
         model = CommonSample.SelectModel()
         hullpanname = model.Name
         hulltype = model.Type
      elif index == 2:
         isPanelActive = 'Yes'
         kcs_hullpan.pan_activate(hullpanname)
      elif index == 3:
         res, location = kcs_ui.string_req('Enter Seam ID:','')
         kcs_hullpan.pan_remove_seam(hullpanname, 5001)
      elif index == 4:
         res, dict = kcs_ui.string_req('Enter Group ID:' ,'')
         dict = int(dict)
         kcs_hullpan.pan_group_delete(hullpanname, dict)
      elif index == 5:
         res, dict = kcs_ui.string_req('Enter Group ID:' ,'')
         dict = int(dict)
         model = CommonSample.SelectModel()
         kcs_hullpan.pan_group_divide(hullpanname, dict, [model, model])
      elif index == 6:
         #model = CommonSample.SelectModel()
         resgroup, dictgroup = kcs_ui.string_req('Enter Group ID:' ,'')
         res, dict = kcs_ui.string_req('Enter Splitting Model ID:' ,'')
         dict = int(dict)
         dictgroup = int(dictgroup)
         kcs_hullpan.pan_sti_split_by_model(dictgroup, dict)
      elif index == 7:
         #model = CommonSample.SelectModel()
         resgroup, dictgroup = kcs_ui.string_req('Enter Group ID:' ,'')
         res, dict = kcs_ui.string_req('Enter Splitting Line:' ,'')
         dictgroup = int(dictgroup)
         kcs_hullpan.pan_sti_split_by_plane(dictgroup, dict)
   else:
      print "User interrupted!"
      break;


#----------------------------------------------------------------------------------
