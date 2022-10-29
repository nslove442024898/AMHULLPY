## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft1.py
#
#      PURPOSE:
#
#          This example shows how to use drawing functions
#

import CommonSample
import kcs_draft                        # to get access to the draft functions
import kcs_ui
import kcs_util
import kcs_db
from KcsObjectCriteria import ObjectCriteria

#-------------------------------------------------------------------------------------------------------------
def GetName(prompt):         # promts user to key in name
   resp, resstr = kcs_ui.string_req(prompt, '')
   if resp == kcs_util.ok():
      return 1, resstr
   else:
      return 0, ''

#-------------------------------------------------------------------------------------------------------------
def GetDwgType():
   try:
      dict = kcs_draft.dwg_type_list_get()
      names = map(lambda x : x[0], dict.values())
      dbs   = map(lambda x : x[1], dict.values())
      types = dict.keys()

      resp, index = kcs_ui.string_select('Drawing type', 'Select drawing type', '', names)
      if resp == kcs_util.ok():
         return 1, types[index-1], dbs[index-1]
      else:
         return 0, 0, ''
   except Exception, e:
      print e
      return 0, 0, ''

#-------------------------------------------------------------------------------------------------------------
def GetDrawingName(dbname):
   try:
      list = []
      kcs_db.object_list_get(ObjectCriteria(), dbname, list)
      if len(list)==0:
         kcs_ui.message_confirm('There are no drawings in %s!' % dbname)
         return 0, ''
      else:
         list = map(lambda x : x.GetName(), list)
         resp, index = kcs_ui.string_select('Objects in %s' % dbname, 'Select drawing', '', list)
         if resp == kcs_util.ok():
            return 1, list[index-1]
         else:
            return 0, ''
   except Exception, e:
      print e
      print kcs_db.error
      return 0, ''

#-------------------------------------------------------------------------------------------------------------
def GetOpenMode():
   actions = ['ReadOnly', 'ReadWrite']
   resp, index = kcs_ui.choice_select('Open mode', 'Choose open mode', actions)
   if resp == kcs_util.ok():
      if index==1:
         return 1, kcs_draft.kcsOPENMODE_READONLY
      else:
         return 1, kcs_draft.kcsOPENMODE_READWRITE
   return 0, kcs_draft.kcsOPENMODE_READONLY

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['dwg_new', 'dwg_open', 'dwg_close', 'dwg_save', 'dwg_save_as', 'dwg_exist', 'dwg_delete']

   while 1:
      resp, index = kcs_ui.choice_select('Drawing operations', 'Choose operation', actions)
      if resp == kcs_util.ok():
         if index == 1:                                                 # create new drawing
            resp, name = GetName('Enter new drawing name:')
            if resp:
               resp, form = GetName('Enter drawing form name:')
               resp, dwgtype, dbname = GetDwgType()
               if resp:
                  try:
                     kcs_draft.dwg_new(name, form, dwgtype)
                  except:
                     CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                               # open existing drawing
            resp, dwgtype, dbname = GetDwgType()
            if resp:
               resp, name = GetDrawingName(dbname)
               if resp:
                  resp, mode = GetOpenMode()
                  if resp:
                     resp, revision = GetName('Enter revision name (only TDM):')
                     try:
                        kcs_draft.dwg_open(name, dwgtype, mode, revision)
                     except:
                        CommonSample.ReportTribonError(kcs_draft)
         elif index == 3:                                               # close current drawing
            try:
               kcs_draft.dwg_close()
            except:
               CommonSample.ReportTribonError(kcs_draft)
         elif index == 4:                                               # save current drawing
            try:
               kcs_draft.dwg_save()
            except:
               CommonSample.ReportTribonError(kcs_draft)
         elif index == 5:                                               # save as
            resp, name = GetName('Enter drawing name to save as:')
            if resp:
               resp, dwgtype, dbname = GetDwgType()
               if resp:
                  try:
                     kcs_draft.dwg_save_as(name, dwgtype)
                  except:
                     CommonSample.ReportTribonError(kcs_draft)
         elif index == 6:                                               # check if drawing exists
            resp, dwgtype, dbname = GetDwgType()
            if resp:
               resp, name = GetName('Enter drawing name to check:')
               if resp:
                  try:
                     if kcs_draft.dwg_exist(name, dwgtype):
                        kcs_ui.message_noconfirm('Drawing exists!')
                     else:
                        kcs_ui.message_noconfirm("Drawing doesn't exist!")
                  except:
                     CommonSample.ReportTribonError(kcs_draft)
         elif index == 7:                                               # delete drawing from drawing databank
            resp, dwgtype, dbname = GetDwgType()
            if resp:
               resp, name = GetDrawingName(dbname)
               if resp:
                  try:
                     kcs_draft.dwg_delete(name, dwgtype)
                  except:
                     CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
  CommonSample.ReportTribonError(kcs_draft)
