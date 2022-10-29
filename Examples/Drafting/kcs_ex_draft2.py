## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft2.py
#
#      PURPOSE:
#
#          This program allows user to select and check modal colour
#

import kcs_draft
import KcsColour
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def GetColour():                                   # displays dialog for colour selection
   Colour = KcsColour.Colour()
   resp, Colour = kcs_ui.colour_select('Select new modal colour:', Colour)
   if resp == kcs_util.ok():
      return 1, Colour
   else:
      return 0, Colour

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['get current modal colour', 'select new modal colour']

   while(1):
      resp, index = kcs_ui.choice_select('Modal colour', 'Select operation', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # get current modal colour
            try:
               colour = KcsColour.Colour()
               kcs_draft.colour_get(colour)
               kcs_ui.message_noconfirm('Current colour: ' + str(colour))
            except:
               CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # set current modal colour
            try:
               resp, colour = GetColour()
               if resp:
                  kcs_draft.colour_set(colour)
            except:
               CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)
