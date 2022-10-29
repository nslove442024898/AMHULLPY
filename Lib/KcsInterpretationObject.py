## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsInterpretationObject.py
#
#      PURPOSE:
#
#          To send options for interpretation during creation of view objects, curved
#          panel.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#

import string
import copy
import types

import KcsPoint3D
import KcsVector3D
import KcsBox

class SymbolicView(object):

   PLANE_BY_X            = -1
   PLANE_BY_Y            = -2
   PLANE_BY_Z            = -3
   PLANE_BY_3POINTS      = -5
   PLANE_BY_PANEL        = -4
   PLANE_BY_CURVE        = -6
   PLANE_BY_RSO          = -7

   TYPE_PANEL              = 0
   TYPE_BRACKET            = 1
   TYPE_STIFFENER          = 2
   TYPE_FLANGE             = 3

   VIEW_DESIGN             = 0
   VIEW_ASSEMBLY           = 1

   CURVE_EXISTING          = 1
   CURVE_BY_NAME           = 0
   CURVE_CUT               = 2
   CURVE_NONE              = 0

   LOOKING_FOR             = 4
   LOOKING_AFT             = 3
   LOOKING_PS              = 1
   LOOKING_SB              = 2
   LOOKING_TOP             = 5
   LOOKING_BOT             = 6

   __ErrorMessages = { TypeError : 'not supported argument type, see documentation of SymbolicView class',
                       ValueError: 'not supported value, see documentation of SymbolicView class' }

#-----------------------------------------------------------------------
   def __init__(self):
      'inits SymbolicView'

      self.__ViewName   = ''
      self.__Looking  = SymbolicView.LOOKING_FOR

      self.__PlaneType  = SymbolicView.PLANE_BY_X

      self.__Origin     = KcsPoint3D.Point3D()
      self.__UAxis      = KcsPoint3D.Point3D()
      self.__VAxis      = KcsPoint3D.Point3D()

      self.__DepthBefore = 100.0
      self.__DepthBehind = 100.0

      self.__ObjectName  = ''
      self.__CompType    = SymbolicView.TYPE_PANEL
      self.__CompNo      = 0
      self.__Reflect     = 0
      self.__OnlyCurrent = 0

      self.__LimMin      = KcsPoint3D.Point3D(-500000, -500000, -500000)
      self.__LimMax      = KcsPoint3D.Point3D( 500000,  500000,  500000)

      self.__ViewType    = SymbolicView.VIEW_DESIGN

      self.__ShellCurveType = SymbolicView.CURVE_EXISTING

      self.__DrawRSO             = 0
      self.__GAView              = 0
      self.__ShellProfiles       = 1
      self.__ShellSeams          = 1
      self.__DrawPlaneViews      = 1
      self.__DrawIntersections   = 1
      self.__AutomaticSelection  = 0
      self.__DrawAsPlate         = 0
      self.__PanelsFilter        = []
      self.__PanelsExclude       = 0
      self.__BlocksFilter        = []
      self.__BlocksExclude       = 0

      self.__ShellCurves         = []
      self.__Assemblies          = []
      #Outfitting options
      self.__DrawPIPE            = 0
      self.__DrawEQUI            = 0
      self.__DrawCWAY            = 0
      self.__DrawSTRU            = 0
      self.__DrawVENT            = 0
      self.__DrawROOM            = 0
      self.__ShThick             = 0
      self.__CrossSection        = 0

#-----------------------------------------------------------------------

   def SetViewName(self, name):
      'sets symbolic view name'

      if type(name) != type(''):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]
      self.__ViewName = string.upper(name)

#-----------------------------------------------------------------------

   def GetViewName(self):
      'returns symbolic view name'

      return self.__ViewName

#-----------------------------------------------------------------------

   def __repr__(self):
      'returns string representation of SymbolicView object'
      planetup = ()
      viewtup = ()

      if self.__Looking == SymbolicView.LOOKING_FOR:
         strLooking = 'FOR'
      elif self.__Looking == SymbolicView.LOOKING_AFT:
         strLooking = 'AFT'
      elif self.__Looking == SymbolicView.LOOKING_PS:
         strLooking = 'PS'
      elif self.__Looking == SymbolicView.LOOKING_SB:
         strLooking = 'SB'
      elif self.__Looking == SymbolicView.LOOKING_TOP:
         strLooking = 'TOP'
      elif self.__Looking == SymbolicView.LOOKING_BOT:
         strLooking = 'BOT'

      if self.__PlaneType == SymbolicView.PLANE_BY_X:
         strPlaneType = 'By X'
      elif self.__PlaneType == SymbolicView.PLANE_BY_Y:
         strPlaneType = 'By Y'
      elif self.__PlaneType == SymbolicView.PLANE_BY_Z:
         strPlaneType = 'By Z'
      elif self.__PlaneType == SymbolicView.PLANE_BY_3POINTS:
         strPlaneType = 'By 3 points'
      elif self.__PlaneType == SymbolicView.PLANE_BY_PANEL:
         strPlaneType = 'By panel'
         if self.__CompType == SymbolicView.TYPE_PANEL:
            strCompType = 'Panel'
         elif self.__CompType == SymbolicView.TYPE_BRACKET:
            strCompType = 'Bracket'
         elif self.__CompType == SymbolicView.TYPE_STIFFENER:
            strCompType = 'Stiffener'
         elif self.__CompType == SymbolicView.TYPE_FLANGE:
            strCompType = 'Flange'
         planetup = (
            '   ObjectName: ' + self.__ObjectName,
            '   CompType: ' + strCompType,
            '   CompNo: ' + str(self.__CompNo),
            '   Reflect: ' + str(self.__Reflect),
            '   OnlyCurrent: ' + str(self.__OnlyCurrent)
            )
      elif self.__PlaneType == SymbolicView.PLANE_BY_CURVE:
         strPlaneType = 'By curve'
         planetup = (
            '   ObjectName: ' + self.__ObjectName,
            '   Reflect: ' + str(self.__Reflect),
            )
      elif self.__PlaneType == SymbolicView.PLANE_BY_RSO:
         strPlaneType = 'By RSO'
         planetup = (
            '   ObjectName: ' + self.__ObjectName,
            '   CompNo: ' + str(self.__CompNo),
            )

      if self.__PlaneType in [SymbolicView.PLANE_BY_X,SymbolicView.PLANE_BY_Y,\
                              SymbolicView.PLANE_BY_Z,SymbolicView.PLANE_BY_3POINTS]:
         planetup = ('   Origin: ' + str(self.__Origin),)
         if self.__PlaneType == SymbolicView.PLANE_BY_3POINTS:

            planetup += (
            '   UAxis: ' + str(self.__UAxis),
            '   VAxis: ' + str(self.__VAxis),
            )

      if self.__ViewType == SymbolicView.VIEW_DESIGN:
         if self.__ShellCurveType == SymbolicView.CURVE_EXISTING:
            strShellCurveType = 'Existing'
         elif self.__ShellCurveType == SymbolicView.CURVE_BY_NAME:
            strShellCurveType = 'By name\n   ShellCurves: ' + str(self.__ShellCurves)
         elif self.__ShellCurveType == SymbolicView.CURVE_CUT:
            strShellCurveType = 'Cut'
         elif self.__ShellCurveType == SymbolicView.CURVE_NONE:
            strShellCurveType = 'None'
         viewtup = (
            '   ViewType: DESIGN',
            '   ShellCurveType: ' + strShellCurveType,
            '   ShellProfiles: ' + str(self.__ShellProfiles),
            '   ShellSeams: ' + str(self.__ShellSeams),
            '   DrawRSO: ' + str(self.__DrawRSO),
            '   DrawAsPlate: ' + str(self.__DrawAsPlate),
            '   AutomaticSelection: ' + str(self.__AutomaticSelection),
            '   GAView: ' + str(self.__GAView),
            )
         if self.__PanelsExclude:
            viewtup += ('   Panels Excluded: ' + str(self.__PanelsFilter),)
         else:
            viewtup += ('   Panels Included: ' + str(self.__PanelsFilter),)
         if self.__BlocksExclude:
            viewtup += ('   Blocks Excluded: ' + str(self.__BlocksFilter),)
         else:
            viewtup += ('   Blocks Included: ' + str(self.__BlocksFilter),)
      else: #SymbolicView.VIEW_ASSEMBLY
         viewtup = (
            '   ViewType: ASSEMBLY',
            '   Assemblies: ' + str(self.__Assemblies)
            )

      tup = (
         'SymbolicView:',
         '   View name: ' + self.__ViewName,
         '   Looking: ' + strLooking,
         '   Plane: ' + strPlaneType,
         ) + planetup + (
         '   Depth before: ' + str(self.__DepthBefore),
         '   Depth behind: ' + str(self.__DepthBehind),
         '   LimMin: ' + str(self.__LimMin),
         '   LimMax: ' + str(self.__LimMax),
         ) + viewtup + (
         '   DrawPlaneViews: ' + str(self.__DrawPlaneViews),
         '   DrawIntersections: ' + str(self.__DrawIntersections),
         )
      return string.join(tup, '\n')

#-----------------------------------------------------------------------

   def SetPlaneByX(self, coord):
      'allows user to specify plane by X coordinate'

      self.__PlaneType  = SymbolicView.PLANE_BY_X
      self.__Origin.SetCoordinates(coord, 0.0, 0.0)

#-----------------------------------------------------------------------

   def SetPlaneByY(self, coord):
      'allows user to specify plane by Y coordinate'

      self.__PlaneType  = SymbolicView.PLANE_BY_Y
      self.__Origin.SetCoordinates(0.0, coord, 0.0)

#-----------------------------------------------------------------------

   def SetPlaneByZ(self, coord):
      'allows user to specify plane by Z coordinate'

      self.__PlaneType  = SymbolicView.PLANE_BY_Z
      self.__Origin.SetCoordinates(0.0, 0.0, coord)

#-----------------------------------------------------------------------

   def SetPlaneBy3Points(self, origin, uaxis, vaxis):
      'specify plane by 3 points'

      if not isinstance(origin, KcsPoint3D.Point3D) or \
         not isinstance(uaxis, KcsPoint3D.Point3D) or \
         not isinstance(vaxis, KcsPoint3D.Point3D):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__PlaneType  = SymbolicView.PLANE_BY_3POINTS
      self.__Origin = copy.deepcopy(origin)
      self.__UAxis  = copy.deepcopy(uaxis)
      self.__VAxis  = copy.deepcopy(vaxis)

#-----------------------------------------------------------------------

   def SetPlaneByPanel(self, panel, comptype, compno, reflect, onlycurrent):
      'specify plane by panel'

      if type(panel) != type('') or type(comptype) != type(1) or type(compno) != type(1):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]
      if comptype != self.TYPE_PANEL and comptype != self.TYPE_BRACKET \
         and comptype != self.TYPE_STIFFENER and comptype != self.TYPE_FLANGE:
         raise ValueError, SymbolicView.__ErrorMessages[ValueError]

      self.__PlaneType = SymbolicView.PLANE_BY_PANEL
      self.__ObjectName   = string.upper(panel)
      self.__CompType    = comptype
      self.__CompNo      = compno
      if reflect:
         self.__Reflect     = 1
      else:
         self.__Reflect     = 0
      if onlycurrent:
         self.__OnlyCurrent = 1
      else:
         self.__OnlyCurrent = 0

#-----------------------------------------------------------------------
   def SetPlaneByCurve(self, curve, reflect):
      'specify plane by curve'

      if type(curve) != type(''):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__PlaneType = SymbolicView.PLANE_BY_CURVE
      self.__ObjectName = string.upper(curve)
      if reflect:
         self.__Reflect = 1
      else:
         self.__Reflect = 0

#-----------------------------------------------------------------------
   def SetPlaneByRSO(self, object, compno):
      'specify plane by RSO'

      if type(object) != type('') or type(compno) != type(1):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__PlaneType = SymbolicView.PLANE_BY_RSO
      self.__ObjectName = string.upper(object)
      self.__CompNo = compno

#-----------------------------------------------------------------------
   def GetPlaneType(self):
      'returns plane type'

      return self.__PlaneType

#-----------------------------------------------------------------------
   def GetOrigin(self):

      return self.__Origin

#-----------------------------------------------------------------------
   def GetUAxis(self):

      return self.__UAxis

#-----------------------------------------------------------------------
   def GetVAxis(self):

      return self.__VAxis

#-----------------------------------------------------------------------
   def IsReflect(self):
      'returns status of reflect flag'

      return self.__Reflect

#-----------------------------------------------------------------------
   def IsOnlyCurrent(self):
      'returns status of only current flag'

      return self.__OnlyCurrent

#-----------------------------------------------------------------------
   def GetComponentNo(self):
      'returns component number'

      return self.__CompNo

#-----------------------------------------------------------------------
   def GetComponentType(self):
      'returns component type'

      return self.__CompType

#-----------------------------------------------------------------------
   def GetObjectName(self):
      'returns object (panel, curve or RSO name) name'

      return self.__ObjectName

#-----------------------------------------------------------------------
   def SetLooking(self, looking):
      'specify looking way'

      if type(looking) != type(self.LOOKING_FOR):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      if looking != self.LOOKING_FOR and looking != self.LOOKING_AFT \
         and looking != self.LOOKING_PS and looking != self.LOOKING_SB \
         and looking != self.LOOKING_TOP and looking != self.LOOKING_BOT:
         raise ValueError, SymbolicView.__ErrorMessages[ValueError]

      self.__Looking  = looking

#-----------------------------------------------------------------------
   def GetLooking(self):
      'returns looking way'

      return self.__Looking

#-----------------------------------------------------------------------
   def SetDepth(self, before, behind):
      'sets before and behind depths'
      if (type(before) != type(0.0) and type(before) != type(1)) or\
         (type(behind) != type(0.0) and type(behind) != type(1)):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__DepthBefore = before;
      self.__DepthBehind = behind;

#-----------------------------------------------------------------------
   def GetDepth(self):
      'returns before and behind depths'

      return (self.__DepthBefore, self.__DepthBehind)

#-----------------------------------------------------------------------
   def SetLimits(self, min3d, max3d):
      'sets limits'

      if not isinstance(min3d, KcsPoint3D.Point3D) or not isinstance(max3d, KcsPoint3D.Point3D):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__LimMin = copy.deepcopy(min3d);
      self.__LimMax = copy.deepcopy(max3d);

#-----------------------------------------------------------------------
   def GetLimits(self):
      'returns limits'

      return (copy.deepcopy(self.__LimMin), copy.deepcopy(self.__LimMax))

#-----------------------------------------------------------------------
   def SetViewType(self, viewtype):
      'allows user to set view type'

      if type(viewtype) != type(1):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      if viewtype != self.VIEW_DESIGN and viewtype != self.VIEW_ASSEMBLY:
         raise ValueError, SymbolicView.__ErrorMessages[ValueError]

      self.__ViewType = viewtype

#-----------------------------------------------------------------------

   def GetViewType(self):
      'returns view type'

      return self.__ViewType

#-----------------------------------------------------------------------

   def SetShellCurves(self, curvetype, curves=[]):
      'Allows user to set shell curve type and names (optional). Valid only for design view!'

      if type(curvetype) != type(1) or (type(curves) != types.TupleType and type(curves) != types.ListType):
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      if curvetype != self.CURVE_EXISTING and curvetype != self.CURVE_BY_NAME and \
         curvetype != self.CURVE_CUT and curvetype != self.CURVE_NONE:
         raise ValueError, SymbolicView.__ErrorMessages[ValueError]

      self.__ShellCurves = []
      for item in curves:
         if type(item) != type(''):
            raise ValueError, SymbolicView.__ErrorMessages[ValueError]
         else:
            self.__ShellCurves.append(item)

      self.__ShellCurveType   = curvetype

#-----------------------------------------------------------------------

   def GetShellCurveType(self):
      'Returns shell curve type. Valid only if desing view'

      return self.__ShellCurveType

#-----------------------------------------------------------------------

   def GetShellCurves(self):
      'Returns shell curve names. Valid only if design view and CURVE_BY_NAME type specified.'

      return copy.deepcopy(self.__ShellCurves)

#-----------------------------------------------------------------------

   def SetDrawRSO(self, value):
      'Sets draw RSO flag'

      if value:
         self.__DrawRSO = 1
      else:
         self.__DrawRSO = 0

#-----------------------------------------------------------------------

   def GetDrawRSO(self):
      'Returns status of draw RSO flag'

      return self.__DrawRSO
#-----------------------------------------------------------------------

   def SetGAView(self, value):
      'Sets GA View flag'

      if value:
         self.__GAView = 1
      else:
         self.__GAView = 0

#-----------------------------------------------------------------------

   def GetGAView(self):
      'Returns status of GA View flag'

      return self.__GAView

#-----------------------------------------------------------------------

   def SetShellProfiles(self, value):
      'Sets shell profiles flag. Valid only if design view.'

      if value:
         self.__ShellProfiles = 1
      else:
         self.__ShellProfiles = 0

#-----------------------------------------------------------------------

   def GetShellProfiles(self):
      'Returns status of shell profiles flag. Valid only if design view.'

      return self.__ShellProfiles

#-----------------------------------------------------------------------

   def SetShellSeams(self, value):
      'Sets shell seams flag. Valid only if design view.'

      if value:
         self.__ShellSeams = 1
      else:
         self.__ShellSeams = 0

#-----------------------------------------------------------------------

   def GetShellSeams(self):
      'Returns status of shell seams flag. Valid only if design view.'

      return self.__ShellSeams

#-----------------------------------------------------------------------

   def SetDrawPlaneViews(self, value):
      'Sets draw plane views flag. Valid only if design view.'

      if value:
         self.__DrawPlaneViews = 1
      else:
         self.__DrawPlaneViews = 0

#-----------------------------------------------------------------------

   def GetDrawPlaneViews(self):
      'Returns status of draw plane views flag. Valid only if design view.'

      return self.__DrawPlaneViews

#-----------------------------------------------------------------------

   def SetDrawIntersections(self, value):
      'Sets draw intersections flag. Valid only if design view.'

      if value:
         self.__DrawIntersections = 1
      else:
         self.__DrawIntersections = 0

#-----------------------------------------------------------------------

   def GetDrawIntersections(self):
      'Returns status of draw intersections flag. Valid only if design view.'

      return self.__DrawIntersections

#-----------------------------------------------------------------------

   def SetAutomaticSelection(self, value):
      'Sets automatic selection flag. Valid only if design view.'

      if value:
         self.__AutomaticSelection = 1
      else:
         self.__AutomaticSelection = 0

#-----------------------------------------------------------------------

   def GetAutomaticSelection(self):
      'Returns status of automatic selection flag. Valid only if design view.'

      return self.__AutomaticSelection

#-----------------------------------------------------------------------

   def SetDrawAsPlate(self, value):
      'Sets draw as plate flag. Valid only if design view.'

      if value:
         self.__DrawAsPlate = 1
      else:
         self.__DrawAsPlate = 0

#-----------------------------------------------------------------------

   def GetDrawAsPlate(self):
      'Returns draw as plate flag. Valid only if design view.'

      return self.__DrawAsPlate

#-----------------------------------------------------------------------

   def SetPanelsFilter(self, panels, exclude=0):
      'Sets panels list and exclude flag. Valid only if design view.'

      if type(panels) != types.ListType and type(panels) != types.TupleType:
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__PanelsFilter = []

      for item in panels:
         if type(item) != type(''):
            raise ValueError, SymbolicView.__ErrorMessages[ValueError]
         else:
            self.__PanelsFilter.append(item)

      if exclude:
         self.__PanelsExclude = 1
      else:
         self.__PanelsExclude = 0

#-----------------------------------------------------------------------

   def GetPanelsFilter(self):
      'Returns panels filter list and exclude flag. Valid only if design view.'

      return (copy.deepcopy(self.__PanelsFilter), self.__PanelsExclude)

#-----------------------------------------------------------------------

   def SetBlocksFilter(self, blocks, exclude=0):
      'Sets blocks list and exclude flag. Valid only if design view.'

      if type(blocks) != types.ListType and type(blocks) != types.TupleType:
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__BlocksFilter = []

      for item in blocks:
         if type(item) != type(''):
            raise ValueError, SymbolicView.__ErrorMessages[ValueError]
         else:
            self.__BlocksFilter.append(item)

      if exclude:
         self.__BlocksExclude = 1
      else:
         self.__BlocksExclude = 0

#-----------------------------------------------------------------------

   def GetBlocksFilter(self):
      'Returns blocks filter list and exclude flag. Valid only if design view.'

      return (copy.deepcopy(self.__BlocksFilter), self.__BlocksExclude)

#-----------------------------------------------------------------------

   def SetAssemblies(self, assemblies):
      'Sets assemblies list. Valid only if assembly view.'

      if type(assemblies) != types.ListType and type(assemblies) != types.TupleType:
         raise TypeError, SymbolicView.__ErrorMessages[TypeError]

      self.__Assemblies = []

      for item in assemblies:
         if type(item) != type(''):
            raise ValueError, SymbolicView.__ErrorMessages[ValueError]
         else:
            self.__Assemblies.append(item)

#-----------------------------------------------------------------------

   def GetAssemblies(self):
      'Returns assemblies. Valid only if assembly view.'

      return copy.deepcopy(self.__Assemblies)

#-------------------------------------------------------------------------------------

   def SetDrawPipes(self, Val):      
      if Val:
         self.__DrawPIPE = 1
      else:
         self.__DrawPIPE = 0
         
   def GetDrawPipes(self):
      return self.__DrawPIPE
      
#-------------------------------------------------------------------------------------

   def SetDrawEquipment(self, Val):
      if Val:
         self.__DrawEQUI = 1
      else:
         self.__DrawEQUI = 0
         
   def GetDrawEquipment(self):
      return self.__DrawEQUI
      
#-------------------------------------------------------------------------------------      

   def SetDrawCableways(self, Val):
      if Val:
         self.__DrawCWAY = 1
      else:
         self.__DrawCWAY = 0
         
   def GetDrawCableways(self):
      return self.__DrawCWAY
      
#-------------------------------------------------------------------------------------      

   def SetDrawStructures(self, Val):
      if Val:
         self.__DrawSTRU = 1
      else:
         self.__DrawSTRU = 0
         
   def GetDrawStructures(self):
      return self.__DrawSTRU
      
#-------------------------------------------------------------------------------------      

   def SetDrawVentilation(self, Val):
      if Val:
         self.__DrawVENT = 1
      else:
         self.__DrawVENT = 0
         
   def GetDrawVentilation(self):
      return self.__DrawVENT
            
#-------------------------------------------------------------------------------------      

   def SetDrawRoomDesign(self, Val):
      if Val:
         self.__DrawROOM = 1
      else:
         self.__DrawROOM = 0
         
   def GetDrawRoomDesign(self):
      return self.__DrawROOM
            
   def SetShThick(self, Val):
      if Val:
         self.__ShThick = 1
      else:
         self.__ShThick = 0

   def GetShThick(self):
      return self.__ShThick
   
#-------------------------------------------------------------------------------------      

   def SetCrossSectionSymbols(self, Val):
      if Val:
         self.__CrossSection = 1
      else:
         self.__CrossSection = 0
         
   def GetCrossSectionSymbols(self):
      return self.__CrossSection      
      

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   ViewName = property (GetViewName, SetViewName, None, 'ViewName - name of symbolic view')
   PlaneType = property (GetPlaneType, None, None, 'PlaneType - type of plane definition')

   def GetOrigin(self): return self.__Origin
   Origin = property (GetOrigin, None, None, 'Origin')
   def GetUAxis(self): return self.__UAxis
   UAxis = property (GetUAxis, None, None, 'UAxis')
   def GetVAxis(self): return self.__VAxis
   VAxis = property (GetVAxis, None, None, 'VAxis')

   Reflect = property (IsReflect, None, None, 'Reflect - reflect flag')
   OnlyCurrent = property (IsOnlyCurrent, None, None, 'OnlyCurrent - only current flag')
   CompNo = property (GetComponentNo, None, None, 'CompNo - component number')
   CompType = property (GetComponentType, None, None, 'CompType - component type')
   ObjectName = property (GetObjectName, None, None, 'ObjectName - object (panel, curve or RSO name) name ')
   Looking = property (GetLooking, SetLooking, None, 'Looking - looking way flag')

   def GetDepthBefore(self): return self.__DepthBefore
   def SetDepthBefore(self, value): self.SetDepth(value, self.__DepthBehind)
   DepthBefore = property (GetDepthBefore, SetDepthBefore, None, 'DepthBefore - depth before')
   def GetDepthBehind(self): return self.__DepthBehind
   def SetDepthBehind(self, value): self.SetDepth(self.__DepthBefore, value)
   DepthBehind = property (GetDepthBehind, SetDepthBehind, None, 'DepthBehind - depth behind')

   def GetLimMin(self): return self.__LimMin
   def SetLimMin(self, value): self.SetLimits(value, self.__LimMax)
   LimMin = property (GetLimMin, SetLimMin, None, 'LimMin - minimal limit')
   def GetLimMax(self): return self.__LimMax
   def SetLimMax(self, value): self.SetLimits(self.__LimMin, value)
   LimMax = property (GetLimMax, SetLimMax, None, 'LimMax - maximal limit')

   ViewType = property (GetViewType, SetViewType, None, 'ViewType')
   ShellCurves = property (GetShellCurves, None, None, '')
   ShellCurveType = property (GetShellCurveType, None, None, '')
   DrawRSO = property (GetDrawRSO, SetDrawRSO, None, 'DrawRSO - draw RSO flag')
   GAView = property (GetGAView, SetGAView, None, 'GAView - GA View flag')
   ShellProfiles = property (GetShellProfiles, SetShellProfiles, None, 'ShellProfiles - shell profiles flag valid for design view')
   ShellSeams = property (GetShellSeams, SetShellSeams, None, 'ShellSeams - shell seams flag valid for design view')
   DrawPlaneViews = property (GetDrawPlaneViews, SetDrawPlaneViews, None, '')
   DrawIntersections = property (GetDrawIntersections, SetDrawIntersections, None, 'DrawIntersections')
   AutomaticSelection = property (GetAutomaticSelection,SetAutomaticSelection, None, 'AutomaticSelection')
   DrawAsPlate = property (GetDrawAsPlate, SetDrawAsPlate, None, 'DrawAsPlate')
   Assemblies = property (GetAssemblies, SetAssemblies, None, 'Assemblies')

   def GetPanelsFilterOnly(self): return self.__PanelsFilter
   PanelsFilter = property (GetPanelsFilterOnly, None, None, 'PanelsFilter - list of panels to include/exclude')
   def GetPanelsExclude(self): return self.__PanelsExclude
   PanelsExclude = property (GetPanelsExclude, None, None, 'PanelsExclude - include/exclude flag')

   def GetBlocksFilterOnly(self): return self.__BlocksFilter
   BlocksFilter = property (GetBlocksFilterOnly, None, None, 'BlocksFilter - list of blocks to include/exclude')
   def GetBlocksExclude(self): return self.__PanelsExclude
   BlocksExclude = property (GetBlocksExclude, None, None, 'BlocksExclude - include/exclude flag')

   Pipes = property (GetDrawPipes, SetDrawPipes, None, '')
   Equipment = property (GetDrawEquipment, SetDrawEquipment, None, '')
   Cableways = property (GetDrawCableways, SetDrawCableways, None, '')
   Structures = property (GetDrawStructures, SetDrawStructures, None, '')
   Ventilation = property (GetDrawVentilation, SetDrawVentilation, None, '')
   RoomDesign = property (GetDrawRoomDesign, SetDrawRoomDesign, None, '')
   ShellThickness = property (GetShThick, SetShThick, None, '')
   CrossSectionSymbols = property (GetCrossSectionSymbols, SetCrossSectionSymbols, None, '')

#-----------------------------------------------------------------------
class CurvedPanelView(object):

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#

   def __init__(self):
      """
      Default setting [] in attribute list below

      ATTRIBUTES:
           Seams          integer           Seams in view [1=Yes]/0=No
           SeamNames      integer           Seam names in view [1=Yes]/0=No
           Plates         integer           Plates in view [1=Yes]/0=No
           Material       integer           Material specification in view 1=Yes/[0=No]
           Stiffeners     integer           Stiffeners in view [1=Yes]/0=No
           StiffNames     integer           Siffener names in view 1=Yes/[0=No]
           Endcuts        integer           Display endcuts in view 1=Yes/[0=No]
           Jigs           integer           Display jigs in view [1=Yes]/0=No
           Heights        integer           Display jig heights in view 1=Yes/[0=No]
           Panels         integer           Intersecting panels in view 1=Yes/[0=No]
           PanelNames     integer           Names of intersecting panels in view 1=Yes/[0=No]
           ShellStiffNames integer          Shell Stiffener names in view 1=Yes/[0=No]
           DirectionMarks integer           Direction Marks in view 1=Yes/[0=No]
           PartNames      integer           PartNames in view 1=Yes/[0=No]
           HoleCrossMarks integer           HoleCrossMarks in view 1=Yes/[0=No]
           FrameCurves    integer           FrameCurves in view 1=Yes/[0=No]
           FrameCurvesNames integer         FrameCurvesNames in view 1=Yes/[0=No]
      """
      self.Seams = 1
      self.SeamNames = 1
      self.Plates = 1
      self.Material = 0
      self.Stiffeners = 1
      self.StiffNames = 0
      self.Endcuts = 0
      self.Jigs = 1
      self.Heights = 0
      self.Panels = 0
      self.PanelNames = 0
      self.ShellStiffNames=0
      self.DirectionMarks=0
      self.PartNames=0
      self.HoleCrossMarks=0
      self.FrameCurves=0
      self.FrameCurvesNames=0
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      tup = (
            'CurvedPanelView:',
            '   Seams      :' + str(self.Seams),
            '   SeamNames  :' + str(self.SeamNames),
            '   Plates     :' + str(self.Plates),
            '   Material   :' + str(self.Material),
            '   Stiffeners :' + str(self.Stiffeners),
            '   StiffNames :' + str(self.StiffNames),
            '   Endcuts    :' + str(self.Endcuts),
            '   Jigs       :' + str(self.Jigs),
            '   Heights    :' + str(self.Heights),
            '   Panels     :' + str(self.Panels),
            '   PanelNames :' + str(self.PanelNames),
            '   ShellStiffNames :' + str(self.ShellStiffNames),
            '   DirectionMarks :' + str(self.DirectionMarks),
            '   PartNames :' + str(self.PartNames),
            '   HoleCrossMarks :' + str(self.HoleCrossMarks),
            '   FrameCurves :' + str(self.HoleCrossMarks),
            '   FrameCurvesNames :' + str(self.FrameCurvesNames) )
      return string.join (tup, '\n')

#-----------------------------------------------------------------------

   def SetSeams( self, Val):
      if Val:  self.__Seams = 1
      else:    self.__Seams = 0

   def GetSeams( self):
      return self.__Seams

#-----------------------------------------------------------------------

   def SetSeamNames( self, Val):
      if Val:  self.__SeamNames = 1
      else:    self.__SeamNames = 0

   def GetSeamNames( self):
      return self.__SeamNames

#-----------------------------------------------------------------------

   def SetPlates( self, Val):
      if Val:  self.__Plates = 1
      else:    self.__Plates = 0

   def GetPlates( self):
      return self.__Plates

#-----------------------------------------------------------------------

   def SetMaterial( self, Val):
      if Val:  self.__Material = 1
      else:    self.__Material = 0

   def GetMaterial( self):
      return self.__Material

#-----------------------------------------------------------------------

   def SetStiffeners( self, Val):
      if Val:  self.__Stiffeners = 1
      else:    self.__Stiffeners = 0

   def GetStiffeners( self):
      return self.__Stiffeners

#-----------------------------------------------------------------------

   def SetStiffNames( self, Val):
      if Val:  self.__StiffNames = 1
      else:    self.__StiffNames = 0

   def GetStiffNames( self):
      return self.__StiffNames

#-----------------------------------------------------------------------

   def SetEndcuts( self, Val):
      if Val:  self.__Endcuts = 1
      else:    self.__Endcuts = 0

   def GetEndcuts( self):
      return self.__Endcuts

#-----------------------------------------------------------------------

   def SetJigs( self, Val):
      if Val:  self.__Jigs = 1
      else:    self.__Jigs = 0

   def GetJigs( self):
      return self.__Jigs

#-----------------------------------------------------------------------

   def SetHeights( self, Val):
      if Val:  self.__Heights = 1
      else:    self.__Heights = 0

   def GetHeights( self):
      return self.__Heights

#-----------------------------------------------------------------------

   def SetPanels( self, Val):
      if Val:  self.__Panels = 1
      else:    self.__Panels = 0

   def GetPanels( self):
      return self.__Panels

#-----------------------------------------------------------------------

   def SetPanelNames( self, Val):
      if Val:  self.__PanelNames = 1
      else:    self.__PanelNames = 0

   def GetPanelNames( self):
      return self.__PanelNames

#--------------------------------------------------------------------------------------------

   def SetShellStiffNames( self, Val):
      if Val:  self.__ShellStiffNames = 1
      else:    self.__ShellStiffNames = 0

   def GetShellStiffNames( self):
      return self.__ShellStiffNames

#-------------------------------------------------------------------------------------

   def SetDirectionMarks( self, Val):
      if Val:  self.__DirectionMarks = 1
      else:    self.__DirectionMarks = 0

   def GetDirectionMarks( self):
      return self.__DirectionMarks
#-------------------------------------------------------------------------------------

   def SetPartNames( self, Val):
      if Val:  self.__PartNames = 1
      else:    self.__PartNames = 0

   def GetPartNames( self):
      return self.__PartNames

#-------------------------------------------------------------------------------------

   def SetHoleCrossMarks( self, Val):
      if Val:  self.__HoleCrossMarks = 1
      else:    self.__HoleCrossMarks = 0

   def GetHoleCrossMarks( self):
      return self.__HoleCrossMarks
#-------------------------------------------------------------------------------------

   def SetFrameCurvesNames( self, Val):
      if Val:  self.__FrameCurvesNames = 1
      else:    self.__FrameCurvesNames = 0

   def GetFrameCurvesNames( self):
      return self.__FrameCurvesNames

#-------------------------------------------------------------------------------------

   def SetFrameCurves( self, Val):
      if Val:  self.__FrameCurves = 1
      else:    self.__FrameCurves = 0

   def GetFrameCurves( self):
      return self.__FrameCurves

#-------------------------------------------------------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
   Seams = property (GetSeams, SetSeams, None, '')
   SeamNames = property (GetSeamNames, SetSeamNames, None, '')
   Plates = property (GetPlates, SetPlates, None, '')
   Material = property (GetMaterial, SetMaterial, None, '')
   Stiffeners = property (GetStiffeners, SetStiffeners, None, '')
   StiffNames = property (GetStiffNames, SetStiffNames, None, '')
   Endcuts = property (GetEndcuts, SetEndcuts, None, '')
   Jigs = property (GetJigs, SetJigs, None, '')
   Heights = property (GetHeights, SetHeights, None, '')
   Panels = property (GetPanels, SetPanels, None, '')
   PanelNames = property (GetPanelNames, SetPanelNames, None, '')
   ShellStiffNames = property (GetShellStiffNames, SetShellStiffNames, None, '')
   DirectionMarks = property (GetDirectionMarks, SetDirectionMarks, None, '')
   PartNames = property (GetPartNames, SetPartNames, None, '')
   HoleCrossMarks = property (GetHoleCrossMarks, SetHoleCrossMarks, None, '')
   FrameCurvesNames = property (GetFrameCurvesNames, SetFrameCurvesNames, None, '')
   FrameCurves = property (GetFrameCurves, SetFrameCurves, None, '')
