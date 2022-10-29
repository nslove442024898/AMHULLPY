## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_hullcurve2.py
#
#      PURPOSE:
#
#          This program creates a new curve based on an existing contour in a drawing
#          and stores it in CGDB
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
import KcsElementHandle

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
	 print sys.exc_info()[1]
         print kcs_draft.error
         return (0, 0)



# get user choice and select entity
try:
   # get view handle
   (set, viewhandle) = SelectView()
   if not set:
      exit()

   kcs_draft.element_highlight(viewhandle)


   # curve name
   curvename = "MMXYZ123"

   # create python contour
   point = KcsPoint2D.Point2D(350.0,200.0)
   contour = KcsContour2D.Contour2D(point)
   point.X = 425.0
   contour.AddLine(point)
   point.Y = 300.0
   # contour.AddLine(point)
   contour.AddArc(point,40.0)
   point.X = 350.0
   point.Y = 200.0
   contour.AddLine(point)

   # set color
   col = KcsColour.Colour("Blue")		
   kcs_draft.colour_set( col)

   # add contour to drawing
   print 'mmm'
   contour_handle = kcs_draft.contour_new(contour)
   print 'bbcc'
   # create curve
   (res) = kcs_hull.pan_curve_store( viewhandle, curvename, contour)
   print "res"
   print res
   #
   if res == kcs_util.success():
      print "out2"
      kcs_ui.message_confirm('Script completed successfully')
   else:	
      kcs_ui.message_confirm('Script Interrupted')
   kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
except:
   print kcs_ui.error
   kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
