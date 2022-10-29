## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft31.py
#
#      PURPOSE:
#
#          This example shows how to use transformation function
#

import sys
import math
import copy
import kcs_ui
import kcs_util
import kcs_draft
import KcsStringlist
import KcsPoint2D
import KcsVector2D
import KcsTransformation2D
import KcsRectangle2D
import KcsElementHandle

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def BuildOptionsList(selected, handle):                           # build options list
   item = ''
   visible = 0
   if selected:
      item = 'Element: ' + GetElementType(handle)+' ('+str(handle)+')'
      try:
         visible = kcs_draft.element_visibility_get(handle)
      except:
         pass
   else:
      item = 'Element: NotSelected'
      visible = 'Element not selected'

   list = KcsStringlist.Stringlist(item)

   try:
      list.AddString('Visible: ' + str(visible))
      list.AddString('Autoscale View')
      list.AddString('Reset Transformation')
      list.AddString('Rotate')
      list.AddString('Move')
      list.AddString('Reflect')
      list.AddString('Scale')
      list.AddString('Transform')
      list.AddString('Redefine transformation')
      list.AddString('Use Toolbar')
   except:
      print KcsStringlist.error

   return list;

#-------------------------------------------------------------------------------------------------------------
def MakeElementCopy():                  # element selection
   try:
      actions = KcsStringlist.Stringlist('View')
      actions.AddString('Subview')
      actions.AddString('Component')
      actions.AddString('Geometry')
   except:
      print KcsStringlist.error

   try:
      while 1:
         res = kcs_ui.choice_select('Select element to copy', '', actions)
         if res[0] == kcs_util.ok():
            point = KcsPoint2D.Point2D(0, 0)
            prompt = 'Indicate element, OC to exit'
            pointres = kcs_ui.point2D_req(prompt, point)                 # request user for point
            if pointres[0] == kcs_util.ok():
               try:
                  if res[1] == 1:
                     handle = kcs_draft.view_identify(point)
                  elif res[1] == 2:
                     handle = kcs_draft.subview_identify(point)
                  elif res[1] == 3:
                     handle = kcs_draft.component_identify(point)
                  else:
                     handle = kcs_draft.geometry_identify(point)
               except:
                  PrintDraftError()
                  return (0, KcsElementHandle.ElementHandle())

               # select owner only for subview, component or geometry
               noowner = 1
               if res[1]>1:
                  prompt = 'Indicate owner, OC to exit'
                  pointres = kcs_ui.point2D_req(prompt, point)
                  if pointres[0] == kcs_util.ok():
                     try:
                        if res[1] == 2:
                           owner = kcs_draft.view_identify(point)
                        elif res[1] == 3:
                           owner = kcs_draft.subview_identify(point)
                        else:
                           owner = kcs_draft.component_identify(point)
                        noowner = 0
                     except:
                        PrintDraftError()

               # create copy of element
               try:
                  if noowner:
                     handle = kcs_draft.element_copy(handle)
                  else:
                     handle = kcs_draft.element_copy(handle, owner)
                  return (1, handle)
               except:
                  PrintDraftError()
            break;
         else:
            break;
   except:
      print PrintDraftError()

   return (0, KcsElementHandle.ElementHandle())

#-------------------------------------------------------------------------------------------------------------
def SelectElement(entselected, handle):                  # element selection
   try:
      actions = KcsStringlist.Stringlist('View')
      actions.AddString('Subview')
      actions.AddString('Component')
      actions.AddString('Geometry')
      actions.AddString('Copy element')
   except:
      print KcsStringlist.error

   result = 1
   while result:
      res = kcs_ui.choice_select('Select element', '', actions)
      if res[0] == kcs_util.ok():
         if res[1]<5:
            point = KcsPoint2D.Point2D(0, 0)
            prompt = 'Indicate element, OC to exit'
            pointres = kcs_ui.point2D_req(prompt, point)                 # request user for point
            if pointres[0] == kcs_util.ok():
               try:
                  if res[1] == 1:
                     handle = kcs_draft.view_identify(point)            # view
                  elif res[1] == 2:
                     handle = kcs_draft.subview_identify(point)         # subview
                  elif res[1] == 3:
                     handle = kcs_draft.component_identify(point)       # component
                  else:
                     handle = kcs_draft.geometry_identify(point)        # geometry
                  return (1, handle)
               except:
                  print 'identification failed'
         else:
            return MakeElementCopy()
      else:
         result = 0
   return (entselected, handle)

#-------------------------------------------------------------------------------------------------------------
def GetElementType(handle):                                       # returns element type
   try:
      if kcs_draft.element_is_contour(handle):
         return 'Contour'
      if kcs_draft.element_is_text(handle):
         return 'Text'
      if kcs_draft.element_is_symbol(handle):
         return 'Symbol'
      if kcs_draft.element_is_subpicture(handle):                 # checks subpictures subtypes
         if kcs_draft.element_is_view(handle):
            return 'View'
         if kcs_draft.element_is_subview(handle):
            return 'Subview'
         if kcs_draft.element_is_component(handle):               # checks component subtypes
            if kcs_draft.element_is_note(handle):
               return 'Note'
            if kcs_draft.element_is_posno(handle):
               return 'Pos number'
            if kcs_draft.element_is_dimension(handle):
               return 'Dimension'
            if kcs_draft.element_is_hatch(handle):
               return 'Hatch'
            return 'Component'
   except:
      return 'Unknown'
   return 'Unknown'

#-------------------------------------------------------------------------------------------------------------
def SelectRotation():                                          # gets rotation data
   agle = 0.0
   point = KcsPoint2D.Point2D(0, 0)
   prompt = 'Select center of rotation, OC to exit'

   pointres = kcs_ui.point2D_req(prompt, point)                 # request user for center of rotation
   if pointres[0] != kcs_util.ok():
      return (0, point, 0.0)

   (set, angle) = kcs_ui.real_req('Angle (degrees)', 0.0)
   if not set:
      return (0, point, 0.0)

   return (1, point, angle)

#-------------------------------------------------------------------------------------------------------------
def SelectVector2D():                                                # gets vector 2D from two points indicated by user
   vector = KcsVector2D.Vector2D()
   start = KcsPoint2D.Point2D(0, 0)
   end   = KcsPoint2D.Point2D(0, 0)

   prompt = 'Select start point of vector , OC to exit'
   pointres = kcs_ui.point2D_req(prompt, start)                      # request user for start point of vector
   if pointres[0] == kcs_util.ok():
      prompt = 'Select end point of vector , OC to exit'
      pointres = kcs_ui.point2D_req(prompt, end)                     # request user for end point of vector
      if pointres[0] == kcs_util.ok():
         vector.X = end.X - start.X
         vector.Y = end.Y - start.Y
         return (1, vector)
   return (0, vector)

#-------------------------------------------------------------------------------------------------------------
def SelectReflectionLine():                                          # reflection line
   start = KcsPoint2D.Point2D(0, 0)
   end   = KcsPoint2D.Point2D(0, 0)

   prompt = 'Select start point of reflection line, OC to exit'
   pointres = kcs_ui.point2D_req(prompt, start)                      # request user for start point of vector
   if pointres[0] == kcs_util.ok():
      prompt = 'Select end point of reflection line, OC to exit'
      pointres = kcs_ui.point2D_req(prompt, end)                     # request user for end point of vector
      if pointres[0] == kcs_util.ok():
         return (1, start, end)
   return (0, start, end)

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
            if extHeight!=0.0 and restWidth/restHeight > extWidth/extHeight:
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
      PrintDraftError();

#-------------------------------------------------------------------------------------------------------------
def ChangeVisibility(handle):             # this function changes visibility of element given by handle
   try:
      visibility = kcs_draft.element_visibility_get(handle)
      if visibility:
         visibility = 0
      else:
         visibility = 1
      kcs_draft.element_visibility_set(handle, visibility)
   except:
      PrintDraftError()

#-------------------------------------------------------------------------------------------------------------
try:           # main
   entselected = 0
   handle = KcsElementHandle.ElementHandle()
   transf = KcsTransformation2D.Transformation2D()                # init transformation class

   # build actions list
   actions = KcsStringlist.Stringlist('')
   actions = BuildOptionsList(entselected, handle)

   result = 1
   while result:
      res = kcs_ui.choice_select('Transformation', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                          # select entity
            (entselected, handle) = SelectElement(entselected, handle)
            actions = BuildOptionsList(entselected, handle)
         elif res[1] == 2:                                        # element visibility
            ChangeVisibility(handle)
            actions = BuildOptionsList(entselected, handle)
         elif res[1] == 3:                                        # autoscale view
            AutoScaleView(handle)
         elif res[1] == 4:                                        # set identity matrix
            transf.IdentityTransf()
         elif res[1] == 5:                                        # rotate
            point = KcsPoint2D.Point2D(0, 0)
            (set, point, angle) = SelectRotation()
            if set:
               transf.Rotate(point, (math.pi/180) * angle)
         elif res[1] == 6:                                        # translate
            vector = KcsVector2D.Vector2D(0, 0)
            (set, vector) = SelectVector2D()
            if set:
               transf.Translate(vector)
         elif res[1] == 7:                                        # reflect
            start = KcsPoint2D.Point2D(0, 0)
            end   = KcsPoint2D.Point2D(0, 0)
            (set, start, end) = SelectReflectionLine()
            if set:
               vector = KcsVector2D.Vector2D(end.X - start.X, end.Y - start.Y)
               transf.Reflect(start, vector)
         elif res[1] == 8:                                        # scale
            (set, scale) = kcs_ui.real_req('Scale factor:', 1.0)
            if set:
               transf.Scale(scale)
         elif res[1] == 9:                                        # make transformation
            if entselected:
               try:
                  kcs_draft.element_transform(handle, transf)
                  kcs_draft.dwg_repaint()
               except:
                  PrintDraftError();
         elif res[1] == 10:                                        # redefine transformation
            if entselected:
               try:
                  kcs_draft.element_transformation_redefine(handle, transf)
                  kcs_draft.dwg_repaint()
               except:
                  PrintDraftError();
         elif res[1] == 11:                                        # Use transformation toolbar
            if entselected:
               try:
                  kcs_draft.element_transform(handle)
                  kcs_draft.dwg_repaint()
               except:
                  PrintDraftError();

      else:
         result = 0

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
