## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft4.py
#
#      PURPOSE:
#
#          This program allows to set the modal position number symbol and
#          the position number height
#

import kcs_draft
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['posno_symbol_set', 'posno_height_get', 'posno_height_set']

   while(1):
      resp, index = kcs_ui.choice_select('Position number functions', 'Select operation', actions)

      if resp == kcs_util.ok():
         if index == 1:                                     # set modal position number symbol
            resp, symbol = kcs_ui.int_req('Position number symbol:', 63)
            if resp:
               try:
                  kcs_draft.posno_symbol_set(symbol)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # get current height of position number symbol
            try:
               height = kcs_draft.posno_height_get()
               kcs_ui.message_noconfirm('Height of position number: ' + str(height))
            except:
               CommonSample.ReportTribonError(kcs_draft)
         elif index == 3:                                   # set current height of position number symbol
            try:
               resp, height = kcs_ui.real_req('Enter position number symbol height:', 1.0)
               if resp == kcs_util.ok():
                  kcs_draft.posno_height_set(height)
            except:
               CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)
