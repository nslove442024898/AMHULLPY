## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsHighlightSet.py
#
#      PURPOSE:
#          The HighlightSet class holds information about elements to highlight
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          private:
#           __Elements    list              list of elements to highlight
#
#      METHODS:
#        AddGeometry2D                      Adds 2d graphical element to highlight set
#        AddGeometry3D                      Adds 3d graphical element to highlight set
#        AddModel                           Adds Model to highlight element set
#        AddSubpicture                      Adds Subpicture to highlight set
#        Reset                              Removes all elements from highlight set

import types
import KcsPoint2D
import KcsArc2D
import KcsRectangle2D
import KcsContour2D
import KcsPoint3D
import KcsPolygon3D
import KcsModel
import KcsElementHandle
import KcsLinetype

ErrorMessages = { TypeError : 'not supported argument type, see documentation of HighlightSet class' }


class HighlightSet(object):

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
# -----------------------------------------------------------------------------------------------------------------

   def __init__(self):
      self.__Elements  = []

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddGeometry2D
#
#      PURPOSE:
#          To add graphical 2D element to highlight set
#
#      INPUT:
#          Parameters:
#           Element          	    Instance of Point2D, Arc2D, Rectangle2D, Contour2D
#           KcsLinetype.Linetype    Linetype used to highlight point
#
# -----------------------------------------------------------------------------------------------------------------

   def AddGeometry2D(self, element, linetype = None):
      if linetype!= None and not isinstance(linetype, KcsLinetype.Linetype):
         raise TypeError, ErrorMessages[TypeError]

      if isinstance(element, KcsPoint2D.Point2D)     or\
         isinstance(element, KcsArc2D.Arc2D)         or\
         isinstance(element, KcsContour2D.Contour2D) or\
         isinstance(element, KcsRectangle2D.Rectangle2D):
            self.__Elements.append( [ element, linetype ] )
      else:
        raise TypeError, ErrorMessages[TypeError]

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddGeometry3D
#
#      PURPOSE:
#          To add graphical 3D element to highlight set
#
#      INPUT:
#          Parameters:
#           Element          	             Instance of Point3D, Polygon3D
#           KcsLinetype.Linetype             Linetype used to highlight point
#           KcsElementHandle.ElementHandle   Handle of view to display geometry or None for all views
#
# -----------------------------------------------------------------------------------------------------------------

   def AddGeometry3D(self, element, viewHandle = None, linetype = None):
      if linetype!= None and not isinstance(linetype, KcsLinetype.Linetype):
         raise TypeError, ErrorMessages[TypeError]

      if viewHandle != None and not isinstance(viewHandle, KcsElementHandle.ElementHandle):
         raise TypeError, ErrorMessages[TypeError]
	
      if isinstance(element, KcsPoint3D.Point3D)  or\
         isinstance(element, KcsPolygon3D.Polygon3D) :
           self.__Elements.append( [ element, linetype, viewHandle ] )
      else:
         raise TypeError, ErrorMessages[TypeError]

#-----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddModel
#
#      PURPOSE:
#          To add Model to highlight set
#
#      INPUT:
#          Parameters:
#           KcsModel.Model          KcsModel class
#
# -----------------------------------------------------------------------------------------------------------------

   def AddModel(self, model ):
      if isinstance( model, KcsModel.Model ):
         self.__Elements.append( [ model ] )
      else:
         raise TypeError, ErrorMessages[TypeError]

#-----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          AddSubpicture
#
#      PURPOSE:
#          To add View, subview or component to highlight set
#
#      INPUT:
#          Parameters:
#           KcsElementHandle.ElementHandle        Handle of subpicture
#
# -----------------------------------------------------------------------------------------------------------------

   def AddSubpicture(self, handle ):
      if not isinstance( handle, KcsElementHandle.ElementHandle):
         raise TypeError, ErrorMessages[TypeError]
      else:
         self.__Elements.append( [ handle ] )


#-----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          Reset
#
#      PURPOSE:
#          To remove all elements from highlight set
#
#      INPUT:
#          Parameters:
#           None
# -----------------------------------------------------------------------------------------------------------------

   def Reset(self):
       self.__Elements = []

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
# -----------------------------------------------------------------------------------------------------------------

   def __repr__(self):
      return 'HighlightSet: %s' % (self.__Elements)

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#

   def GetElements(self): return self.__Elements
   Elements    = property (GetElements, None, None, 'Elements - list of elements in highlight set')
