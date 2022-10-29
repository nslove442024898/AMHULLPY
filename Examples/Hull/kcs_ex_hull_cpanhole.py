## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hull_cpanhole.py
#
#      PURPOSE:
#
#               This program presents kcs_chm.cpan_hole_create: hole handling function for a curved panel.
#
#
#
#----------------------------------------------------------------------------------
import string
import kcs_ui
import kcs_util
import kcs_chm
import KcsPoint3D
import KcsStat_point3D_req
import KcsPanHoleOptions
import KcsModel
import CommonSample

#------------------------------------------------------------
# Internal procedure PrintHoleOptions
#------------------------------------------------------------
def PrintHoleOptions( HoleOptions ):
   print "Design: ",
   print HoleOptions.GetDesign()

   print "Rotation: ",
   print HoleOptions.GetDirection()

   print "Develop: ",
   print HoleOptions.GetDevelop()

   print "BurnOption: ",
   print HoleOptions.GetBurnOption()

   print "MarkOption: ",
   print HoleOptions.GetMarkOption()

   print "MarkType: ",
   print HoleOptions.GetMarkType()

   print "MarkLen: ",
   print HoleOptions.GetMarkLen()

   print "Symmetry: ",
   print HoleOptions.GetSymmetry()

   if HoleOptions.IsOriginAlongAxis() == 1:
      ( Axis, Pt1, HasApprox ) = HoleOptions.GetOriginAlongAxis()
      print "OriginAlongAxis:"
      print "   Axis: ",
      print Axis
      print "   Pt1: ",
      print Pt1
      print "   HasApprox: ",
      print HasApprox
   elif HoleOptions.IsOriginAlongLine() == 1:
      ( Pt1, Pt2 ) = HoleOptions.GetOriginAlongLine()
      print "OriginAlongLine:"
      print "   Pt1: ",
      print Pt1
      print "   Pt2",
      print Pt2
   else:
      ( Axis, Pt1 ) = HoleOptions.GetOriginAsStored()
      print "OriginAsStored:"
      print "   Axis: ",
      print Axis
      print "   Pt1",
      print Pt1

#------------------------------------------------------------
# Start of Main Script
#------------------------------------------------------------

Trace = 1


#
#  Create main menu
#
Model       = KcsModel.Model('PT')
HoleOptions = KcsPanHoleOptions.PanHoleOptions()
Origin      = KcsPoint3D.Point3D()
OriginSec   = KcsPoint3D.Point3D()

while 1:
   actions = (
      'Select Curved Panel',
      'Add Hole to Panel',
      'Store Panel',
      'Set Origin Along Line',
      'Set Origin Along Axis',
      'Set Origin As Stored',
      'Set Direction',
      'Set Design',
      'Set Develop',
      'Set Burn/Mark',
      'Set MarkOption',
      'Set MarkType',
      'Set Marking length',
      'Set Symmetry'
      )

   (status, index) = kcs_ui.choice_select('Curved Hull','Holes', actions)

   if status == kcs_util.ok():
      if Trace == 1:
         print "index=",
         print index

      if index == 1:
         Model = CommonSample.SelectModel()
         if Trace == 1:
            print Model

      elif index == 2:
         try:
            kcs_chm.cpan_hole_create( Model.Name, HoleOptions)
         except:
            kcs_ui.message_confirm( 'cpan_hole_create failed!')

      elif index == 3:
         try:
            kcs_chm.store( Model)
         except:
            kcs_ui.message_confirm( 'Failed to store the panel')

      elif index == 4:
         res, Origin = kcs_ui.point3D_req('Give the First Point:', Origin)
         if res == kcs_util.ok():
            res, OriginSec = kcs_ui.point3D_req('Give the Second Point:', OriginSec)
            if res == kcs_util.ok():
               HoleOptions.SetOriginAlongLine(Origin, OriginSec)
         res = kcs_util.ok()

      elif index == 5:
         if Trace == 1:
            print 'Set Origin Along Axis'
         (res, location) = kcs_ui.string_req('Enter Axis (1=X, 2=Y, 3=Z):', '1')
         if res == kcs_util.ok():
            nLoc = int(location)
            ( res, Origin ) = kcs_ui.point3D_req('Indicate the point:', Origin )
            if res == kcs_util.ok():
               HoleOptions.SetOriginAlongAxis( nLoc, Origin, 1)
         res = kcs_util.ok()

      elif index == 6:
         res, location = kcs_ui.string_req('Enter Approximate Axis (1=X, 2=Y, 3=Z):','')
         if res == kcs_util.ok():
            nLoc = int(location)
            res, Origin = kcs_ui.point3D_req('Give apprixomate coordinate:', Origin)
            if res == kcs_util.ok():
               HoleOptions.SetOriginAsStored( nLoc, Origin)
         res = kcs_util.ok()

      elif index == 7:
         res, Origin = kcs_ui.point3D_req('Give orientation point or vector:', Origin)
         if res == kcs_util.ok():
            HoleOptions.SetDirection(Origin)
         res = kcs_util.ok()

      elif index == 8:
         res, strInput = kcs_ui.string_req('Enter Hole Designation:','')
         if res == kcs_util.ok():
            HoleOptions.SetDesign(strInput)
         res = kcs_util.ok()

      elif index == 9:
         res, strInput = kcs_ui.string_req('Enter Develop (0=Do not develop, 1=Develop)','0')
         if res == kcs_util.ok():
            nTmp = int( strInput)
            HoleOptions.SetDevelop(nTmp)
         res = kcs_util.ok()

      elif index == 10:
         res, strInput = kcs_ui.string_req('Enter Burn/Mark (1=Burn hole, 0=Only mark hole):','1')
         if res == kcs_util.ok():
            nTmp = int( strInput)
            HoleOptions.SetBurnOption(nTmp)
         res = kcs_util.ok()

      elif index == 11:
         res, strInput = kcs_ui.string_req('Enter Mark option (0=Contour, 1=Cross mark or 2=Contour+cross):','0')
         if res == kcs_util.ok():
            nTmp = int( strInput)
            HoleOptions.SetMarkOption(nTmp)
         res = kcs_util.ok()

      elif index == 12:
         res, strInput = kcs_ui.string_req('Enter Mark Type (0=Over Hole, 1=Small or 2=Special):','0')
         if res == kcs_util.ok():
            nTmp = int( strInput)
            HoleOptions.SetMarkType(nTmp)
         res = kcs_util.ok()

      elif index == 13:
         res, strInput = kcs_ui.string_req('Enter Marking length:','100')
         if res == kcs_util.ok():
            rTmp = float( strInput)
            HoleOptions.SetMarkLen(rTmp)
         res = kcs_util.ok()

      elif index == 14:
         res, strInput = kcs_ui.string_req('Enter Symmetry (0,1 or 2:','0')
         if res == kcs_util.ok():
            nTmp = int( strInput)
            if nTmp == 2:
               nTmp = 12
            HoleOptions.SetSymmetry(nTmp)
         res = kcs_util.ok()

   else:
      print "User interrupted!"
      break;

   if Trace == 1:
      PrintHoleOptions( HoleOptions)


print "******************** Script completed **************************"


