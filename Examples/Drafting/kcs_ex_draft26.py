## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft26.py
#
#      PURPOSE:
#
#          This example shows how to handle layers, linetypes and colors
#

import sys
import kcs_ui
import kcs_util
import kcs_draft

import KcsColour
import KcsLinetype
import KcsLayer

import KcsElementHandle
import KcsModel
import KcsPoint2D
import KcsStringlist
import CommonSample

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints exception on console and output window
   print sys.exc_info()[1]
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def BuildActionsList():   # build actions list
   # build actions list
   actions = KcsStringlist.Stringlist('Show layer')
   actions.AddString('Hide layer')
   actions.AddString('Layers state')
   actions.AddString('Element layer get')
   actions.AddString('Element layer set')
   actions.AddString('Model layer set')
   actions.AddString('Element lintype get')
   actions.AddString('Element linetype set')
   actions.AddString('Element colour get')
   actions.AddString('Element colour set')
   return actions

#-------------------------------------------------------------------------------------------------------------
def SelectElement():
   actions = KcsStringlist.Stringlist('View')
   actions.AddString('Subview')
   actions.AddString('Component')
   actions.AddString('Geometry')

   handle = KcsElementHandle.ElementHandle()
   point = KcsPoint2D.Point2D()

   while 1:
      res = kcs_ui.choice_select('Element type', '', actions)
      if res[0]==kcs_util.ok():
         try:
            if res[1] == 1:         # select view
               pointres, point = kcs_ui.point2D_req('Select view, OC to exit', point)
               if pointres == kcs_util.ok():
                  handle = kcs_draft.view_identify(point)
                  return 1, handle
            elif res[1] == 2:
               pointres, point = kcs_ui.point2D_req('Select subview, OC to exit', point)
               if pointres == kcs_util.ok():
                  handle = kcs_draft.subview_identify(point)
                  return 1, handle
            elif res[1] == 3:
               pointres, point = kcs_ui.point2D_req('Select component, OC to exit', point)
               if pointres == kcs_util.ok():
                  handle = kcs_draft.component_identify(point)
                  return 1, handle
            elif res[1] == 4:
               pointres, point = kcs_ui.point2D_req('Select geometry, OC to exit', point)
               if pointres == kcs_util.ok():
                  handle = kcs_draft.geometry_identify(point)
                  return 1, handle
         except:
            PrintDraftError()
      else:
         break;
   return 0, handle

#-------------------------------------------------------------------------------------------------------------
def SelectGeometry():                                        # allows user to select element
   point = KcsPoint2D.Point2D()
   res, point = kcs_ui.point2D_req('Select geometry, OC to exit', point)
   if res==kcs_util.ok():
      hadle = KcsElementHandle.ElementHandle()
      try:
         handle = kcs_draft.geometry_identify(point)
         return 1, handle
      except:
         return 0, handle

#-------------------------------------------------------------------------------------------------------------
def SelectLinetype():                                       # allows user to select linetype
   try:
      linetypes = KcsLinetype.GetLinetypes().values()
      linetypes.sort()
      resp, index = kcs_ui.string_select('Line type', 'Line types:', 'Select line type:', linetypes)
      if resp == kcs_util.ok():
         return 1, KcsLinetype.Linetype(linetypes[index-1])
      else:
         return 0, KcsLinetype.Linetype()
   except:
      print sys.exc_info()[1]
      return 0, KcsLinetype.Linetype()

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

#-------------------------------------------------------------------------------------------------------------
def SelectLayer():
   actions = KcsStringlist.Stringlist('Layer: 100')
   actions.AddString('Layer: 101')
   actions.AddString('Layer: 102')
   actions.AddString('Layer: 103')
   actions.AddString('Layer: 104')
   actions.AddString('Layer: 105')
   actions.AddString('Layer: 106')
   actions.AddString('Layer: 107')
   actions.AddString('Layer: 108')
   actions.AddString('User defined')

   res = kcs_ui.choice_select('Select layer', '', actions)
   if res[0] == kcs_util.ok():
      if res[1] != 10:
         return 1, KcsLayer.Layer(100 + res[1] - 1)
      else:
         resp, id = kcs_ui.int_req('Layer id:', 0)
         if resp == kcs_util.ok():
            return 1, KcsLayer.Layer(id)

   return 0, KcsLayer.Layer(0)

#-------------------------------------------------------------------------------------------------------------
def LayersStateMenu():
    actions = [ 'Shown layers', 'Hidden layers', 'Reset layers state' ]

    res = kcs_ui.choice_select('Layers state', '', actions)
    if res[0]==kcs_util.ok():
       if res[1] == 1:         # layers shown
           if( kcs_draft.dwg_layers_is_shown() ):
               layers = kcs_draft.dwg_layers_shown_get()
               list = map( str, layers )
               list = map( lambda item: item.replace('\n', ''), list)
               kcs_ui.string_select('List of shown layers','','', list)
           else:
               kcs_ui.message_confirm('Shown layers filter not enabled')
       if res[1] == 2:         # layers hidden
           if( kcs_draft.dwg_layers_is_hidden() ):
               layers = kcs_draft.dwg_layers_hidden_get()
               list = map( str, layers )
               list = map( lambda item: item.replace('\n', ''), list)
               kcs_ui.string_select('List of shown layers','','', list)
           else:
               kcs_ui.message_confirm('Hidden layers filter not enabled')

       if res[1] == 3:         # show all layers
          kcs_draft.layer_show_all()


#-------------------------------------------------------------------------------------------------------------
try:           # main
   actions = BuildActionsList()
   while 1:
      res = kcs_ui.choice_select('Place volume', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # layer show
               try:
                  resp, layer = SelectLayer()
                  if resp:
                     kcs_draft.layer_show(layer)
               except:
                  PrintDraftError()

            elif res[1] == 2:       # layer hide
               try:
                  resp, layer = SelectLayer()
                  if resp:
                     kcs_draft.layer_hide(layer)
               except:
                  PrintDraftError()

            elif res[1] == 3:       # Show layers state
               try:
                  LayersStateMenu()
               except:
                  PrintDraftError()

            elif res[1] == 4:       # layer get
               resp, handle = SelectElement()
               if resp:
                  try:
                     layer = KcsLayer.Layer()
                     kcs_draft.element_layer_get(handle, layer)
                     kcs_ui.message_noconfirm('Element layer: '+str(layer))
                  except:
                     print sys.exc_info()[1]
                     PrintDraftError()

            elif res[1] == 5:       # layer set
               resp, handle = SelectElement()
               if resp:
                  try:
                     layer = KcsLayer.Layer()
                     resp, layerid = kcs_ui.int_req('Input layer ID:', 0)
                     if resp == kcs_util.ok():
                        layer.SetLayer(layerid)
                        print layer
                        kcs_draft.element_layer_set(handle, layer)
                  except:
                     PrintDraftError()

            elif res[1] == 6:       # model layer set
               (modres, modhandle) = SelectModel();
               if modres == 1:
                  try:
                     model = KcsModel.Model()
                     model = kcs_draft.model_properties_get(modhandle, model)
                     PresentModelInformation(model)

                     layer = KcsLayer.Layer()
                     resp, layerid = kcs_ui.int_req('Input layer ID:', 0)
                     if resp == kcs_util.ok():
                        layer.SetLayer(layerid)
                        model.ReflCode = 2

                        viewgiven, viewhandle = CommonSample.SelectView('Select model view, Esc for all model views')
                        if viewgiven:
                           kcs_draft.model_layer_set(model, layer, viewhandle)
                        else:
                           kcs_draft.model_layer_set(model, layer)
                  except:
                     PrintDraftError()

            elif res[1] == 7:       # linetype get
               resp, handle = SelectGeometry()
               if resp:
                  try:
                     linetype = KcsLinetype.Linetype()
                     kcs_draft.element_linetype_get(handle, linetype)
                     kcs_ui.message_noconfirm('Element linetype: '+str(linetype))
                  except:
                     print sys.exc_info()[1]
                     PrintDraftError()

            elif res[1] == 8:       # linetype set
               resp, handle = SelectElement()
               if resp:
                  try:
                     linetype = KcsLinetype.Linetype()
                     resp, linetype = SelectLinetype()
                     if resp:
                        kcs_draft.element_linetype_set(handle, linetype)
                  except:
                     PrintDraftError()

            elif res[1] == 9:       # colour get
               resp, handle = SelectGeometry()
               if resp:
                  try:
                     colour = KcsColour.Colour()
                     kcs_draft.element_colour_get(handle, colour)
                     kcs_ui.message_noconfirm('Element colour: '+str(colour))
                  except:
                     PrintDraftError()

            elif res[1] == 10:       # colour set
               resp, handle = SelectGeometry()
               if resp:
                  try:
                     colour = KcsColour.Colour()
                     resp, colour = kcs_ui.colour_select('Select colour', colour)
                     if resp == kcs_util.ok():
                        kcs_draft.element_colour_set(handle, colour)
                  except:
                     PrintDraftError()
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
   print kcs_draft.error;
