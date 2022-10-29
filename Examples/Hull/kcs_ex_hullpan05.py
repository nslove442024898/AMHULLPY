## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#----------------------------------------------------------------------------------
#
#      NAME:
#
#          kcs_ex_hullpan05.py
#
#      PURPOSE:
#
#               This program presents kcs_hullpan: Hullpan module variables
#
#
#
#----------------------------------------------------------------------------------

import kcs_hullpan
import kcs_ui
import kcs_util

def ShowKwdTypes():
   list = map( lambda x: '%i: %s' % (x, kcs_hullpan.kcsSCHEME_KEYWORD_TYPES[x]), kcs_hullpan.kcsSCHEME_KEYWORD_TYPES.keys() )
   kcs_ui.string_select('Schema keyword types', '', '',list )

def ShowKeywordDetails( kwdStr, kwd ):
   kcs_ui.message_debug( kwdStr )
   kcs_ui.message_debug( kwd )
   title = '%s - keyword details \n' % kwdStr
   msg   = 'TYPE : %i - %s' % (kwd['TYPE'], kcs_hullpan.kcsSCHEME_KEYWORD_TYPES[kwd['TYPE']])
   kcs_ui.message_confirm( title + msg )

def ShowKeywords( stmtStr ):
   stmt = kcs_hullpan.kcsSCHEME_STATEMENTS[stmtStr]
   list = map( str , stmt.keys()  )
   title = 'Stetement keywords ( %s )' % stmtStr

   res = kcs_util.ok()
   while res == kcs_util.ok() :
     (res, kwdNo ) = kcs_ui.string_select( title , '', '',list )
     if res == kcs_util.ok() :
        kwd = stmt.keys()[kwdNo-1]
        ShowKeywordDetails( kwd, stmt[kwd] )

def ShowStatements():
   list = map( str, kcs_hullpan.kcsSCHEME_STATEMENTS.keys() )

   res = kcs_util.ok()
   while res == kcs_util.ok() :
     (res, stmtNo ) = kcs_ui.string_select('Schema satements', '', '',list )

     if res == kcs_util.ok() :
        stmt = kcs_hullpan.kcsSCHEME_STATEMENTS.keys()[ stmtNo-1 ]
        ShowKeywords( stmt )


#----------------------------------------------------------------------------------
# Create main menu
#----------------------------------------------------------------------------------

choices  = [ 'kcsSCHEME_STATEMENTS', 'kcsSCHEME_KEYWORD_TYPES' ]

res = kcs_util.ok()
while res==kcs_util.ok() :
   res, act = kcs_ui.choice_select( 'Planar hull variables', '', choices )

   if res == kcs_util.ok() :
      if act == 1 :
         ShowStatements()
      elif act == 2:
         ShowKwdTypes()
