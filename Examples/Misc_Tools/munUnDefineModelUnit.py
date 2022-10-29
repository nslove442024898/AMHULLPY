## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.



import kcs_ui
import kcs_att
import kcs_att_General
import kcs_draft
import kcs_util
import KcsModel
import KcsPoint2D
import KcsStringlist

#===============================================================#
# Name :
#       munUnDefineModelUnit.py
# Purpose:
#         This File Serves to UnDefine a Model Unit             #
#===============================================================#





# Function that checks if a model has a valid model unit attribute and if present detaches the attribute
#========================================================================================================#
def DetachModelUnit(model,att_val):
    att=None
    data=""
    found=0
    try:
        print "In the Detach Model"
        att=kcs_att.attribute_first_get(model,1)
        while att and not found:
            found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
            if not found:
                att=kcs_att.attribute_next_get(1)
        if found:
           print "In Found Detach Model"
           data=kcs_att.string_get(att,0)
           if data==att_val:
              print "In Equal Detach Model"
              print data
              kcs_att.attribute_detach(model,att)
              kcs_att.model_save(model)
              return 1
        else:
            return 0
    except:
        print "Attribute detach error "+str(kcs_att.error)
        return 0







# Function that checks if the model has a model unit attribute and returns the same if found
#============================================================================================#
def CheckModelUnit(point):
    mod=KcsModel.Model()
    model_unit_value=""
    att=None
    found=0
    res=0
    err=0
    flag=1
    while flag:
        try:
            model=kcs_draft.model_identify(point,mod)
            model[0].PartId=0
            flag=0
            try:
                att=kcs_att.attribute_first_get(model[0],1)
                while att and not found:
                    found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
                    if not found:
                        att=kcs_att.attribute_next_get(1)
                if found:
                    model_unit_value=kcs_att.string_get(att,0)
            except:
                err=1
                print "Attribute Error :"+str(kcs_att.error)
        except:
            print "Model Error "+str(kcs_draft.error)
            err=1
        if found:
            break
        if (err!=1 and not found) :
           kcs_ui.message_confirm("No Model Unit Attached")
        elif (err==1 and not found) :
            kcs_ui.message_confirm(" Model  not  Identified")
        pp=kcs_ui.point2D_req("Select a Model",point)
        if pp[0]==kcs_util.operation_complete():
           flag=0
        elif pp[0]==kcs_util.exit_function():
           flag=0
        else:
           flag=1
           err=0

    if found:
        return model_unit_value
    elif err==1:
        return 0
    else:
        return None








# Portrays Info about the traversed models
#=======================================================#
def ModelInfo(model):
    try:
        st=KcsStringlist.Stringlist(str(model.Name))
        st.AddString(str(model.Type))
        st.AddString(str(model.PartId))
        kcs_ui.string_select("Model Info","","",st)
    except:
        print "Model Info"+str(kcs_ui.error)





# The main function which is used to undefine a Model Unit#
#==========================================================#
def UnDefine():
    model_unit=""
    nInd=1
    point=KcsPoint2D.Point2D()
    pp=kcs_ui.point2D_req("Select a Model",point)
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
                        print name
                    except:
                        print "Error :"+str(kcs_draft.error)
                    mod=KcsModel.Model()
                    try:
                        model=kcs_draft.model_properties_get(viewhandle,mod)
                    except:
                        print "Error : kcs_draft.model_properties_get : "+str(kcs_draft.error)
                    if DetachModelUnit(model,model_unit)==1:
                        print "Info : Attribute Dettached"
                    else:
                        print "Info : Attribute Not Dettached"
                    viewhandle=kcs_draft.element_sibling_next_get(viewhandle)
                    nInd=nInd+1
                except:
                    nInd=0
                    print "Error :"+str(kcs_draft.error)
        except:
            print "draft Error "+str(kcs_draft.error)
    #elif model_unit==None:
    #    kcs_ui.message_confirm("No ModelUnit Attached")
    #else:
    #    kcs_ui.message_confirm("Model  not  Identified")








# This function definiton to be written in order that the script runs when the userdefined menu is clicked #
#==============================================================================================================#
def run(*args):
    UnDefine()



