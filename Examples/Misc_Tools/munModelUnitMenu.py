## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.






import kcs_gui
import kcs_util

#==============================================================#
# Name :
#      munModelUnitMenu.py  #
# Purpose:
#     This File Contains a Class for creating Model Unit Menu #
#==============================================================#



#============================================================================================#
# Attributes:
#           main_pos -is the position of the user menu added
#           main_caption -is the Caption of the user menu added
#           main_menu_id -is the id of the main frame menu
#           usr_menu_id -is the id of the user menu added
#           usr_def_munit_id -is the id of the user menu item for define model unit added
#           usr_hl_munit_id -is the id of the user menu item for highlight model unit added
#           usr_udef_munit_id -is the id of the user menu item for Undefine model unit added
#============================================================================================#



class CModelUnitMenu:
    def __init__(self,pos,cap):
        self.main_pos=pos
        self.main_caption=cap
        self.main_menu_id=0
        self.usr_menu_id=0
        self.usr_def_munit_id=0
        self.usr_hl_munit_id=0
        self.usr_udef_munit_id=0
        self.usr_unhl_munit_id=0


# Function to Create Main Menu #
#===========================#
    def CreateMenu(self):
        try:
            self.main_menu_id=kcs_gui.menu_get(None,0)
            self.usr_menu_id=kcs_gui.menu_add(self.main_menu_id,self.main_pos,self.main_caption)
        except:
            print "Model Unit Menu :- Create Menu Module "
            print kcs_gui.error

# Function to Create Sub Menu #
#=============================#
    def CreateDefineModelUnitMenu(self,pos,caption,script):
        try:
            self.usr_def_munit_id=kcs_gui.menu_item_usr_add(self.usr_menu_id,pos,caption,script)
        except:
            print "Model Unit Menu :- Create Define Model Unit Menu Module "
            print kcs_gui.error


# Function to Create Sub Menu #
#=============================#
    def CreateHighLightModelUnitMenu(self,pos,caption,script):
        try:
            self.usr_hl_munit_id=kcs_gui.menu_item_usr_add(self.usr_menu_id,pos,caption,script)
        except:
            print "Model Unit Menu :- Create High Light Model Unit Menu Module "
            print kcs_gui.error


# Function to Create Sub Menu #
#=============================#
    def CreateUnDefineModelUnitMenu(self,pos,caption,script):
        try:
            self.usr_udef_munit_id=kcs_gui.menu_item_usr_add(self.usr_menu_id,pos,caption,script)
        except:
            print "Model Unit Menu :- Create UnDefine Model Unit Menu Module "
            print kcs_gui.error


# Function to Create Sub Menu #
#=============================#
    def CreateUnHighLightModelUnitMenu(self,pos,caption,script):
        try:
            self.usr_unhl_munit_id=kcs_gui.menu_item_usr_add(self.usr_menu_id,pos,caption,script)
        except:
            print "Model Unit Menu :- Create UnHighLight Model Unit Menu Module "
            print kcs_gui.error




