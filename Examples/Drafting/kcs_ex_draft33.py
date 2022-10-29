## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft33.py
#
#      PURPOSE:
#
#          This example shows how to use part functions
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

import KcsStringlist
import KcsPoint2D
import KcsElementHandle
import KcsModel
import KcsRectangle2D
import KcsVector2D
import KcsModelDrawAssyCriteria

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def DefineModel():                                                # allows user to define model
   model = KcsModel.Model()
   try:
      res, model.Type = kcs_ui.string_req("Input model type:", model.Type)
      if res == kcs_util.ok():
         res, model.Name = kcs_ui.string_req("Input model name:", model.Name)
         if res == kcs_util.ok():
            res, model.PartId = kcs_ui.int_req("Input part id:", model.PartId)
            if res == kcs_util.ok():
               return (1, model)
   except:
      print sys.exc_info()[1]
      print kcs_ui.error

   return (0, model)

#-------------------------------------------------------------------------------------------------------------
def SelectModel():                                                # select model
   actions = KcsStringlist.Stringlist('Select subview')
   actions.AddString('Select component')
   actions.AddString('Select geometry')

   point = KcsPoint2D.Point2D()

   try:
      while 1:
         res = kcs_ui.choice_select('select model', '', actions)
         if res[0]==kcs_util.ok():
            if res[1] == 1:                                          # select views and subviews
               prompt = 'Indicate subview, OC to exit'
               resp = kcs_ui.point2D_req(prompt, point)    # request user for point
               if resp[0] == kcs_util.ok():
                  try:
                     handle = kcs_draft.subview_identify(point)      # subview
                     kcs_ui.message_noconfirm('indicated subview: ' + str(handle))
                     return (1, handle)
                  except:
                     kcs_ui.message_noconfirm('view not found')
            if res[1] == 2:
               prompt = 'Indicate component, OC to exit'
               resp = kcs_ui.point2D_req(prompt, point)    # request user for point
               if resp[0] == kcs_util.ok():
                  try:
                     handle = kcs_draft.component_identify(point)      # component
                     kcs_ui.message_noconfirm('indicated component: ' + str(handle))
                     return (1, handle)
                  except:
                     kcs_ui.message_noconfirm('component not found')
            if res[1] == 3:
               prompt = 'Indicate geometry, OC to exit'
               resp = kcs_ui.point2D_req(prompt, point)    # request user for point
               if resp[0] == kcs_util.ok():
                  try:
                     handle = kcs_draft.geometry_identify(point)      # geometry
                     kcs_ui.message_noconfirm('indicated geometry: ' + str(handle))
                     return (1, handle)
                  except:
                     kcs_ui.message_noconfirm('geometry not found')
         else:
            break
   except:
      print kcs_ui.error

   return (0, KcsElementHandle.ElementHandle())

#-------------------------------------------------------------------------------------------------------------
def PresentModelInformation(model):
   try:
      properties = KcsStringlist.Stringlist('----------------- Model Properties -----------------------')
      properties.AddString('')
      properties.AddString('Model Name: ' + model.Name)
      properties.AddString('Model Type: ' + model.Type)
      properties.AddString('----------------------------------------------------------');
      properties.AddString('Part Type: ' + model.PartType)
      properties.AddString('Part ID: ' + str(model.PartId))
      properties.AddString('----------------------------------------------------------');
      properties.AddString('SubPart Type: ' + model.SubPartType)
      properties.AddString('SubPart ID: ' + str(model.SubPartId))
      properties.AddString('----------------------------------------------------------');
      properties.AddString('Reflection Code: ' + str(model.ReflCode))
   except:
      print sys.exc_info()[1]
      print KcsStringlist.error

   try:
      kcs_ui.string_select('Model properties', '', '', properties)
   except:
      print sys.exc_info()[1]
      print kcs_ui.error

   return

#-------------------------------------------------------------------------------------------------------------
def CreateAssemblyCriteria(criteria):
   while 1:
      # build actions list
      actions = KcsStringlist.Stringlist('Assembly name: ' + criteria.GetAssemblyName())

      if criteria.IsRecursive():
         actions.AddString('Mode: Recursive')
      else:
         actions.AddString('Mode: Parts')

      answer = ''
      if criteria.IsModelTypeEnabled('PlanePanel'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('PlanePanel: ' + answer)

      if criteria.IsModelTypeEnabled('CurvedPanel'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('CurvedPanel: ' + answer)

      if criteria.IsModelTypeEnabled('Pipe'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('Pipe: ' + answer)

      if criteria.IsModelTypeEnabled('Equipment'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('Equipment: ' + answer)

      if criteria.IsModelTypeEnabled('Cableway'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('Cableway: ' + answer)

      if criteria.IsModelTypeEnabled('Structure'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('Structure: ' + answer)

      if criteria.IsModelTypeEnabled('PlacedVolume'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('PlacedVolume: ' + answer)

      if criteria.IsModelTypeEnabled('Ventilation'):
         answer = 'Yes'
      else:
         answer = 'No'
      actions.AddString('Ventilation: ' + answer)

      res = kcs_ui.choice_select('Assembly model types', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:
            resp, name = kcs_ui.string_req('Assembly name:', criteria.GetAssemblyName())
            if resp:
               criteria.SetAssemblyName(name)
         if res[1] == 2:
            if criteria.IsRecursive():
               criteria.SetRecursive(0)
            else:
               criteria.SetRecursive(1)
         if res[1] == 3:
            if criteria.IsModelTypeEnabled('PlanePanel'):
               criteria.EnableModelType('PlanePanel', 0)
            else:
               criteria.EnableModelType('PlanePanel', 1)
         elif res[1] == 4:
            if criteria.IsModelTypeEnabled('CurvedPanel'):
               criteria.EnableModelType('CurvedPanel', 0)
            else:
               criteria.EnableModelType('CurvedPanel', 1)
         elif res[1] == 5:
            if criteria.IsModelTypeEnabled('Pipe'):
               criteria.EnableModelType('Pipe', 0)
            else:
               criteria.EnableModelType('Pipe', 1)
         elif res[1] == 6:
            if criteria.IsModelTypeEnabled('Equipment'):
               criteria.EnableModelType('Equipment', 0)
            else:
               criteria.EnableModelType('Equipment', 1)
         elif res[1] == 7:
            if criteria.IsModelTypeEnabled('Cableway'):
               criteria.EnableModelType('Cableway', 0)
            else:
               criteria.EnableModelType('Cableway', 1)
         elif res[1] == 8:
            if criteria.IsModelTypeEnabled('Structure'):
               criteria.EnableModelType('Structure', 0)
            else:
               criteria.EnableModelType('Structure', 1)
         elif res[1] == 9:
            if criteria.IsModelTypeEnabled('PlacedVolume'):
               criteria.EnableModelType('PlacedVolume', 0)
            else:
               criteria.EnableModelType('PlacedVolume', 1)
         elif res[1] == 10:
            if criteria.IsModelTypeEnabled('Ventilation'):
               criteria.EnableModelType('Ventilation', 0)
            else:
               criteria.EnableModelType('Ventilation', 1)
      else:
         break


#-------------------------------------------------------------------------------------------------------------
def SelectView():
   point = KcsPoint2D.Point2D()

   prompt = 'Indicate view, OC to exit'
   resp = kcs_ui.point2D_req(prompt, point)    # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.view_identify(point)      # view
         kcs_ui.message_noconfirm('indicated view: ' + str(handle))
         return (1, handle)
      except:
         kcs_ui.message_noconfirm('view not found')

   return (0, KcsElementHandle.ElementHandle())

#-------------------------------------------------------------------------------------------------------------
def AutoScaleView(handle):             # this function makes autscale for selected view
                                       # it will not effect transformation matrix!
   RestRect = KcsRectangle2D.Rectangle2D()
   ExtRect  = KcsRectangle2D.Rectangle2D()

   try:
      if kcs_draft.element_is_view(handle):
         RestRect    = kcs_draft.view_restriction_area_get(handle)
         ExtRect     = kcs_draft.element_extent_get(handle)
         if not ExtRect.IsEmpty():
            restWidth   = abs(RestRect.Corner1.X - RestRect.Corner2.X)
            restHeight  = abs(RestRect.Corner1.Y - RestRect.Corner2.Y)
            extWidth    = abs(ExtRect.Corner1.X - ExtRect.Corner2.X)
            extHeight   = abs(ExtRect.Corner1.Y - ExtRect.Corner2.Y)

            # scale view
            scale = 1.0
            if restWidth/restHeight > extWidth/extHeight:
               scale = restHeight/extHeight  # scale based on heights
            else:
               scale = restWidth/extWidth    # scale based on widths
            kcs_draft.view_scale(handle, scale)

            # move view
            ExtRect     = kcs_draft.element_extent_get(handle)

            ExtCenter   = KcsPoint2D.Point2D((ExtRect.Corner1.X + ExtRect.Corner2.X)/2, (ExtRect.Corner1.Y + ExtRect.Corner2.Y)/2)
            RestCenter  = KcsPoint2D.Point2D((RestRect.Corner1.X + RestRect.Corner2.X)/2, (RestRect.Corner1.Y + RestRect.Corner2.Y)/2)

            vector = KcsVector2D.Vector2D()
            vector.SetFromPoints(ExtCenter, RestCenter)
            kcs_draft.view_move(handle, vector)
         else:
            kcs_ui.message_noconfirm('Selected view is empty!')
      else:
         kcs_ui.message_noconfirm('Selected element is not a view!')
   except:
      print sys.exc_info()[1]

#-------------------------------------------------------------------------------------------------------------

try:           # main
   # build actions list
   actions = KcsStringlist.Stringlist('Show model properties')
   actions.AddString('Draw model')
   actions.AddString('Draw assembly model')

   model = KcsModel.Model()
   assembly = KcsModelDrawAssyCriteria.ModelDrawAssyCriteria()

   while 1:
      res = kcs_ui.choice_select('Part functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # show model properties
               while 1:
                  (modres, modhandle) = SelectModel();
                  if modres == 1:
                     try:
                        model = kcs_draft.model_properties_get(modhandle, model)
                        PresentModelInformation(model)
                     except:
                        print sys.exc_info()[1]
                        PrintDraftError()
                  else:
                     break;
            if res[1] == 2:
               try:
                  modres, model = DefineModel()
                  if modres == 1:
                     vres, vhandle = SelectView()
                     if vres==1:
                        kcs_draft.model_draw(model, vhandle)
                        AutoScaleView(vhandle)
                     else:
                        kcs_draft.model_draw(model)
               except:
                  print sys.exc_info()[1]
                  PrintDraftError()
            if res[1] == 3:
               try:
                  CreateAssemblyCriteria(assembly)
                  vres, vhandle = SelectView()
                  if vres==1:
                     kcs_draft.model_draw(assembly, vhandle)
                     AutoScaleView(vhandle)
                  else:
                     kcs_draft.model_draw(assembly)
                  kcs_ui.message_noconfirm('Assembly inserted ok!')
               except:
                  print sys.exc_info()[1]
                  PrintDraftError()
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]


