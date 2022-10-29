## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.


#=================================================================================#
# Name:
#   munModel_Unit.py
# Pupose:
# This File contains the sample code snippet for a user defined attribute script
# to be inserted while attaching the attribute to a model
#================================================================================#

def get(*args):
    import kcs_att
    import kcs_att_General
    res=""
    found=None
    args[0].PartId=0
    att=kcs_att.attribute_first_get(args[0],0)
    while att and not found:
        found=kcs_att.attribute_is(att,kcs_att_General.kcs_General_ModelUnit())
        if not found:
            att=kcs_att.attribute_next_get()
    if found:
        res=kcs_att.string_get(att,0)
    return res
