## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.



import kcs_ui
import kcs_att
import kcs_util
import kcs_att_General
import KcsModel
import KcsPoint2D
import kcs_draft
import KcsStringlist


#===============================================================================#
# Name :
#        munHighlightModelUnit.py                                               #
# Purpose :                                                                     #
#        This File Contains functions to Highlight a models
#        with a ModelUnits Attached                                             #
#===============================================================================#





#===============================================================================#
#         Checks if Model unit Attributes are attached to the Model             #
#===============================================================================#
def CheckAttributes(model,att_val):
    att_lst=[]
    att=None
    found=0
    try:
        try:
            att=kcs_att.attribute_first_get(model,1)
        except:
            print " Error : "+str(kcs_att.error)
        while att and not found:
              found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
              if found==1:
                 att_lst.append(kcs_att.string_get(att,0))
              if not found:
                  try:
                      att=kcs_att.attribute_next_get(1)
                  except:
                      print "Error : "+str(kcs_att.error)
    except:
        print "Error : "+str(kcs_att.error)
    if len(att_lst)>0:
        for i in range(len(att_lst)):
            if att_lst[i]==att_val:
                print att_lst[i]
                return 1
    return 0








#==================================#
#   Gets all the Sub view          #
#==================================#
def GetAllSubViews(subviewlst):
    nInd=1
    name=""
    vhandle=kcs_draft.element_child_first_get()
    while nInd:
          try:
              name=kcs_draft.subpicture_name_get(vhandle)
              GetSubView(vhandle,subviewlst)
              vhandle=kcs_draft.element_sibling_next_get(vhandle)
              nInd=nInd+1
          except:
              nInd=0




def GetSubView(handle,subviewlst):
    nInd=1
    name=""
    viewhandle=kcs_draft.element_child_first_get(handle)
    while nInd:
           try:
                if kcs_draft.element_is_subview(viewhandle):
                   try:
                       name=kcs_draft.subpicture_name_get(viewhandle)
                       subviewlst.append([name,viewhandle])
                   except:
                       print "Error : "+str(kcs_draft.error)
                name=kcs_draft.subpicture_name_get(viewhandle)
                viewhandle=kcs_draft.element_sibling_next_get(viewhandle)
                nInd=nInd+1
           except:
               #print "In Subview "+kcs_draft.error
               nInd=0





#========================================#
# Function for highlighting a Model Unit #
#========================================#
def HighLightModelUnit():
    model_unit=""
    svlst=[]
    GetAllSubViews(svlst)
    nInd=1
    point=KcsPoint2D.Point2D()
    pt=kcs_ui.point2D_req("Please Indicate a model",point)
    model_unit=CheckModelUnit(point)
    if model_unit!=None and model_unit!=0:
        try:
            handle=kcs_draft.subview_identify(point)
            viewhandle=kcs_draft.element_parent_get(handle)
            viewhandle=kcs_draft.element_child_first_get(viewhandle)
            while nInd:
                try:
                    try:
                        name=kcs_draft.subpicture_name_get(viewhandle)
                    except:
                        print "Error : "+str(kcs_draft.error)
                    mod=KcsModel.Model()
                    model=kcs_draft.model_properties_get(viewhandle,mod)
                    #ModelInfo(model)
                    if CheckAttributes(model,model_unit)==1:
                        try:
                            for i in range(len(svlst)):
                                if svlst[i][0]==name:
                                   kcs_draft.element_highlight(svlst[i][1])
                        except:
                            print kcs_draft.error
                    viewhandle=kcs_draft.element_sibling_next_get(viewhandle)
                    nInd=nInd+1
                except:
                    nInd=0

        except:
            print "Error : "+str(kcs_draft.error)
    #elif model_unit==None:
    #    kcs_ui.message_confirm(" No ModelUnit Attached ")
    #else:
    #    kcs_ui.message_confirm(" Model not Identified ")








#======================#
# Checks for ModelUnit #
#======================#
def CheckModelUnit(point):
    flag=1
    att=None
    found=0
    res=0
    err=0
    model_unit_value=""
    while flag:
        try:
            mod=KcsModel.Model()
            model=kcs_draft.model_identify(point,mod)
            model[0].PartId=0
            print str(model[0].Name)
            try:
                att=kcs_att.attribute_first_get(model[0],1)
                while att and not found:
                        found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
                        if not found:
                            att=kcs_att.attribute_next_get(1)
                if found:
                        try:
                            model_unit_value=kcs_att.string_get(att,0)
                        except:
                            print "string get"+str(kcs_att.error)
            except:
                print "Attribute error : "+str(kcs_att.error)
                err=1
        except:
            print "Draft error : "+str(kcs_draft.error)
            err=1
        if found:
            break
        if (err!=1 and not found) :
            kcs_ui.message_confirm("No Model Unit Attached")
        elif (err==1 and not found):
            kcs_ui.message_confirm("Model not Identified ")
        pp=kcs_ui.point2D_req("Select a Model",point)
        if pp[0]==kcs_util.operation_complete():
           flag=0
        elif pp[0]==kcs_util.exit_function():
           flag=0
        else:
           flag=1
           err=0

    if found: # if Successfully got a Model Unit
        return model_unit_value
    elif err==1: # if Error Occured
        return 0
    else:
        return None # if Could not find a Model Unit








#=======================#
# Info about the Model  #
#=======================#
def ModelInfo(model):
    try:
       st=KcsStringlist.Stringlist("Name : "+str(model.Name))
       st.AddString("Type : "+str(model.Type))
       st.AddString("Type : "+str(model.PartId))
       kcs_ui.string_select("Mdoel Info","","",st)
    except:
       print "Define Model Unit :- \n Model Info Module :-"+str(kcs_draft.error)
       kcs_ui.message_confirm("Define Model Unit :- \n Model Info Module :-"+str(kcs_draft.error))



# This function should be Defined so that the script is called when a user clicks on the user defined menu #
def run(*args):
    HighLightModelUnit()



