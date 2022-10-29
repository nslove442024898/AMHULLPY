## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft28.py
#
#      PURPOSE:
#
#          This example creates new point 3d dimension.
#

import kcs_ui
import kcs_util
import kcs_draft
import KcsStringlist
import KcsPoint3D
import KcsPoint2D
import KcsStat_point3D_req

#-------------------------------------------------------------------------------------------------------------
def BuildOptionsList(handle, fromlocpoint, note, height, rotation):     # build options list
   item = ''
   if fromlocpoint:
      item = 'SubView: From loc point'
   else:
      item = 'SubView: ' + str(handle)

   list = KcsStringlist.Stringlist(item)

   try:
      list.AddString('Select 3D Point')
      list.AddString('Select location point')
      list.AddString('Note: ' + note)
      list.AddString('Height: ' + str(height))
      list.AddString('Rotation: ' + str(rotation))
      list.AddString('Insert')
   except:
      print KcsStringlist.error
   return list;

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
               print 'ok'
            except:
               print 'except'
               subview = -1
               fromlocpoint = 1
   return (subview, fromlocpoint)

#-------------------------------------------------------------------------------------------------------------
def SelectPoint(point3d):                                         # allows user to input 3D point in 2 ways:
   actions = KcsStringlist.Stringlist('Key in')                   # key in
   actions.AddString('Select')                                    # by selection
   res = kcs_ui.choice_select('Point3d', '', actions)
   if res[0]==kcs_util.ok():
      if res[1] == 1:
         (set, coord) = kcs_ui.real_req('X:', point3d.X)
         if set == kcs_util.ok():
            point3d.X = coord
            (set, coord) = kcs_ui.real_req('Y:', point3d.Y)
            if set == kcs_util.ok():
               point3d.Y = coord
               (set, coord) = kcs_ui.real_req('Z:', point3d.Z)
               if set == kcs_util.ok():
                  point3d.Z = coord
      elif res[1] == 2:
            msg = 'Please give a position'
            status = KcsStat_point3D_req.Stat_point3D_req()
            result = kcs_ui.point3D_req(msg, status, point3d)
            if result[0] == kcs_util.ok():
               print 'The given position is', result[1]
               point3d = result[1]
   return point3d

#-------------------------------------------------------------------------------------------------------------
try:
   note = ''
   point3d = KcsPoint3D.Point3D()
   point2d = KcsPoint2D.Point2D()
   height = 10.0
   rotation = 0.0
   subview = -1
   fromlocpoint = 1

   actions = KcsStringlist.Stringlist('Select 3D Point')

   result = 1
   while result:
      actions = BuildOptionsList(subview, fromlocpoint, note, height, rotation)
      res = kcs_ui.choice_select('Dimension', '', actions)
      if res[0]==kcs_util.ok():
         if res[1] == 1:                                                                        # select subview
            (subview, fromlocpoint) = SelectSubview(subview, fromlocpoint);
            actions = BuildOptionsList(subview, fromlocpoint, note, height, rotation)
         if res[1] == 2:                                                                        # select 3D point
            point3d = SelectPoint(point3d)
         elif res[1] == 3:                                                                      # select location point
            msg = 'Please give a location point'
            result = kcs_ui.point2D_req(msg, point2d)
            if result[0] == kcs_util.ok():
               print 'The given position is', result[1]
               point2d = result[1]
         elif res[1] == 4:                                                                      # input annotation text
            (set, note) = kcs_ui.string_req('Input annotation text:', note)
            actions = BuildOptionsList(subview, fromlocpoint, note, height, rotation)
         elif res[1] == 5:                                                                      # input height of dimension
            (set, height) = kcs_ui.real_req('Height:', height)
            actions = BuildOptionsList(subview, fromlocpoint, note, height, rotation)
         elif res[1] == 6:
            (set, rotation) = kcs_ui.real_req('Rotation:', rotation)                            # input rotation of dimension
            actions = BuildOptionsList(subview, fromlocpoint, note, height, rotation)
         elif res[1] == 7:                                                                      # insert dimension
            try:
               if fromlocpoint:
                  kcs_draft.dim_point_3d(point3d, point2d, height, rotation, note)
               else:
                  kcs_draft.dim_point_3d(point3d, point2d, height, rotation, note, subview)
            except:
               print kcs_draft.error
      else:
         result = 0

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print kcs_draft.error
