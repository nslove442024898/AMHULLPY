## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          SpecSearch.py
#
#      PURPOSE:
#          The SpecSearch class contains search criterias and search
#          results.
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          __SCProject           String      Search criteria, Project
#          __SCSpec              String      Search criteria, Specification
#          __SCFunction          String      Search criteria, Function
#          __SCNomDia            Integer     Search criteria, Nominal diameter
#          __SCFlow              Real        Search criteria, Flow
#          __SCPressClass        String      Search criteria, Pressure Class
#          __SearchResult        List        Result list of a search
#          __Choice              Integer     Choosen index in result list (optional, default 1)
#
#      METHODS:
#          SetSCProject                      Sets value of SCProject, SearchResult will be cleared
#          SetSCSpec                         Sets value of SCSpec, SearchResult will be cleared
#          SetSCFunction                     Sets value of SCFunction, SearchResult will be cleared
#          SetSCNomDia                       Sets value of SCNomDia, SearchResult will be cleared
#          SetSCFlow                         Sets value of SCFlow, SearchResult will be cleared
#          SetSCPressClass                   Sets value of SCPressClass, SearchResult will be cleared
#          Search                            Performs a spec search using current SC*
#          SetChoice                         Sets value of Choice
#          GetComponent(index)               Gets the component value at [index]
#          GetChoosenComponent               Gets the component pointe out by __Choice
#
import types
import string
#
class SpecSearch(object):
#
#
#    Variables
#
      ErrorMessages = { TypeError : 'not supported argument type, see documentation of SpecSearch class',
                      ValueError : 'not supported argument value, see documentation of SpecSearch class'}

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          None
#
      def __init__(self):
         self.__SCProject          = None
         self.__SCSpec             = None
         self.__SCFunction         = None
         self.__SCNomDia           = -1
         self.__SCFlow             = -1.0
         self.__SCPressClass       = None
         self.__Choice             = 0
         self.__SearchResult       = []
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
#
      def __repr__(self):
         tup = (
            "SCProject       :" + str(self.__SCProject),
            "SCSpec          :" + str(self.__SCSpec),
            "SCFunction      :" + str(self.__SCFunction),
            "SCNomDia        :" + str(self.__SCNomDia),
            "SCFlow          :" + str(self.__SCFlow),
            "SCPressClass    :" + str(self.__SCPressClass),
            "Choice          :" + str(self.__Choice),
            "SearchResult    :" + str(self.__SearchResult))
         return string.join (tup, '\n')

#
#      METHOD:
#          SetSCProject
#
#      PURPOSE:
#          To set search criteria Project
#
#      INPUT:
#          Parameters:
#          Project   String      Search criteria Project
#
      def SetSCProject(self, Project):
         if type(Project) != type("") and Project != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCProject = Project
#
#      METHOD:
#          SetSCSpec
#
#      PURPOSE:
#          To set search criteria Specification
#
#      INPUT:
#          Parameters:
#          Spec   String      Search criteria Specification
#
      def SetSCSpec(self, Spec):
         if type(Spec) != type("") and Spec != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCSpec = Spec
#
#
#      METHOD:
#          SetSCFunction
#
#      PURPOSE:
#          To set search criteria Function
#
#      INPUT:
#          Parameters:
#          Func   String      Search criteria Function
#
      def SetSCFunction(self, Func):
         if type(Func) != type("") and Func != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCFunction = Func
#
#
#      METHOD:
#          SetSCNomDia
#
#      PURPOSE:
#          To set search criteria Nominal Diameter
#
#      INPUT:
#          Parameters:
#          NomDia   Integer      Search criteria Nominal Diameter
#
      def SetSCNomDia(self, NomDia):
         if type(NomDia) != type(0) and NomDia != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCNomDia = NomDia
#
#
#      METHOD:
#          SetSCFlow
#
#      PURPOSE:
#          To set search criteria Flow
#
#      INPUT:
#          Parameters:
#          Flow   Real      Search criteria Flow
#
      def SetSCFlow(self, Flow):
         if type(Flow) != type(0.0) and type(Flow) != type(0) and Flow != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCFlow = Flow
#
#
#      METHOD:
#          SetSCPressClass
#
#      PURPOSE:
#          To set search criteria Pressure Class
#
#      INPUT:
#          Parameters:
#          PressClass   String      Search criteria Pressure Class
#
      def SetSCPressClass(self, PressClass):
         if type(PressClass) != type("") and PressClass != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__SearchResult = []
         self.__SCPressClass = PressClass
#
#      METHOD:
#          Search
#
#      PURPOSE:
#          Performs a search and fills up SearcResult with components matching
#          current SearcCriterias
#
#      INPUT:
#          Parameters:
#
      def Search(self):
         try:
            import kcs_spec
         except:
            return
         self.__Choice = 0
         return kcs_spec.spec_search(self)
#
#      METHOD:
#          SetChoice
#
#      PURPOSE:
#          To set Choice to the index of the choosen component in SearchResult list
#
#      INPUT:
#          Parameters:
#          Choice   Integer      Value for Choice
#
      def SetChoice(self, Choice):
         if type(Choice) != type(0) and Choice != None:
            raise TypeError, self.ErrorMessages[TypeError]

         self.__Choice = Choice
#
#
#      METHOD:
#          GetComponent
#
#      PURPOSE:
#          Get a Component from the SearchResult
#
#      INPUT:
#          Parameters:
#          Index   Integer      Index of the Component
#
      def GetComponent(self, Index):
         if type(Index) != type(0):
            raise TypeError, self.ErrorMessages[TypeError]
         try:
            return self.__SearchResult[Index]
         except:
            return None
#
#
#      METHOD:
#          GetChoosenComponent
#
#      PURPOSE:
#          Get the Component currently pointed out by Choice
#
#      INPUT:
#          Parameters:
#          Index   Integer      Index of the Component
#
      def GetChoosenComponent(self):
         try:
            return self.__SearchResult[self.__Choice]
         except:
            return None

#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
      def GetSCProject(self): return self.__SCProject
      def GetSCSpec(self): return self.__SCSpec
      def GetSCFunction(self): return self.__SCFunction
      def GetSCNomDia(self): return self.__SCNomDia
      def GetSCFlow(self): return self.__SCFlow
      def GetSCPressClass(self): return self.__SCPressClass
      def GetChoice(self): return self.__Choice
      def GetSearchResult(self): return self.__SearchResult

      SCProject          = property (GetSCProject , SetSCProject)
      SCSpec             = property (GetSCSpec , SetSCSpec)
      SCFunction         = property (GetSCFunction , SetSCFunction)
      SCNomDia           = property (GetSCNomDia , SetSCNomDia)
      SCFlow             = property (GetSCFlow , SetSCFlow)
      SCPressClass       = property (GetSCPressClass , SetSCPressClass)
      Choice             = property (GetChoice , SetChoice)
      SearchResult       = property (GetSearchResult)
