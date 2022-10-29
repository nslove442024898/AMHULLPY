## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hullpan02.py
#
#      PURPOSE:
#
#               This program presents kcs_hullpan: copy, move, regenerate, split, topology
#
#
#
#----------------------------------------------------------------------------------
import string
import kcs_ui
import kcs_util
import kcs_draft
import kcs_hullpan
import CommonSample
import KcsPoint3D
import KcsVector2D
import KcsVector3D
import KcsPlane3D
import KcsStat_point3D_req
import KcsModel
import KcsTransformation3D
from KcsCopyPanOptions import CopyPanOptions
from KcsMovePanOptions import MovePanOptions
from KcsSplitPanOptions import SplitPanOptions

from KcsPoint2D               import Point2D
from KcsCursorType            import CursorType, CursorTypes
from KcsStat_point2D_req      import Stat_point2D_req, Point2dDefModes


#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
isPanelActive = ''
hullpanname = ''
hulltype = ''
location = ''
model    = KcsModel.Model()
copyOpt  = CopyPanOptions()
moveOpt  = MovePanOptions()
splitOpt = SplitPanOptions()

LOCATION_TYPE = [ 'Principial plane', 'Defined plane', 'Plane Object' ]
PLANE_DESC    = ['X', 'Y', 'Z' ]
YES_NO_DESC   = ['No', 'Yes']

moveOpt.SetPrincipalPlane(1,1, 'FR1')
newPanelNames = ['TMP_P1', 'TMP_P2']
newBlockNames = ['', '']
newSC = ['','']


def SetMoveOptions( opt ):

   status = kcs_util.ok()

   while( status == kcs_util.ok() ):

      actions = (
         'Location: ' + LOCATION_TYPE[ opt._MovePanOptions__LocationType -1 ],
         'PrincipalPlane: ' + PLANE_DESC[ opt._MovePanOptions__Coordinate -1] ,
         'Position: ' + str( opt._MovePanOptions__CoordinateValue),
         'Relative: '+ str( YES_NO_DESC[opt._MovePanOptions__RelativePosition]),
         'Define Plane',
         'PlaneObject: ' + opt._MovePanOptions__ObjectName )

      (status, index) = kcs_ui.choice_select('Move options', '', actions)
      if status == kcs_util.ok():
         if index == 1:
            (status, index) = kcs_ui.choice_select('Location type', '', LOCATION_TYPE)
            if status == kcs_util.ok():
               opt._MovePanOptions__LocationType = index
         elif index == 2:
            (status, index) = kcs_ui.choice_select('Select plane', '', PLANE_DESC)
            if status == kcs_util.ok():
               opt._MovePanOptions__Coordinate = index
         elif index == 3:
            (res, value) = kcs_ui.string_req('Input position value/string', opt._MovePanOptions__CoordinateValue)
            if res == kcs_util.ok():
               opt._MovePanOptions__CoordinateValue = value
         elif index == 4:
            (status, index) = kcs_ui.choice_select('Relative position', '', YES_NO_DESC)
            if status == kcs_util.ok():
               opt._MovePanOptions__RelativePosition =  index - 1
         elif index == 5:
            while(1):
               actions = (
                  'Origin: ' + str( opt._MovePanOptions__Origin),
                  'U Axis: ' + str( opt._MovePanOptions__Uaxis),
                  'V Axis: ' + str( opt._MovePanOptions__Vaxis) )

               (status, index) = kcs_ui.choice_select('Plane definition', '', actions)
               if status == kcs_util.ok():
                  if index == 1:
                     (res, value) = kcs_ui.string_req('Input values: X Y Z')
                     if res == kcs_util.ok():
                        valList = value.split(' ')
                        try:
                           opt._MovePanOptions__Origin.SetCoordinates( valList[0], valList[1], valList[2])
                        except:
                           pass
                  elif index == 2:
                     (res, value) = kcs_ui.string_req('Input values: X Y Z')
                     if res == kcs_util.ok():
                        valList = value.split(' ')
                        try:
                           opt._MovePanOptions__Uaxis.SetCoordinates( valList[0], valList[1], valList[2])
                        except:
                           pass
                  elif index == 3:
                     (res, value) = kcs_ui.string_req('Input values: X Y Z')
                     if res == kcs_util.ok():
                        valList = value.split(' ')
                        try:
                           opt._MovePanOptions__Vaxis.SetCoordinates( valList[0], valList[1], valList[2])
                        except:
                           pass
               else:
                  break


         elif index == 6:
            (res, value) = kcs_ui.string_req('Input plane name')
            if res == kcs_util.ok():
               opt._MovePanOptions__ObjectName = value

def MovePanel( model ):
   actions = (
      'Set move options ',
      'Move panel' )

   while( 1 ):
      (status, index) = kcs_ui.choice_select('Move panel %s' % model.Name, '', actions)
      if status == kcs_util.ok():
         if index == 1:
            SetMoveOptions( moveOpt )
         elif index == 2:
            kcs_hullpan.pan_move( model.Name, moveOpt )
            kcs_draft.model_draw( model )
            kcs_draft.dwg_repaint()
      else:
         break

def CopyPanel( model ):
   opt = copyOpt

   #check if names for new panels are set
   try:
      opt.GetNameMapping()[model.Name]
   except:
      opt.SetNameMapping({model.Name : newPanelNames[0]})

   while(1):
      actions = (
         'Set move options ',
         'Block: ' + opt.GetBlockName(),
         'Name mapping: ' + str(opt.GetNameMapping()[model.Name]),
         'Copy panel')

      (status, index) = kcs_ui.choice_select('Copy panel %s' % model.Name, '', actions)
      if status == kcs_util.ok():
         if index == 1:
            SetMoveOptions( copyOpt )
         elif  index == 2:
            (res, value) = kcs_ui.string_req('Input block name')
            if res == kcs_util.ok():
               opt.SetBlockName( value )
         elif index == 3:
            nameMap = {}
            res, value = kcs_ui.string_req('Input new panel name' ,'')
            if res == kcs_util.ok():
               nameMap[model.Name] = value
               opt.SetNameMapping(nameMap)

         elif index == 4:
            kcs_hullpan.pan_copy(model.Name, opt)
            panelName = model.Name
            try:
               kcs_draft.model_draw( model )
               model.Name = opt.GetNameMapping()[model.Name]
               kcs_draft.model_draw( model )
            except:
               pass
            model.Name = panelName
            kcs_draft.dwg_repaint()
      else:
         break

def SplitPanel( model ):

   pt3D  = KcsPoint3D.Point3D(500, 500, 0)
   norm  = KcsVector3D.Vector3D(1,0,0)
   plane = KcsPlane3D.Plane3D( pt3D, norm)

   #check if names for new panels are set
   try:
      oldmapping = splitOpt.GetPanelMapping()
      for i in range(len(oldmapping)):
         newPanelNames[i] = oldmapping[i]['Name']
         newBlocknames[i] = oldmapping[i]['Block']
         newSC[i]         = oldmapping[i]['SymmetryCode']
   except:
      pass

   while( 1 ):

      names = ''
      try:
         names = str( oldmapping[0]['Name'] +', '+ oldmapping[1]['Name'])
      except:
         pass

      actions = (
         'Define spliting plane',
         'Names: ' + str( newPanelNames[0] + ' ' + newPanelNames[1]),
         'Blocks: ' + str( newBlockNames[0] + ' ' + newBlockNames[1]),
         'Side codes: ' + str( newSC[0] + ' ' + newSC[1]),
         'Split Panel')

      (status, index) = kcs_ui.choice_select('Split panel %s' % model.Name, '', actions)
      if status == kcs_util.ok():
         if index == 1:
            (status, index) = kcs_ui.choice_select('Select normal to plane', '', PLANE_DESC)
            if status == kcs_util.ok():
               if index == 1:
                  norm.SetComponents(1,0,0)
               elif index == 2:
                  norm.SetComponents(0,1,0)
               elif index == 3:
                  norm.SetComponents(0,0,1)

            pt0 = KcsPoint3D.Point3D()
            stat3d = KcsStat_point3D_req.Stat_point3D_req()
            stat3d.Initial3D = 1
            stat3d.Initial2D = 2
            stat3d.Locktype  = 2
            stat3d.Lockvec   = norm
            kcs_ui.point3D_req('Select 3D',  stat3d, pt0 )
            plane = KcsPlane3D.Plane3D(pt0, norm)
         elif index == 2:
            (res, value) = kcs_ui.string_req('Input names for new panels: PANEL1 PANEL2', newPanelNames[0] + ' ' + newPanelNames[1])
            if res == kcs_util.ok():
               valList = value.split(' ')
               try:
                  newPanelNames[0] = valList[0]
                  newPanelNames[1] = valList[1]
               except:
                  pass
         elif index == 3:
            (res, value) = kcs_ui.string_req('Input blocks for new panels: BLOCK1 BLOCK2',newBlockNames[0] + ' ' + newBlockNames[1])
            if res == kcs_util.ok():
               valList = value.split(' ')
               try:
                  newBlockNames[0] = valList[0]
                  newBlockNames[1] = valList[1]
               except:
                  pass
         elif index == 4:
            (res, value) = kcs_ui.string_req('Input side code for new panels: SIDE_P1 SIDE_P2', 'S S')
            if res == kcs_util.ok():
               valList = value.split(' ')
               try:
                  newSC[0] = valList[0]
                  newSC[1] = valList[1]
               except:
                  pass
         elif index == 5:
            splitOpt = SplitPanOptions()
            splitOpt.SetCuttingPlane(plane)
            splitOpt.AddPanelMapping(newPanelNames[0],newBlockNames[0],newSC[0])
            splitOpt.AddPanelMapping(newPanelNames[1],newBlockNames[1],newSC[1])
            panelName = model.Name
            try:
               kcs_hullpan.pan_split(panelName, splitOpt)
            except:
               pass
            try:
               kcs_draft.model_draw( model )
               model.Name = newPanelNames[0]
               kcs_draft.model_draw( model )
               model.Name = newPanelNames[1]
               kcs_draft.model_draw( model )
            except:
               pass
            model.Name = panelName
            kcs_draft.dwg_repaint()
      else:
         break



def ShowTopology( model ):
   actions = ( 'Defining', 'Dependent primary','Dependent all' )

   topList = None
   status = kcs_util.ok()

   while( status == kcs_util.ok() ):
      (status, index) = kcs_ui.choice_select('Panel topology', '', actions)
      if status == kcs_util.ok():
         if index == 1:
            topList = kcs_hullpan.pan_topology(model, 'defining')
         elif index == 2:
            topList = kcs_hullpan.pan_topology(model, 'dependent primary')
         elif index == 3:
            topList = kcs_hullpan.pan_topology(model, 'dependent all')

         msgList = map( lambda(x):x.Name, topList )
         if msgList == []:
            msgList = ['empty']


         kcs_ui.string_select('Topology %s %s' % (actions[index-1],model.Name) , '', '', msgList)


while 1:
   actions = (
      'Panel: ' +hullpanname,
      'Activated: ' +isPanelActive,
      'Move',
      'Copy',
      'Recreate',
      'Split',
      'Topology'
      )

   (status, index) = kcs_ui.choice_select('Operations on the Panels', '', actions)
   if status == kcs_util.ok():
      if index == 1:
         model = CommonSample.SelectModel()

         if model and model.Type == 'plane panel':
            model.PartType = ''
            model.PartId = 0
            hullpanname = model.Name
            hulltype = model.Type
            list = kcs_hullpan.pan_list_active()

            if hullpanname in list:
               isPanelActive = 'Yes'
            else:
               isPanelActive = 'No'
      elif index == 2:
         isPanelActive = 'Yes'
         kcs_hullpan.pan_activate(hullpanname)
      elif index == 3:
         MovePanel( model )
      elif index == 4:
         CopyPanel( model )
      elif index == 5:
         kcs_hullpan.pan_recreate(hullpanname)
         kcs_draft.model_draw( model )
      elif index == 6:
         SplitPanel( model )
      elif index == 7:
         ShowTopology( model )
   else:
      print "User interrupted!"
      break;


#----------------------------------------------------------------------------------
