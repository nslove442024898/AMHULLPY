## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft3.py
#
#      PURPOSE:
#
#          This program allows user to set the modal hatch pattern.
#

import kcs_draft
import kcs_ui
import kcs_util
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def GetPageAndDetail():                               # get page and detail from user
   resp, page = kcs_ui.int_req('Enter page:', 1)
   if resp == kcs_util.ok():
      resp, detail = kcs_ui.int_req('Enter detail:', 1)
      if resp == kcs_util.ok():
         return 1, page, detail
   return 0, 0, 0

#-------------------------------------------------------------------------------------------------------------
def GetAngleAndDistance():                            # get angle and distance from user
   resp, angle = kcs_ui.real_req('Enter angle:', 0.0)
   if resp == kcs_util.ok():
      resp, distance = kcs_ui.real_req('Enter detail:', 1.0)
      if resp == kcs_util.ok():
         return 1, angle, distance
   return 0, 0, 0

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['userdef_hatch_pattern_set', 'hatch_pattern_set', 'std_hatch_pattern_set']

   while 1:
      resp, index = kcs_ui.choice_select('Model hatch pattern', 'Select hatch pattern set function', actions)
      if resp == kcs_util.ok():
         if index == 1:
            resp, page, detail = GetPageAndDetail()
            if resp:
               try:
                  kcs_draft.userdef_hatch_pattern_set(page, detail)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:
            resp, angle, distance = GetAngleAndDistance()
            if resp:
               try:
                  kcs_draft.hatch_pattern_set(angle, distance)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
         elif index == 3:
            resp, pattern = kcs_ui.int_req('Enter hatch pattern ID:', 1)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.std_hatch_pattern_set(pattern)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break

except:
   CommonSample.ReportTribonError(kcs_ui)
