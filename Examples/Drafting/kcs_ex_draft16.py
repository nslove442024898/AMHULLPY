## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft16.py
#
#      PURPOSE:
#
#          This program translates a 3d-coordinate to a 2d-coordinate
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsPoint3D
import KcsStat_point3D_req
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:
   view_handle = None

   try:
      kcs_ui.message_confirm('This script shows how to use point_transform function.')

      # select view
      point   = KcsPoint2D.Point2D()
      resp, point = kcs_ui.point2D_req('Indicate view which will be used as transformation data source', point)
      if resp:
         try:
            view_handle = kcs_draft.view_identify(point)
         except:
            CommonSample.ReportTribonError(kcs_draft)

   except:
      CommonSample.ReportTribonError(kcs_ui)

   # select point and transform it
   if view_handle != None:
      point3d = KcsPoint3D.Point3D()
      status  = KcsStat_point3D_req.Stat_point3D_req()
      try:
         resp, point3d = kcs_ui.point3D_req('Select 3D point you want to transform', status, point3d)
         if resp == kcs_util.ok():
            point2d = KcsPoint2D.Point2D()
            try:
               kcs_draft.point_transform(view_handle, point3d, point2d)
               kcs_ui.message_noconfirm('Point 2D: %f, %f' % (point2d.X, point2d.Y))
            except:
               CommonSample.ReportTribonError(kcs_draft)
      except:
         CommonSample.ReportTribonError(kcs_ui)
   else:
      kcs_ui.message_noconfirm('View not defined!')

except:
   pass
