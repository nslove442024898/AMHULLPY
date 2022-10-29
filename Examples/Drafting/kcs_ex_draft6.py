## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft6.py
#
#      PURPOSE:
#
#          This program sets some modal symbol properties
#

import kcs_draft
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['set new symbol rotation', 'set new symbol height']

   while(1):
      resp, index = kcs_ui.choice_select('Modal symbol properties', 'Select property to change', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # set current modal symbol rotation
            rotation = 0.0
            try:
               rotation = kcs_draft.symbol_rotation_get()
            except:
               CommonSample.ReportTribonError(kcs_draft)
            resp, rotation = kcs_ui.real_req('Enter new value for modal symbol rotation:', rotation)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.symbol_rotation_set(rotation)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # set current modal symbol height
            height = 0.0
            try:
               height = kcs_draft.symbol_height_get()
            except:
               CommonSample.ReportTribonError(kcs_draft)
            resp, height = kcs_ui.real_req('Enter new value for modal symbol height:', height)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.symbol_height_set(height)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)

