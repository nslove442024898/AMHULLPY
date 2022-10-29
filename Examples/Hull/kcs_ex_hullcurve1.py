## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_hullcurve1.py
#
#      PURPOSE:
#
#          This program updates an existing panel and creates a new curve statement
#          based on an existing contour in a drawing.
#

import kcs_draft
import KcsPoint2D
import KcsColour
import KcsContour2D

import kcs_dex
import kcs_hull
import kcs_hullpan
import kcs_ui
import kcs_util
import KcsUtilDexPan
import KcsUtilPan
import KcsUtilPanSch
import KcsUtilPos

import KcsTBDVitDef
import math
import string
import KcsStringlist


#---------------------------------------------------------------------------------------------------
def	SelectView():
   point = KcsPoint2D.Point2D()
   prompt = 'Indicate view, OC to exit'
   handle = -1

   resp = kcs_ui.point2D_req(prompt, point)			 # request user for point
   if resp[0] == kcs_util.ok():
      try:
         handle = kcs_draft.view_identify(point)
         return (1, handle)
      except:
         print kcs_draft.error
         return (0, 0)



# get user choice and select entity
try:
   # get view handle
   (set, viewhandle) = SelectView()
   if not set:
      exit()

   kcs_draft.element_highlight(viewhandle)

   # get panel
   pan = kcs_ui.req_pick_mod("Pick panel",1,2)
   if pan[1] != "plane panel":
      kcs_ui.message_confirm("Not a planar panel")
      exit()
   panel = pan[2]
   plane = KcsUtilPan.getPlane( panel)
   print plane[0]

   # curve name
   curvename = "XYZ"

   # create python contour
   point = KcsPoint2D.Point2D(350.0,200.0)
   contour = KcsContour2D.Contour2D(point)
   point.X = 425.0
   contour.AddLine(point)
   point.Y = 300.0
   contour.AddArc(point,40.0)
   point.X = 350.0
   point.Y = 200.0
   contour.AddLine(point)

   # set color
   col = KcsColour.Colour("Blue")		
   kcs_draft.colour_set( col)

   # add contour to drawing
   contour_handle = kcs_draft.contour_new(contour)

   # create curve
   (res, stmt) = kcs_hull.pan_curve_create( viewhandle, panel, curvename, plane[0], contour)

   # modify panel
   if res == kcs_util.success():
      print "out1"
      kcs_hull.pan_modify(panel,2)
      kcs_hull.pan_exec_stmt( 0, stmt)
      kcs_hull.pan_store()
      kcs_hull.pan_skip()
      kcs_ui.message_confirm('Script completed successfully')
   else:	
     kcs_ui.message_confirm('Script IInterrupted')
   kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
except:
   print kcs_ui.error
   kcs_draft.highlight_off(0)                      # highlight off all highlighted entities


