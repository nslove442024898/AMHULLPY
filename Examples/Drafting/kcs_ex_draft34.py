## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft34.py
#
#      PURPOSE:
#
#          This example shows how to use view functions
#

import sys
import kcs_ui
import kcs_util
import kcs_draft
import copy

import KcsStringlist
import KcsPoint2D
from   KcsPoint3D import Point3D
import KcsElementHandle
import KcsTransformation3D
import KcsTransformation2D
import KcsBox
import KcsText
import KcsVector3D
import KcsModel

import CommonSample

viewhandle = KcsElementHandle.ElementHandle()
projection = KcsTransformation3D.Transformation3D()

#-------------------------------------------------------------------------------------------------------------
def PrintDraftError():                                            # prints draft exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_draft.error)
   print kcs_draft.error

#-------------------------------------------------------------------------------------------------------------
def SelectElement():
   # build actions list
   actions = KcsStringlist.Stringlist('Select view')
   actions.AddString('Select geometry')

   res = kcs_ui.choice_select('Element type', '', actions)
   try:
      if res[0]==kcs_util.ok():
         if res[1] == 1:                     # select view
            return CommonSample.SelectView('Select view, OC to exit')
         elif res[1] == 2:
            return CommonSample.SelectGeometry('Select geometry, OC to exit')
   except:
      print sys.exc_info()[1]
      PrintDraftError()

   return (0, KcsElementHandle.ElementHandle())

#-------------------------------------------------------------------------------------------------------------
def PresentProjection(proj):
   try:
      type = 0
      matrix = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
      proj.GetByRow(type, matrix)

      properties = KcsStringlist.Stringlist('----------------- View Projection -----------------------')
      properties.AddString('')
      properties.AddString(str(matrix[0]))
      properties.AddString(str(matrix[1]))
      properties.AddString(str(matrix[2]))
      properties.AddString(str(matrix[3]))
      properties.AddString('')
      properties.AddString('Transformation Type: ' + str(type))
   except:
      print sys.exc_info()[1]
      print KcsStringlist.error

   try:
      kcs_ui.string_select('View Projection', '', '', properties)
   except:
      print sys.exc_info()[1]
      print kcs_ui.error

   return

#-------------------------------------------------------------------------------------------------------------
def PresentTransformation(transf):
   try:
      type = 0
      matrix = [ [0,0,0], [0,0,0], [0,0,0] ]
      transf.GetByRow(type, matrix)

      properties = KcsStringlist.Stringlist('----------------- Element transformation -----------------------')
      properties.AddString('')
      properties.AddString(str(matrix[0]))
      properties.AddString(str(matrix[1]))
      properties.AddString(str(matrix[2]))
      properties.AddString('')
      properties.AddString('Transformation Type: ' + str(type))
      properties.AddString('')
      properties.AddString('decompose:')
      properties.AddString('scale: '+ str(transf.GetScale()))
      properties.AddString('XY shear: ' + str(transf.GetXYShear()))
      properties.AddString('XY translation: ' + str(transf.GetTranslation()))
      properties.AddString('rotation: ' + str(transf.GetRotation()))
      properties.AddString('reflection: ' + str(transf.GetReflection()))
   except:
      print sys.exc_info()[1]
      print KcsStringlist.error

   try:
      kcs_ui.string_select('View Projection', '', '', properties)
   except:
      print sys.exc_info()[1]
      print kcs_ui.error

   return

#-------------------------------------------------------------------------------------------------------------
def SelectPoint(prompt, point):
   x = point.X;
   y = point.Y;
   z = point.Z;

   try:
      res, x = kcs_ui.real_req(prompt + ' X:', x)
      if res==kcs_util.ok():
         res, y = kcs_ui.real_req(prompt + ' Y:', y)
         if res==kcs_util.ok():
            res, z = kcs_ui.real_req(prompt + ' Z:', z)
            if res == kcs_util.ok():
               point.X = x
               point.Y = y
               point.Z = z
               return 1
   except:
      return 0

   return 0

#-------------------------------------------------------------------------------------------------------------
def GetVector3D(prompt):
   vec = KcsVector3D.Vector3D()
   vec.SetComponents(0, 0, 0)

   resp, vec.X = kcs_ui.real_req(prompt + ' X:', vec.X)
   if resp == kcs_util.ok():
      resp, vec.Y = kcs_ui.real_req(prompt + ' Y:', vec.Y)
      if resp == kcs_util.ok():
         resp, vec.Z = kcs_ui.real_req(prompt + ' Z:', vec.Z)
         if resp == kcs_util.ok():
            return 1, vec

   return 0, vec

#-------------------------------------------------------------------------------------------------------------
def GetDrawCode():
   actions = KcsStringlist.Stringlist('Draw code 0')
   actions.AddString('Draw code 1')
   actions.AddString('Default')

   res = kcs_ui.choice_select('Draw code', '', actions)
   if res[0]==kcs_util.ok():
      return 1, res[1]-1
   else:
      return 0, 0

#-------------------------------------------------------------------------------------------------------------
def GetProjectionVectors():
   uVector = KcsVector3D.Vector3D()
   vVector = KcsVector3D.Vector3D()

   actions = KcsStringlist.Stringlist('Plane ZY')
   actions.AddString('Plane ZX')
   actions.AddString('Plane XY')
   actions.AddString('User defined vectors')

   res = kcs_ui.choice_select('Define projection', '', actions)
   try:
      if res[0]==kcs_util.ok():
         if res[1] == 1:         # get view projection
            uVector.SetComponents(0, 0, 1)
            vVector.SetComponents(0, 1, 0)
         elif res[1] == 2:
            uVector.SetComponents(0, 0, 1)
            vVector.SetComponents(1, 0, 0)
         elif res[1] == 3:
            uVector.SetComponents(1, 0, 0)
            vVector.SetComponents(0, 1, 0)
         elif res[1] == 4:
            resp, uVector = GetVector3D('uVector')
            if resp:
               resp, vVector = GetVector3D('vVector')
               if not resp:
                  return (0, uVector, vVector)
            else:
               return (0, uVector, vVector)
         return (1, uVector, vVector)
   except:
      return (0, uVector, vVector)

#-------------------------------------------------------------------------------------------------------------
def CreateSymbolicView():
   point = Point3D(52500, 0, 0)
   uVector = KcsVector3D.Vector3D(0, 1, 0)
   vVector = KcsVector3D.Vector3D(0, 0, 1)
   name = ''
   forward = backward = 100.0

   box = KcsBox.Box(Point3D(), uVector, vVector, 80000.0, 80000.0, 80000.0)
   box.SetAxisParallelBox(Point3D(-500000, -500000, -500000), Point3D(500000, 500000, 500000))

   while 1:
      actions = KcsStringlist.Stringlist('View name: ' + name)
      actions.AddString('Location: '+ str(point.X) + ' ' + str(point.Y) + ' ' + str(point.Z));
      actions.AddString('U Vector: '+ str(uVector.X) + ' ' + str(uVector.Y) + ' ' + str(uVector.Z));
      actions.AddString('V Vector: '+ str(vVector.X) + ' ' + str(vVector.Y) + ' ' + str(vVector.Z));
      actions.AddString('Forward dist: ' + str(forward))
      actions.AddString('Backward dist: ' + str(backward))
      actions.AddString('Box: ('+ str(box.Origin.X) + ' ' + str(box.Origin.Y) + ' ' + str(box.Origin.Z) + ')')
      actions.AddString('Create')

      res = kcs_ui.choice_select('Symbolic view', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # get view projection
               resp, names = kcs_ui.string_req('Symbolic view name:', name)
            if res[1] == 2:
               p1 = copy.deepcopy(point)
               if SelectPoint('Location point, coordinate', p1):
                  point = copy.deepcopy(p1)
            if res[1] == 3:
               p1 = Point3D(uVector.X, uVector.Y, uVector.Z)
               if SelectPoint('U Vector, coordinate', p1):
                  uVector = KcsVector3D.Vector3D(p1.X, p1.Y, p1.Z)
            if res[1] == 4:
               p1 = Point3D(vVector.X, vVector.Y, vVector.Z)
               if SelectPoint('V Vector, coordinate', p1):
                  vVector = KcsVector3D.Vector3D(p1.X, p1.Y, p1.Z)
            if res[1] == 5:
               dist = forward
               resp, dist = kcs_ui.real_req('Forward distance:', forward)
               if resp==kcs_util.ok():
                  forward = dist
            if res[1] == 6:
               dist = backward
               resp, dist = kcs_ui.real_req('Backward distance:', forward)
               if resp==kcs_util.ok():
                  backward = dist
            if res[1] == 7:
               p1 = Point3D()
               p2 = Point3D()
               if SelectPoint('Lower-left (min z) box corner, coordinate', p1):
                  if SelectPoint('Upper-right (max z) box corner, coordinate', p2):
                     box.SetAxisParallelBox(p1, p2)
            if res[1] == 8:
               handle = kcs_draft.view_symbolic_new(name, point, uVector, vVector, forward, backward, box)
               kcs_ui.message_noconfirm('View handle: '+str(handle))
               # test created view using plane panel: 'JUMBO-BHD70' from SP project
               kcs_ui.message_noconfirm('test created view using plane panel: "JUMBO-BHD70" from SP project.')
               try:
                  model = KcsModel.Model('plane panel', 'JUMBO-BHD70')
                  kcs_draft.model_draw(model, handle)
                  kcs_ui.message_noconfirm('Model draw succeed!')
               except:
                  kcs_ui.message_noconfirm(kcs_draft.error)
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()


#-------------------------------------------------------------------------------------------------------------
try:           # main
   model = KcsModel.Model()

   # build actions list
   actions = ['Get view projection',
              'Set view projection',
              'Get view slice depth',
              'Get element transformation',
              'Create symbolic view',
              'Get symbolic view planes',]

   while 1:
      res = kcs_ui.choice_select('View functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # get view projection
               vresp, vhandle = CommonSample.SelectView('Select view, OC to exit')
               if vresp==1:
                  kcs_draft.view_projection_get(vhandle, projection)
                  PresentProjection(projection)
            if res[1] == 2:
                  resp, uVector, vVector = GetProjectionVectors()
                  if resp:
                     resp, drawcode = GetDrawCode()
                     if resp:
                        resp, vhandle = CommonSample.SelectView('Select view, OC to exit')
                        if resp:
                           if drawcode==0:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector, 0)
                           elif drawcode==1:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector, 1)
                           else:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector)
            if res[1] == 3:
               vresp, vhandle = CommonSample.SelectView('Select view, OC to exit')
               if vresp==1:
                  sres, fdist, bdist = kcs_draft.view_slicedepth_get(vhandle)
                  if sres==0:
                     kcs_ui.message_noconfirm('View is not sliced!')
                  elif sres==1:
                     print 'Total distance: ', fdist
                     kcs_ui.message_noconfirm('Total distance: ' + str(fdist))
                  else:
                     print 'Forward distance: ', fdist, '    Backward distance: ', bdist
                     kcs_ui.message_noconfirm('Forward distance: ' + str(fdist) + '    Backward distance: ' + str(bdist))
            if res[1] == 4:
               eresp, ehandle = SelectElement()
               if eresp == 1:
                  transf = KcsTransformation2D.Transformation2D()
                  kcs_draft.element_transformation_get(ehandle, transf)
                  PresentTransformation(transf)
            if res[1] == 5:
               CreateSymbolicView()
            if res[1] == 6:
               vresp, vhandle = CommonSample.SelectView('Select symbolic view')
               if vresp:
                  try:
                     plane1, plane2 = kcs_draft.view_slice_planes_get(vhandle)
                     kcs_ui.message_confirm(str(plane1))
                     kcs_ui.message_confirm(str(plane2))
                  except TBException, e:
                     kcs_ui.message_confirm(str(e))
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]



try:
   # build actions list
   actions = KcsStringlist.Stringlist('Get view projection')
   actions.AddString('Set view projection')
   actions.AddString('Get view slice depth')
   actions.AddString('Get element transformation')
   actions.AddString('Create symbolic view')

   while 1:
      res = kcs_ui.choice_select('View functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # get view projection
               vresp, vhandle = CommonSample.SelectView('Select view, OC to exit')
               if vresp==1:
                  kcs_draft.view_projection_get(vhandle, projection)
                  PresentProjection(projection)
            if res[1] == 2:
                  resp, uVector, vVector = GetProjectionVectors()
                  if resp:
                     resp, drawcode = GetDrawCode()
                     if resp:
                        resp, vhandle = CommonSample.SelectView('Select view, OC to exit')
                        if resp:
                           if drawcode==0:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector, 0)
                           elif drawcode==1:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector, 1)
                           else:
                              kcs_draft.view_projection_set(vhandle, uVector, vVector)
            if res[1] == 3:
               vresp, vhandle = CommonSample.SelectView('Select view, OC to exit')
               if vresp==1:
                  sres, fdist, bdist = kcs_draft.view_slicedepth_get(vhandle)
                  if sres==0:
                     kcs_ui.message_noconfirm('View is not sliced!')
                  elif sres==1:
                     print 'Total distance: ', fdist
                     kcs_ui.message_noconfirm('Total distance: ' + str(fdist))
                  else:
                     print 'Forward distance: ', fdist, '    Backward distance: ', bdist
                     kcs_ui.message_noconfirm('Forward distance: ' + str(fdist) + '    Backward distance: ' + str(bdist))
            if res[1] == 4:
               eresp, ehandle = SelectElement()
               if eresp == 1:
                  transf = KcsTransformation2D.Transformation2D()
                  kcs_draft.element_transformation_get(ehandle, transf)
                  PresentTransformation(transf)
            if res[1] == 5:
               CreateSymbolicView()
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintDraftError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]

