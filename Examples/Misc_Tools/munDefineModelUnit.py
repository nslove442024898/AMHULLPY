## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_ui
import kcs_util
import kcs_draft
import KcsModel
import KcsPoint2D
import KcsStringlist
import kcs_att
import kcs_att_General



#================================================================================#
# Name:
#     munDefineModelUnit.py                                                 #
#                                                                               #
# Purpose:
# This File Contains functions to Define a Model Unit for Selected Model objects #
#================================================================================#






#=======================================================================#
# This is a Utility function to check if duplicate Models are Selected #
#=======================================================================#
def CheckDuplicate(lst,model):
    res=0
    if len(lst)>0:
        for cnt in range(len(lst)):
            if lst[cnt].Name==model.Name and lst[cnt].Type==model.Type:
                res=1
                break
    else:
        res=-1
    return res





#================================================================================#
# This Function Checks if a ModelUnit is already attached to the specified model #
#================================================================================#
def ModelUnitExist(model):
    att=None
    model.PartId=0
    found=0
    try:
        att=kcs_att.attribute_first_get(model,1)
        while att and not found:
            found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
            if not found:
                att=kcs_att.attribute_next_get(1)
        if found:
            return 1
        else:
            return 0
    except:
        print "ModelUnitExists :-"+str(kcs_att.error)





#===================================================#
# This Function is Used to Define a Model Unit      #
#===================================================#
def DefineModelUnit():
    model_lst=[]
    operation_status=0
    while operation_status==0:
        mod=KcsModel.Model()
        point=KcsPoint2D.Point2D()
        res=kcs_ui.point2D_req("Select a Model",point)
        if res[0]==kcs_util.operation_complete():
            operation_status=1
        elif res[0]==kcs_util.exit_function():
            operation_status=-1
        try:
            model=kcs_draft.model_identify(point,mod)
            if ModelUnitExist(mod)==0:
                val=CheckDuplicate(model_lst,mod)
                if val==-1:
                    mod.PartId=0
                    if ShowModel(mod):        # New Addition Made on 20-12-2001
                        model_lst.append(mod)
                elif val==0:
                    mod.PartId=0
                    if ShowModel(mod):        # New Addition Made on 20-12-2001
                        model_lst.append(mod)
            else:
                kcs_ui.message_confirm(" Object Cannot be Selected as already part of ModelUnit")
        except:
            print "Define Model Unit :- \n Error :-"+str(kcs_draft.error)
            res=kcs_ui.answer_req("Define Model","Do You wish to select more Models?")
            if res==202:
               operation_status=1
    if len(model_lst)>0 and operation_status==1:
        #ModelInfo(model_lst)
        res=kcs_ui.string_req("Enter the name of the Model Unit","Name")
        if res[0]==271:
           try:
               for cnt in range(len(model_lst)):
                   model_lst[cnt].PartId=0
                   att=kcs_att.attribute_create(model_lst[cnt],"General","ModelUnit")
                   #kcs_att.attribute_attach(model_lst[cnt],att)
                   kcs_att.string_set(model_lst[cnt],att,0,res[1])
                   kcs_att.model_save(model_lst[cnt])
           except:
               print "Define Model Unit :- \n Error :-"+str(kcs_att.error)
    else:
        kcs_ui.message_confirm("No Model Selected")
    kcs_draft.highlight_off(0)






#======================================================#
# This function portrays the Info about  Model Objects #
#======================================================#
def ModelInfo(model_lst):
    import KcsStringlist
    for cnt in range(len(model_lst)):
        try:
            st=KcsStringlist.Stringlist("Name : "+str(model_lst[cnt].Name))
            st.AddString("Type : "+str(model_lst[cnt].Type))
            st.AddString("Type : "+str(model_lst[cnt].PartId))
            kcs_ui.string_select("Mdoel Info","","",st)
        except:
            print "Define Model Unit :- \n Model Info Module :-"+str(kcs_draft.error)
            kcs_ui.message_confirm("Define Model Unit :- \n Model Info Module :-"+str(kcs_draft.error))




#=============================================================================================#
# This function serves the purpose of displaying the model selected for Defining a Model Unit #
#=============================================================================================#
def ShowModel(model):
    svlist=[]
    viewhandle=[]
    GetAllSubViews(svlist)
    for obj in svlist:
            if model.Name == obj[0]:
                viewhandle.append(obj[1])
                kcs_draft.element_highlight(obj[1])

    res=kcs_ui.answer_req("Define Model Unit","Name : "+model.Name)
    if res==201:
        return 1
    else:
        for obj in viewhandle:
            kcs_draft.highlight_off(obj)
        return 0




#==================================#
#   Gets all the Views             #
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



#==================================#
#   Gets all the Sub Views         #
#==================================#
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







#========================================================================================#
# This function is necessary for the script to run when clicked on the user defined menu #
#========================================================================================#
def run(*args):
    DefineModelUnit()


