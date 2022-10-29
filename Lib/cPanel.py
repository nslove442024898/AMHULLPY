## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

"""MODULE: cPanel v. 1.305
The module for handling different kinds of panel limits, as encountered
in the BOUNDARY statement of the Hull Modelling Language in TRIBON."""

import string
import kcs_hullpan
import KcsPoint2D
import KcsPoint3D
import KcsModel
import kcs_util
import kcs_draft
import kcs_ui
import kcs_dex
import KcsTransformation3D
import cCoordRef

def GetTransformationMatrix(name):
  """GetTransformationMatrix(name) -> Transformation3D class instance (or None)

Uses Data Extraction to retrieve the transfromation matrix for the panel.
If successful, returns the Transformation3D class instance, which can be used
next to transform the panel coordinate system (U,V) points to the ship's
coordinate system (X, Y, Z). If an error occurs, None is returned."""
  st = "HULL.PANEL('" + name + "').TRANSFORMATION_MATRIX"
  if kcs_dex.extract(st) == 0:
    n = kcs_dex.next_result() - 10
    if n == 16:
      get = kcs_dex.get_indexedreal
      tra = KcsTransformation3D.Transformation3D()
      tra.type = 0
      tra.matrix11=get(0)
      tra.matrix12=get(1)
      tra.matrix13=get(2)
      tra.matrix14=get(3)
      tra.matrix21=get(4)
      tra.matrix22=get(5)
      tra.matrix23=get(6)
      tra.matrix24=get(7)
      tra.matrix31=get(8)
      tra.matrix32=get(9)
      tra.matrix33=get(10)
      tra.matrix34=get(11)
      tra.matrix41=get(12)
      tra.matrix42=get(13)
      tra.matrix43=get(14)
      tra.matrix44=get(15)
      return tra
  return None

#------------------------------------------------------------

def GetBoundaryCorners(name, reflected=0):
  """GetBoundaryCorners(name, [reflected])-> corner list

Uses Data Extraction to extract the corner information for the boundary
of the given panel. The corners are given as Point3D class instances.
The coordinates are expressed in the XYZ ship's coordinate system.
In the case of an error, the None object is returned."""
  st1 = "HULL.PANEL('" + name + "')."
  if kcs_dex.extract(st1 + "NBOUNDARY") == 0:
    if kcs_dex.next_result() == 1: # integer result
      nbou = kcs_dex.get_int()
      tra = GetTransformationMatrix(name)
      if tra is not None:
        corners = []
        if kcs_dex.extract(st1 + "BOUNDARY(1:" + str(nbou) + ").CORNER") == 0:
          while kcs_dex.next_result() == 6: # 2D vector result
            cor = kcs_dex.get_reavec2d()
            point = KcsPoint3D.Point3D(cor[0], cor[1])
            point.Transform(tra)
            if reflected: point.Y = -point.Y
            corners.append(point)
          if len(corners) == nbou: return corners

  return None # Error return

#------------------------------------------------------------

def PanelDataType(name):
  """PanelDataType(name) -> integer

Returns the panel's data type, or 0, if the panel does not exist"""
  DT = 0
  if kcs_dex.extract("HULL.PANEL('" + string.upper(name) + "').OC1") == 0:
    if kcs_dex.next_result() == 1:
      DT = kcs_dex.get_int()
  return DT

#------------------------------------------------------------

def FindFreePanelName(prefix, n):
  print "Entering FindFreePanelName"
  maxN = 1
  for k in range(n): maxN = maxN * 10
  id = 1
  format = "%s%0" + str(n) + "d"
  while id < maxN:
    name = format % (prefix, id)

    if PanelDataType(name) == 0: return name
    id = id + 1
  return ""

#------------------------------------------------------------

def pan_delete(panName, CheckSubPanels = 1):
  """pan_delete(panName, [CheckSubPanels = 1]) -> (status, list)

Deletes the given panel from the model. If CheckSubPanels is not
zero, an attempt to delete the subpanels first is performed.

Result:
status - 0 (panel 'panName' deleted), 1 (panel 'panName' NOT deleted)
list   - list of subpanels, that for some reason have not been deleted

NOTE: Would like to have this in kcs_hullpan :-)"""
  def DoDelete(panel, scheme):
    try:
      kcs_hullpan.pan_init(scheme, scheme)
      try:
        kcs_hullpan.stmt_exec(0, "PAN, '%s', DELETE;" % panel)
      finally:
        kcs_hullpan.pan_skip()
      return 0
    except:
      return 1
  uname = string.upper(panName)
  scheme = "DEL_" + uname
  st1 = "HULL.PANEL('" + uname + "')."
  NotDeleted = []
  if CheckSubPanels:
    st = st1 + "NSUBPANEL"

    nSub = 0
    if kcs_dex.extract(st) == 0:
      if kcs_dex.next_result() == 1:
        nSub = kcs_dex.get_int()

    if nSub > 0:
      st = st1 + "SUBPANEL(1:" + str(nSub) + ").NAME"
      names = []
      if kcs_dex.extract(st) == 0:
        while kcs_dex.next_result() == 3:
          names.append(kcs_dex.get_string())

      for name in names:
        if DoDelete(name, scheme):
          NotDeleted.append(name)

  status = DoDelete(uname, scheme)
  return (status, NotDeleted)

#------------------------------------------------------------

def GetModelItem(message, model_type="", level=1):
  """GetModelItem(message [, model_type [, level]]) -> (status, model)

Prompts the user to indicate the model item
  message  - message displayed as a prompt
  model_type - (optional) required model type (default - any)
  level      - (optional) confirmation level:
               0 - no confirmation
               1 - with confirmation, whole model highlighted
               2 - with confirmation, model part highlighted
Result:
  status - kcs_util.ok(), or other status code
  model  - Model class instance"""
  p = KcsPoint2D.Point2D()
  OK = kcs_util.ok()
  CANCEL = kcs_util.cancel()
  YES = kcs_util.yes()
  ref = ["", ", REF"]
  if model_type == "": title = "Get model item"
  else: title = "Get " + model_type
  while 1:
    try:
      res = kcs_ui.point2D_req(message, p)
    except:
      res = [CANCEL]
    if res[0] == OK:
      model = KcsModel.Model()
      try:
        res2 = kcs_draft.model_identify(p, model)
        if model_type != "" and model.Type != model_type:
          kcs_ui.message_confirm(model_type + " expected!")
        elif level == 0: return (OK, model)
        else:
          s = "%s '%s'%s" % (model.Type, model.Name, ref[model.ReflCode])
          if level == 1:
            s = s + ", OK?"
          elif level == 2:
            s = s + (" (%s, ID: %d), OK?" % (model.PartType, model.PartId))
          else:
            s = ""
          if s != "":
            handle = kcs_draft.element_highlight(res2[level])
            ans = kcs_ui.answer_req(title, s)
            kcs_draft.highlight_off(handle)
            if ans == YES: return (OK, model)
      except:
        pass
    else:
      return (res[0], None)

#---------------------------------------------------------------------

class AnyPanelLimit:
  """The base class for all kinds of panel limits

Attributes:
  ref      - reflection status (0 - non-reflected, 1 - reflected)
  add_info - any additional string to be added to the limit definition
             in the BOUNDARY statement"""

  def __init__(self, lref=0):
    """Basic initialization of the class fields"""
    self.ref = lref
    self.add_info = ""

  def StringForm(self):
    """StringForm() -> string

Should be redefined in child classes, and indicate the basic
string form of the limit in the BOUNDARY statement. Additional
tokens will be added by the __repr__ function"""
    return ""

  def __repr__(self):
    """Official representation of the class, as  given in the BOUNDARY statement.
Used by the repr() function"""
    s = self.StringForm()
    if self.add_info != "":
      s = s  + ", " + self.add_info
    if self.ref != 0:
      s = s + ", REF"
    return s

# If repr() function does not uniquely identify the limit,
# the __str__() function should be defined so, that
# it returns a unique identifier of the limit
  __str__ = __repr__

  def AddInfo(self, s):
    """Defines an additional tokens in the limit definition"""
    self.add_info = s

  def IsSameAs(self, other):
    """<object>.IsSameAs(otherLimit) -> Integer

Compares current limit to otherLimit, and returns a status code:
   1  - two limits define the same physical limit
   0  - two limits define the different physical limits
   -1 - otherLimit is not an instance of AnyPanelLimit class, or other error
Comparison is done by comparing the str() function results."""
    try:
      if isinstance(other, AnyPanelLimit):
        res = (str(self) == str(other)) # 1 - same, 0 - not the same
      else:
        res = -1 # not a limit
    except:
      res = -1 # other error (exception caught)
    return res

  def IsSameAsTrusted(self, other):
    """<object>.IsSameAsTrusted(otherLimit) -> Integer

Compares current limit to otherLimit, assuming that otherLimit is
an AnyPanelLimit instance and has a method __str__()
Returns a status code:
   1  - two limits define the same physical limit
   0  - two limits define the different physical limits"""
    return (str(self) == str(other)) # 1 - same, 0 - not the same

#---------------------------------------------------------------------

CoordPrefix = ["X=", "Y=", "Z="]

class CoordinateLimit(AnyPanelLimit):
  """Panel limit given by the coordinate value, for example 2000,
FR20, FR20+200, LP-5+500, itp., as recognized by the CoordRef class

Additional attributes:
   coord   CoordRef  CoordRef class instance describing the position of the limit"""
  def __init__(self, axis, coord_str):
    """CoordinateLimit(axis, coord_str)

axis      - 1 for X, 2 for Y, 3 for Z
coord_str - coordinate position reference as a string

Can raise ValueError or AttributeError exceptions, if coord_str is not valid"""
    AnyPanelLimit.__init__(self)
    self.coord = cCoordRef.CoordRef(axis, coord_str)

  def StringForm(self):
    return repr(self.coord)

  def __del__(self):
    del self.coord

  def Axis(self):
    """Axis() -> Integer

Returns the axis number: 1 for X, 2 for Y, 3 for Z"""
    return self.coord.axis

  def __str__(self):
    return str(self.coord)

#---------------------------------------------------------------------

class PanelLimit(AnyPanelLimit):
  """Panel limit given as the name of the panel, possibly reflected"""
  def __init__(self, panel, lref=0):
    """PanelLimit(panel, lref)

panel - the name of the panel
lref  - reflection code"""
    AnyPanelLimit.__init__(self, lref)
    self.panel = string.upper(panel)

  def StringForm(self):
    return "'" + self.panel + "'"

#---------------------------------------------------------------------

class OuterShellLimit(AnyPanelLimit):
  """Hull form limit, possibly reflected"""
  def StringForm(self):
    return "'__HULLFORM__'"

#---------------------------------------------------------------------

ThreePointsPlane = 99

class Panel:
  """Maintains the list of panel limits, and helps building the BOUNDARY statement

Attributes:
   plane     - identifier of the panel's plane
               (1, 2, 3 for X, Y, Z, or 99 for a panels going through three points)
   boundary  - list of limits (AnyPanelLimit descendants)
   coord     - CoordRef class instance for plane = 1, 2, or 3
   ORI, UAX, VAX - three CoordRef3D class instances for plane = 99"""

  def __init__(self, panelPlane, panelLoc):
    """Panel(panelPlane, panelLoc)

panelPlane - 1 for X, 2 for Y, 3 for Z, 99 for three points plane
panelLoc   - single string as the position reference for panelPlane = 1, 2 or 3, or
             a list of three string describing the 3D coordinates for ORI, UAX and VAX terms"""
    self.plane = panelPlane
    self.boundary = []
    status = 0
    if panelPlane != ThreePointsPlane:
      try:
        self.coord = cCoordRef.CoordRef(panelPlane, panelLoc)
      except:
        status = 1
    elif len(panelLoc) == 3:
      try:
        self.ORI = cCoordRef.CoordRef3D(panelLoc[0])
        self.UAX = cCoordRef.CoordRef3D(panelLoc[1])
        self.VAX = cCoordRef.CoordRef3D(panelLoc[2])
      except:
        status = 1
    else:
      status = 1

    if status != 0:
      raise ValueError, "Panel: Invalid panel location data!"

  def PanelPosition(self):
    """PanelPosition() -> string

Defines the position of the panel in the PANEL statement"""
    if self.plane == ThreePointsPlane:
      return "ORI=" + repr(self.ORI) + ", UAX=" + repr(self.UAX) + \
             ", VAX=" + repr(self.VAX)
    else:
      return str(self.coord)

  def AddLimit(self, new_bou):
    """AddLimit(new_bou) -> integer

Adds a new limit to the limit list. Returns an integer indicating the status of the operation:
  1  - the limit has been added
  0  - the limit was the same, as the recent one
  -1 - the limit was not acceptable (not a limit)"""
    if len(self.boundary) == 0:
      if isinstance(new_bou, AnyPanelLimit): status = 1
      else: status = -1
    else:
      last = self.boundary[-1]
      res = last.IsSameAs(new_bou)
      if res == 1: status = 0
      elif res == 0: status = 1
      else: status = -1
    if status == 1:
      self.boundary.append(new_bou)
    return status

  def RemoveLimitInd(self, index=-1):
    """RemoveLimitInd(index)

Removes the given limit from the boundary list. index is optional.
If not given, defaults to -1 indicating the last limit to be removed"""
    try:
      del self.boundary[index]
    except:
      pass

  def RemoveLimit(self, limit):
    """RemoveLimit(limit)

Removes all occurrances of the limit equivalent to the limit given as an argument
in terms of the IsSameAsTrusted method"""
    if isinstance(limit, AnyPanelLimit):
      lb = len(self.boundary)
      i = 0
      while i < lb:
        if limit.IsSameAsTrusted(self.boundary[i]) == 1:
          del self.boundary[i]
          lb = lb - 1
        else:
          i = i + 1

  def BoundaryStmt(self, bou_list = None):
    """BoundaryStmt(bou_list) -> string

Returns the text of the BOUNDARY statement, as defined by the limits in the bou_list.
If bou_list is not given, the function processes the self.boundary list """
    if bou_list is None: BList = self.boundary
    else: BList = bou_list
    return "BOU, " + string.joinfields(map(str, BList), "/ ") + ";"

  def CheckBoundary(self, block, name, location):
    """CheckBoundary(block, name, location) -> (status, list of corners)

Creates a dummy panel using the self.boundary limit list. If correct, reads
the corner coordinates and returns it in the result tuple.
Input parameters:
    block    - hull block name
    name     - dummy panel name
    location - one of: 'P', 'S', 'SP' - location code of the panel

Output parameters (status):
    0 - everything OK
    1 - error initializing panel/scheme (pan_init)
    2 - error on PANEL statement
    3 - error on BOUNDARY statement
    4 - error in getting panel corners
Higher error code means, that the previous checks passed"""
    stPAN = "PAN, '%s', %s, BLO='%s', DT=191, %s;" % \
       (name, location, block, self.PanelPosition())
    stBOU = self.BoundaryStmt()
    stPLA = "PLA, MAT=10;"
    status = 1
    try:
      try:
        kcs_hullpan.pan_init(name, name)
        status = 2
        kcs_hullpan.stmt_exec(0, stPAN)
        status = 3
        kcs_hullpan.stmt_exec(0, stBOU)
        kcs_hullpan.stmt_exec(0, stPLA)
#        kcs_hullpan.pan_store()
        status = 4
        res = GetBoundaryCorners(name)
        if res is not None: status = 0
# Try to delete the dummy box panel from the model views
        model = KcsModel.Model("plane panel", name)
        try:
          kcs_draft.model_delete(model)
        except:
          pass
      finally:
        kcs_hullpan.pan_skip()
    except:
      pass

    if status == 0:
      return (status, res)
    else:
      return (status, None) # Error return
