## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_hull_remarkinglength.py
#
#      PURPOSE:
#
#          This program presents two Vitesse functions for measuring
#          in curved panel - remarking_length and remarking_length_ext.
#
import kcs_chm
import kcs_ui
import kcs_util
import kcs_draft
import kcs_dex
import KcsInterpretationObject
import KcsModel
import KcsPoint2D
import CommonSample

FLAG_BEVEL_GAP = 1
FLAG_EXCESS_1 = 2
FLAG_EXCESS_2 = 4
FLAG_EXCESS_3 = 8
FLAG_EXCESS_4 = 16
FLAG_EXCESS_5 = 32
FLAG_COMPENSATION = 64
FLAG_SHRINKAGE = 128

#----------------------------------------------------------------------------------
# SelectSeam - create curved seam model from identification
#---------------------------------------------------------------------------------
def SelectSeam(message):
   pt    = KcsPoint2D.Point2D()
   model = KcsModel.Model("seam/butt",'')
   resp, pt = kcs_ui.point2D_req(message, pt)
   if resp != kcs_util.ok():
      return

   try:
      kcs_draft.model_identify(pt, model)
      return model
   except:
      pass
   # use data extraction
   model = KcsModel.Model("curved panel",'')
   model.PartType = 'seam'
   try:
      kcs_draft.model_identify(pt, model)
   except:
      return
   if model.PartId<=5000 or model.PartId>=6000:
      return
   id = model.PartId - 5000

   string_res=''
   try:
       res = kcs_dex.extract("HULL.CPAN('"+model.Name+"').ISEAM("+str(id)+").NAME")
       if res == 0:
          type = kcs_dex.next_result()
          if type == 3:
              string_res=kcs_dex.get_string()
   except:
       pass
   if len(string_res)==0:
      return

   model = KcsModel.Model("seam/butt",string_res)
   return model


#----------------------------------------------------------------------------------
# SelectStiffener - create curved stiffener model from identification
#---------------------------------------------------------------------------------
def SelectStiffener(message):
   pt    = KcsPoint2D.Point2D()
   model = KcsModel.Model("longitudinal",'')
   resp, pt = kcs_ui.point2D_req(message, pt)
   if resp != kcs_util.ok():
      return

   try:
      kcs_draft.model_identify(pt, model)
      if model.PartId<=6000 or model.PartId>=7000:
         return
      resModel = KcsModel.Model('curved stiffener',model.Name + "-S" + str(model.PartId-6000))
      return resModel
   except:
      pass

   model = KcsModel.Model("transversal",'')
   try:
      kcs_draft.model_identify(pt, model)
      if model.PartId<=6000 or model.PartId>=7000:
         return
      resModel = KcsModel.Model('curved stiffener',model.Name + "-S" + str(model.PartId-6000))
      return resModel
   except:
      pass

   # or use data extraction with curved panel
   model = KcsModel.Model("curved panel",'')
   model.PartType = 'stiffener'
   try:
      kcs_draft.model_identify(pt, model)
   except:
      return
   if model.PartId<=6000 or model.PartId>=7000:
      return
   id = model.PartId - 6000

   string_res=''
   try:
       res = kcs_dex.extract("HULL.CPAN('"+model.Name+"').STIF("+str(id)+").NAME")
       if res == 0:
          type = kcs_dex.next_result()
          if type == 3:
              string_res=kcs_dex.get_string()
   except:
       pass
   if len(string_res)==0:
      return

   model = KcsModel.Model("curved stiffener",string_res)
   return model


#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------
def MainMenu():
   act = 255
   hullpanname = ''
   pt    = KcsPoint2D.Point2D()

   modelFrom  = KcsModel.Model()
   modelAlong = KcsModel.Model()
   modelTo    = KcsModel.Model()

   while 1:
      if len(hullpanname)==0:
         actions = (
            'Select Curved Panel',
            )
      else:
         actions = (
            'Panel: '+hullpanname,
            'From : '+modelFrom.Name+' '+modelFrom.Type[:10],
            'Along: '+modelAlong.Name+' '+modelAlong.Type[:10],
            'To   : '+modelTo.Name+' '+modelTo.Type[:10],
            'Change measure options',
            'Calculate length'
            )

      (status, index) = kcs_ui.choice_select('Curved panel measuring','Operations', actions)

      if status == kcs_util.ok():
         if index == 1:
            model = KcsModel.Model("curved panel",'')
            resp, pt = kcs_ui.point2D_req('Indicate curved panel', pt)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.model_identify(pt, model)
                  hullpanname = model.Name
               except:
                  kcs_ui.message_noconfirm('Identification failed')
         elif index == 2:
            newModel = ObjectMenu(modelFrom,'Select object to measure from')
            if newModel:
              modelFrom = newModel
         elif index == 3:
            newModel = ObjectMenu(modelAlong,'Select object to measure along')
            if newModel:
              modelAlong = newModel
         elif index == 4:
            newModel = ObjectMenu(modelTo,'Select object to measure to')
            if newModel:
              modelTo = newModel
         elif index == 5:
            act = FlagMenu(act)
         elif index == 6:
            try:
               ret = kcs_chm.remarking_length(modelFrom,modelAlong,modelTo)
            except TBException,e:
               kcs_ui.message_confirm('Error in remarking_length '+e.strError+'.\nExtended calculations stopped')
            else:
               try:
                  ret2 = kcs_chm.remarking_length_ext(act,hullpanname,modelFrom,modelAlong,modelTo)
               except TBException,e:
                  if e.strError == 'kcs_ShrinkageObjectError':
                     kcs_ui.message_confirm('Error in remarking_length_ext.\nSet shrinkage object in database to consider shrinkage')
                  else:
                     kcs_ui.message_confirm('Error in remarking_length_ext.\n'+e.strError)
               else:
                  kcs_ui.message_confirm('Length basic: ' + str(ret) + '\nLength extended: ' + str(ret2) + '\n\nDifference: ' + str(ret2-ret))


      else:
         print "User interrupted!"
         break;


#----------------------------------------------------------------------------------
# Create object menu
#
# The object types that are accepted by remarking length functions are:
#
# Hull curves
# Seams and butts
# Shell stiffeners
# Curves along Jig rows and columns
# Frame curves
# Planar panel limits
# Hole crossmarks
#
# returns: model or None
#----------------------------------------------------------------------------------
def ObjectMenu(oldModel, message = "Select object"):
   pt    = KcsPoint2D.Point2D()
   while 1:
      actions = (
         'Hull curve / frame curve',
         # seams can be used with type 'hull curve' and 'seam/butt'
         'Seam/butt',
         'Shell stiffener',
         'Planar panel limit',
         'Hole crossmark',
         '? Plane ?',
         #not working for 'longitudinal',
         #not working for 'transversal',
         'FREE PICK'
         )
      (status, index) = kcs_ui.choice_select('Curved panel measuring',message, actions)

      if status == kcs_util.ok():

         if index == 1:
            res, strName = kcs_ui.string_req("Key in hull curve name (OPTIONS to select)", oldModel.Name)
            if res == kcs_util.ok():
               model = KcsModel.Model("hull curve",strName)
               return model
            elif res == kcs_util.options():
               model = KcsModel.Model("hull curve",'')
               resp, pt = kcs_ui.point2D_req(message, pt)
               if resp == kcs_util.ok():
                  try:
                     kcs_draft.model_identify(pt, model)
                     return model
                  except:
                     kcs_ui.message_noconfirm('Identification failed')

         elif index == 2:
            while 1:
               res, strName = kcs_ui.string_req("Key in seam/butt name (OPTIONS to select)", oldModel.Name)
               if res == kcs_util.ok():
                  model = KcsModel.Model("seam/butt",strName)
                  return model
               elif res == kcs_util.options():
                  model = SelectSeam(message)
                  if model == None:
                     kcs_ui.message_noconfirm('Identification failed')
                  else:
                     return model
               else:
                  break

         elif index == 3:
            while 1:
               res, strName = kcs_ui.string_req("Key in stiffener name (OPTIONS to select)", oldModel.Name)
               if res == kcs_util.ok():
                  model = KcsModel.Model("curved stiffener",strName)
                  return model
               elif res == kcs_util.options():
                  model = SelectStiffener(message)
                  if model == None:
                     kcs_ui.message_noconfirm('Identification failed')
                  else:
                     return model
               else:
                  break

         elif index == 4:
            model = KcsModel.Model("plane panel",'')
            resp, pt = kcs_ui.point2D_req(message, pt)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.model_identify(pt, model)
                  model.PartType = ''
                  model.PartId = 0
                  return model
               except:
                  kcs_ui.message_noconfirm('Identification failed')

         elif index == 5:
            model = KcsModel.Model("curved panel",'')
            resp, pt = kcs_ui.point2D_req(message, pt)
            if resp == kcs_util.ok():
               try:
                  kcs_draft.model_identify(pt, model)
                  return model
               except:
                  kcs_ui.message_noconfirm('Identification failed')

         elif index == 6:
            model = KcsModel.Model("plane",'')

         elif index == 7:
            model = CommonSample.SelectModel()
            if model!=None:
               kcs_ui.message_debug(model)
               return model
            else:
               kcs_ui.message_noconfirm('Identification failed')
               continue

         else:
            continue
      else:
         break

   return None


#----------------------------------------------------------------------------------
def OnOff(flag):
   if flag:
      return "ON"
   else:
      return "OFF"


#----------------------------------------------------------------------------------
# Create extended flags menu
#----------------------------------------------------------------------------------
def FlagMenu(activity):
   message = "Click to change setting"
   flags = [0, FLAG_BEVEL_GAP,
            FLAG_EXCESS_1, FLAG_EXCESS_2, FLAG_EXCESS_3, FLAG_EXCESS_4, FLAG_EXCESS_5,
            FLAG_COMPENSATION, FLAG_SHRINKAGE]

   status = kcs_util.ok()

   while( status == kcs_util.ok() ):
      actions = (
         'Bevel Gap : '+ OnOff(activity & FLAG_BEVEL_GAP),
         'Excess 1  : '+ OnOff(activity & FLAG_EXCESS_1),
         'Excess 2  : '+ OnOff(activity & FLAG_EXCESS_2),
         'Excess 3  : '+ OnOff(activity & FLAG_EXCESS_3),
         'Excess 4  : '+ OnOff(activity & FLAG_EXCESS_4),
         'Excess 5  : '+ OnOff(activity & FLAG_EXCESS_5),
         'Compensation  : '+ OnOff(activity & FLAG_COMPENSATION),
         'Shrinkage  : '+ OnOff(activity & FLAG_SHRINKAGE)
         )
      (status, index) = kcs_ui.choice_select('Curved panel measuring',message, actions)

      if status == kcs_util.ok():
         if activity & flags[index]:
            activity = activity & ~flags[index]
         else:
            activity = activity | flags[index]

   return activity


#----------------------------------------------------------------------------------
MainMenu()
