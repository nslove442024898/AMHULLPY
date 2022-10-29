## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui07.py
#
#      PURPOSE:
#
#          Example usage of vitesse utility functions:
#				1. app_window_minimize()
#				2. app_window_maximize()
#				3. app_window_restore()
#

import kcs_ui
import kcs_util
import KcsStringlist

#------------------------------------------------------------------------------------
#   Function selection
#------------------------------------------------------------------------------------

actions = KcsStringlist.Stringlist('Minimalize window')
actions.AddString('Maximize window')
actions.AddString('Restore window')

try:
    (status, option) = kcs_ui.choice_select('Utility functions', 'Select option', actions)
    if status == kcs_util.ok() :
        if option == 1 :
            kcs_ui.app_window_minimize()
        elif option == 2 :
            kcs_ui.app_window_maximize()
        elif option == 3 :
            kcs_ui.app_window_restore()
    else:
        print "User interrupted!"
except:
    print kcs_ui.error
