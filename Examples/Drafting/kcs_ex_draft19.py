## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft19.py
#
#      PURPOSE:
#
#          This program allows user to draw a model and change its colour
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsModel
import KcsColour
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   actions = ['Draw model', 'Change model colour']

   while(1):
      resp, index = kcs_ui.choice_select('Changing model colour', 'Select function', actions)
      if resp == kcs_util.ok():
         if index == 1:                                     # draw model
            resp, modeltype = kcs_ui.string_req('Enter model type: ', '')
            if resp == kcs_util.ok():
               resp, modelname = kcs_ui.string_req('Enter model name: ', '')
               if resp == kcs_util.ok():
                  model = KcsModel.Model( modeltype, modelname)
                  try:
                     kcs_draft.model_draw(model)
                  except:
                     CommonSample.ReportTribonError(kcs_draft)
         elif index == 2:                                   # change model colour
            point = KcsPoint2D.Point2D()
            resp, point = kcs_ui.point2D_req('Select model', point)
            if resp == kcs_util.ok():
               try:
                  model = KcsModel.Model()
                  model_ident = kcs_draft.model_identify(point, model)
                  view_handle = kcs_draft.view_identify(point)
                  colour = KcsColour.Colour()
                  resp, colour = kcs_ui.colour_select('Select new model colour', colour)
                  kcs_draft.model_colour_set(model_ident[0], colour, view_handle)
               except:
                  CommonSample.ReportTribonError(kcs_draft)
      else:
         break;
except:
   CommonSample.ReportTribonError(kcs_ui)
