## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

"""MODULE: cCoordRef v. 1.303
PURPOSE: Define classes CoordRef, and CoordRef3D for manipulating coordinates
expressed as frame or horizontal/vertical longitudinal position references
with the possible offset"""

import string
import stringutils
import kcs_util

axisPrefix = ['FR', 'LP', 'LP'] #Coordinate reference prefix (X, Y, and Z respectively)
axisChar = "XYZ"                #Coordinate characters

class CoordRef:
  """Holds the information about the frame or longitudinal position reference
of the form:
1/ simple coordinate value (e.g. 12500)
2/ FR/LP reference with an optional offset (e.g. FR25, LP5+200, etc.)

The FR/LP number can be a real number (e.g. FR10.5-300).
Offset can be a real number too (e.g. LP3+120.5)

ATTRIBUTES:
  axis           Integer       corresponding axis of the reference
  refPos         Real          FR or LP number
  offset         Real          offset from the refPos position"""

  def __init__(self, refAxis, reference=""):
    """Constructor function:
INPUT parameters:
refAxis    Integer       axis of the reference (1 - X, 2 - Y, 3 - Z)
reference  String        string representation of the position reference
                         if empty, instance is initialized to 0.0

ValueError or AttributeError exceptions will be raised,
if the parameters are not valid."""
    if refAxis in [1,2,3]:
      self.axis = refAxis
      locRef = string.upper(string.strip(reference))
      if locRef == "":
        self.refPos = -11000.0 # no FR/LP reference
        self.offset = 0.0
      elif locRef[:2] == axisPrefix[refAxis-1]: # Is reference a FR/LP reference string?
        n, refLen = 3, len(locRef)
        # FR/LP number could have a SIGN - scan from index 3
        for c in locRef[3:]:
          if (c == "-") or (c == "+"): break
          n = n + 1
        try:
          self.refPos = string.atof(locRef[2:n])
          if n<refLen: self.offset = string.atof(locRef[n:])
          else: self.offset = 0.0
        except:
          raise ValueError, "CoordRef: FR/LP term or offset not valid (%s)!" % reference
      else: # reference is not a FR/LP reference string, try coordinate form (e.g. '20000')
        self.refPos = -11000.0
        try:
          self.offset = string.atof(locRef)
        except: # if none of the accepted string forms are detected, an exception is raised
          raise ValueError, "CoordRef: Reference string syntax error (%s)!" % reference
    else:
      raise ValueError, "CoordRef: Invalid reference axis number (%d)!" % refAxis

  def __repr__(self):
    """Prints the class"""
    if self.refPos < -10000:
      return stringutils.TrimNum(self.offset, 2)
    else:
      s = axisPrefix[self.axis-1] + stringutils.TrimNum(self.refPos, 2)
      if self.offset == 0.0: return s
      else:
        s_offs = stringutils.TrimNum(self.offset, 2)
        if self.offset < 0.0: return s + s_offs
        else: return s + "+" + s_offs

  def __str__(self):
    """Prints the class with the axis indication"""
    return axisChar[self.axis-1] + "=" + repr(self)

  def __float__(self):
    """float(<object>) -> coordinate value (real)

Computes the coordinate value.
If there are problems in computing the value, ValueError exception is raised."""
    if self.refPos > -10000:
      if self.refPos >= 0.0: int_refPos = int(self.refPos + 0.001)
      else: int_refPos = int(self.RefPos - 0.001)
      if abs(self.refPos - int_refPos) < 1.0E-3: # integer FR/LP number
        status, coord = kcs_util.pos_to_coord(self.axis, int_refPos)
      else: # decimal (with fraction) FR/LP number
        if int_refPos > self.refPos: int_refPos = int_refPos - 1
        res = kcs_util.pos_to_coord(self.axis, int_refPos)
        res1 = kcs_util.pos_to_coord(self.axis, int_refPos + 1)
        status = (res[0] != 0 or res1[0] != 0)
        if status == 0:
          coord = res[1] + (res1[1] - res[1])*(self.refPos - int_refPos)
    else:
      status, coord = 0, 0.0
    if status == 0: return coord + self.offset
    else: raise ValueError, "CoordRef: Error computing coordinate (%s)" % str(self)

  def SetPosition(self, ref_No, offs):
    """Sets the refPos and offset attributes of the instance"""
    self.refPos = ref_No
    self.offset = offs

  def __add__(self, other):
    """Implements operation coord + offs, where coord is a CoordRef class instance
and offs is a number. Resulting position is NOT adjusted"""
    p = CoordRef(self.axis)
    p.SetPosition(self.refPos, self.offset + float(other))
    return p

  __radd__ = __add__

  def __sub__ (self, other):
    """Implements operations:
    coord - offs, where coord is a CoordRef class instance and offs is a number.
                  Resulting position is NOT adjusted
    coord1 - coord2, where coord1 and coord2 are both CoordRef class instances.
                  The result is the difference between the coordinates.
                  ValueError exception is raised, if the axes are not the same"""
    if isinstance(other, CoordRef):
      if self.axis == other.axis:
        return float(self) - float(other)
      else:
        raise ValueError, "CoordRef: Cannot subtract positions along different axes!"
    else:
      p = CoordRef(self.axis)
      p.SetPosition(self.refPos, self.offset - float(other))
      return p

  def __rsub__(self, other):
    """Implements operations: offs - coord, and coord1 - coord
where coord, coord1 are CoordRef class instance and offs is a number.
The result is the difference between the coordinates.
ValueError exception is raised, if the axes are not the same"""
    return float(other) - float(self)

  def __cmp__(self, other):
    """Implements comparison operation. Relevant only for both arguments being
the CoordRef class instances along the same axis"""
    try:
      if self.axis == other.axis:
        delta = float(self) - float(other)
        if delta > 0.001: return 1
        elif delta > -0.001: return 0
        else: return -1
      else:
        return 1 #Meaningless result! Cannot compare along different axes!
    except:
      return 1

  def AddOffset(self, offs):
    """Shorthand for coord = coord + offs"""
    self.offset = self.offset + offs

  def Adjust(self):
    """Adjusts current position by recalculating refPos to the closest FR/LP position."""
    try:
      coord = float(self)
      res = kcs_util.coord_to_pos(self.axis, coord)
      if res[0] == 0:
        self.refPos = float(res[1])
        self.offset = res[2]
    except:
      pass

#------------------------------------------------------------------------

class CoordRef3D:
  """Holds an information about the coordinates of a 3D point"""
  def __init__(self, reference):
    """Constructor function.

reference should have the form of a string containing three coordinate
references in the form defined for the CoordRef class, separated by a comma.
The references will be interpreted in sequence as X, Y, and Z."""
    refs = string.splitfields(reference, ',')
    if len(refs) == 3:
      self.X = CoordRef(1, refs[0])
      self.Y = CoordRef(2, refs[1])
      self.Z = CoordRef(3, refs[2])
    else:
      raise ValueError, "CoordRef3D: 3 coordinate references expected!"

  def __repr__(self):
    """Prints the class"""
    return repr(self.X) + ',' + repr(self.Y) + ',' + repr(self.Z)
