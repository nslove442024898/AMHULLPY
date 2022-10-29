## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_shellstiff.py
#
#      PURPOSE:
#
#          This script will create a simple longitudinal at Z=8000 via the
#          Vitesse function kcs_chm.run_XML. Then the profile will be split/combined
#          by the Vitesse functions kcs_chm.stiffener_split/kcs_chm.stiffener_combine.
#
#
#----------------------------------------------------------------------------

import kcs_draft
import kcs_ui
import kcs_util
import kcs_chm
import KcsElementHandle
import KcsPoint3D
import KcsVector3D
import KcsPlane3D
import KcsModel
from xml.dom.ext        import PrettyPrint
from xml.dom.minidom    import Document

#------------------------------------------------------
#
# Procedure CreateXMLShProf:
#
# Create a XML description for a longitudinal
#
#      INPUT:
#
#      Parameters:
#
#      Doc                The XMLDocument
#      Surface            The name of the surface
#      LongName           The name of the longitudinal
#
#------------------------------------------------------
def CreateXMLShProf( Doc, Surface, LongName ):
   AddRoot = 0
   try:
      Root = Doc.documentElement
      if Root == None:
         AddRoot = 1
   except:
      AddRoot = 1

   if AddRoot == 1:
#
#     Add the root node
#
      Root = Doc.createElement("Ship")
      Doc.appendChild(Root)

#
#  Create a "ShellProfile" element
#
   ShProf = Doc.createElement("ShellProfile")
   Root.appendChild(ShProf)

#
#  Add the "ObjName" attribute. (This is the name of the long to be created)
#
   ShProf.setAttribute( "ObjId", LongName )

#
#  Set profile type and dimensions
#
   Mat = Doc.createElement("Material")
   ShProf.appendChild(Mat)
   Mat.setAttribute( "Type", "10" )
   Mat.setAttribute( "Parameters", "200 15" )
   Mat.setAttribute( "Grade", "A" )
#
#  Create a curve branch element and a curve by principal plane Z=8000
#
   Branch = Doc.createElement("Branch")
   ShProf.appendChild(Branch)
   Trace = Doc.createElement("Trace")
   Branch.appendChild(Trace)
   ByPrPlane = Doc.createElement("ByPrincipalPlane")
   Trace.appendChild(ByPrPlane)
   ByPrPlane.setAttribute( "Surface", Surface)
   ByPrPlane.setAttribute( "Z", "8000" )
#
#  Add a limit box to the trace curve
#
   Box = Doc.createElement("Box")
   Trace.appendChild(Box)
   Box.setAttribute( "XMin", "FR50" )
   Box.setAttribute( "XMax", "FR75" )
   Box.setAttribute( "YMin", "0" )

   ShStiff = Doc.createElement("ShellStiffener")
   Branch.appendChild(ShStiff)



#------------------------------------------------------
#
# Procedure AddSchemaRef:
#
# Adds the XML schema reference to an XML document
#
#      INPUT:
#
#      Parameters:
#
#      Doc                The XMLDocument
#
#------------------------------------------------------

def AddSchemaRef( Doc, Schema ):
#
#   Is there a root node?
#
   AddRoot = 0
   try:
      Root = Doc.documentElement
      if Root == None:
         AddRoot = 1
   except:
      AddRoot = 1

   if Schema == "":
#
#     The XML schema is in directory SB_SYSTEM\xml#
#     SB_SYSTEM from the environment.
#
      Schema = kcs_util.TB_environment_get( "SB_SYSTEM" )
      Schema = Schema + "\\xml\\CurvedHull.xsd"
      if Trace == 1:
         print Schema

   if AddRoot == 1:
#
#     Add the root node
#
      Root = Doc.createElement("Ship")
      Doc.appendChild(Root)
   try:
#
#     Add the schema reference attributes
#
      Root.setAttribute( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
      Root.setAttribute( "xsi:noNamespaceSchemaLocation", Schema)
   except:
      print "Error in AddSchemaRef"

#------------------------------------------------------------
# Start of Main Script
#------------------------------------------------------------

try:
   Res   = 0
   Trace = 1

   if Trace == 1:
      print "******************** Start of script *********************"
#
#  Create a new XML document
#
   if Trace==1:
      print "Create a new XML document"

   Doc = Document()
#
#  Add the schema reference.
#
   AddSchemaRef( Doc, "" )
   if Trace == 1:
      print "Added Schema Reference"
#
#  Ask the user for the surface name
#
   ( Answer, Surface ) = kcs_ui.string_req( 'Please select the surface:', 'SPHULL' )
#
#  Ask the user for the long name
#
   ( Answer, LongName ) = kcs_ui.string_req( 'Name of the longitudinal:', 'SPL900' )
   if Answer != kcs_util.ok():
      Res = 1

#
#  Create an XML definition for a shell profile
#
   if Res == 0:
      try:
         if Trace == 1:
            print "Calling CreateXMLShProf..."
         CreateXMLShProf( Doc, Surface, LongName )
      except:
         Res = 1
         print "Failed to create the XML definition for a shell profile"

#
#  Save the XML document to a file
#
   if Res == 0:
      try:
         XMLFile = open('c:\\temp\\Profile.xml', 'w')
         if Trace == 1:
            print "Opened a file"
         try:
            PrettyPrint( Doc, XMLFile)
            if Trace == 1:
               print "Printed XML document to the file"
         except:
            Res = 1
            print "PrettyPrint failed"

         XMLFile.close()
         if Trace == 1:
            print "Closed the file"
      except:
         Res = 1
         print "Failed to save the XML document to the file"


#
#  Run the XML file to create the longitudinal
#
   if Res == 0:
      try:
         if Trace == 1:
            print "Calling kcs_chm.run_XML..."
         ModelList = kcs_chm.run_XML('c:\\temp\\Profile.xml', 'c:\\temp\\Profile.log')
         print ""
      except:
         print "run_XML failed!"
         print kcs_chm.error
         Res = 1


   if Res == 0:
#
#  Split the longitudinal, by a principal plane
#
      if Trace == 1:
         print "Create a principal plane: X=FR60"
      (TmpRes, XCoord ) = kcs_util.pos_to_coord( 1, 60 )
      if Trace == 1:
          print "XCoord=",
          print XCoord
      Pt   = KcsPoint3D.Point3D( XCoord, 0.0, 0.0 );
      Norm = KcsVector3D.Vector3D( 1.0, 0.0, 0.0 );

      SplittingObj = KcsPlane3D.Plane3D( Pt, Norm)
      ObjToSplit = KcsModel.Model( "longitudinal", LongName)

      try:
         if Trace == 1:
            print "Splitting the longitudinal"
         kcs_chm.stiffener_split( ObjToSplit, SplittingObj );
         if Trace == 1:
            print "Split OK"
      except:
         print "Split failed"
         Res = 1

      if Res == 0:
         try:
            if Trace == 1:
               print "Store ",
               print ObjToSplit.Name
            kcs_chm.store( ObjToSplit )
         except:
            print "Failed to store the shell profile"
            kcs_chm.skip( ObjToSplit );
            Res = 1
      else:
         kcs_chm.skip( ObjToSplit )
#
#  Send stiffeners to profile DB
#
   choices = ( 'Yes', 'No' )
   (status, index) = kcs_ui.choice_select( 'To Profile DB', 'Send stiffeners to profile DB?', choices)
   if status == kcs_util.ok():
      if index == 1:
         if Res == 0:
            try:
               Stiff1 = KcsModel.Model( "curved stiffener", LongName + "-S1" )
               Stiff2 = KcsModel.Model( "curved stiffener", LongName + "-S2")
               if Trace == 1:
                  print "Send to profile db"
               kcs_chm.stiffener_to_profdb( Stiff1 )
               kcs_chm.stiffener_to_profdb( Stiff2 )
            except:
               print "Send to profile db failed"
#
#  Combine stiffeners
#
   if Res == 0:
      (status, index) = kcs_ui.choice_select( 'Stiffener', 'Combine Stiffeners?', choices)
      if status == kcs_util.ok():
         if index == 1:
            Long   = KcsModel.Model( "longitudinal", LongName )
            Stiff1 = KcsModel.Model( "curved stiffener", LongName + "-S1" )
            Stiff2 = KcsModel.Model( "curved stiffener", LongName + "-S2")
            try:
               if Trace == 1:
                  print "Combining the longitudinal"
               Stiff3 = kcs_chm.stiffener_combine( Stiff1, Stiff2 )
               if Trace == 1:
                  print "Combine OK"
            except:
               print "Failed to combine shell stiffeners"
               Res = 1;

            if Res == 0:
               try:
                  if Trace == 1:
                     print "Store ",
                     print Long.Name
                  kcs_chm.store( Long )
                  if Trace == 1:
                     print "Store OK"
               except:
                  print "Failed to store the shell profile"
                  kcs_chm.skip( Long );
                  Res = 1
            else:
               kcs_chm.skip( Long )
#
#  Recreate the longitudinal
#
   if Res == 0:
      try:
         if Trace == 1:
            print "Recreate the longitudinal"
         Long = KcsModel.Model( "longitudinal", LongName )
         kcs_chm.recreate( Long );

      except:
         print "Failed to recreate!"
         Res = 1

      if Res == 0:
         try:
            kcs_chm.store( Long )
         except:
            print "Failed to store the shell profile"
            kcs_chm.skip( Long );
            Res = 1

#
#  Delete the longitudinal
#
      choices = ( 'Yes', 'No' )
      (status, index) = kcs_ui.choice_select( 'Longitudinal', 'Delete Longitudinal?', choices)
      if status == kcs_util.ok():
         if index == 1:
            if Trace == 1:
               print "Delete the longitudinal"
            ObjRef = KcsModel.Model( "longitudinal", LongName)
            try:
               kcs_chm.delete( ObjRef );
            except:
               Res = 1
               print "Failed to delete the longitudinal"

   print "******************** Script completed **************************"

except:
   print "Script terminated due to unhandled exception"

