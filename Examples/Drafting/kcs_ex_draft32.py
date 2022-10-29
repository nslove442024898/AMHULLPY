## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft32.py
#
#      PURPOSE:
#
#          This example shows how to exchange drawing between other formats
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

import KcsStringlist
import KcsPoint2D
import KcsElementHandle

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def SelectModels():
   subpictures = []
   point = KcsPoint2D.Point2D()
   level = 3

   actions = KcsStringlist.Stringlist('Select view')
   actions.AddString('Select subview')
   actions.AddString('Exit')

   while 1:
      if level == 1:
         levelstr = 'Low'
      elif level == 2:
         levelstr = 'Medium'
      elif level == 3:
         levelstr = 'High'
      elif level == 4:
         levelstr = 'Extra'
      else:
         levelstr = 'High'
         level = 3

      res = kcs_ui.choice_select('3d face dxf export', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                          # select views and subviews
            prompt = 'Indicate view, OC to exit'
            resp = kcs_ui.point2D_req(prompt, point)    # request user for point
            if resp[0] == kcs_util.ok():
               try:
                  handle = kcs_draft.view_identify(point)      # view
                  subpictures = subpictures + [handle]
                  kcs_ui.message_noconfirm('indicated view: ' + str(handle))
               except:
                  kcs_ui.message_noconfirm('view not found')
         if res[1] == 2:
            prompt = 'Indicate subview, OC to exit'
            resp = kcs_ui.point2D_req(prompt, point)    # request user for point
            if resp[0] == kcs_util.ok():
               try:
                  handle = kcs_draft.subview_identify(point)      # subview
                  subpictures = subpictures + [handle]
                  kcs_ui.message_noconfirm('indicated subview: ' + str(handle))
               except:
                  kcs_ui.message_noconfirm('subview not found')
         if res[1] == 3:
            return subpictures
      else:
         break

   return []

#-------------------------------------------------------------------------------------------------------------
def Export3dFaceDxf():
   strFile = ''
   subpictures = []
   level = 3

   while 1:
      if level == 1:
         levelstr = 'Low'
      elif level == 2:
         levelstr = 'Medium'
      elif level == 3:
         levelstr = 'High'
      elif level == 4:
         levelstr = 'Extra'
      else:
         levelstr = 'High'
         level = 3

      actions = KcsStringlist.Stringlist('Selected views/subviews:' + str(len(subpictures)))
      actions.AddString('Detail level: ' + levelstr)
      actions.AddString('Export')

      res = kcs_ui.choice_select('Import/Export', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                          # select views and subviews
            subpictures = SelectModels()
         if res[1] == 2:
            level = level + 1;
            if level == 5:
               level = 1
         if res[1] == 3:
            strres, strFile = kcs_ui.string_req('File name:', strFile)
            if strres == kcs_util.ok():
               kcs_ui.message_noconfirm('exporting ...')
               kcs_draft.dwg_dxf_3d_export(strFile, subpictures, level)
               kcs_ui.message_noconfirm('export succeed!')
               break
      else:
         break


#-------------------------------------------------------------------------------------------------------------
try:           # main
   strFile = ''

   # build actions list
   actions = KcsStringlist.Stringlist('Export to dxf')
   actions.AddString('Export to dxf facet')
   actions.AddString('Import from dxf')

   while 1:
      res = kcs_ui.choice_select('Import/Export', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:                                          # export to dxf
               strres, strFile = kcs_ui.string_req('File name:', strFile)
               if strres == kcs_util.ok():
                  kcs_ui.message_noconfirm('exporting ...')
                  kcs_draft.dwg_dxf_export(strFile)
                  kcs_ui.message_noconfirm('export succeed!')
            elif res[1] == 2:                                        # export to dxf (face)
               Export3dFaceDxf()
            elif res[1] == 3:                                        # import from dxf file
               strres, strFile = kcs_ui.string_req('File name:', strFile)
               if strres == kcs_util.ok():
                  strDwgName = ''
                  strres, strDwgName = kcs_ui.string_req('Drawing name:', strDwgName)
                  if strres == kcs_util.ok():
                     kcs_ui.message_noconfirm('importing ...')
                     kcs_draft.dwg_dxf_import(strFile, strDwgName)
                     kcs_ui.message_noconfirm('import succeed!')
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]


