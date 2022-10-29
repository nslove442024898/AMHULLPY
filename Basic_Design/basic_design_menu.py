## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import kcs_gui
"""The Quick Panel Menu in Basic Design

This script adds the Quick Panel menu to the Basic Design application.
It is added as menu number args[0]. Two sub menus called "Longitudinal" and "Transversal" are created to contain these functions."""

def add(*args):
#
#     First, we need to retrieve the main menu.
#
   try:
      main_menu = kcs_gui.menu_get(None,0)
   except:
      print "Failed retrieving main menu: ",kcs_gui.error

#
#     Add the menu.
#
   try:
      num = args[0]
      my_menu = kcs_gui.menu_add(main_menu,num,"Quick Panel")
   except:
      print "Failed adding menu: ",kcs_gui.error
#
#   Add sub menu Longitudinal
#
   try:
      long_menu = kcs_gui.menu_add(my_menu,0,"Longitudinal")
   except:
      print "Failed adding menu: ",kcs_gui.error
#
#     Add the following functions to the new sub menu:
#
#
   try:
      kcs_gui.menu_item_usr_add(long_menu,0,"&Deck","KcsMenuTBD01Deck")
      kcs_gui.menu_item_usr_add(long_menu,1,"&Long Bhd","KcsMenuTBD02LBHD")
      kcs_gui.menu_item_usr_add(long_menu,2,"&Inclined Bhd","KcsMenuTBD03LBHDI")
      kcs_gui.menu_item_usr_add(long_menu,3,"&Stringer","KcsMenuTBD05Stringer")
      kcs_gui.menu_item_usr_add(long_menu,4,"&Girder","KcsMenuTBD06Girder")
   except:
      print "Failed adding menu items: ",kcs_gui.error
#
#   Add sub menu Transversal
#
   try:
      trans_menu = kcs_gui.menu_add(my_menu,1,"Transversal")
   except:
      print "Failed adding menu: ",kcs_gui.error
#
#     Add the following functions to the new sub menu:
#
#
   try:
      kcs_gui.menu_item_usr_add(trans_menu,0,"&Trans Bhd","KcsMenuTBD04TBHD")
      kcs_gui.menu_item_usr_add(trans_menu,1,"&Deck Web","KcsMenuTBD07DWeb")
      kcs_gui.menu_item_usr_add(trans_menu,2,"&Corrugated Bhd","KcsMenuTBD10KBHD")
   except:
      print "Failed adding menu items: ",kcs_gui.error
#
#   Add menu items
#
   try:
      kcs_gui.menu_item_usr_add(my_menu,2,"&Stiffening","KcsMenuTBD08Stiffener")
      kcs_gui.menu_item_usr_add(my_menu,3,"&Defaults","KcsMenuTBD09Defaults")
   except:
      print "Failed adding menu items: ",kcs_gui.error
