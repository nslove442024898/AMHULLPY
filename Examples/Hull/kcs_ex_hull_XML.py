## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------
#
#       NAME:
#
#          _usrkcs_ex_hull_XML_py -
#
#       PURPOSE:
#
#          This python script shows how to use PyXML to create an XML document.
#          The script uses the DOM (Document Object Model) interface to build up
#          XML tree structure of elements and attributes.
#
#          The example will create an XML file containing a number of shell curves.
#          This script will also generate the curves by using the Vitesse function
#          "kcs_chm.run_XML".
#
#----------------------------------------------------------------------------


import KcsPoint3D
import kcs_ui
import kcs_util
import kcs_chm
from xml.dom.ext        import PrettyPrint
from xml.dom.minidom    import Document

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


   print "AddSchemaRef 1"
   if Schema == "":
#
#     The XML schema is in directory SB_SYSTEM\xml#
#     SB_SYSTEM from the environment.
#
      Schema = kcs_util.TB_environment_get( "SB_SYSTEM" )
      Schema = Schema + "\\xml\\CurvedHull.xsd"
      print Schema

   if AddRoot == 1:
#
#     Add the root node
#
      Root = NewDoc.createElement("Ship")
      NewDoc.appendChild(Root)
   try:
#
#     Add the schema reference attributes
#
      Root.setAttribute( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
      Root.setAttribute( "xsi:noNamespaceSchemaLocation", Schema)
   except:
      print "Error in AddSchemaRef"

#------------------------------------------------------
#
# Procedure XMLCurvePrincipalPlane:
#
# This method creates and adds a "ByPrincipal" curve definition
# to a given node.
#
#      INPUT:
#
#      Parameters:
#
#      Doc                The XMLDocument
#      Node               The node (element) in th XML document.
#                         A new "ByPrincipal" element will be added
#                         to this node.
#      SurfName           The name of the surface
#      Axis, Coord        Axis ("X", "Y" or "Z") and coordinate value for the principal plane
#      MinPt, MaxPt       Two 3d points (KcsPoint3D) defining the limit box.
#
#
#
#------------------------------------------------------

def XMLCurvePrincipalPlane( Doc, Node, SurfName, Axis, Coord, MinPt, MaxPt):
#
#  Create a new element, "ByPrincipalPlane"
#
   NewElem = Doc.createElement("ByPrincipalPlane")
#
#  Add the child element to the given node
#
   Node.appendChild( NewElem )
#
#  Add the surface name
#
   NewElem.setAttribute( "Surface", SurfName )
#
#  Add the coordinate value
#
   if Axis == "X" or Axis == "x" :
      NewElem.setAttribute( "X", str(Coord) )
   elif Axis == "Y" or Axis == "y":
      NewElem.setAttribute( "Y", str(Coord) )
   else:
      NewElem.setAttribute( "Z", str(Coord) )
#
#  Create a new element, "Box", It will be added under the "ByPrincipalPlane" node
#
   NewElem = Doc.createElement("Box")
   Node.appendChild( NewElem )
#
#  Add the min/max values to the "Box" element.
#
   NewElem.setAttribute( "XMin", str(MinPt.X) )
   NewElem.setAttribute( "YMin", str(MinPt.Y) )
   NewElem.setAttribute( "ZMin", str(MinPt.Z) )
   NewElem.setAttribute( "XMax", str(MaxPt.X) )
   NewElem.setAttribute( "YMax", str(MaxPt.Y) )
   NewElem.setAttribute( "ZMax", str(MaxPt.Z) )


#---------------------------------------------------------------------------
#
#      METHOD:
#
#        XMLPrincipalPlaneCurves
#
#      PURPOSE:
#
#        Create XML "HullCurve" elements for curves defined in a interval of principal
#        planes.
#
#
#
#      INPUT:
#
#      Parameters:
#
#      Doc                XMLDocument
#
#      BlockLimit         integer            0 = ordinary seam
#                                            1 = the seam is a block limit
#
#      SurfName           string             The name of the surface
#
#      NamePrefix         string             The name prefix for the curve
#      NameStartNo        integer            The start number for the curve names.
#      NameNoPartition    integer            The interval for the curve numbers.
#                                            ( Example: NamePrefix = "SPX", NameStartNo = 100
#                                            and NameNoPartition = 10. The first seam will
#                                            be named "SPX100", the second "SPX110" the
#                                            third "SPX120" etc. )
#
#      Axis               string             The coordinate axis: "X", "Y" or "Z".
#      Start              real               Start value
#      Stop               real               Stop value
#      Partition          real               Interval
#
#      MinPt              Point3D            MinPt and MaxPt is the limit box
#      MaxPt              Point3D            for the seams.
#
#
#
#      RESULT:
#
#         The XMLDocument (the DOM-tree) will be updated with
#         new "Seam" elements.
#
#----------------------------------------------------------------------------------------------
def XMLPrincipalPlaneCurves(
   Doc,
   BlockLimit,
   SurfName,
   NamePrefix,
   NameStartNo,
   NameNoPartition,
   Axis,
   Start,
   Stop,
   Partition,
   MinPt,
   MaxPt ):

#
#  Get the root node. (I.e. the "Ship" element).
#
   Root = Doc.documentElement
   CurrentValue  = Start
   CurrentNameNo = NameStartNo
   while CurrentValue <= Stop:
#
#     Create a new "Seam" element.
#
      ShSeam = Doc.createElement("HullCurve")
#
#     Place the new "Seam" element under the "Ship" element
#
      Root.appendChild(ShSeam)
#
#     Add the "ObjName" attribute. (This is the name of the seam to be created)
#
      ObjName = NamePrefix + str(CurrentNameNo)
      ShSeam.setAttribute( "ObjId", ObjName )
#
#     Create XML data for a curve by principal plane
#
      XMLCurvePrincipalPlane( Doc, ShSeam, SurfName, Axis, CurrentValue, MinPt, MaxPt )

      CurrentValue = CurrentValue + Partition
      CurrentNameNo = CurrentNameNo + NameNoPartition
      if Trace == 1:
         print "CurrentValue = ",
         print CurrentValue



#------------------------------------------------------------
# Start of Main Script
#------------------------------------------------------------

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

   if Res == 0:
#
#     Create a new XML document
#
      if Trace == 1:
         print "Create a new XML document"

      NewDoc = Document()
#
#     Add the schema reference.
#
      AddSchemaRef( NewDoc, "" )
      if Trace == 1:
         print "Added Schema Reference"

#
#     Set a limit box.
#
      BoxMin = KcsPoint3D.Point3D( 10000.0,  0.0,     -1000.0 )
      BoxMax = KcsPoint3D.Point3D( 100000.0, 30000.0, 40000.0 )
#
#     Create XML definitions for curves in an interval
#
      try:
         XMLPrincipalPlaneCurves(
            NewDoc,
            0,
            SurfaceName,
            CurvePrefix,
            100,
            10,
            "X",
            20000,
            30000,
            5000,
            BoxMin,
            BoxMax )
      except:
         print "XMLPrincipalPlaneCurves failed!"
         Res = 1

      if Res == 0:
         try:
#
#           Save the XML-tree to a file.
#
            XMLFile = open('c:\\temp\\MyXML.xml', 'w')
            if Trace == 1:
               print "Opened a file"
            try:
               PrettyPrint( NewDoc, XMLFile)
               if Trace == 1:
                  print "Printed XML DOM tree to the file"
            except:
               Res = 1
               print "PrettyPrint failed"

            XMLFile.close()
            if Trace == 1:
               print "Closed the file"
         except:
            Res = 1
            print "Failed to save the XML-tree to the file"

      if Res == 0:
#
#        Run the XML file.
#
         try:
            if Trace == 1:
               print "Calling kcs_chm.run_XML..."
            ModelList = kcs_chm.run_XML('c:\\temp\\MyXML.xml', 'c:\\temp\\MyXML.log')
            if Trace == 1:
               print "run_XML succeeded."
         except:
            print "run_XML failed!"
            print kcs_chm.error
            Res = 1

      if Res == 0:
#
#        Test function output_XML: Generate an XML file from the created model objects.
#
         try:
            if Trace == 1:
               print "Calling kcs_chm.ouput_XML..."
            kcs_chm.output_XML( ModelList, 'c:\\temp\\MyXML2.xml' )
         except:
            print "output_XML failed!"
            print kcs_chm.error
            Res = 1
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
