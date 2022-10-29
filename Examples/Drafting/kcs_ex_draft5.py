## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft5.py
#
#      PURPOSE:
#
#          This program sets some modal text properties
#

import kcs_draft
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['text_height_set', 'text_slant_set', 'text_aspect_set']

   while(1):
      resp, index = kcs_ui.choice_select('Modal text properties', 'Select function', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # set modal text height
            resp, height = kcs_ui.real_req('Enter modal text height: ', 14.0)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.text_height_set(height)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # set text slant
            resp, slant = kcs_ui.real_req('Enter modal text slant: ', 45.0)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.text_slant_set(slant)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 3:                                   # set text aspect ratio
            resp, aspect = kcs_ui.real_req('Enter modal text aspect: ', 2.0)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.text_aspect_set(aspect)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)
