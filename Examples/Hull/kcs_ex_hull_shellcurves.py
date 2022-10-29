## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#------------------------------------------------------------------------------
#       NAME:
#
#          _usrkcs_ex_hull_shcurves_py -
#
#       PURPOSE:
#
#          This python script shows how to create planar curves
#          with the vitesse functions "kcs_chm.curve_principal_create" and
#          "kcs_chm.curve_planar_create".
#
#------------------------------------------------------------------------------


import kcs_draft
import kcs_util
import kcs_ui
import kcs_chm
import KcsElementHandle
import KcsPoint3D
import KcsVector3D
import KcsPlane3D


try:
   Trace = 1
   Res   = 0

   if Trace == 1:
      print "******************** Start of script **************************"
#
#  Get the name of the surface
#
   ( Answer, SurfaceName ) = kcs_ui.string_req( 'Please select the surface:', 'SPHULL' )
   if Answer != kcs_util.ok():
      Res = 1
#
#  Get the seam/curve prefix
#
   if Res == 0:
      ( Answer, CurvePrefix ) = kcs_ui.string_req( 'Seam/Curve Prefix:', 'VITESSE_CURVE' )
      if Answer != kcs_util.ok():
         Res = 1
   print "Res = ",
   print Res

#
#  Create shell curves by principal plane in the interval 40000(2000)60000
#  The curves will be named "VITESSE_CURVE1", "VITESSE_CURVE", "VITESSE_CURVE3", etc. The curves will
#  be stored on SB_CGDB
#
   if Res == 0:
      Start     = 40000
      Stop      = 60000
      Partition = 8000
      CurveNo   = 1

      MinPt = KcsPoint3D.Point3D( 39000.0, 0.0,    -1000.0 )
      MaxPt = KcsPoint3D.Point3D( 61000.0, 40000.0, 40000.0 )

      Current = Start
      ModelList = []
      while Current < Stop+1:
         PlaneStr = "X=" + str(Current)

         if Trace == 1:
            print "PlaneStr:",
            print PlaneStr

         try:
            CurveName = CurvePrefix + str(CurveNo)
            if Trace == 1:
               print "CurveName= ",
               print CurveName
               print "SurfaceName= ",
               print SurfaceName
            Model = kcs_chm.curve_principal_create( CurveName, PlaneStr, MinPt, MaxPt, SurfaceName )
            ModelList.append( Model )
            if Trace == 1:
               print "kcs_chm.curve_principal_create succeeded"
         except:
            Res = 1
            print "Failed to generate curve by principal plane: ",
            print PlaneStr

         if Res == 0:
            try:
               kcs_chm.store( Model )
               if Trace == 1:
                  print "Store succeeded"
            except:
               print "Failed to store curve: ",
               print CurveName
         else:
            try:
               kcs_chm.skip( Model )
            except:
               print "Failed to skip curve: ",
               print CurveName

         if Trace == 1:
            print "Next curve..."
         Current = Current + Partition
         CurveNo = CurveNo + 1

         if Trace == 1:
            print "Curveposition = ",
            print str(Current)
            print "CurveNo = ",
            print str(CurveNo)

#
#  Create a curve by the vitesse function "kcs_chm.curve_planar_create".
#
      Pnt   = KcsPoint3D.Point3D( 60000.0, 0.0, 0.0)
      Norm  = KcsVector3D.Vector3D(1.0, 0.3, 0.0)
      Plane = KcsPlane3D.Plane3D( Pnt, Norm)

      MinPt = KcsPoint3D.Point3D( 10000.0, 0.0,    -1000.0 )
      MaxPt = KcsPoint3D.Point3D( 150000.0, 40000.0, 40000.0 )

      CurveName = CurvePrefix + str(CurveNo);

      try:
         if Trace == 1:
            print "Call kcs_chm.curve_planar_create"
            print "CurveName=",
            print CurveName
            print "SurfaceName=",
            print SurfaceName
         Model = kcs_chm.curve_planar_create( CurveName, Plane, MinPt, MaxPt, SurfaceName)
         ModelList.append( Model )
      except:
         print "kcs_chm.curve_planar_create failed"
         Res = 1

      if Res == 0:
         try:
            kcs_chm.store( Model )
            if Trace == 1:
               print "Store succeeded"
         except:
            print "Failed to store curve: ",
            print CurveName
      else:
         try:
            kcs_chm.skip( Model )
         except:
            print "Failed to skip curve: ",
            print CurveName

#
#     Ask if created curve should be deleted
#
      if len(ModelList) > 0:
         choices = ( 'Yes', 'No' )
         (status, index) = kcs_ui.choice_select( 'Curves', 'Delete Curves?', choices)
         if status == kcs_util.ok():
            if index == 1:
               Loop = 0
               while Loop < len(ModelList):
                  Model = ModelList[Loop]
                  try:
                     kcs_chm.delete( Model)
                     if Trace == 1:
                        print "Deleted",
                        print Model.Name
                  except:
                     print "Failed to delete ",
                     print Model.Name
                  Loop = Loop + 1


   print "******************** Script completed **************************"

except:
   print "Script interrupted due to unhandled exception"


