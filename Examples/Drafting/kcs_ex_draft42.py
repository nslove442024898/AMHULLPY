## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft42.py
#
#      PURPOSE:
#
#          This example shows how to use model object revision functions
#
import sys
import CommonSample
import KcsModelObjectRevision
import KcsPoint2D
import KcsModel
import kcs_draft
import kcs_ui
import kcs_util
import KcsElementHandle


#-------------------------------------------------------------------------------------------------------------
def GetName(prompt):         # promts user to key in name
   resp, resstr = kcs_ui.string_req(prompt, '')
   if resp == kcs_util.ok():
      return 1, resstr
   else:
      return 0, ''

#-------------------------------------------------------------------------------------------------------------
def GetModelAndView():
   view_handle = KcsElementHandle.ElementHandle()
   model = KcsModel.Model()
   point = KcsPoint2D.Point2D()

   try:
      resp, point = kcs_ui.point2D_req('Select model', point)
      if resp == kcs_util.ok():
         model_ident = kcs_draft.model_identify(point, model)
         view_handle = kcs_draft.view_identify(point)
         return (1, model, view_handle)
   except:
      print sys.exc_info()[1]
      print kcs_ui.error
   return (0, model, view_handle)

#-------------------------------------------------------------------------------------------------------------
def DisplayList(model, view_handle, title, header, prompt):
   list = []
   kcs_draft.model_object_revision_get(model, view_handle, list)
   if len(list) == 0:
      kcs_ui.message_confirm('No revisions...')

   strlist = []
   revNamelist = []
   for item in list:
      strlist.append(item.getRevisionName() + '; ' + item.getRevisionRemark() + '; ' + item.getCreatedBy() + '; ' + item.getCreatedDate() )
      revNamelist.append(item.getRevisionName())

   status, index = kcs_ui.string_select(title, header, prompt, strlist)
   if status == kcs_util.ok():
      return 1, revNamelist[index-1]
   else:
      return 0, ''


#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['List revisions', 'List and exchange revision', 'Save revision']

   model = KcsModel.Model()
   view_handle = KcsElementHandle.ElementHandle()
   revision = KcsModelObjectRevision.ModelObjectRevision()

   while 1:
      resp, index = kcs_ui.choice_select('Revision functions', 'Choose function', actions)
      if resp == kcs_util.ok():
         res, model, view_handle = GetModelAndView()
         if res == 1:
            if index == 1:
               DisplayList(model, view_handle, 'List revisions', '', '')
            elif index == 2:
               res, revisionName = DisplayList(model, view_handle, 'List and exchange revision', '','')
               if res == 1:
                  revision.setRevisionName(revisionName)
                  kcs_draft.model_object_revision_set(model, revision, view_handle)
            elif index == 3:
               revisionName = 'Defname'
               revisionRemark = 'DefRemark'
               saveSpools = kcs_util.no()
               res, revisionName = kcs_ui.string_req('Revision name', revisionName)
               if res == kcs_util.ok():
                  res, revisionRemark = kcs_ui.string_req('Revision remark', revisionRemark)
                  if res == kcs_util.ok():
                     revision.setRevisionName(revisionName)
                     revision.setRevisionRemark(revisionRemark)
                     modelType = model.GetType()
                     if model.GetType() == 'pipe':
                        saveSpools = kcs_ui.answer_req('Question','Do you want to create revisions for spools?')
                  if saveSpools == kcs_util.yes():
                     kcs_draft.model_object_revision_save(model, revision, view_handle, 1)
                  else:
                     kcs_draft.model_object_revision_save(model, revision, view_handle, 0)
      else:
         break;
except:
   kcs_ui.message_confirm('Except')
   CommonSample.ReportTribonError(kcs_draft)
