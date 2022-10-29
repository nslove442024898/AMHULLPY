## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import KcsInterpretationObject
import KcsPoint3D
import KcsTransformation2D

import kcs_draft
import kcs_ui
import kcs_util

import string

def DefinePlaneByPanel(obj):

    objtypes = {  'Panel'       : KcsInterpretationObject.SymbolicView.TYPE_PANEL,
                  'Bracket'     : KcsInterpretationObject.SymbolicView.TYPE_BRACKET,
                  'Stiffener'   : KcsInterpretationObject.SymbolicView.TYPE_STIFFENER,
                  'Flange'      : KcsInterpretationObject.SymbolicView.TYPE_FLANGE
            }

    panelname = obj.GetObjectName()
    reflect = obj.IsReflect()
    onlycurrent = obj.IsOnlyCurrent()
    comptype = obj.GetComponentType()
    compno = obj.GetComponentNo()

    while 1:
        strPanel = 'Name: %s' % panelname
        if reflect:
            strReflect = 'Reflect: Yes'
        else:
            strReflect = 'Reflect: No'
        if onlycurrent:
            strOnlyCurrent = 'Only current: Yes'
        else:
            strOnlyCurrent = 'Only current: No'
        strCompType = 'Component type: %s' % objtypes.keys()[objtypes.values().index(comptype)]
        strCompNo = 'Component number: %d' % compno

        if comptype == KcsInterpretationObject.SymbolicView.TYPE_PANEL:
            actions = [strPanel, strReflect, strOnlyCurrent, strCompType, '--- SET ---']
        else:
            actions = [strPanel, strReflect, strOnlyCurrent, strCompType, strCompNo, '--- SET ---']

        resp, action = kcs_ui.choice_select('Plane by panel settings', 'Select', actions)

        if resp == kcs_util.ok():
            if action == 1:
                resp, panel = kcs_ui.string_req('Panel name', panelname)
                if resp == kcs_util.ok():
                    panelname = panel
            elif action == 2:
                reflect = not reflect
            elif action == 3:
                onlycurrent = not onlycurrent
            elif action == 4:
                if objtypes.values().index(comptype) == len(objtypes.values())-1:
                    comptype = objtypes.values()[0]
                else:
                    comptype = objtypes.values()[objtypes.values().index(comptype)+1]
            elif action == 5:
                if comptype != KcsInterpretationObject.SymbolicView.TYPE_PANEL:
                    resp, res = kcs_ui.int_req('Component number:', compno)
                    if resp == kcs_util.ok():
                        compno = res
                else:
                    action = 6
            if action == 6:
                print 'set plane'
                obj.SetPlaneByPanel(panelname, comptype, compno, reflect, onlycurrent)
        else:
            break

def DefinePlaneByCurve(obj):

    curvename = obj.GetObjectName()
    reflect = obj.IsReflect()

    while 1:
        strCurve = 'Name: %s' % curvename
        if reflect:
            strReflect = 'Reflect: Yes'
        else:
            strReflect = 'Reflect: No'

        actions = [strCurve, strReflect, '--- SET ---']
        resp, action = kcs_ui.choice_select('Plane by panel settings', 'Select', actions)

        if resp == kcs_util.ok():
            if action == 1:
                resp, curve = kcs_ui.string_req('Curve name', curvename)
                if resp == kcs_util.ok():
                    curvename = curve
            elif action == 2:
                reflect = not reflect
            elif action == 3:
                obj.SetPlaneByCurve(curvename, reflect)
        else:
            break

def DefinePlaneByRSO(obj):

    rsoname = obj.GetObjectName()
    compno = obj.GetComponentNo()

    while 1:
        strRSO = 'Name: %s' % rsoname
        strCompNo = 'Component: %d' % compno

        actions = [strRSO, strCompNo, '--- SET ---']
        resp, action = kcs_ui.choice_select('Plane by RSO Settings', 'Select', actions)

        if resp == kcs_util.ok():
            if action == 1:
                resp, rso = kcs_ui.string_req('RSO object:', rsoname)
                if resp == kcs_util.ok():
                    rsoname = rso
            elif action == 2:
                resp, res = kcs_ui.int_req('Component number:', compno)
                if resp == kcs_util.ok():
                    compno = res
            elif action == 3:
                obj.SetPlaneByRSO(rsoname, compno)
                print 'set'
        else:
            break

def GetPlaneTypeName(planetype):

    if planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_X:
        return 'BY X'
    elif planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_Y:
        return 'BY Y'
    elif planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_Z:
        return 'BY Z'
    elif planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_3POINTS:
        return 'BY 3 POINTS'
    elif planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_PANEL:
        return 'BY PANEL'
    elif planetype == KcsInterpretationObject.SymbolicView.PLANE_BY_CURVE:
        return 'BY CURVE'
    else:
        return 'BY RSO'

LookingName = { KcsInterpretationObject.SymbolicView.LOOKING_FOR : 'FOR',
                KcsInterpretationObject.SymbolicView.LOOKING_AFT : 'AFT',
                KcsInterpretationObject.SymbolicView.LOOKING_PS  : 'PS',
                KcsInterpretationObject.SymbolicView.LOOKING_SB  : 'SB',
                KcsInterpretationObject.SymbolicView.LOOKING_TOP : 'TOP',
                KcsInterpretationObject.SymbolicView.LOOKING_BOT : 'BOT' }

def GetCoordinate(axis):

        while 1:
            try:
                resp, res = kcs_ui.string_req('Position or coordinate:', '')
                if resp == kcs_util.ok():
                    if axis == 1:
                        sep = 'FR'
                    else:
                        sep = 'LP'
                    res = string.split(res, sep)
                    print res
                    if len(res) == 2:
                        coord = kcs_util.pos_to_coord(axis, int(res[1]))[1]
                    else:
                        coord = float(res[0])
                    print coord
                    return coord
                else:
                    return None
            except:
                kcs_ui.message_noconfirm("Can't translate coordiante!")

def GetPoint3D(prompt):

    while 1:
        try:
            resp, res = kcs_ui.string_req(prompt, '')
            if resp == kcs_util.ok():
                coords = string.split(res, ',')
                return KcsPoint3D.Point3D(float(coords[0]), float(coords[1]), float(coords[2]))
            else:
                return None
        except:
            kcs_ui.message_noconfirm("Wrong point coordinates!")

def SelectPlane(obj):

    resp = kcs_util.ok()

    while resp == kcs_util.ok():
        resp, res = kcs_ui.choice_select('Plate type', 'Select', ['By X', 'By Y', 'By Z', \
                                                                  'By 3 Points', 'By panel', \
                                                                  'By curve', 'By RSO'])
        if resp == kcs_util.ok():
            if res == 1:
                coord = GetCoordinate(1)
                if coord != None:
                    obj.SetPlaneByX(coord)
            elif res == 2:
                coord = GetCoordinate(2)
                if coord != None:
                    obj.SetPlaneByY(coord)
            elif res == 3:
                coord = GetCoordinate(3)
                if coord != None:
                    obj.SetPlaneByZ(coord)
            elif res == 4:
                origin = GetPoint3D('Origin')
                if origin != None:
                    uaxis = GetPoint3D('U Axis')
                    if uaxis != None:
                        vaxis = GetPoint3D('V Axis')
                        if vaxis != None:
                            obj.SetPlaneBy3Points(origin, uaxis, vaxis)
            elif res == 5:
                DefinePlaneByPanel(obj)
            elif res == 6:
                DefinePlaneByCurve(obj)
            elif res == 7:
                DefinePlaneByRSO(obj)

def SelectLimits(obj):
    resp = kcs_util.ok()

    while resp == kcs_util.ok():
        min, max = obj.GetLimits()
        actions = [ 'Min: %g, %g, %g' % (min.X, min.Y, min.Z),\
                    'Max: %g, %g, %g' % (max.X, max.Y, max.Z),\
                    'Depth before: %g' % obj.GetDepth()[0],\
                    'Depth behind: %g' % obj.GetDepth()[1] ]

        (resp, res) = kcs_ui.choice_select('Symbolic view limits', 'Set limits', actions)
        if resp == kcs_util.ok():
            if res == 1:
                pt = GetPoint3D('Minimum')
                if pt != None:
                    obj.SetLimits(pt, obj.GetLimits()[1])
            elif res == 2:
                pt = GetPoint3D('Maximum')
                if pt != None:
                    obj.SetLimits(obj.GetLimits()[0], pt)
            elif res == 3:
                resp, value = kcs_ui.real_req('Depth before:', obj.GetDepth()[0])
                if resp==kcs_util.ok():
                    obj.SetDepth(value, obj.GetDepth()[1])
            elif res == 4:
                resp, value = kcs_ui.real_req('Depth behind:', obj.GetDepth()[1])
                if resp==kcs_util.ok():
                    obj.SetDepth(obj.GetDepth()[0], value)

def DefineFilter(obj):
    while 1:
        if obj.GetBlocksFilter()[1]:
            blocksExc = 'Exclude blocks: Yes'
        else:
            blocksExc = 'Exclude blocks: No'

        if obj.GetPanelsFilter()[1]:
            panelsExc = 'Exclude panels: Yes'
        else:
            panelsExc = 'Exclude panels: No'

        actions = [blocksExc, 'Blocks: %s' % string.join(obj.GetBlocksFilter()[0], ', '),\
                   panelsExc, 'Panels: %s' % string.join(obj.GetPanelsFilter()[0], ', ')]

        resp, value = kcs_ui.choice_select('Filter', 'Select', actions)

        if resp == kcs_util.ok():
            if value == 1:
                blocks, exclude = obj.GetBlocksFilter()
                if exclude:
                    obj.SetBlocksFilter(blocks, 0)
                else:
                    obj.SetBlocksFilter(blocks, 1)
            elif value == 2:
                blocks, exclude = obj.GetBlocksFilter()
                resp, value = kcs_ui.string_req('Blocks:', string.join(blocks, ', '))
                if resp == kcs_util.ok():
                    obj.SetBlocksFilter(string.split(value, ','), exclude)
            if value == 3:
                panels, exclude = obj.GetPanelsFilter()
                if exclude:
                    obj.SetPanelsFilter(panels, 0)
                else:
                    obj.SetPanelsFilter(panels, 1)
            elif value == 4:
                panels, exclude = obj.GetPanelsFilter()
                resp, value = kcs_ui.string_req('Panels:', string.join(panels, ', '))
                if resp == kcs_util.ok():
                    obj.SetPanelsFilter(string.split(value, ','), exclude)
        else:
            return None

def EditDesignViewOptions(obj):
    while 1:
        if obj.GetShellCurveType() == KcsInterpretationObject.SymbolicView.CURVE_EXISTING:
            curvetype = "Curve type: Existing"
        elif obj.GetShellCurveType() == KcsInterpretationObject.SymbolicView.CURVE_BY_NAME:
            curvetype = "Curve type: By name"
        elif obj.GetShellCurveType() == KcsInterpretationObject.SymbolicView.CURVE_CUT:
            curvetype = "Curve type: Cut"
        elif obj.GetShellCurveType() == KcsInterpretationObject.SymbolicView.CURVE_NONE:
            curvetype = "Curve type: None"

        if obj.GetShellSeams():
            seams = 'Seams: Yes'
        else:
            seams = 'Seams: No'

        if obj.GetShellProfiles():
            profiles = 'Profiles: Yes'
        else:
            profiles = 'Profiles: No'

        if obj.GetAutomaticSelection():
            selection = 'Automatic sel.: Yes'
        else:
            selection = 'Automatic sel.: No'

        if obj.GetDrawAsPlate():
            drwasplate = 'Draw as plate: Yes'
        else:
            drwasplate = 'Draw as plate: No'

        if obj.GetDrawPlaneViews():
            planeviews = 'Draw plane views: Yes'
        else:
            planeviews = 'Draw plane views: No'

        if obj.GetDrawIntersections():
            intersect = 'Draw intersect: Yes'
        else:
            intersect = 'Draw intersect: No'

        if obj.GetDrawRSO():
            rso = 'Draw RSO: Yes'
        else:
            rso = 'Draw RSO: No'

        actions = [selection, drwasplate, planeviews, intersect, rso, seams, profiles, 'Filter', curvetype]

        if obj.GetShellCurveType() == KcsInterpretationObject.SymbolicView.CURVE_BY_NAME:
            curves = string.join(obj.GetShellCurves(), ', ')
            actions.append('Curves: %s' % curves)

        resp, value = kcs_ui.choice_select('Design view', 'Select', actions)

        if resp == kcs_util.ok():
            if value == 1:
                if obj.GetAutomaticSelection():
                    obj.SetAutomaticSelection(0)
                else:
                    obj.SetAutomaticSelection(1)
            elif value == 2:
                if obj.GetDrawAsPlate():
                    obj.SetDrawAsPlate(0)
                else:
                    obj.SetDrawAsPlate(1)
            elif value == 3:
                if obj.GetDrawPlaneViews():
                    obj.SetDrawPlaneViews(0)
                else:
                    obj.SetDrawPlaneViews(1)
            elif value == 4:
                if obj.GetDrawIntersections():
                    obj.SetDrawIntersections(0)
                else:
                    obj.SetDrawIntersections(1)
            elif value == 5:
                if obj.GetDrawRSO():
                    obj.SetDrawRSO(0)
                else:
                    obj.SetDrawRSO(1)
            elif value == 6:
                if obj.GetShellSeams():
                    obj.SetShellSeams(0)
                else:
                    obj.SetShellSeams(1)
            elif value == 7:
                if obj.GetShellProfiles():
                    obj.SetShellProfiles(0)
                else:
                    obj.SetShellProfiles(1)
            elif value == 8:
                DefineFilter(obj)
            elif value == 9:
                index = obj.GetShellCurveType()
                if index==3:
                    obj.SetShellCurves(0, obj.GetShellCurves())
                else:
                    obj.SetShellCurves(index+1, obj.GetShellCurves())
            else:
                value = string.join(obj.GetShellCurves(), ', ')
                resp, value = kcs_ui.string_req('Curves:', value)
                if resp == kcs_util.ok():
                    obj.SetShellCurves(obj.GetShellCurveType(), string.split(value, ','))
        else:
            return None

def EditAssemblyViewOptions(obj):
    resp, value = kcs_ui.string_req('Assemblies:', string.join(obj.GetAssemblies(), ', '))
    if resp == kcs_util.ok():
        obj.SetAssemblies(string.split(value, ','))

def EditViewOptions(obj):
    if obj.GetViewType() == KcsInterpretationObject.SymbolicView.VIEW_DESIGN:
        EditDesignViewOptions(obj)
    else:
        EditAssemblyViewOptions(obj)

try:
    obj = KcsInterpretationObject.SymbolicView()
    obj.SetViewName('TEST')
    obj.SetPlaneByPanel('JUMBO-PLF7000', KcsInterpretationObject.SymbolicView.TYPE_PANEL, 0, 0, 1)

    resp = kcs_util.ok()
    while resp == kcs_util.ok():
        if obj.GetViewType() == KcsInterpretationObject.SymbolicView.VIEW_DESIGN:
            viewtype = "DESIGN"
        else:
            viewtype = "ASSEMBLY"
        (resp, res) = kcs_ui.choice_select('Symbolic view', 'Set properties', ['View name:%s' % obj.GetViewName(),\
                                                                               'Plane: %s' % GetPlaneTypeName(obj.GetPlaneType()), \
                                                                               'Looking: %s' % LookingName[obj.GetLooking()],\
                                                                               'Limits',
                                                                               'View type: %s' % viewtype,
                                                                               'View options',
                                                                               'Create'
                                                                               ])
        if resp == kcs_util.ok():
            if res==1:
                (resp, res) = kcs_ui.string_req('View name', obj.GetViewName())
                if resp == kcs_util.ok():
                    obj.SetViewName(res)
            elif res==2:
                SelectPlane(obj)
            elif res==3:
                index = LookingName.keys().index(obj.GetLooking())
                if index == len(LookingName.keys())-1:
                    obj.SetLooking(LookingName.keys()[0])
                else:
                    obj.SetLooking(LookingName.keys()[index+1])
            elif res==4:
                SelectLimits(obj)
            elif res==5:
                if obj.GetViewType() == KcsInterpretationObject.SymbolicView.VIEW_DESIGN:
                    obj.SetViewType(KcsInterpretationObject.SymbolicView.VIEW_ASSEMBLY)
                else:
                    obj.SetViewType(KcsInterpretationObject.SymbolicView.VIEW_DESIGN)
            elif res==6:
                EditViewOptions(obj)
            elif res==7:
                try:
                    handle = kcs_draft.view_symbolic_new(obj)
                    print 'handle: ', handle
                    transf = KcsTransformation2D.Transformation2D()
                    kcs_draft.element_transformation_get(handle, transf)
                    print 'Scale: ', transf.GetScale()
                    kcs_draft.view_scale(handle, 0.02)
                    kcs_draft.element_transformation_get(handle, transf)
                    print 'After scale: ', transf.GetScale()
                except:
                    kcs_ui.message_noconfirm(kcs_draft.error)

except Exception, e:
    print e
