## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
from KcsDrawTable import *
import kcs_draft
import kcs_dex
import kcs_chm
import kcs_ui
import KcsInterpretationObject
import KcsPoint2D
import KcsVector2D
import KcsModel
import KcsColour
from math import *
import string

def TrimNum(num, prec=-1):
  """TrimNum(num, prec) -> string

Returns the shortest possible string representation of the number 'num'.
If an optional 'prec' argument is given, the number is first represented with
'prec' decimal digits after the decimal point.
Examples:
TrimNum(1.240)    -> '1.24'
TrimNum(1.288, 2) -> '1.29'"""
  try:
    if prec < 0: s = str(num)
    else: s = ("%0." + str(prec) + "f") % num
  except:
    return "****"
  return s

def CPanDist(PanelName, BaseSeam, EndSeam, FramePrefix, StartFrame, EndFrame, Suffix):
  """
        PanelName = Name of the Curved Panel to get info from
        BaseSeam = name of the seam to count distance from
        EndSeam = Name of Last seam to mesure to
        FramePrefix = Frame curve prefix
        Startframe = number of the first frame to add info for
        EndFrame = Last frame to add data for
        Suffix = Drawing name suffix
  """

  #get the number of decimals to use
  nDecStr = kcs_draft.default_value_get('DIM_LIN_DEC')
  resStr = string.split(nDecStr, ':')
  nDec = int(resStr[1])

  #Close the current drawing if any
  kcs_draft.dwg_close()
  #Create a new drawing
  kcs_draft.dwg_new(PanelName + Suffix, 'CPANDIST_PICT')
  #Create the properties for the Curved Panel view
  IntObj = KcsInterpretationObject.CurvedPanelView()
  #Create the view
  CPView = kcs_chm.view_curvedpanel_new(PanelName, IntObj)

  #Place the curved panel view in the drawing
  Handle = kcs_draft.view_identify('CPANVIEW')
  Extent = kcs_draft.view_restriction_area_get(Handle)

  ViewExtent = kcs_draft.element_extent_get(CPView)
  testP = KcsPoint2D.Point2D(Extent.Corner1.X, Extent.Corner1.Y)
  Dist1X = testP.DistanceToPoint(KcsPoint2D.Point2D(Extent.Corner2.X, Extent.Corner1.Y))

  Dist1Y = testP.DistanceToPoint(KcsPoint2D.Point2D(Extent.Corner1.X, Extent.Corner2.Y))

  testPP = KcsPoint2D.Point2D(ViewExtent.Corner1.X, ViewExtent.Corner1.Y)

  Dist2X = testPP.DistanceToPoint(KcsPoint2D.Point2D(ViewExtent.Corner2.X, ViewExtent.Corner1.Y))

  Dist2Y = testPP.DistanceToPoint(KcsPoint2D.Point2D(ViewExtent.Corner1.X, ViewExtent.Corner2.Y))

  reaScale = max(Dist2X/Dist1X, Dist2Y/Dist1Y)
  reaScale = max(reaScale*1.2, 50.0)
  Scale = 1/reaScale

  kcs_draft.view_scale(CPView, Scale)


  ViewExtent = kcs_draft.element_extent_get(CPView)
  xp=(Extent.Corner1.X + Extent.Corner2.X)/2
  yp=(Extent.Corner1.Y + Extent.Corner2.Y)/2
  CpointForm = KcsPoint2D.Point2D(xp, yp)
  xp=(ViewExtent.Corner1.X + ViewExtent.Corner2.X)/2
  yp=(ViewExtent.Corner1.Y + ViewExtent.Corner2.Y)/2
  CpointView = KcsPoint2D.Point2D(xp, yp)
  DeltaVec = KcsVector2D.Vector2D()
  DeltaVec.SetFromPoints(CpointView, CpointForm)
  kcs_draft.view_move(CPView, DeltaVec)

  #Add dimensioning
  col1 = KcsColour.Colour("Black")
  FromList = []
  AlongList = []
  ToList = []
  model = KcsModel.Model()
  model.SetType('seam/butt')
  model.SetName(BaseSeam)
  FromList.append(model)

  if StartFrame != EndFrame:
    Frames = range(StartFrame,EndFrame+1)
    for fr in Frames:
        model1 = KcsModel.Model()
        model1.SetType('hull curve')
        frameName = FramePrefix + str(fr)
        model1.SetName(frameName)
        ToList.append(model1)

  nppanel = 0
  dexString ="HULL.CPANEL('" + PanelName + "').NPPANEL"
  kcs_dex.extract(dexString)
  type = kcs_dex.next_result()
  while type >= 0:
      if type == 1:
          nppanel = kcs_dex.get_int()
      type = kcs_dex.next_result()

  if nppanel > 0:
      dexString ="HULL.CPANEL('" + PanelName + "').PPANEL"
      kcs_dex.extract(dexString)
      type = kcs_dex.next_result()
      while type >= 0:
          if type == 3:
              stiName = kcs_dex.get_string()
              model1 = KcsModel.Model()
              model1.SetType('plane panel')
              model1.SetName(stiName)
              ToList.append(model1)
          type = kcs_dex.next_result()

  for frame in ToList:
      kcs_draft.model_draw(frame, CPView)
      fname = frame.GetName()
      elem = kcs_draft.element_identify(fname)
      if elem:
          kcs_draft.element_colour_set(elem, col1)

  model1 = KcsModel.Model()
  model1.SetType('seam/butt')
  model1.SetName(EndSeam)
  ToList.append(model1)

  nsti = 0
  NameList = []
  dexString ="HULL.CPANEL('" + PanelName + "').NSTIFFENER"
  kcs_dex.extract(dexString)
  type = kcs_dex.next_result()
  while type >= 0:
      if type == 1:
          nsti = kcs_dex.get_int()
      type = kcs_dex.next_result()

  if nsti > 0:
      dexString ="HULL.CPANEL('" + PanelName + "').STIFFENER(1:" + str(nsti*2) + ").NAME"
      kcs_dex.extract(dexString)
      type = kcs_dex.next_result()
      while type >= 0:
          if type == 3:
              stiName = kcs_dex.get_string()
              model2 = KcsModel.Model()
              model2.SetType('curved panel')
              model2.PartType = 'stiffener'
              model2.PartId = 1
              model2.SetName(stiName)
              AlongList.append(model2)
          type = kcs_dex.next_result()

      dexString ="HULL.CPANEL('" + PanelName + "').STIFFENER(1:" + str(nsti*2) + ").PROF.PART_ID.SHO"
      kcs_dex.extract(dexString)
      type = kcs_dex.next_result()
      while type >= 0:
          if type == 3:
              stiName = kcs_dex.get_string()
              NameList.append(stiName)
          else:
              NameList.append('')
          type = kcs_dex.next_result()

  resList = kcs_draft.dim_shell_new(CPView, FromList, AlongList, ToList, 1, col1)

  #Create the table data
  TableData = []
  RowData = []
  RowData.append('....................\n....................')
  for toModel in ToList:
      toName = toModel.GetName()
      toName = '    ' + toName
      RowData.append(toName)
  TableData.append(RowData)

  index = 0
  for alongModel in AlongList:
      RowData = []
      if NameList[index] == '':
        alongName = alongModel.GetName()
      else:
        alongName = NameList[index]
      RowData.append(alongName)
      for toModel in ToList:
          try:
              resLength = kcs_chm.remarking_length(FromList[0], alongModel, toModel)
          except:
              resLength = 0.0
          length = TrimNum(resLength, nDec)
          RowData.append(length)
      TableData.append(RowData)


  ViewHandle = kcs_draft.view_identify('TABLEVIEW')
  #Add the table to the view
  AddTable(TableData, ViewHandle, 'Long. Girth Length   (Base seam ' + BaseSeam + ')')

  #Un-comment the next line if the drawing is to be automaticaly stored.
  #kcs_draft.dwg_save()
