## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          CommonSample.py
#
#      PURPOSE:
#
#          This file contains some usefull fuctions for Tribon python scripts examples
#
#          Implemented functions:
#              ReportTribonError(module, output)
#              SelectView(prompt)
#              SelectSubview(prompt)
#              SelectComponent(prompt)
#              SelectGeometry(prompt)
#              SubpictureInsert(name, parenthandle=None)
#              Point2DLockReq(prompt, point, status, buttons)

###############################################################################################
##       Warning:
##             This file can be used by different examples so don't import Tribon libraries
##             at the beginning of this module because of licence handling.
##             Every Tribon module should be imported by specific common function.
##             It doesn't relate to Tribon python classes.
###############################################################################################

from KcsElementHandle import ElementHandle
from KcsPoint2D       import Point2D
from KcsStringlist    import Stringlist
from KcsRline2D       import Rline2D
from KcsRectangle2D   import Infinity

#-------------------------------------------------------------------------------------------------------------
#                    name:          ReportTribonError(module, output)
#
#                    purpose:       used to report tribon module error
#
#                    arguments:     module      tribon module         tribon module from which error should be read
#                                   output      integer               selects display window for error message
#                                                                     0 - console and command window
#                                                                     1 - only console window
#                                                                     2 - only command window
#
#                    results:       None
#
#-------------------------------------------------------------------------------------------------------------
def ReportTribonError(module, output=0):
   try:
      import kcs_ui
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return

   try:
      if output == 1 or output == 0:
         print module.error
      if output == 2 or output == 0:
         kcs_ui.message_noconfirm('Error code: ' + module.error)
   except:
      print 'ReportTribonError function failed!'


#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectView(prompt)
#
#                    purpose:       used to interactive selection of view
#
#                    arguments:     prompt         string         prompt displayed during selection
#
#                    results:       tuple:   (rescode, viewhandle)
#                                         rescode: 0   - view not selected
#                                                  1   - view selected
#
#-------------------------------------------------------------------------------------------------------------
def SelectView(prompt):
   try:
      import kcs_draft
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return (0, ElementHandle())

   point = Point2D()

   resp = kcs_ui.point2D_req(prompt, point)           # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.view_identify(point)      # view
         return (1, handle)
      except:
         print kcs_draft.error

   return (0, ElementHandle())

#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectSubiew(prompt)
#
#                    purpose:       used to interactive selection of subview
#
#                    arguments:     prompt         string         prompt displayed during selection
#
#                    results:       tuple:   (rescode, handle)
#                                         rescode: 0  - subview not selected
#                                                  2  - subview selected
#
#-------------------------------------------------------------------------------------------------------------
def SelectSubview(prompt):
   try:
      import kcs_draft
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return (0, ElementHandle())

   point = Point2D()

   resp = kcs_ui.point2D_req(prompt, point)           # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.subview_identify(point)   # subview identify
         return (2, handle)
      except:
         print kcs_draft.error

   return (0, ElementHandle())

#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectComponent(prompt)
#
#                    purpose:       used to interactive selection of component
#
#                    arguments:     prompt         string         prompt displayed during selection
#
#                    results:       tuple:   (rescode, handle)
#                                         rescode: 0  - component not selected
#                                                  3  - component selected
#
#-------------------------------------------------------------------------------------------------------------
def SelectComponent(prompt):
   try:
      import kcs_draft
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return (0, ElementHandle())

   point = Point2D()

   resp = kcs_ui.point2D_req(prompt, point)              # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.component_identify(point)    # component identify
         return (3, handle)
      except:
         print kcs_draft.error

   return (0, ElementHandle())

#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectSubpicture(prompt, level=3)
#
#                    purpose:       used to interactive selection of subpicture
#                                   function will display user choice dialog box to select type of subpicture
#
#                    arguments:     prompt         string         prompt displayed during selection
#                                   level          integer        defines max level of wanted subpicture
#                                                                    1 - view
#                                                                    2 - view and subview
#                                                                    3 - view, subview and component
#
#                    results:       tuple:   (rescode, handle)
#                                         rescode: 0  - subpicture not selected
#                                                  1  - view selected
#                                                  2  - subview selected
#                                                  3  - component selected
#
#-------------------------------------------------------------------------------------------------------------
def SelectSubpicture(prompt, level=3):
   try:
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return (0, ElementHandle())

   actions = Stringlist('View')
   if level>1:
      actions.AddString('Subview')
   if level>2:
      actions.AddString('Component')

   res, action = kcs_ui.choice_select('Select', prompt, actions)
   if res == kcs_util.ok():
      if action == 1:
         return SelectView('Select view, OC to exit')
      elif action == 2:
         return SelectSubview('Select subview, OC to exit')
      elif action == 3:
         return SelectComponent('Select component, OC to exit')

   return (0, ElementHandle())

#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectGeometry(prompt)
#
#                    purpose:       used to interactive selection of geometry
#
#                    arguments:     prompt         string         prompt displayed during selection
#
#                    results:       tuple:   (rescode, handle)
#                                         rescode: 0  - geometry not selected
#                                         rescode: 1  - geometry selected
#
#-------------------------------------------------------------------------------------------------------------
def SelectGeometry(prompt):
   try:
      import kcs_draft
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return (0, ElementHandle())

   point = Point2D()

   resp = kcs_ui.point2D_req(prompt, point)               # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.geometry_identify(point)      # geometry
         return (1, handle)
      except:
         pass

   return (0, ElementHandle())

#-------------------------------------------------------------------------------------------------------------
#                    name:          SubpictureInsert(name, parenthandle=None)
#
#                    purpose:       used to insert subpicture under any parent
#
#                    arguments:     name         string         saved subpicture name
#
#                    results:       0 - if not success: kcs_draft.error should be check
#                                   1 - success
#
#-------------------------------------------------------------------------------------------------------------
def SubpictureInsert(name, parenthandle=None):
   try:
      import kcs_draft
      import kcs_ui
      import kcs_util
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return 0

   try:
      # check if given handle (if given) is a handle to subpicture
      if None != parenthandle:
         if not kcs_draft.element_is_subpicture(parenthandle):
            kcs_draft.error = 'kcs_HandleInvalid'
            return 0

      #################################################
      # suppose that saved subpicture is a view
      try:
         kcs_draft.subpicture_insert(name)
         return 1
      except:
         if kcs_draft.error != 'kcs_SubpictureNotValid':
            return 0

      #################################################
      # suppose that saved subpicture is a subview
      bViewCreated = 0

      # get view from given handle
      if parenthandle == None:
         bViewCreated = 1
         viewhandle = kcs_draft.view_new('')
      elif kcs_draft.element_is_view(parenthandle):
         viewhandle = parenthandle
      elif kcs_draft.element_is_subview(parenthandle):
         viewhandle = kcs_draft.element_parent_get(parenthandle)
      elif kcs_draft.element_is_component(parenthandle):
         viewhandle = kcs_draft.element_parent_get(kcs_draft.element_parent_get(parenthandle))
      else:
         kcs_draft.error = 'kcs_HandleInvalid'
         return 0

      # try to insert it under given view
      try:
         kcs_draft.subpicture_insert(name, viewhandle)
      except:
         if kcs_draft.error != 'kcs_SubpictureNotValid':
            return 0

      #################################################
      # suppose that saved subpicture is a component
      bSubviewCreated = 0

      # get subview from given handle
      if parenthandle == None:
         kcs_draft.subpicture_current_set(viewhandle)
         subviewhandle = kcs_draft.subview_new()
         bSubviewCreated = 1
      elif kcs_draft.element_is_view(parenthandle):
         kcs_draft.subpicture_current_set(parenthandle)
         subviewhandle = kcs_draft.subview_new()
      elif kcs_draft.element_is_subview(parenthandle):
         subviewhandle = parenthandle
      elif kcs_draft.element_is_component(parenthandle):
         subviewhandle = kcs_draft.element_parent_get(parenthandle)
      else:
         kcs_draft.error = 'kcs_HandleInvalid'
         return 0

      # try to insert it under given subview
      kcs_draft.subpicture_insert(name, subviewhandle)
   except:
      if bViewCreated:
         kcs_draft.element_delete(viewhandle)
      if bSubviewCreated:
         kcs_draft.element_delete(subviewhandle)
      return 0

   return 1

#-------------------------------------------------------------------------------------------------------------
#                    name:          Point2DLockReq(prompt, point, status, buttons)
#
#                    purpose:       used as a wrapper function for point2D_req
#                                   it takes care about locking stuff:
#                                      - draws locking help lines during selection and
#                                      - adjust result point considering locking mode.
#
#                    arguments:     same as kcs_draft.point2_req but status and buttons are required
#
#                    results:       same as kcs_draft.point2D_req
#
#-------------------------------------------------------------------------------------------------------------
def Point2DLockReq(prompt, point, status, buttons):
   try:
      import kcs_draft
      import kcs_util
      import kcs_ui
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return 0, point

   # handle to highlighted help line
   nHighlightHnd = None
   try:
      while(1):
         # if there is highligthed help line turn it off
         if nHighlightHnd!=None:
            kcs_draft.highlight_off(nHighlightHnd)
            nHighlightHnd = None

         # draw help locking lines
         if buttons.IsLockEnabled():
            # get help point
            hlppoint = status.GetHelpPoint()
            if hlppoint == None:
               print 'Warning: Help point not defined for locking lines!'
               hlppoint = Point2D(0, 0)
            if buttons.GetCheckedLock()=='U':
               nHighlightHnd = kcs_draft.line_highlight(Rline2D(Point2D(-Infinity, hlppoint.Y), Point2D(Infinity, hlppoint.Y)))
            if buttons.GetCheckedLock()=='V':
               nHighlightHnd = kcs_draft.line_highlight(Rline2D(Point2D(hlppoint.X, -Infinity), Point2D(hlppoint.X, Infinity)))

         # select point
         resp, point = kcs_ui.point2D_req(prompt, point, status, buttons)

         # if lock button pressed update buttons state
         if resp == kcs_util.v_lock():
            if buttons.GetCheckedLock() == 'V':
               buttons.SetCheckedLock(None)
            else:
               buttons.SetCheckedLock('V')
         elif resp == kcs_util.u_lock():
            if buttons.GetCheckedLock() == 'U':
               buttons.SetCheckedLock(None)
            else:
               buttons.SetCheckedLock('U')
         elif resp == kcs_util.unlock():
            buttons.SetCheckedLock(None)
         else:
            # turn off highlights
            if nHighlightHnd != None:
               kcs_draft.highlight_off(nHighlightHnd)
               nHighlightHnd = None
            # correct result point if lock enabled
            if buttons.IsLockEnabled():
               if buttons.GetCheckedLock() == 'U':
                  point.Y = hlppoint.Y
               elif buttons.GetCheckedLock() == 'V':
                  point.X = hlppoint.X
            # return results
            return resp, point
   except:
      if nHighlightHnd!=None:
         kcs_draft.highlight_off(nHighlightHnd)
      return kcs_util.cancel(), point

#-------------------------------------------------------------------------------------------------------------
#                    name:          SelectModel()
#
#                    purpose:       Function returns Model indicated on drawing
#
#                    arguments:     Types   - List of strings representing allowed model types or None if any model
#                                   Message - Message string
#
#                    results:       KcsModel.Model class if success
#                                   None if operation aborted or model not found
#
#-------------------------------------------------------------------------------------------------------------

def SelectModel(Types = None, Message="Indicate model"):
   try:
      import kcs_ui
      import kcs_util
      import kcs_draft
      import KcsModel
   except:
      print 'Tribon library not found! Probably no licence for that library.'
      return

   pt        = Point2D()
   ModelInfo = KcsModel.Model()

   try:
      resp = kcs_util.ok()
      while resp == kcs_util.ok():

         resp, pt = kcs_ui.point2D_req(Message, pt)

         if resp == kcs_util.ok():
            try:
               kcs_draft.model_identify(pt, ModelInfo)

               if Types != None:
                  if ModelInfo.Type in Types:
                     return ModelInfo
               else:
                  return ModelInfo
            except:
               print kcs_draft.error

   except:
      print kcs_ui.error
