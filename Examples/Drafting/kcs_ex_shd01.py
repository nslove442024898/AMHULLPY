## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_shd01.py
#
#      PURPOSE:
#
#          This example shows how to use the shading functions
#
import kcs_ui
import kcs_draft
import math

import KcsPoint2D
import KcsPoint3D
import KcsTransformation3D
import KcsVector3D

def run():
    poi = KcsPoint2D.Point2D()
    kcs_ui.message_confirm('Create new shaded view')
    res,poi = kcs_ui.point2D_req('Indicate View', poi)

    view = kcs_draft.view_identify(poi)
    try:
        kcs_draft.shd_new(view)
    except:
        kcs_ui.message_noconfirm('Not able to create a new shaded view')
        return

    poi1 = KcsPoint3D.Point3D()
    poi2 = KcsPoint3D.Point3D()
    kcs_ui.message_confirm('Zoom to box')
    res,poi1 = kcs_ui.point3D_req('Indicate min point', poi1)
    res,poi2 = kcs_ui.point3D_req('Indicate max point', poi2)
    kcs_draft.shd_zoom_box(poi1,poi2)

    kcs_ui.message_confirm('Rotate')
    tra = KcsTransformation3D.Transformation3D()
    vec = KcsVector3D.Vector3D(0.0,0.0,1.0)
    tra.Rotate(poi1,vec,math.pi/4)
    kcs_draft.shd_projection_set(tra)

    kcs_ui.message_confirm('Auto Scale')
    kcs_draft.shd_autoscale()

#------------------------------------------------------------------------------
#  Start of main body
#------------------------------------------------------------------------------
if __name__ == "__main__":
    run()
