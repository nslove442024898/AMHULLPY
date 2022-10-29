## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_db01.py
#
#      PURPOSE:
#
#          This example shows how to use object copy/list functions
#

import sys
from string import *

import kcs_ui
import kcs_util
import kcs_db
import kcs_draft

from KcsStringlist import Stringlist
from KcsObject import Object
from KcsObjectCriteria import ObjectCriteria
from KcsDateTime import DateTime
from KcsStringlist import Stringlist

#-------------------------------------------------------------------------------------------------------------
def PrintDbError():                                            # prints db exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_db.error)
   print kcs_db.error

#-------------------------------------------------------------------------------------------------------------
def ShowResult(crit, objlist):
   critstrlist = []
   critstrlist = split(str(crit), '\n')
   critstrlist = critstrlist[1:]

   objstrlist = []
   index = 1
   for item in objlist:
      stritems = split(str(item), '\n')
      stritems[0] = '----------------- Object %i: -----------------' % index
      index = index+1
      objstrlist = objstrlist + stritems

   list = Stringlist('------------------------------ objects mathing criteria ------------------------------')

   for item in critstrlist:
      list.AddString(item)

   list.AddString('------------------------------ result list ------------------------------')

   for item in objstrlist:
      list.AddString(item)

   kcs_ui.string_select('Objects', 'Founded %i:' % len(objlist), '', list)

#-------------------------------------------------------------------------------------------------------------
def GetDateTime():
   res, date = kcs_ui.string_req('Key in date and time in format: "YYYY-MM-DD HH:MM:SS.CC"', '')
   if res:
      date = replace(date, '-', ':')
      date = replace(date, ' ', ':')
      date = replace(date, '.', ':')
      datelist = map(int, split(date, ':'))
      try:
         date = apply(DateTime, datelist)
         return 1, date
      except:
         print sys.exc_info()[1]
   return 0, None

#-------------------------------------------------------------------------------------------------------------
def SetSizeCriteria(crit):
   actions = Stringlist('equal to size')
   actions.AddString('less then size')
   actions.AddString('less or equal size')
   actions.AddString('more then size')
   actions.AddString('more or equal size')
   actions.AddString('exclude size from criteria')

   res = kcs_ui.choice_select('Object size', '', actions)
   if res[0] == kcs_util.ok():
      try:
         if res[1] == 1:
            resp, size = kcs_ui.int_req('Size of object:', 0)
            if resp == kcs_util.ok():
               crit.SetSize('=', size)
         elif res[1] == 2:
            resp, size = kcs_ui.int_req('Size of object:', 0)
            if resp == kcs_util.ok():
               crit.SetSize('<', size)
         elif res[1] == 3:
            resp, size = kcs_ui.int_req('Size of object:', 0)
            if resp == kcs_util.ok():
               crit.SetSize('<=', size)
         elif res[1] == 4:
            resp, size = kcs_ui.int_req('Size of object:', 0)
            if resp == kcs_util.ok():
               crit.SetSize('>', size)
         elif res[1] == 5:
            resp, size = kcs_ui.int_req('Size of object:', 0)
            if resp == kcs_util.ok():
               crit.SetSize('>=', size)
         elif res[1] == 6:
            crit.SetSize(None)
      except:
         print sys.exc_info()[1]


#-------------------------------------------------------------------------------------------------------------
def SetCreationDateTime(crit):
   actions = Stringlist('equal to date')
   actions.AddString('before date')
   actions.AddString('befor or equal date')
   actions.AddString('after date')
   actions.AddString('after or equal date')
   actions.AddString('between dates')
   actions.AddString('exclude date from criteria')

   res = kcs_ui.choice_select('Date and time', '', actions)
   if res[0] == kcs_util.ok():
      try:
         if res[1] == 1:
            resp, date = GetDateTime()
            if resp:
               crit.SetCreationDate('=', date)
         elif res[1] == 2:
            resp, date = GetDateTime()
            if resp:
               crit.SetCreationDate('<', date)
         elif res[1] == 3:
            resp, date = GetDateTime()
            if resp:
               crit.SetCreationDate('<=', date)
         elif res[1] == 4:
            resp, date = GetDateTime()
            if resp:
               crit.SetCreationDate('>', date)
         elif res[1] == 5:
            resp, date = GetDateTime()
            if resp:
               crit.SetCreationDate('>=', date)
         elif res[1] == 6:
            resp, date1 = GetDateTime()
            if resp:
               resp, date2 = GetDateTime()
               if resp:
                  crit.SetCreationDate(date1, date2)
      except:
         print sys.exc_info()[1]

def RetriveObjects(crit, dbname):
   while 1:
      actions = Stringlist('Db name: ' + dbname)
      actions.AddString('---- CRITERIA -----')
      actions.AddString('Object name: ' + str(crit.GetName()))
      actions.AddString('Code1: ' + str(crit.GetCode1()))
      actions.AddString('Code2: ' + str(crit.GetCode2()))

      dates = crit.GetCreationDate()
      if dates == None:
         datestr = 'None'
      elif isinstance(dates[0], DateTime):
         datestr = ('%04i-%02i-%02i - %04i-%02i-%02i') % (dates[0].GetDateTime()[:3] + dates[1].GetDateTime()[:3])
      else:
         datestr = dates[0] + ' ' + '%04i-%02i-%02i' % (dates[1].GetDateTime()[:3])

      actions.AddString('Date: ' + datestr)
      actions.AddString('Size: ' + str(crit.GetSize()))
      actions.AddString('List objects')

      res = kcs_ui.choice_select('Object list', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # get database name
               resp = kcs_ui.string_req('Database name:', dbname)
               if resp[0] == kcs_util.ok():
                  dbname = resp[1]
            elif res[1] == 2:
               pass
            elif res[1] == 3:
               name = crit.GetName()
               if name == None:
                  name = ''
               resp, name = kcs_ui.string_req('Name criteria:', name)
               if resp != kcs_util.ok():
                  crit.SetName(None)      # name criteria not set
               else:
                  crit.SetName(name)      # name criteria set
            elif res[1] == 4:
               code = crit.GetCode1()
               if code == None:
                  code = 0
               resp, code = kcs_ui.int_req('Code1 criteria:', code)
               if resp != kcs_util.ok():
                  code = None
               crit.SetCode1(code)        # object code1 criteria
            elif res[1] == 5:
               code = crit.GetCode2()
               if code == None:
                  code = 0
               resp, code = kcs_ui.int_req('Code2 criteria:', code)
               if resp != kcs_util.ok():
                  code = None
               crit.SetCode2(code)        # object code2 criteria
            elif res[1] == 6:
               SetCreationDateTime(crit)
            elif res[1] == 7:
               SetSizeCriteria(crit)
            elif res[1] == 8:
               try:
                  list = []
                  kcs_db.object_list_get(crit, dbname, list)
                  ShowResult(crit, list)
               except:
                  PrintDbError()
         else:
            break
      except:
         print sys.exc_info()[1]


#-------------------------------------------------------------------------------------------------------------
   # main
dbname = ''

crit = ObjectCriteria()
crit.SetName(None)
crit.SetCode1(None)
crit.SetCode2(None)
crit.SetSize(None)
crit.SetCreationDate(None)

while 1:
   actions = Stringlist('Db name: ' + dbname)
   actions.AddString('---- CRITERIA -----')
   actions.AddString('Object name: ' + str(crit.GetName()))
   actions.AddString('Code1: ' + str(crit.GetCode1()))
   actions.AddString('Code2: ' + str(crit.GetCode2()))

   dates = crit.GetCreationDate()
   if dates == None:
      datestr = 'None'
   elif isinstance(dates[0], DateTime):
      datestr = ('%04i-%02i-%02i - %04i-%02i-%02i') % (dates[0].GetDateTime()[:3] + dates[1].GetDateTime()[:3])
   else:
      datestr = dates[0] + ' ' + '%04i-%02i-%02i' % (dates[1].GetDateTime()[:3])

   actions.AddString('Date: ' + datestr)
   actions.AddString('Size: ' + str(crit.GetSize()))
   actions.AddString('List objects')

   res = kcs_ui.choice_select('Object list', '', actions)

   try:
      if res[0]==kcs_util.ok():
         if res[1] == 1:         # get database name
            resp = kcs_ui.string_req('Database name:', dbname)
            if resp[0] == kcs_util.ok():
               dbname = resp[1]
         elif res[1] == 2:
            pass
         elif res[1] == 3:
            name = crit.GetName()
            if name == None:
               name = ''
            resp, name = kcs_ui.string_req('Name criteria:', name)
            if resp != kcs_util.ok():
               crit.SetName(None)      # name criteria not set
            else:
               crit.SetName(name)      # name criteria set
         elif res[1] == 4:
            code = crit.GetCode1()
            if code == None:
               code = 0
            resp, code = kcs_ui.int_req('Code1 criteria:', code)
            if resp != kcs_util.ok():
               code = None
            crit.SetCode1(code)        # object code1 criteria
         elif res[1] == 5:
            code = crit.GetCode2()
            if code == None:
               code = 0
            resp, code = kcs_ui.int_req('Code2 criteria:', code)
            if resp != kcs_util.ok():
               code = None
            crit.SetCode2(code)        # object code2 criteria
         elif res[1] == 6:
            SetCreationDateTime(crit)
         elif res[1] == 7:
            SetSizeCriteria(crit)
         elif res[1] == 8:
            try:
               list = []
               kcs_db.object_list_get(crit, dbname, list)
               ShowResult(crit, list)
            except:
               PrintDbError()
      else:
         break
   except:
      print sys.exc_info()[1]

