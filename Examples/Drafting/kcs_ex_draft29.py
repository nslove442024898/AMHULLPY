## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft29.py
#
#      PURPOSE:
#
#          This example creates new 3d linear dimension.
#

import kcs_ui
import kcs_util
import kcs_draft
import KcsStringlist
import KcsPoint3D
import KcsPoint2D
import KcsStat_point3D_req
import KcsPolygon3D
import KcsVector3D

#-------------------------------------------------------------------------------------------------------------
def BuildOptionsList(handle, fromlocpoint, points, type, index):      # build options list
   item = ''
   if handle<0:
      item = 'SubView: NotSelected'
   else:
      item = 'SubView: ' + str(handle)

   list = KcsStringlist.Stringlist(item)

   try:
      list.AddString('Measure points:' + str(len(points.Polygon)))
      list.AddString('Select ProjDirection')
      list.AddString('Select WitDirection')
      list.AddString('Select Position')
      if type==1:
         list.AddString('Type: Normal')
      elif type==2:
         list.AddString('Type: Chain')
      else:
         list.AddString('Type: Staircase')
      list.AddString('Base point:' + str(index))
      list.AddString('Insert')
   except:
      print KcsStringlist.error
   return list;

#-------------------------------------------------------------------------------------------------------------
def SelectDirection(points, direction, witness):               # allows user to select direction in 4 ways (3 for wintess vector)
   actions = KcsStringlist.Stringlist('X Axis')                # build options list
   try:
      actions.AddString('Y Axis')
      actions.AddString('Z Axis')
      actions.AddString('Key in')
      if len(points.Polygon)>=2 and not witness:               # if there are more then 1 measure point calculate
         actions.AddString('From first 2 points')              # direction using first 2 of them
   except:
      print KcsStringlist.error

   res = kcs_ui.choice_select('Direction', '', actions)
   if res[0] == kcs_util.ok():
      if res[1]==1:
         direction.SetComponents(1, 0, 0)                      # along X axis
      elif res[1]==2:
         direction.SetComponents(0, 1, 0)                      # along Y axis
      elif res[1]==3:
         direction.SetComponents(0, 0, 1)                      # along Z axis
      elif res[1]==4:
         xvalue = 0
         yvalue = 0
         zvalue = 0
         (set, xvalue) = kcs_ui.real_req('X', direction.X)     # key in values
         if set == kcs_util.ok():
            (set, yvalue) = kcs_ui.real_req('Y', direction.Y)
            if set == kcs_util.ok():
               (set, zvalue) = kcs_ui.real_req('Z', direction.Z)
               if set == kcs_util.ok():
                  direction.SetComponents(xvalue, yvalue, zvalue)
      elif res[1]==5:                                          # calculate form first 2 points of measure points table
         point1 = points.Polygon[0]
         point2 = points.Polygon[1]
         direction.SetComponents(point2.X-point1.X, point2.Y-point1.Y, point2.Z-point1.Z)
   return direction

#-------------------------------------------------------------------------------------------------------------
def SelectSubview(subview, fromlocpoint):                      # allows user to select subview in 2 ways:
   actions = KcsStringlist.Stringlist('from location point')   # based on location point or
   actions.AddString('Select')                                 # select in drawing
   res = kcs_ui.choice_select('Subview', '', actions)
   if res[0]==kcs_util.ok():
      if res[1] == 1:
         fromlocpoint = 1
      elif res[1] == 2:
         subviewpoint = KcsPoint2D.Point2D()
         msg = 'Please indicate a subview'
         result = kcs_ui.point2D_req(msg, subviewpoint)
         if result[0] == kcs_util.ok():
            subviewpoint = result[1]
            try:
               subview = kcs_draft.subview_identify(subviewpoint)   # find subview
               fromlocpoint = 0
            except:
               subview = -1
               fromlocpoint = 1
   return (subview, fromlocpoint)

#-------------------------------------------------------------------------------------------------------------
try:                                                           # main program
   type = 1
   position = KcsPoint2D.Point2D(0, 0)
   points = KcsPolygon3D.Polygon3D(KcsPoint3D.Point3D(0, 0, 0))
   direction = KcsVector3D.Vector3D(0, 0, 0)
   witvector = KcsVector3D.Vector3D(0, 0, 0)
   subview = -1
   fromlocpoint = 1
   index = 1

   actions = KcsStringlist.Stringlist('Select 3D Point')

   result = 1
   while result:
      actions = BuildOptionsList(subview, fromlocpoint, points, type, index)
      res = kcs_ui.choice_select('Linear dimension', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                    # select point to subview identify
            subviewpoint = KcsPoint2D.Point2D()
            msg = 'Please indicate a subview'
            result = kcs_ui.point2D_req(msg, subviewpoint)
            if result[0] == kcs_util.ok():
               subviewpoint = result[1]
               try:
                  subview = kcs_draft.subview_identify(subviewpoint)   # find subview
                  fromlocpoint = 0
               except:
                  subview = -1
                  fromlocpoint = 1
               actions = BuildOptionsList(subview, fromlocpoint, points, type, index)
         elif res[1] == 2:                                  # get polygon points
            point3d = KcsPoint3D.Point3D(0, 0, 0)
            newpoints = KcsPolygon3D.Polygon3D(point3d)
            msg = 'Please select a measure point'
            status = KcsStat_point3D_req. Stat_point3D_req()
            nextpoint = 1
            size = 0
            while nextpoint:
               result = kcs_ui.point3D_req(msg, status, point3d)
               if result[0] == kcs_util.ok():
                  if size==0:
                     newpoints = KcsPolygon3D.Polygon3D(result[1])
                  else:
                     newpoints.AddPoint(result[1])
                  size = size+1
               elif result[0] == kcs_util.operation_complete():
                  points = newpoints
                  nextpoint = 0
               else:
                  nextpoint = 0
         elif res[1] == 3:                                  # select new direction
            direction = SelectDirection(points, direction, 0)
         elif res[1] == 4:                                  # select new witness lines direction
            witvector = SelectDirection(points, witvector, 1)
         elif res[1] == 5:                                  # select location point
            msg = 'Please give a location point'
            result = kcs_ui.point2D_req(msg, KcsPoint2D.Point2D())
            if result[0] == kcs_util.ok():
               position = result[1]
         elif res[1] == 6:                                  # select dimension type
            if type==1:
               type = 2
            elif type==2:
               type = 3
            else:
               type = 1
            actions = BuildOptionsList(subview, fromlocpoint, points, type, index)
         elif res[1] == 7:
            try:
               base = index                                 # select index
               res, base = kcs_ui.int_req('index for base point:', base)
               if res == kcs_util.ok():
                  index = base;
                  actions = BuildOptionsList(subview, fromlocpoint, points, type, index)
            except:
               print kcs_ui.error
         elif res[1] == 8:                                  # create new linear 3d dimension
            try:
               if fromlocpoint:
                  kcs_draft.dim_linear_new(points, type, direction, position, witvector, index-1)
               else:
                  kcs_draft.dim_linear_new(points, type, direction, position, witvector, subview, index-1)
            except:
               print kcs_draft.error
      else:
         result = 0

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print kcs_draft.error

