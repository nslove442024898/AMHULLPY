## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import kcs_draft
import KcsRectangle2D
import KcsVector2D
import KcsPoint2D
import KcsText
import KcsRline2D
import KcsLinetype
import math

def AddTable(Data, ViewHandle, Name):
    """
    AddTable will create a table starting att top left corner in the given view.
    Data is a list of lists containing strings. The first list should contain the Column headers.
    The length of the headers will determin the width of the columns.
    The following lists are the rows of the table.
    Name is the name of the table.

    If the table width excceds the width of the view, the table will wrap.
    """
    #
    # Get the number and width of columns
    #
    Headers = Data[0]
    nCol = len(Headers)
    ColWidth = []
    RowHeight = []
    for str in Headers:
	text = KcsText.Text(str)
	text.SetHeight(2.5)
	textElem = kcs_draft.text_new(text)
	Extent = kcs_draft.element_extent_get(textElem)
	kcs_draft.element_delete(textElem)
	ColWidth.append((Extent.Corner2.X - Extent.Corner1.X))
    #
    # Get the number and height of Rows
    #
    text = KcsText.Text('A')
    text.SetHeight(2.5)
    textElem = kcs_draft.text_new(text)
    Extent = kcs_draft.element_extent_get(textElem)
    kcs_draft.element_delete(textElem)
    RowH = ((Extent.Corner2.Y - Extent.Corner1.Y))
    RowSpace = 0.25*RowH
    LineStart = RowH + RowSpace
    for rows in Data:
        text.SetString(rows[0])
        text.SetHeight(2.5)
	textElem = kcs_draft.text_new(text)
	Extent = kcs_draft.element_extent_get(textElem)
	kcs_draft.element_delete(textElem)
	RowH = ((Extent.Corner2.Y - Extent.Corner1.Y))
        RowHeight.append((RowH + 2*RowSpace))

    nRow = len(Data)

    ViewExtent = kcs_draft.view_restriction_area_get(ViewHandle)

    TabWidth = (ViewExtent.Corner2.X - ViewExtent.Corner1.X)
    TabHeight = (ViewExtent.Corner2.Y - ViewExtent.Corner1.Y)

    #
    # Check if the table has to be split after a column
    #
    MaxWidth = 0.0
    SplitTab = []
    col = 0
    for width in ColWidth:
	MaxWidth = MaxWidth + width
	if TabWidth < MaxWidth :
	    SplitTab.append(col)
	    MaxWidth = ColWidth[0] + width
	col = col + 1
	
    SplitTab.append(nCol)

    #
    # Get top left co-ordinate
    #
    TopLeft = KcsPoint2D.Point2D(ViewExtent.Corner1.X, ViewExtent.Corner2.Y)

    kcs_draft.subpicture_current_set(ViewHandle)

    #
    # Add the table
    #
    LineType = KcsLinetype.Linetype()
    LineTypeW = KcsLinetype.Linetype('SolidWide')

    MaxWidth = 0.0
    for I in range(SplitTab[0]):
	MaxWidth = MaxWidth + ColWidth[I]

    Rectangle = KcsRectangle2D.Rectangle2D()
    TabName = KcsText.Text(Name)
    TabName.SetHeight(2.5)
    textElem = kcs_draft.text_new(TabName)
    Extent = kcs_draft.element_extent_get(textElem)
    kcs_draft.element_delete(textElem)
    RowH = ((Extent.Corner2.Y - Extent.Corner1.Y))
    RowH = RowH + 2*RowSpace
    p1 = KcsPoint2D.Point2D(TopLeft.X, TopLeft.Y-RowH)
    p2 = KcsPoint2D.Point2D(TopLeft.X + MaxWidth+ RowSpace, TopLeft.Y)
    TopLeft.Y = p1.Y
    Rectangle.SetCorners(p1, p2)
    rectElem = kcs_draft.rectangle_new(Rectangle)
    kcs_draft.element_linetype_set(rectElem, LineType)
    Cpoint = KcsPoint2D.Point2D((p1.X + p2.X)/2, p1.Y + RowSpace)
    Cpoint.X = Cpoint.X - Extent.Corner2.X/2
    TabName.SetPosition(Cpoint)
    textElem = kcs_draft.text_new(TabName)

    start = 0
    LP1 = KcsPoint2D.Point2D()
    LP2 = KcsPoint2D.Point2D()
    line = KcsRline2D.Rline2D(LP1, LP2)
    CellText = KcsText.Text()
    CellText.SetHeight(2.5)
    for num in SplitTab:
	p1.X = TopLeft.X + RowSpace
	Cpoint.X = TopLeft.X
	p1.Y = TopLeft.Y
	Cpoint.Y = TopLeft.Y
	MaxWidth = 0.0
	for I in range(start+1, num):
	    MaxWidth = MaxWidth + ColWidth[I]
	MaxWidth = MaxWidth + ColWidth[0]

	LP1.X = Cpoint.X
	LP1.Y = Cpoint.Y
	LP2.X = LP1.X + MaxWidth + RowSpace
	LP2.Y = LP1.Y
	line.Start = LP1
	line.End = LP2
	LineElem = kcs_draft.line_new(line)
	kcs_draft.element_linetype_set(LineElem, LineTypeW)
	
	#
	# Add first column
	#
	LineNum = 2
	nHeight = 0
	for J in Data:
	        LineNum = LineNum + 1
		CellText.SetString(J[0])
		p1.Y = Cpoint.Y - LineStart
		Cpoint.Y = Cpoint.Y - RowHeight[nHeight]
		nHeight = nHeight + 1
		CellText.SetPosition(p1)
		textElem = kcs_draft.text_new(CellText)
		if LineNum == 3:
		    LP1.X = Cpoint.X
		    LP1.Y = Cpoint.Y
		    LP2.X = LP1.X + MaxWidth+ RowSpace
		    LP2.Y = LP1.Y
		    line.Start = LP1
		    line.End = LP2
		    LineElem = kcs_draft.line_new(line)
		    kcs_draft.element_linetype_set(LineElem, LineType)
		    LineNum = 0

		
	p1.X = TopLeft.X + ColWidth[0]
	Cpoint.X = TopLeft.X + ColWidth[0]+ RowSpace
	p1.Y = TopLeft.Y
	Cpoint.Y = TopLeft.Y
	#
	# Add the other columns. Alignment Right
	#
	for I in range(start+1,num):
	    Cpoint.X = Cpoint.X + ColWidth[I]
	    Cpoint.Y = TopLeft.Y
	    nHeight = 0
	    for J in Data:
		CellText.SetString(J[I])
		textElem = kcs_draft.text_new(CellText)
		Extent = kcs_draft.element_extent_get(textElem)
		kcs_draft.element_delete(textElem)
		p1.Y = Cpoint.Y - LineStart
		Cpoint.Y = Cpoint.Y - RowHeight[nHeight]
		nHeight = nHeight + 1
		p1.X = Cpoint.X - (Extent.Corner2.X - Extent.Corner1.X)
		CellText.SetPosition(p1)
		textElem = kcs_draft.text_new(CellText)
		
	TopLeft.Y = Cpoint.Y - LineStart
	start = num-1
