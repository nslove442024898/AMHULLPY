## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft18.py
#
#      PURPOSE:
#
#          This program shows how to use functions handling default values
#

import kcs_draft
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['default_value_get', 'default_value_set']

   while(1):
      resp, index = kcs_ui.choice_select('Setting default values', 'Select function', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # set modal text height
            resp, valuename = kcs_ui.string_req('Enter value name: ', 'TEXT_FONT')
            if resp == kcs_util.ok():
               try:
                  value = kcs_draft.default_value_get(valuename)
                  kcs_ui.message_noconfirm(value)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # set text slant
            resp, value = kcs_ui.string_req('Enter default value name and its value: ', 'TEXT_FONT = 7')
            if resp == kcs_util.ok():
               try:
                  kcs_draft.default_value_set(value)
                  kcs_ui.message_noconfirm('Value set: ' + value)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)
