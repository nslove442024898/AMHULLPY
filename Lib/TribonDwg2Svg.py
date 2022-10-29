## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
from win32com.client import Dispatch
from win32com.client import gencache

from xml.dom.minidom import Document
from xml.dom.ext import PrettyPrint

from math import *
from os import remove
import string;

import kcs_draft
import kcs_util

CADMODULE			= gencache.EnsureModule('{196E4B75-A752-497D-B18A-D51C658E95C0}', 0, 1, 0)

LWPOLYLINE          = "LWPOLYLINE"
LINE                = "LINE"
ARC                 = "ARC"
TEXT                = "TEXT"
CIRCLE              = "CIRCLE"
INSERT              = "INSERT"

MAXSIZEINPIXELS     = 1000

LINEWIDTH           = 0.0539429

TbEnv = Dispatch("TbRuntime.TBEnvironment")

class RgbColour:
    Values = (  (  0, 0, 0),(255,   0,   0),(255, 255,   0),(  0, 255,   0),
                (  0, 255, 255),(  0,   0, 255),(255,   0, 255),(0, 0, 0),
                (152, 152, 152),(192, 192, 192),(255,   0,   0),(255, 128, 128),
                (166,   0,   0),(166,  83,  83),(128,   0,   0),(128,  64,  64),
                ( 76,   0,   0),( 76,  38,  38),( 38,   0,   0),( 38,  19,  19),
                (255,  64,   0),
                (255, 159, 128),(166,  41,   0),(166, 104,  83),(128,  32,   0),
                (128,  80,  64),( 76,  19,   0),( 76,  48,  38),( 38,  10,   0),
                ( 38,  24,  19),(255, 128,   0),(255, 191, 128),(166,  83,   0),
                (166, 124,  83),(128,  64,   0),(128,  96,  64),( 76,  38,   0),
                ( 76,  57,  38),( 38,  19,   0),( 38,  29,  19),(255, 191,   0),
                (255, 223, 128),(166, 124,   0),(166, 145,  83),(128,  96,   0),
                (128, 112,  64),( 76,  57,   0),( 76,  67,  38),( 38,  29,   0),
                ( 38,  33,  19),(255, 255,   0),(255, 255, 128),(166, 166,   0),
                (166, 166,  83),(128, 128,   0),(128, 128,  64),( 76,  76,   0),
                ( 76,  76,  38),( 38,  38,   0),( 38,  38,  19),(191, 255,   0),
                (223, 255, 128),(124, 166,   0),(145, 166,  83),( 96, 128,   0),
                (112, 128,  64),( 57,  76,   0),( 67,  76,  38),( 29,  38,   0),
                ( 33,  38,  19),(128, 255,   0),(191, 255, 128),( 83, 166,   0),
                (124, 166,  83),( 64, 128,   0),( 96, 128,  64),( 38,  76,   0),
                ( 57,  76,  38),( 19,  38,   0),( 29,  38,  19),( 64, 255,   0),
                (159, 255, 128),( 41, 166,   0),(104, 166,  83),( 32, 128,   0),
                ( 80, 128,  64),( 19,  76,   0),( 48,  76,  38),( 10,  38,   0),
                ( 24,  38,  19),(  0, 255,   0),(128, 255, 128),(  0, 166,   0),
                ( 83, 166,  83),(  0, 128,   0),( 64, 128,  64),(  0,  76,   0),
                ( 38,  76,  38),(  0,  38,   0),( 19,  38,  19),(  0, 255,  64),
                (128, 255, 159),(  0, 166,  41),( 83, 166, 104),(  0, 128,  32),
                ( 64, 128,  80),(  0,  76,  19),( 38,  76,  48),(  0,  38,  10),
                ( 19,  38,  24),(  0, 255, 128),(128, 255, 191),(  0, 166,  83),
                ( 83, 166, 124),(  0, 128,  64),( 64, 128,  96),(  0,  76,  38),
                ( 38,  76,  57),(  0,  38,  19),( 19,  38,  29),(  0, 255, 191),
                (128, 255, 223),(  0, 166, 124),( 83, 166, 145),(  0, 128,  96),
                ( 64, 128, 112),(  0,  76,  57),( 38,  76,  67),(  0,  38,  29),
                ( 19,  38,  33),(  0, 255, 255),(128, 255, 255),(  0, 166, 166),
                ( 83, 166, 166),(  0, 128, 128),( 64, 128, 128),(  0,  76,  76),
                ( 38,  76,  76),(  0,  38,  38),( 19,  38,  38),(  0, 191, 255),
                (128, 223, 255),(  0, 124, 166),( 83, 145, 166),(  0,  96, 128),
                ( 64, 112, 128),(  0,  57,  76),( 38,  67,  76),(  0,  29,  38),
                ( 19,  33,  38),(  0, 128, 255),(128, 191, 255),(  0,  83, 166),
                ( 83, 124, 166),(  0,  64, 128),( 64,  96, 128),(  0,  38,  76),
                ( 38,  57,  76),(  0,  19,  38),( 19,  29,  38),(  0,  64, 255),
                (128, 159, 255),(  0,  41, 166),( 83, 104, 166),(  0,  32, 128),
                ( 64,  80, 128),(  0,  19,  76),( 38,  48,  76),(  0,  10,  38),
                ( 19,  24,  38),(  0,   0, 255),(128, 128, 255),(  0,   0, 166),
                ( 83,  83, 166),(  0,   0, 128),( 64,  64, 128),(  0,   0,  76),
                ( 38,  38,  76),(  0,   0,  38),( 19,  19,  38),( 64,   0, 255),
                (159, 128, 255),( 41,   0, 166),(104,  83, 166),( 32,   0, 128),
                ( 80,  64, 128),( 19,   0,  76),( 48,  38,  76),( 10,   0,  38),
                ( 24,  19,  38),(128,   0, 255),(191, 128, 255),( 83,   0, 166),
                (124,  83, 166),( 64,   0, 128),( 96,  64, 128),( 38,   0,  76),
                ( 57,  38,  76),( 19,   0,  38),( 29,  19,  38),(191,   0, 255),
                (223, 128, 255),(124,   0, 166),(145,  83, 166),( 96,   0, 128),
                (112,  64, 128),( 57,   0,  76),( 67,  38,  76),( 29,   0,  38),
                ( 33,  19,  38),(255,   0, 255),(255, 128, 255),(166,   0, 166),
                (166,  83, 166),(128,   0, 128),(128,  64, 128),( 76,   0,  76),
                ( 76,  38,  76),( 38,   0,  38),( 38,  19,  38),(255,   0, 191),
                (255, 128, 223),(166,   0, 124),(166,  83, 145),(128,   0,  96),
                (128,  64, 112),( 76,   0,  57),( 76,  38,  67),( 38,   0,  29),
                ( 38,  19,  33),(255,   0, 128),(255, 128, 191),(166,   0,  83),
                (166,  83, 124),(128,   0,  64),(128,  64,  96),( 76,   0,  38),
                ( 76,  38,  57),( 38,   0,  19),( 38,  19,  29),(255,   0,  64),
                (255, 128, 159),(166,   0,  41),(166,  83, 104),(128,   0,  32),
                (128,  64,  80),( 76,   0,  19),( 76,  38,  48),( 38,   0,  10),
                ( 38,  19,  24),( 84,  84,  84),(118, 118, 118),(152, 152, 152),
                (187, 187, 187),(221, 221, 221),(255, 255, 255),
                (125, 125, 125),(255, 255, 255) )

class Dxf2Svg:
    def __init__(self):
        self.dxf = None
        self.xml = None

        self.dxfmin = None
        self.dxfmax = None

        self.height = 0

    def Convert(self, dxffile, xmlfile):
        self.dxf = Dispatch("TbCadInterface.TbDatabase")
        if self.dxf.ReadDxfFile(dxffile)==0:
            self.CreateXmlDocument()
            root = self.CreateRootElement()
            if root != None:
                self.ExportLinetypes(root)
                self.ProcessBlocks(root)
                self.SaveXmlFile(xmlfile)

    def SaveXmlFile(self, filename):
        file = open(filename, "w")
        PrettyPrint(self.xml, file)
        file.close()

    def CreateXmlDocument(self):
        try:
            self.xml = Document()
            return 1
        except Exception, e:
            return 0

    def CreateRootElement(self):
        svg = self.xml.createElementNS("http://www.w3.org/2000/svg", "svg")

        self.dxfmin = self.dxf.GetEXTMIN()
        self.dxfmax = self.dxf.GetEXTMAX()

        #print "Extents: ", self.dxfmin.x, " ", self.dxfmin.y, " ", self.dxfmax.x, " ", self.dxfmax.y

        width   = abs(self.dxfmax.x-self.dxfmin.x)
        height  = abs(self.dxfmax.y-self.dxfmin.y)

        if width==0 or height==0:
            AddToLogFile("Drawing extents not supported!")
            return None

        self.height = height

        if width>height:
            nwidth = MAXSIZEINPIXELS
            nheight = int(float(height)/width * MAXSIZEINPIXELS);
        else:
            nwidth = int(float(width)/height * MAXSIZEINPIXELS);
            nheight = MAXSIZEINPIXELS

        svg.setAttribute("width", str(nwidth))
        svg.setAttribute("height", str(nheight))

        svg.setAttribute("viewBox", "%d %d %d %d" % (int(self.dxfmin.x-1), int(self.height-self.dxfmax.y-1), int(width+2), int(height+2)))
        svg.setAttribute("xmlns:vnet", "http://www.aveva.com/VNET")
        svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
        svg.setAttribute("xml:space", "preserve")
        svg.setAttribute("zoomAndPan", "magnify")
        svg.setAttribute("style", "fill:none;stroke:black")

        rect = self.xml.createElement("rect")
        rect.setAttribute("x", "0")
        rect.setAttribute("y", "0")
        rect.setAttribute("width", str(nwidth))
        rect.setAttribute("height", str(nheight))
        rect.setAttribute("style", "stroke:none; fill:white")
        svg.appendChild(rect)

        self.xml.appendChild(svg)

        return svg

    def ExportLinetypes(self, xmlnode):
        try:
            Linetypes = self.dxf.GetLinetypes()
            style = xmlnode.ownerDocument.createElement("style")
            style.setAttribute("type", "text/css")
            xmlnode.appendChild(style)

            value = ""
            for nIndex in range(0, Linetypes.Count):
                lt = Linetypes.GetAt(nIndex)
                if not self.IsStandardLinetype(lt):
                    pattern = "stroke-dasharray:"
                    for nSegIndex in range(0, lt.NumberOfSegments):
                        seg = lt.GetSegmentAt(nSegIndex)
                        if nSegIndex==0:
                            pattern = pattern + str(fabs(seg.Length))
                        else:
                            pattern = pattern + "," + str(fabs(seg.Length))
                    value = value + "." + lt.Name + " {stroke:#000000;stroke-linecap:round;stroke-linejoin:round;stroke-width:0.72;" + pattern + "}\n"

            if value != "":
                cdata = xmlnode.ownerDocument.createCDATASection(value)
                style.appendChild(cdata)
        except Exception, e:
            pass

    def ProcessBlocks(self, xmlnode):
        blocks = self.dxf.GetBlocks()
        for index in range(0, blocks.Count):
            block = blocks.GetAt(index)
            self.ProcessBlock(block, xmlnode)

    def CreateVnetId(self, node, block):
        try:
            compid = int(string.split(block.Name, "-")[-1])
            if compid == 1000:  #boundary
                return
            model = string.join(string.split(block.Name, "-")[1:-1], "-")
        except:
            return

        if compid>6000 and compid<7000:
            strvnetid = "stiffener %d of /%s" % (compid-6000, model)
        elif compid>1000 and compid<2000:
            strvnetid = "bracket %d of /%s" % (compid-1000, model)
        elif compid>23000 and compid<24000:
            strvnetid = "doubling %d of /%s" % (compid-23000, model)
        elif compid>7000 and compid<8000:
            strvnetid = "flange %d of /%s" % (compid-7000, model)
        elif compid>8000 and compid<9000:
            strvnetid = "pillar %d of /%s" % (compid-8000, model)
        elif compid>2000 and compid<3000:
            strvnetid = "plate %d of /%s" % (compid-2000, model)
        elif compid>5000 and compid<6000:
            return; #seam not supported by sz030
        else:
            strvnetid = "Part %d of /%s" % (compid, model)

        metadata = node.ownerDocument.createElement("metadata")
        node.appendChild(metadata)
        vnetid = metadata.ownerDocument.createElement("vnet:id")
        vnetid.appendChild(vnetid.ownerDocument.createTextNode(strvnetid))
        metadata.appendChild(vnetid)

    def CreateGElement(self, block, xmlnode):
        g = xmlnode.ownerDocument.createElement("g")
        g.setAttribute("id", block.Name)
        self.CreateVnetId(g, block)
        return g

    def ProcessBlock(self, block, xmlnode):
        if block.EntityCount > 0:
            g = self.CreateGElement(block, xmlnode)
            xmlnode.appendChild(g)

            for index in range(0, block.EntityCount):
                entity = block.GetEntityAt(index)
                if entity.IsVisible():
                    if entity.Type == LWPOLYLINE:
                        self.ExportLwPolyline(entity, g)
                    elif entity.Type == LINE:
                        self.ExportLine(entity, g)
                    elif entity.Type == ARC:
                        self.ExportArc(entity, g)
                    elif entity.Type == TEXT:
                        self.ExportText(entity, g)
                    elif entity.Type == CIRCLE:
                        self.ExportCircle(entity, g)
                    elif entity.Type == INSERT:
                        pass
                    else:
                        print "\nElement not supported: " + entity.Type

    def GetEntityColour(self, entity):
        colourIdx = entity.Colour;
        rgbvalues = RgbColour.Values[colourIdx]
        return "#%.2X%.2X%.2X" % rgbvalues;

    def CalculateArc1(self, vs, ve):
        x1, y1, bulge, x2, y2 = float(vs.x), float(vs.y), float(vs.Bulge), float(ve.x), float(ve.y)
        alpha = abs(2 * atan(bulge))
        l2 = sqrt((x2 - x1)*(x2 - x1) + (y2 - y1) * (y2 - y1)) / 2.0
        R = l2 / sin(alpha)
        if bulge<0:
            fs =  1
        else:
            fs = 0

        return (R, R, 0.0, 0, fs, ve.x, self.height-ve.y)

    def CalculateArc2(self, center, start, end, radius):
        start = start * pi/180.0
        end = end * pi/180.0
        x1 = center.x + radius * cos(start)
        y1 = center.y + radius * sin(start)
        x2 = center.x + radius * cos(end)
        y2 = center.y + radius * sin(end)
        return (x1, self.height-y1, radius, radius, 0.0, 0, 0, x2, self.height-y2)

    def ExportArc(self, entity, xmlnode):
        lt = entity.GetLinetype()
        colour = self.GetEntityColour(entity)

        arc = CADMODULE.ITbEntArc(entity)

        path = xmlnode.ownerDocument.createElement("path")
        path.setAttribute("style", "stroke:%s; stroke-width:%f" % (colour, LINEWIDTH))

        pathd = "M%f %fA%f %f %f %d %d %f %f" % self.CalculateArc2(arc.GetCenterPoint(), arc.StartAngle, arc.EndAngle, arc.Radius)
        path.setAttribute("d", pathd)

        if not self.IsStandardLinetype(lt):
            path.setAttribute("class", lt.Name);

        xmlnode.appendChild(path)

    def ExportLwPolyline(self, entity, xmlnode):
        lt = entity.GetLinetype()
        colour = self.GetEntityColour(entity)
        lwpoly = CADMODULE.ITbEntLWPolyline(entity)

        if lwpoly.VertexCount > 0:
            path = xmlnode.ownerDocument.createElement("path")
            path.setAttribute("style", "stroke:%s; stroke-width:%f" % (colour, LINEWIDTH))

            vs = lwpoly.GetVertexAt(0)
            pathd = "M%f %f" % (vs.x, self.height-vs.y)
            for index in range(1, lwpoly.VertexCount):
                ve = lwpoly.GetVertexAt(index)
                if vs.Bulge != 0.0:
                    pathd = pathd + ("A%f %f %f %d %d %f %f" % self.CalculateArc1(vs, ve))
                else:
                    pathd = pathd + ("L%f %f" % (ve.x, self.height-ve.y))
                vs = ve;

            path.setAttribute("d", pathd)

            if not self.IsStandardLinetype(lt):
                path.setAttribute("class", lt.Name);

            xmlnode.appendChild(path)

    def ExportLine(self, entity, xmlnode):
        lt = entity.GetLinetype()
        colour = self.GetEntityColour(entity)

        line = CADMODULE.ITbEntLine(entity)
        s = line.GetStartPoint()
        e = line.GetEndPoint()

        path = xmlnode.ownerDocument.createElement("path")
        path.setAttribute("d", "M%f %fL%f %f" % (s.x, self.height-s.y, e.x, self.height-e.y))
        path.setAttribute("style", "stroke:%s; stroke-width:%f" % (colour, LINEWIDTH))

        if not self.IsStandardLinetype(lt):
            path.setAttribute("class", lt.Name);

        xmlnode.appendChild(path)

    def ExportText(self, entity, xmlnode):
        colour = self.GetEntityColour(entity)

        text = CADMODULE.ITbEntText(entity)
        p = text.GetAlignmentPoint()
        x, y = p.x, self.height - p.y
        h = text.Height
        r = text.Rotation

        style = text.GetTextStyle()

        textnode = xmlnode.ownerDocument.createElement("text")
        textnode.setAttribute("x", str(x))
        textnode.setAttribute("y", str(y))
        textnode.setAttribute("font-family", style.FontName)
        textnode.setAttribute("style", "stroke-width:%f" % (LINEWIDTH,))
        textnode.setAttribute("font-size", "%f" % (h, ))
        textnode.setAttribute("fill", colour)
        if r != 0.0:
            textnode.setAttribute("transform", "rotate(%f %f %f)" % (-r,x,y))

        textnode.appendChild(textnode.ownerDocument.createTextNode(text.Text))
        xmlnode.appendChild(textnode)

    def IsStandardLinetype(self, lt):
        return lt.Name == "BYLAYER" or lt.Name=="BYBLOCK" or lt.Name == "CONTINUOUS";

    def ExportCircle(self, entity, xmlnode):
        lt = entity.GetLinetype()
        colour = self.GetEntityColour(entity)

        circle = CADMODULE.ITbEntCircle(entity)
        c = circle.GetCenterPoint()
        r = circle.Radius

        circlenode = xmlnode.ownerDocument.createElement("circle")
        circlenode.setAttribute("cx", "%f" % (c.x, ))
        circlenode.setAttribute("cy", "%f" % (self.height-c.y, ))
        circlenode.setAttribute("r", "%f" % (r, ))
        circlenode.setAttribute("style", "stroke:%s; stroke-width:%f" % (colour, LINEWIDTH))

        if not self.IsStandardLinetype(lt):
            circlenode.setAttribute("class", lt.Name);

        xmlnode.appendChild(circlenode)

def CloseCurrentDrawing():
    try:
        kcs_draft.dwg_close()
    except:
        pass

def DeleteFile(filename):
    try:
        remove(filename)
    except:
        pass

def ReadInputFile(TbEnv):
    result = []
    try:
        filename = TbEnv.Variable("SVG_INPUT")
        f = open(filename)
        lines = f.readlines()
        f.close()
        for line in lines:
            try:
                line = string.replace(line, "\n", "")
                strs = string.split(line, " ")
                result.append((strs[0], strs[-1]))
            except:
                pass
    except Exception, e:
        pass
    return result

def AddToLogFile(message):
    try:
        filename = TbEnv.Variable("SVG_OUTPUT")+"svg.output"
        f = open(filename, "a")
        f.writelines([message+"\n", ])
        f.close()
    except:
        pass

def CreateLogFile():
    try:
        filename = TbEnv.Variable("SVG_OUTPUT")+"svg.output"
        f = open(filename, "w")
        f.writelines(["Drawing conversion started\n",])
        f.close()
    except:
        pass

def ExportDrawing(type, name, output):
    AddToLogFile("Exporting drawing %s from drawing database %s" % (name, str(type)))
    CloseCurrentDrawing()
    try:
        AddToLogFile("   Opening drawing ...")
        try:
            kcs_draft.dwg_open(name, type, kcs_draft.kcsOPENMODE_READONLY)
        except TBException, e:
            AddToLogFile(str(e))
            return
        DeleteFile(output + "result.dxf")
        AddToLogFile("   Exporting to dxf ...")
        kcs_draft.dwg_dxf_export(output+"result.dxf", 14, 0, 0)

        AddToLogFile("   Exporting to svg ...")
        exp = Dxf2Svg()
        svgname = name;
        svgname = string.replace(name, ":", "-")
        exp.Convert(output+"result.dxf", output+svgname + ".svg")
        AddToLogFile("   Ready")

        DeleteFile(output + "result.dxf")
    except Exception, e:
        AddToLogFile(str(e))

try:
    CreateLogFile()
    drawings = ReadInputFile(TbEnv)

    #TbEnv.SetVariable("DXF_SVG", "TRUE") #Currently set by UI
    for drawing in drawings:
        ExportDrawing(drawing[0], drawing[1], TbEnv.Variable("SVG_OUTPUT"))

    kcs_util.exit_program()
except Exception, e:
    AddToLogFile(str(e))






