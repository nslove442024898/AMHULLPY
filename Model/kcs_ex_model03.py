## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_model03.py
#
#      PURPOSE:
#
#          This example shows how to use model_status_set.
#

import kcs_model
import kcs_draft
import kcs_ui
import kcs_util

import KcsModel
import KcsPoint2D
import CommonSample

StatusTypeNames = { kcs_model.kcsSTATTYPE_DESIGN : 'DESIGN',
                    kcs_model.kcsSTATTYPE_MANUFACTURING : 'MANUFACTURING',
                    kcs_model.kcsSTATTYPE_ASSEMBLY : 'ASSEMBLY',
                    kcs_model.kcsSTATTYPE_MATERIAL_CONTROL: 'MATERIAL CONTROL' }


#-------------------------------------------------------------------------------------------------------------
def SelectModel():
   try:
      model = KcsModel.Model()
      resp, point = kcs_ui.point2D_req('Select model', KcsPoint2D.Point2D())
      if resp == kcs_util.ok():
         model, subview, comp = kcs_draft.model_identify(point, model)
         return 1, model
   except Exception, e:
      print e
      CommonSample.ReportTribonError(kcs_draft)
   return 0, None

#-------------------------------------------------------------------------------------------------------------
def SelectStatusType():
   try:
      keys = StatusTypeNames.keys()
      values = StatusTypeNames.values()
      resp, index = kcs_ui.choice_select('Status type', 'Select status type', values)
      if resp == kcs_util.ok():
         return keys[index-1]
   except:
      pass
   return None

#-------------------------------------------------------------------------------------------------------------
def SelectStatusValue(type):
   try:
      dict = kcs_model.status_values_get(type)

      resp, index = kcs_ui.string_select('Status value', '', 'Select status value', dict.values())
      if resp == kcs_util.ok():
         return dict.keys()[index-1]
   except:
      pass
   return None

#-------------------------------------------------------------------------------------------------------------
DRAWING = 1
MODEL = 2

def SelectObjectType():
   resp, index = kcs_ui.choice_select('Object type', 'Select object type', ['Drawing', 'Model'])
   if resp == kcs_util.ok():
      if index == 1:
         return DRAWING
      else:
         return MODEL
   else:
      return 0

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
try:
   while 1:
      objtype = SelectObjectType()
      if objtype:
         while 1:
            type = SelectStatusType()
            if type != None:
               value = SelectStatusValue(type)
               if value != None:
                  # if MODEL select model object in current drawing
                  if objtype == MODEL:
                     resp, model = SelectModel()
                  else:
                     resp = 1

                  # change status
                  if resp:
                     try:
                        if objtype == MODEL:
                           kcs_model.model_status_set(model, type, value)
                        else:
                           kcs_draft.dwg_status_set(type, value)
                     except:
                        if objtype == MODEL:
                           CommonSample.ReportTribonError(kcs_model)
                        else:
                           CommonSample.ReportTribonError(kcs_draft)
                        break;
                  else:
                     break
            else:
               break
      else:
         break;
except Exception, e:
   print e
