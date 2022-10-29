## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsPanelSchema.py
#
#      PURPOSE:
#          The PanelSchema class contains functions operating on panel schema
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          None
#
#      METHODS:
#          SetValue                                    Set value of statement
#          GetValue                                    Get value of statement
#
#          Internal functions:
#
#          SplitKeyword                                Splits keyword into items
#          MergeKeyword                                Merges keyword items into string
#          SplitStatement                              Splits statement into items
#          MergeStatement                              Merges statement items into string
#          GetStatements                               Returns all panel statements as list
#          ValuesToDict                                Convert between formats
#          DictToValues                                Convert between formats
#          GetStatementFromValues                      Convert statement to list of values
#          GetStatementAsValues                        Convert list of values to statement
#
#

import types
import string


bUseKcsHull = 1
try:
    import kcs_hullpan
except:
    bUseKcsHull = 0

ErrorMessages = { TypeError : 'not supported argument type, see documentation of PanelSchema class',
                  ValueError : 'not supported argument value, see documentation of PanelSchema class'}

class PanelSchema(object):

# --------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#          panelName        String          Name of panel
# --------------------------------------------------------------------------

    def __init__(self, panelName = ""):
        self.__PanelName = panelName

# --------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class
# --------------------------------------------------------------------------

    def __repr__(self):
        return "PanelSchema: "+self.__PanelName

# --------------------------------------------------------------------------
#
#      METHOD:
#          SetValue
#
#      PURPOSE:
#          To set value of keyword in panel schema statement
#
#      INPUT:
#          Parameters:
#          Group           Integer/String       Index of statement in group or statement string
#          Keyword         String               Name of keyword
#          Value           String               Value of keyword
#
#      RESULT:
#          Statement       String               New statement string
# --------------------------------------------------------------------------

    def SetValue( self, Group, Keyword, Value ):

        if type(Group) not in [type(0), type('')]:
            raise TypeError, ErrorMessages[TypeError]

        if type(Keyword) != type(''):
            raise TypeError, ErrorMessages[TypeError]

        if type(Value) != type(''):
            raise TypeError, ErrorMessages[TypeError]

        #look for keyword
        found   = 0
        stmt = self.GetStatementAsValues( Group )
        for item in stmt:
            if item['Keyword'] == Keyword:
                item['Value'] = Value
                found = 1
                break

        #add new keyword if not found
        if not found :
            kwd = self.ValuesToDict( Keyword, Value, None, None )
            stmt.append( kwd )

        #create statement
        resStmt = self.GetStatementFromValues( stmt )

        #execute statement
        if type(Group) == type(0):
            kcs_hullpan.stmt_exec_single( Group, resStmt, self.__PanelName )

        return resStmt


# --------------------------------------------------------------------------
#
#      METHOD:
#          GetValue
#
#      PURPOSE:
#          To get value of keyword in panel schema statement
#      INPUT:
#          Parameters:
#          Group           Integer/String       Index of statement in group or statement string
#          Keyword         String               Name of keyword
#
#      RESULT:
#          Value           String               Value of keyword
# --------------------------------------------------------------------------

    def GetValue(self,Group, Keyword):

        if type(Group) not in [type(0), type('')]:
            raise TypeError, ErrorMessages[TypeError]

        if type(Keyword) != type(''):
            raise TypeError, ErrorMessages[TypeError]

        #analise statement
        kwds = self.SplitStatement( Group )

        #find keyword
        for item in kwds:
            kwd = self.SplitKeyword( item[0] )
            #found, return keyword value
            if kwd[0] == Keyword:
                return kwd[1]


# --------------------------------------------------------------------------
#
#      METHOD:
#          GetStatements
#
#      PURPOSE:
#          To get panel statements as list
#      INPUT:
#          Parameters:
#          None
#
#      RESULT:
#          List of statements in current panel in format [ Group, Statement ]
# --------------------------------------------------------------------------

    def GetStatements(self):

        groups = []

        #read statements
        group = kcs_hullpan.group_next(self.__PanelName, -2, 0 )

        try:
            while 1:
                statement = kcs_hullpan.stmt_get(self.__PanelName, group )
                groups.append( (group, statement) )
                group = kcs_hullpan.group_next(self.__PanelName, 1, group )
        except:
            pass

        return groups



# --------------------------------------------------------------------------
#
#      METHOD:
#          SplitKeyword
#
#      PURPOSE:
#          To split keyword string into items [keyword, value, operator]
#      INPUT:
#          Parameters:
#          Keyword          String              Keyword as string
#
#      RESULT:
#          List [Keyword, Value, Operator]
# --------------------------------------------------------------------------

    def SplitKeyword(self, Keyword):
        #check if string value without keyword
        import re
        reObj = re.match("\s*'", Keyword)
        if reObj != None:
            return (Keyword, None, None)

        #split expression to keyword,value, operator
        reObj = re.search('\s*=\s*',Keyword)
        #stand-alone keyword
        if reObj == None:
            return (Keyword,None,None)
        #regular keyword
        else:
            return [Keyword[:reObj.start()],Keyword[reObj.end():], Keyword[reObj.start(): reObj.end()]]


# --------------------------------------------------------------------------
#
#      METHOD:
#          MergeKeyword
#
#      PURPOSE:
#          To merge keyword items [keyword, value, operator] into string
#      INPUT:
#          Parameters:
#          List :  [keyword, value, operator]
#
#      RESULT:
#          Keyword as single string
# --------------------------------------------------------------------------

    def MergeKeyword(self, Keyword):
        #check if string value without keyword
        kwd = ''

        key  = Keyword[0]
        val  = Keyword[1]
        oper = Keyword[2]

        if key == None :
            key = ''

        if val == None :
            val = ''

        if oper == None :
            oper = ''

        if key != '' and val != '' and oper == '':
            oper = '='

        kwd = key + oper + val

        return kwd


# --------------------------------------------------------------------------
#
#      METHOD:
#          MergeStatement
#
#      PURPOSE:
#          To merge statemet items into single string
#      INPUT:
#          Parameters:
#          List :  [ keywords ]
#
#      RESULT:
#          Statement as single string
# --------------------------------------------------------------------------

    def MergeStatement(self, Statement):
        kwdsItem = Statement

        statement = ''

        for item in kwdsItem:
            statement += item[0]+item[1];

        return statement


# --------------------------------------------------------------------------
#
#      METHOD:
#          SplitStatement
#
#      PURPOSE:
#          To split statement into pairs {keyword string, separator}
#      INPUT:
#          Parameters:
#          Statement        String      Statement as string
#
#      RESULT:
#          List : [ keywords ]
#
# --------------------------------------------------------------------------

    def SplitStatement(self, Statement):
        if type(Statement) == type(0):
            group = Statement
            statement = kcs_hullpan.stmt_get(self.__PanelName, group )
        elif type(Statement) == type(''):
            statement = Statement
        else:
            raise TypeError, ErrorMessages[TypeError]

        #split statement into keywords and separators
        items = []
        lastIndex = 0
        currIndex = 0
        inParenthesis = 0
        kwdReady      = 0
        currKwd  = ''
        currSep  = ''

        for currIndex in range( len( statement ) ):
            currChar = statement[currIndex]


            if kwdReady:
                if currChar in [' ','\t']:
                    currSep += currChar
                    continue
                else:
                    items.append( [ currKwd.strip(), currSep ] )
                    currKwd = ''
                    currSep = ''
                    kwdReady = 0

            if inParenthesis:
                currKwd += currChar
                if currChar == "'":
                    inParenthesis = 0
                continue

            if currChar == "'":
                currKwd += currChar
                inParenthesis = 1
            elif currChar in [',',';','/']:
                kwdReady = 1
                currSep += currChar
            else:
                currKwd += currChar

        #check last keyword if remained
        currKwd = currKwd.strip()
        if currKwd != '':
            items.append( [ currKwd, currSep ] )

        keywords = items
        keywords2 = []
        bKeyword  = 0

        #concatenate compound list values
        statementKwd = None
        for item in keywords:
            res = self.SplitKeyword( item[0] )

            #first is statement keyword
            if statementKwd == None:
                statementKwd = res[0].strip()
                keywords2.append( item )
                continue

            #regular keyword kkk=vvv
            if res[2] != None :
                bKeyword = 1
                keywords2.append( item )
            #other keywords
            else:
                #not followed by regular keyword
                if not bKeyword or  res[0] == None:
                    keywords2.append( item )
                    bKeyword = 0
                #followed by regular keyword, check if keyword or value
                else:

                    if bUseKcsHull :
                        stmtKwds = kcs_hullpan.kcsSCHEME_STATEMENTS[ statementKwd ].keys()
                        bIsValue = not ( res[0].strip() in stmtKwds )
                    else:
                        reObj = re.match("\s*(LP|FR|P)?[+-]?\d+", res[0])
                        bIsValue = ( reObj != None )

                    if bIsValue:
                        keywords2[-1] = [ keywords2[-1][0] + keywords2[-1][1] + item[0], item[1] ]
                    else:
                        keywords2.append( item )
                        bKeyword = 0



        return keywords2

# --------------------------------------------------------------------------
#
#      METHOD:
#          ValuesToDict
#
#      PURPOSE:
#          To store values from list to dictionary with keys:
#      INPUT:
#          Parameters: in eg. string 'X=FR100,' equals to [ 'X', 'FR100', '=', ',' ]
#           Keyword,        String/None or List [ Keyword, Value, Operator, Separator ]
#           Value,          String/None ( default None )
#           Operator,       String/None ( default None )
#           Separator       String/None ( default None )
#
#
#      RESULT:
#          Dictionary with keys:
#           'Keyword'
#           'Value'
#           'Operator'
#           'Separator'
# --------------------------------------------------------------------------

    def ValuesToDict( self, Kwd, Val=None, Oper=None, Sep=None ):
        if( type( Kwd) == type([]) ):
            return { 'Keyword' : Kwd[0], 'Value' : Kwd[1],  'Operator' : Kwd[2], 'Separator' : Kwd[3] }
        else:
            return { 'Keyword' : Kwd, 'Value' : Val, 'Operator' : Oper, 'Separator' : Sep }

# --------------------------------------------------------------------------
#
#      METHOD:
#          DictToValues
#
#      PURPOSE:
#          To store values from dictionary to list
#          See method ValuesToDict
#      INPUT:
#           dict            dictionary
#
#      RESULT:
#          List [ Keyword, Value, Operator, Separator ]
# --------------------------------------------------------------------------


    def DictToValues( self, dict ):
        return [ dict['Keyword'], dict['Value'], dict['Operator'], dict['Separator'] ]

# --------------------------------------------------------------------------
#
#      METHOD:
#          GetStatementAsValues
#
#      PURPOSE:
#          To get single statement as list of values
#      INPUT:
#          Parameters:
#          Group           Integer/String       Index of statement in group or statement string
#
#      RESULT:
#          Dictionary:
#               List of keyword values ( dictionary, see ValuesToDict )
# --------------------------------------------------------------------------

    def GetStatementAsValues(self,Group ):

        if type(Group) not in [type(0), type('')]:
            raise TypeError, ErrorMessages[TypeError]

        #analise statement
        kwds = self.SplitStatement( Group )

        keywords = []

        for item in kwds:
            kwd = self.SplitKeyword( item[0] )
            keywords.append( self.ValuesToDict( kwd[0], kwd[1], kwd[2], item[1] ))

        return keywords

# --------------------------------------------------------------------------
#
#      METHOD:
#          GetStatementFromValues
#
#      PURPOSE:
#          To get statement string from dictionary containing statement values
#      INPUT:
#          Parameters:
#           Keywords    List ( see GetStatementAsValues )
#
#      RESULT:
#          Statement as string
#
# --------------------------------------------------------------------------

    def GetStatementFromValues( self, stmtAsList ):

        if type(stmtAsList) != type([]):
            raise TypeError, ErrorMessages[TypeError]


        kwds = []

        for item in  stmtAsList:
            kwd = self.DictToValues( item )
            strKwd = self.MergeKeyword( kwd[0:3] )

            keyword   = kwd[0]
            value     = kwd[1]
            operator  = kwd[2]
            separator = kwd[3]

            #check ending sing ';'
            if item == stmtAsList[-1]:
                separator = ';'
            else:
                if separator == None:
                    separator = ', '
                elif type(separator) == type(''):
                    if separator == '' or separator.find( ';' ) >= 0 :
                        separator = ', '

            strKwd = self.MergeKeyword( [keyword, value, operator] )
            kwds.append( [strKwd, separator] )

        resStmt = self.MergeStatement( kwds)

        return resStmt


#-------------------------------------------------------------------
#
#      New style of access to attributes from Python version 2.2
#
    def GetPanelName(self): return self.__PanelName
    def SetPanelName(self,value):
       if type(value)!= type(''):
          raise TypeError, ErrorMessages[TypeError]
       self.__PanelName = value
    PanelName = property (GetPanelName, SetPanelName, None, 'Panel to analyse schema')
