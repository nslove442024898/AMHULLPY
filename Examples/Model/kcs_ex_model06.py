## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import string
import kcs_ui
import kcs_util
import kcs_model
import KcsStringlist
import KcsModel
import KcsCommonProperties

OK = kcs_util.ok()
CANCEL  = kcs_util.cancel()

#---------------------------------------------------------------------------------
#  Get TDM Attribute
#---------------------------------------------------------------------------------
def GetTDMAttribute():
   list = []
   list.append('TYPE CODE 1:')   #01
   list.append('TYPE CODE 2:')   #02
   list.append('TYPE CODE 3:')   #03
   list.append('TYPE CODE 4:')   #04
   list.append('PLANING UNIT:')  #05
   list.append('COST CODE:')     #06
   list.append('ALIAS 1:')       #07
   list.append('ALIAS 2:')       #08
   list.append('ALIAS 3:')       #09
   list.append('ALIAS 4:')       #10
   list.append('DESCRIPTION:')   #11
   list.append('REMARKS:')       #12
   return list
#---------------------------------------------------------------------------------
#  Get TDM Attribute value
#---------------------------------------------------------------------------------
def GetTDMAttributeValue(tdm):
   table = []
   s1, s2, s3, s4 = tdm.GetAlias()
   q1, q2, q3, q4 = tdm.GetTypeCode()
   table.append(str(q1) )  #01
   table.append(str(q2) )  #02
   table.append(str(q3) )  #03
   table.append(str(q4) )  #04
   table.append(tdm.GetPlanningUnit())  #05
   table.append(tdm.GetCostCode()    )  #06
   table.append(s1      )  #07
   table.append(s2      )  #08
   table.append(s3      )  #09
   table.append(s4      )  #10
   table.append(tdm.GetDescription() )  #11
   table.append(tdm.GetRemarks()     )  #12
   return table

#---------------------------------------------------------------------------------
# Select TDM Attribute
#---------------------------------------------------------------------------------
def SelectTDMAttributeValue(tab1, tab2):
   strtable = []
   for name in tab1:
      ind = tab1.index(name)
      strtable.append(name + tab2[ind])
   list = KcsStringlist.Stringlist(strtable[0])
   for name in strtable[1:]:
      list.AddString(name)
   res = kcs_ui.string_select('Attributes', 'Current attributes','', list)

   if res[0] == OK:
      return (tab1[res[1]-1], tab2[res[1]-1], res[1]-1) ;
   else:
      return ('', '', -1)

#---------------------------------------------------------------------------------
# Show TDM Attribute
#---------------------------------------------------------------------------------
def ShowTDMAttribute():

   tab1 = GetTDMAttribute()
   tab2 = GetTDMAttributeValue(tdm)

   name, value, index = SelectTDMAttributeValue(tab1, tab2)

#---------------------------------------------------------------------------------
# Check library and active model
#---------------------------------------------------------------------------------
def CheckModel(type, name):

   if (type==1)or(type==2)or(type==11)or(type==12)or(type==15):
      import kcs_hull
   elif (type==3)or(type==4)or(type==13):
      import kcs_pipe
      import KcsPipeName
      try:
         kcs_pipe.pipe_activate(KcsPipeName.PipeName(name))
      except:
         print kcs_pipe.error
   elif (type==5):
      import kcs_equip
      try:
         kcs_equip.equip_cancel()
      except:
         pass
      try:
         kcs_equip.equip_activate(name)
      except:
         print kcs_equip.error
   elif (type==6)or(type==7)or(type==8):
      import kcs_cable
      try:
         if(type==6):
            kcs_cable.cable_activate(name)
         elif (type==7):
            kcs_cable.cway_activate(name)
      except:
         print kcs_cable.error
   elif (type==9):
      import kcs_struct
      try:
         kcs_struct.struct_activate(name)
      except:
         print kcs_struct.error
   elif (type==18):
      import kcs_assembly
      try:
         kcs_assembly.assembly_cancel()
      except:
         pass
      try:
         name = '-'+ name
         kcs_assembly.assembly_activate(name)
      except:
         print kcs_assembly.error

#---------------------------------------------------------------------------------
#  Cancel active model
#---------------------------------------------------------------------------------
def CancelModel(type):

   if (type==3)or(type==4)or(type==13):
      kcs_pipe.pipe_cancel()
   elif (type==5):
      kcs_equip.equip_cancel()
   elif (type==6):
      kcs_cable.cable_cancel()
   elif (type==7):
      kcs_cable.cway_cancel()
   elif (type==9):
      kcs_struct.struct_cancel()
   elif (type==18):
      kcs_assembly.assembly_cancel()

#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
next = 1
while next:

   model = KcsModel.Model()
   tdm   = KcsCommonProperties.CommonProperties()

   main = KcsStringlist.Stringlist('Model object')
   main.AddString('Drawing')
   (status, index) = kcs_ui.choice_select('TDM ATRIBUTTES','Do you want show properties set for ?:',main)
   if status == OK:
      if index == 1:
         tab = KcsStringlist.Stringlist('plane panel')   #01
         tab.AddString('hull curve')                     #02
         tab.AddString('pipe')                           #03
         tab.AddString('pipe spool')                     #04
         tab.AddString('equipment')                      #05
         tab.AddString('cable way')                      #06
         tab.AddString('cable')                          #07
         tab.AddString('penetration')                    #08
         tab.AddString('struct')                         #09
         tab.AddString('placed volume')                  #10
         tab.AddString('longitudinal')                   #11
         tab.AddString('transversal')                    #12
         tab.AddString('ventilation')                    #13
         tab.AddString('subsurface')                     #14
         tab.AddString('lines fairing curve')            #15
         tab.AddString('accomodation')                   #16
         tab.AddString('curved panel')                   #17
         tab.AddString('assembly')                       #18

         res = kcs_ui.string_select('TDM ATTRIBUTES FOR MODEL', 'Select type of model ', '', tab)
         if res[0]==OK:
            index=res[1]
            model.SetType(tab.StrList[index-1])
            name = kcs_ui.string_req("Key in name of model part:  ")
            if name[0] == OK:
               model.SetName(name[1])
               CheckModel(index, name[1])
               try:
                  tdm = kcs_model.model_properties_get(model)
                  ShowTDMAttribute()
               except:
                  kcs_model.error
            else:
               continue
         else:
            CancelModel(index)
      elif index == 2: # for drawing
         import kcs_draft
         try:
            tdm = kcs_draft.dwg_properties_get()
            ShowTDMAttribute()
         except:
            kcs_model.error
   else:
      print "User interrupted!"
      break;
#---------------------------------------------------------------------------------
