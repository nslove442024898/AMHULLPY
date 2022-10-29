## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft30.py
#
#      PURPOSE:
#
#          This example shows how to navigate throw elements, create new subview and component, and set them current.
#

import kcs_ui
import kcs_util
import kcs_draft
import KcsStringlist
import KcsPoint2D
import KcsElementHandle
import KcsRectangle2D

elementname = { 'view':1, 'subview':2, 'component':3, 'element':4 }
maxsize = 1000

#-------------------------------------------------------------------------------------------------------------
def ShowChildren():                                      # allows user to iterate throw children of selected subpicture
   actions = KcsStringlist.Stringlist('Next')

   handle = KcsElementHandle.ElementHandle()

   # select parent subpicture
   (res, parent) = SelectSubpictureFromTree()
   if res:
      # find first child item
      try:
         handle = kcs_draft.element_child_first_get(parent)
         kcs_draft.element_highlight(handle)             # highlight founded element
      except:
         kcs_draft.highlight_off(0)                      # highlight off all highlighted elements
         PrintDraftError();
         return;

      # iterate
      result = 1
      while result:
         res = kcs_ui.choice_select('Action', '', actions)
         if res[0]==kcs_util.ok():
            if res[1] == 1:                              # set selected subpicture as current
               try:
                  kcs_draft.highlight_off(0)
                  handle = kcs_draft.element_sibling_next_get(handle)
                  kcs_draft.element_highlight(handle)
               except:
                  kcs_draft.highlight_off(0)             # highlight off all highlighted elements
                  if kcs_draft.error != 'kcs_NotFound':
                     PrintDraftError();
                  return;
         else:
            result = 0;

      kcs_draft.highlight_off(0)

#-------------------------------------------------------------------------------------------------------------
def PrintSubpictureExtents():
   (res, handle) = SelectSubpictureFromTree()
   if res:
      try:
         rect = kcs_draft.element_extent_get(handle)
         kcs_ui.message_noconfirm('Element extent:' + str(rect))
      except:
         PrintDraftError()

#-------------------------------------------------------------------------------------------------------------
def SelectEntity():                                            # function for selecting subpicture
   actions = KcsStringlist.Stringlist('Select Subpicture')
   actions.AddString('Select Geometry')
   res = kcs_ui.choice_select('Selection', '', actions)
   if res[0]==kcs_util.ok():
      if res[1] == 1:                                          # select subpicture
         return SelectSubpictureFromTree()
      else:
         point = KcsPoint2D.Point2D()
         prompt = 'Indicate geometry, OC to exit'
         try:
            resp = kcs_ui.point2D_req(prompt, point)           # request user for point
            if resp[0] == kcs_util.ok():
               try:
                  handle = kcs_draft.geometry_identify(point)  # geometry
                  return (1, handle)
               except:
                  return (0, KcsElementHandle.ElementHandle())
         except:
            PrintDraftError();
            return (0, KcsElementHandle.ElementHandle())

   return (0, KcsElementHandle.ElementHandle())


#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error


#-------------------------------------------------------------------------------------------------------------
def GetCurrentSubpicture():                                       # returns current subpicture path
   result = []
   handles = []
   try:
      handles = kcs_draft.subpicture_current_get()
   except:
      print sys.exc_info()[1]
   return handles

#-------------------------------------------------------------------------------------------------------------
def GetElementType(handle):                                       # returns element type
   try:
      if kcs_draft.element_is_contour(handle):
         return 'Contour '
      if kcs_draft.element_is_text(handle):
         return 'Text '
      if kcs_draft.element_is_symbol(handle):
         return 'Symbol '
      if kcs_draft.element_is_subpicture(handle):                 # checks subpictures subtypes
         if kcs_draft.element_is_view(handle):
            return 'View '
         if kcs_draft.element_is_subview(handle):
            if kcs_draft.element_is_burning_sketch(handle):
               return 'Burning sketch subview '
            elif kcs_draft.element_is_detail_sketch(handle):
               return 'Detail sketch subview '
            elif kcs_draft.element_is_nesting(handle):
               return 'Nesting subview '
            else:
               return 'Subview '
         if kcs_draft.element_is_component(handle):               # checks component subtypes
            if kcs_draft.element_is_note(handle):
               return 'Component: Note '
            if kcs_draft.element_is_posno(handle):
               return 'Component: Position number '
            if kcs_draft.element_is_dimension(handle):
               return 'Component: Dimension '
            if kcs_draft.element_is_hatch(handle):
               return 'Component: Hatch '
            return 'Component '
   except:
      return 'Unknown'
   return 'Unknown'

#-------------------------------------------------------------------------------------------------------------
def GetElements(componenthandle, tree):
   contours = 0
   symbols = 0
   texts = 0
   others = 0
   space = '              '
   try:
      elementhandle = kcs_draft.element_child_first_get(componenthandle)
      nIndex = 1
      while nIndex:
         try:
            if kcs_draft.element_is_contour(elementhandle):
               contours = contours + 1
            elif kcs_draft.element_is_text(elementhandle):
               texts = texts + 1
            elif kcs_draft.element_is_symbol(elementhandle):
               symbols = symbols + 1
            else
               others = others + 1

            elementhandle = kcs_draft.element_sibling_next_get(elementhandle)
            if len(tree)>maxsize:
               nIndex = 0
         except:
            nIndex = 0
   except:
      print 'component has no elements'

   text = 'Contours:%i  Symbols:%i     Texts:%i   Others:%i' % (contours, symbols, texts, others)
   eleminfo = [space+text, KcsElementHandle.ElementHandle(), elementname['element']]
   tree.append(eleminfo)

#-------------------------------------------------------------------------------------------------------------
def GetComponents(subviewhandle, tree):                           # creates list of all components within given subview
   componenthandle = KcsElementHandle.ElementHandle()
   try:
      componenthandle = kcs_draft.element_child_first_get(subviewhandle)   # get first component item
      nIndex = 1
      while nIndex:
         try:
            # get component name
            name = kcs_draft.subpicture_name_get(componenthandle)
            # and create information about component
            if len(name)>0:
               name = '           name: '+name
            compinfo = ['       '+GetElementType(componenthandle)+str(nIndex)\
                        +': ('+str(componenthandle)+')' + name,
                        componenthandle,
                        elementname['component']]  # create info
            # add component information to info table
            tree.append(compinfo)
            # add geometries information to info table
            eleminfo = []
            GetElements(componenthandle, eleminfo)
            for item in eleminfo:
               tree.append(item)

            nIndex = nIndex+1

            componenthandle = kcs_draft.element_sibling_next_get(componenthandle)   # get next sibling item
            if len(tree)>maxsize:
               nIndex = 0
         except:
            nIndex = 0
   except:
      print 'exception: ', kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def GetSubviews(viewhandle, tree):                                # creates list of all subviews within given view
   subviewhandle = 0
   try:
      subviewhandle = kcs_draft.element_child_first_get(viewhandle)        # get first subview item
      nIndex = 1
      while nIndex:
         try:
            name = kcs_draft.subpicture_name_get(subviewhandle)
            if len(name)>0:
               name = '           name: '+name
            subviewinfo = ['   '+GetElementType(subviewhandle)+str(nIndex)+': ('+str(subviewhandle)+')'+name,
                           subviewhandle,
                           elementname['subview']]      # create info
            tree.append(subviewinfo)
            GetComponents(subviewhandle, tree)
            nIndex = nIndex+1
            subviewhandle = kcs_draft.element_sibling_next_get(subviewhandle)       # get next sibling item
            if len(tree)>maxsize:
               nIndex = 0
         except:
            nIndex = 0
   except:
      print 'exception: ', kcs_draft.error


#-------------------------------------------------------------------------------------------------------------
def GetDrawingInfo():
   dwgname = ''
   formname = 'NoForm'
   try:
      dwgname  = kcs_draft.dwg_name_get()
      formname = kcs_draft.form_name_get()
   except:
      PrintDraftError()

   return '---------- subpicture tree      for drawing:  ' + dwgname + '      with form:  ' + formname + ' ----------'

#-------------------------------------------------------------------------------------------------------------
def SelectSubpictureFromTree():           # creates list of all subpictures, marks current and allows user to select subpicture
   viewhandle = 0
   tree = []

   try:
      viewhandle = kcs_draft.element_child_first_get()   # get first view

      nIndex = 1
      while nIndex:
         try:
            name = kcs_draft.subpicture_name_get(viewhandle)
            if len(name)>0:
               name = '           name: '+name
            viewinfo = [GetElementType(viewhandle)+str(nIndex)+': ('+str(viewhandle)+')' + name,
                        viewhandle,
                        elementname['view']]   # create info
            tree.append(viewinfo)
            GetSubviews(viewhandle, tree)       # step into
            nIndex = nIndex+1
            viewhandle = kcs_draft.element_sibling_next_get(viewhandle) # get next sibling view
            if len(tree)>maxsize:
               nIndex = 0
         except:
            nIndex = 0
   except:
      print 'exception: ', kcs_draft.error

   # create Stringlist
   properties = KcsStringlist.Stringlist(GetDrawingInfo())

   # get current path
   current = GetCurrentSubpicture()

   if len(tree)==0:
      properties.AddString('no views defined')
   else:
      nItemIndex = 0
      for item in tree:
         nItemIndex = nItemIndex + 1
         if nItemIndex>1000:    # too much elements to display
            break;
         if item[1] in current:
            properties.AddString(item[0] + ' - CURRENT')
         else:
            properties.AddString(item[0])

   # select subpicture
   (result, selection) = kcs_ui.string_select('Subpicture tree', '', '', properties)
   if result == kcs_util.ok() and selection>1 and len(tree)>0:
      if tree[selection-2][2] == elementname['element']:
         return (0, KcsElementHandle.ElementHandle())
      else:
         return (1, (tree[selection-2])[1])
   else:
      return (0, KcsElementHandle.ElementHandle())


#-------------------------------------------------------------------------------------------------------------
try:           # main

   # build actions list
   actions = KcsStringlist.Stringlist('Select current subpicture')
   actions.AddString('Set automatic')
   actions.AddString('Create new view')
   actions.AddString('Create new subview')
   actions.AddString('Create new component')
   actions.AddString('Change subpicture name')
   actions.AddString('Find parent')
   actions.AddString('Show children')
   actions.AddString('Get subpicture extents')
   actions.AddString('Show subpictures')

   result = 1
   while result:
      res = kcs_ui.choice_select('Subpictures', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                    # set selected subpicture as current
            (valid, handle) = SelectSubpictureFromTree()
            if valid:
               try:
                  kcs_draft.subpicture_current_set(handle)
               except:
                  PrintDraftError()
         elif res[1] == 2:                                  # set automatic mode
               try:
                  kcs_draft.subpicture_current_set()
               except:
                  PrintDraftError()
         elif res[1] == 3:                                  # create new view
            name = ''
            (set, name) = kcs_ui.string_req('view name', '')
            try:
               handle = kcs_draft.view_new(name)
               kcs_ui.message_noconfirm('Created view with handle: ' + str(handle))
            except:
               PrintDraftError()
         elif res[1] == 4:                                  # create new subview
            name = ''
            (set, name) = kcs_ui.string_req('subview name', '')
            try:
               handle = kcs_draft.subview_new(name)
               kcs_ui.message_noconfirm('Created subview with handle: ' + str(handle))
            except:
               PrintDraftError()
         elif res[1] == 5:                                  # create new component
            handle = 0
            name = ''
            (set, name) = kcs_ui.string_req('component name', '')
            try:
               handle = kcs_draft.component_new(name)
               kcs_ui.message_noconfirm('Created component with handle: ' + str(handle))
            except:
               PrintDraftError()
         elif res[1] == 6:                                  # change subpicture name
            (valid, handle) = SelectSubpictureFromTree()
            if valid:
               try:
                  name = kcs_draft.subpicture_name_get(handle)
                  (set, name) = kcs_ui.string_req('subpicture name', name)
                  kcs_draft.subpicture_name_set(handle, name)
               except:
                  PrintDraftError()
         elif res[1] == 7:                                  # find parent
            (valid, handle) = SelectEntity()
            if valid:
               try:
                  parent = kcs_draft.element_parent_get(handle)
                  kcs_ui.message_noconfirm('Parent handle for element '+str(handle)+' is: ' + str(parent));
               except:
                  PrintDraftError()
         elif res[1] == 8:                                  # iterates throw all children
            ShowChildren()
         elif res[1] == 9:                                  # get subpicture extents
            PrintSubpictureExtents()
         elif res[1] == 10:                                 # list all subpictures
            SelectSubpictureFromTree()
      else:
         result = 0

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print 'exception: ', kcs_draft.error

