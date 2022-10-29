## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft38.py
#
#      PURPOSE:
#
#          This example shows how to use drawing revision functions
#

import CommonSample
import kcs_draft                        # to get access to the draft functions
import kcs_ui
import kcs_util

#-------------------------------------------------------------------------------------------------------------
def FreezeRevision():
   try:
      kcs_draft.dwg_revision_freeze()
      kcs_ui.message_confirm('Revision frozen')
   except:
      CommonSample.ReportTribonError(kcs_draft)

#-------------------------------------------------------------------------------------------------------------
def UnFreezeRevision():
   try:
      kcs_draft.dwg_revision_unfreeze()
      kcs_ui.message_confirm('Revision unfrozen')
   except:
      CommonSample.ReportTribonError(kcs_draft)

#-------------------------------------------------------------------------------------------------------------
def AddRevision():
   try:
      resp, revname = kcs_ui.string_req('Enter revision name:', '')
      if resp == kcs_util.ok():
         resp, revremark = kcs_ui.string_req('Enter revision remark:', '')
         kcs_draft.dwg_revision_new(revname, revremark)
   except Exception, e:
      print e
      print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['freeze revision', 'unfreeze revision', 'add new revision']

   while 1:
      resp, index = kcs_ui.choice_select('Revision operations', 'Choose operation', actions)
      if resp == kcs_util.ok():
         if index == 1:                                                 # freeze revision
            FreezeRevision()
         elif index == 2:                                               # unfreeze revision
            UnFreezeRevision()
         elif index == 3:                                               # add revision
            AddRevision()
      else:
         break;
except:
  CommonSample.ReportTribonError(kcs_ui)
