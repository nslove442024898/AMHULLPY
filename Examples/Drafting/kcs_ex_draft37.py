## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft37.py
#
#      PURPOSE:
#
#          This example shows how to use subpicture save and insert functions
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

import KcsElementHandle
import KcsStringlist
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def SubpictureSave():
   try:
      res, handle = CommonSample.SelectSubpicture('Select subpicture to save, OC to exit')
      if res:
         kcs_draft.subpicture_save(handle, 1)
   except:
      CommonSample.ReportTribonError(kcs_draft)

#-------------------------------------------------------------------------------------------------------------
def SubpictureInsert(db=kcs_draft.kcsSBD_PICT):
   try:
      resp, name = kcs_ui.string_req('Subpicture name:', '')
      if resp == kcs_util.ok():
         res, handle = CommonSample.SelectSubpicture('Select parent subpicture, OC if no parent', 2)
         if res:
            kcs_draft.subpicture_insert(name, handle,db)
         else:
            kcs_draft.subpicture_insert(name,db)
   except:
      CommonSample.ReportTribonError(kcs_draft)

#-------------------------------------------------------------------------------------------------------------
def SubpictureInsertEx():
   try:
      resp, name = kcs_ui.string_req('Subpicture name:', '')
      if resp == kcs_util.ok():
         res, handle = CommonSample.SelectSubpicture('Select parent subpicture, OC if no parent', 3)
         if res:
            if not CommonSample.SubpictureInsert(name, handle):
               CommonSample.ReportTribonError(kcs_draft)
         else:
            if not CommonSample.SubpictureInsert(name, None):
               CommonSample.ReportTribonError(kcs_draft)
   except:
      CommonSample.ReportTribonError(kcs_draft)

#-------------------------------------------------------------------------------------------------------------
try:           # main
   # build actions list
   actions = KcsStringlist.Stringlist('Save')
   actions.AddString('Insert')
   actions.AddString('Insert + add subpictures')

   while 1:
      res = kcs_ui.choice_select('Subpicture', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # subpicture save
               SubpictureSave()
            elif res[1] == 2:       # subpicture insert
               SubpictureInsert()
            elif res[1] == 3:
               SubpictureInsertEx() # create parent subpicture if needed and insert saved subpicture
            elif res[1] == 4:       # subpicture insert in SBD_STD
               SubpictureInsert(kcs_draft.kcsSBD_STD)
         else:
            break;
      except:
         print sys.exc_info()[1]
         CommonSample.ReportTribonError(kcs_ui)

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
   print kcs_draft.error;

