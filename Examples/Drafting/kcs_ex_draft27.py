## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft27.py
#
#      PURPOSE:
#
#          This example sets print options and print current drawing
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsStringlist
import KcsPrintOptions
import KcsPoint2D


#-------------------------------------------------------------------------------------------------------------
def BuildOptionsList(options):
    list = KcsStringlist.Stringlist('Printer: '+options.GetPrinterName())
    if options.GetOrientation()==0:
        list.AddString('Orient: Default')
    elif options.GetOrientation()==1:
        list.AddString('Orient: Portrait')
    else:
        list.AddString('Orient: Landscape')

    if options.IsPrintToFile():
        list.AddString('PrintToFile: Yes')
    else:
        list.AddString('PrintToFile: No')

    list.AddString('File: '+options.GetFileName())

    if options.GetNumberOfCopies()==0:
        list.AddString('No of copies: Default')
    else:
        list.AddString('No of copies: ' + str(options.GetNumberOfCopies()))

    if options.GetEffectivePrintArea()==0:
        list.AddString('Area: Default')
    elif options.GetEffectivePrintArea()==1:
        list.AddString('Area: Drawing Form')
    elif options.GetEffectivePrintArea()==2:
        list.AddString('Area: Drawing Extension')
    elif options.GetEffectivePrintArea()==3:
        list.AddString('Area: Current Window')
    elif options.GetEffectivePrintArea()==4:
        list.AddString('Area: Capture Area')

    if options.GetAutoOrient()==1:
        list.AddString('AutoOrient: Yes')
    elif options.GetAutoOrient()==2:
        list.AddString('AutoOrient: No')
    elif options.GetAutoOrient()==3:
        list.AddString('AutoOrient: 90')
    elif options.GetAutoOrient()==4:
        list.AddString('AutoOrient: 180')
    elif options.GetAutoOrient()==5:
        list.AddString('AutoOrient: 270')
    else:
        list.AddString('AutoOrient: Default')

    if options.GetCenterOnPage()==0:
        list.AddString('CenterOnPage: Default')
    elif options.GetCenterOnPage()==1:
        list.AddString('CenterOnPage: Yes')
    else:
        list.AddString('CenterOnPage: No')

    if options.GetScaleToFit()==0:
        list.AddString('ScaleToFit: Default')
    elif options.GetScaleToFit()==1:
        list.AddString('ScaleToFit: Yes')
    else:
        list.AddString('ScaleToFit: No')

    if options.GetScale()==0.0:
        list.AddString('Scale: Default')
    else:
        list.AddString('Scale: ' + str(options.GetScale()))

    if options.Point1 == options.Point2:
        list.AddString('Capture Area: Not set')
    else:
        list.AddString('Capture Area: Set')

    list.AddString('Print Drawing')



    return list;


#-------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    # get user choice and select entity
    options = KcsPrintOptions.PrintOptions('');
    actions = KcsStringlist.Stringlist('')
    actions = BuildOptionsList(options);

    result = 1
    while result:
        res = kcs_ui.choice_select('Print', '', actions)
        if res[0]==kcs_util.ok():
            if res[1] == 1:
                (set, name) = kcs_ui.string_req('Device name', options.GetPrinterName())
                options.SetPrinterName(name)
                actions = BuildOptionsList(options);
            elif res[1] == 2:
                if options.GetOrientation()==0:
                    options.SetOrientation(1)
                elif options.GetOrientation()==1:
                    options.SetOrientation(2)
                elif options.GetOrientation()==2:
                    options.SetOrientation(0)
                actions = BuildOptionsList(options);
            elif res[1] == 3:
                if options.IsPrintToFile():
                    options.SetPrintToFile(0)
                else:
                    options.SetPrintToFile(1)
                actions = BuildOptionsList(options);
            elif res[1] == 4:
                (set, name) = kcs_ui.string_req('File name', options.GetFileName())
                options.SetFileName(name)
                actions = BuildOptionsList(options);
            elif res[1] == 5:
                (set, copies) = kcs_ui.int_req('Number of copies', options.GetNumberOfCopies())
                if set == kcs_util.ok():
                    options.SetNumberOfCopies(copies)
                actions = BuildOptionsList(options);
            elif res[1] == 6:
                if options.GetEffectivePrintArea()==0:
                    options.SetEffectivePrintArea(1)
                elif options.GetEffectivePrintArea()==1:
                    options.SetEffectivePrintArea(2)
                elif options.GetEffectivePrintArea()==2:
                    options.SetEffectivePrintArea(3)
                elif options.GetEffectivePrintArea()==3:
                    options.SetEffectivePrintArea(4)
                elif options.GetEffectivePrintArea()==4:
                    options.SetEffectivePrintArea(0)
                    options.Point1 = KcsPoint2D.Point2D()
                    options.Point2 = KcsPoint2D.Point2D()
                actions = BuildOptionsList(options);
            elif res[1] == 7:
                if options.GetAutoOrient()==0:
                    options.SetAutoOrient(1)
                elif options.GetAutoOrient()==1:
                    options.SetAutoOrient(2)
                elif options.GetAutoOrient()==2:
                    options.SetAutoOrient(3)
                elif options.GetAutoOrient()==3:
                    options.SetAutoOrient(4)
                elif options.GetAutoOrient()==4:
                    options.SetAutoOrient(5)
                else:
                    options.SetAutoOrient(0)
                actions = BuildOptionsList(options);
            elif res[1] == 8:
                if options.GetCenterOnPage()==0:
                    options.SetCenterOnPage(1)
                elif options.GetCenterOnPage()==1:
                    options.SetCenterOnPage(2)
                else:
                    options.SetCenterOnPage(0)
                actions = BuildOptionsList(options);
            elif res[1] == 9:
                if options.GetScaleToFit()==0:
                    options.SetScaleToFit(1)
                elif options.GetScaleToFit()==1:
                    options.SetScaleToFit(2)
                else:
                    options.SetScaleToFit(0)
                actions = BuildOptionsList(options);
            elif res[1] == 10:
                (set, scale) = kcs_ui.real_req('Scale', options.GetScale())
                if set == kcs_util.ok():
                    options.SetScale(scale)
                actions = BuildOptionsList(options);
            elif res[1] == 11:
                if options.GetEffectivePrintArea()==4:
                    pt1 = KcsPoint2D.Point2D()
                    res,pt1 = kcs_ui.point2D_req('First Point',pt1)
                    pt2 = KcsPoint2D.Point2D()
                    res,pt2 = kcs_ui.point2D_req('Second Point',pt2)
                    options.Point1=pt1
                    options.Point2=pt2
                else:
                    kcs_ui.message_noconfirm("Area has to be set to 'Capture Area' first.")
                actions = BuildOptionsList(options);
            elif res[1] == 12:
                try:
                    print options
                    kcs_draft.dwg_print(options)
                except:
                    print kcs_draft.error
        else:
            result = 0

    kcs_ui.message_noconfirm('Script interrupted')
