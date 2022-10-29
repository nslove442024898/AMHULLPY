## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hullcurved_views01.py
#
#      PURPOSE:
#
#               This program presents kcs_chm: view handling functions.
#
#
#
#----------------------------------------------------------------------------------
import string
import kcs_ui
import kcs_util
import kcs_chm
import KcsShellXViewOptions
import KcsBodyPlanViewOptions
import KcsInterpretationObject
import CommonSample
import KcsModel

#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
view = 0
options = KcsInterpretationObject.CurvedPanelView()
shellx = KcsShellXViewOptions.ShellXViewOptions()
body = KcsBodyPlanViewOptions.BodyPlanViewOptions()
seams = []
surfaces = []
bodyseams = []
location = 'TB_SHELLX'
loc = 'TB_BODY'

shellx.SetShellXViewName(location)
body.SetBodyPlanViewName(loc)

#
# Initilize some settings for the shellX view
#
shellx.SetSternLimits( -1, 30000.0 )
shellx.SetStemLimits( -1, 100000.0 )


while 1:
   actions = (
      'Set ShellX View Name: ',
      'Set ShellX Surface Name',
      'Set ShellX Select Seams',
      'Set ShellX Exclude Seams',
      'Create ShellX View: ',
      'Set Bodyplan View Name: ',
      'Create Body Plan View',
      'Create Curved Stiffener View',
      'Create Curved Plate View',
      'Create Curved Panel View',
      'Modify View',
      'Recreate View'
      )

   (status, index) = kcs_ui.choice_select('Views','Curved Hull Views', actions)

   if status == kcs_util.ok():
      if index == 1:
         res, location = kcs_ui.string_req('Enter View Name:','')
         shellx.SetShellXViewName(location)

      elif index == 2:
         res, location = kcs_ui.string_req('Enter Surface Name:','')
         shellx.SetSurfName(location)

      elif index == 3:
         res, location = kcs_ui.string_req('Enter Seam to exclude/include:','')
         seams.append(location)
         shellx.SetSelectSeams(seams)

      elif index == 4:
         shellx.SetExceptSeams()

      elif index == 5:
         view = kcs_chm.view_shellexp_new(shellx)

      elif index == 6:
         res, loc = kcs_ui.string_req('Enter Bodyplan View Name:','')
         body.SetBodyPlanViewName(loc)

      elif index == 7:
         view = kcs_chm.view_bodyplan_new(body)

      elif index == 8:
         res, model_name = kcs_ui.string_req('Enter name of shell stiffener:','')
         model = KcsModel.Model( "curved stiffener", model_name);
#        Please note that the selected stiffener must be on the profile data bank.
         view = kcs_chm.view_shprof_new(model)

      elif index == 9:
#        The user should indicate a curved plate
         object = CommonSample.SelectModel()
         view = kcs_chm.view_devpla_new(object)

      elif index == 10:
         object = CommonSample.SelectModel()
         view = kcs_chm.view_curvedpanel_new(object, options)

      elif index == 11:
         view_options = kcs_chm.view_modify(view)

      elif index == 12:
         kcs_chm.view_recreate(view)
   else:
      print "User interrupted!"
      break;


#----------------------------------------------------------------------------------





