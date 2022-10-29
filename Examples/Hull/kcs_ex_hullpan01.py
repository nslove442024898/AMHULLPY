## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_hullpan01.py
#
#      PURPOSE:
#
#               This program presents kcs_hullpan: active, store, skip, delete and list_active functions.
#
#
#
#----------------------------------------------------------------------------------
import string
import kcs_ui
import kcs_util
import kcs_hullpan
import CommonSample
#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
hullpanname = ''
list = []

while 1:
   actions = (
      'Panel: '+hullpanname,
      'Activate',
      'Store All',
      'Store',
      'Skip',
      'Skip All',
      'List Activated',
      'Delete'
      )

   (status, index) = kcs_ui.choice_select('Panels','Operations on the Panels', actions)

   if status == kcs_util.ok():
      if index == 1:
         model = CommonSample.SelectModel()
         hullpanname = model.Name
      elif index == 2:
         try:
            kcs_hullpan.pan_activate(hullpanname)
            kcs_ui.message_confirm('Activated:' +hullpanname)
         except:
            kcs_ui.message_confirm('Panel not activated! Error: %s' % kcs_hullpan.error)
      elif index == 3:
         try:
            kcs_hullpan.pan_store()
            kcs_ui.message_confirm('Stored All')
         except:
            kcs_ui.message_confirm('Panel not stored! Error: %s' % kcs_hullpan.error)
      elif index == 4:
         try:
            kcs_hullpan.pan_store(hullpanname)
            kcs_ui.message_confirm('Stored:' +hullpanname)
         except:
            kcs_ui.message_confirm('Panel not stored! Error: %s' % kcs_hullpan.error)
      elif index == 5:
         try:
            kcs_hullpan.pan_skip(hullpanname)
            kcs_ui.message_confirm('Skipped:' +hullpanname)
         except:
            kcs_ui.message_confirm('Panel not stored! Error: %s' % kcs_hullpan.error)
      elif index == 6:
         try:
            kcs_hullpan.pan_skip()
            kcs_ui.message_confirm('Skipped')
         except:
            kcs_ui.message_confirm('Panel not stored! Error: %s' % kcs_hullpan.error)
      elif index == 7:
         list = kcs_hullpan.pan_list_active()
         (status, index) = kcs_ui.string_select('Drawings', 'Select drawing:', '', list)
      elif index == 8:
         kcs_hullpan.pan_delete(hullpanname)
         kcs_ui.message_confirm('Deleted:' +hullpanname)
   else:
      print "User interrupted!"
      break;


#----------------------------------------------------------------------------------
