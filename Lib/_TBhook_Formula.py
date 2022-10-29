## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_Formula - Formula retrieval
#
#  If this script is found in the PYTHONPATH it will be used to retrieve
#  formula values ( $-values) automatically.
#  The signature of the interface methods must not be changed.
#
#  Support for new formulas may be added.
#  This is done by adding a number of Python statements like:
#
#  elif FormulaNumber == <my new formula no>:
#    <my formula definition>
#
#  just after the definition of test rule 10000.
#  ( Please observe the indentation used in the Python language.)
#
#  if FormulaNumber == 10000:
#    FormulaValue = 'TestOfFormula10000'
#    Formula = (FormulaValue)
#    return Formula
#
#  Formula numbers 10001 to 10999 are free for definition.
#  All formulas are supplied by the calling Tribon application
#  with a model context in input parameters;
#
#  Input:
#  ModelType     - Model type eg. 'plane panel'
#  ModelName     - Model name eg. panel name
#  PartType      - Part type eg. 'plate'
#  PartId        - Part identity eg. 2001
#  SubPartType
#  SubPartId
#  ReflCode      - Reflection code ( = 0 when not reflected; = 1 when reflected)
#
#  The contents of those parameters varies with the calling application
#  and the actual model ( panel, plate etc) defined upon call of this script.
#
#  Output:
#  FormulaValue  - The value of the formula ( a string).
#
#  'Extra' output parameters ( see below) should be passed on to Tribon with
#  null values.
#
#  Formulas with numbers in the intervall 5001 to 5999 may also be used.
#  However, please observe that formula in this intervall are predefined for
#  specific purposes. They have predefined extra input and output parameters.
#  The number and definition of the extra input and output parameters vary
#  with the formula number.
#  Supported formulas of this kind have their stub defined in this script.
#  Code may be added for those formulas in order to define the output parameters.
#
#  Input:
#  ModelType     - Model type eg. 'plane panel'
#  ModelName     - Model name eg. panel name
#  PartType      - Part type eg. 'plate'
#  PartId        - Part identity eg. 2001
#  SubPartType
#  SubPartId
#  ReflCode      - Reflection code ( = 0 when not reflected; = 1 when reflected)
#
#  ParNInt - Number of input integers ( 0 to 10)
#  ParNRea - Number of input reals    ( 0 to 10)
#  ParNStr - Number of input strings  ( 0 to 10)
#  PI0     - Input integer 1
#  PI1     -   "      "    2
#  PI2     -   "      "    3
#  PI3     -   "      "    4
#  PI4     -   "      "    5
#  PI5     -   "      "    6
#  PI6     -   "      "    7
#  PI7     -   "      "    8
#  PI8     -   "      "    9
#  PI9     -   "      "    10
#  PR0     - Input real    1
#  PR1     -   "      "    2
#  PR2     -   "      "    3
#  PR3     -   "      "    4
#  PR4     -   "      "    5
#  PR5     -   "      "    6
#  PR6     -   "      "    7
#  PR7     -   "      "    8
#  PR8     -   "      "    9
#  PR9     -   "      "    10
#  PS0     - Input string  1
#  PS1     -   "      "    2
#  PS2     -   "      "    3
#  PS3     -   "      "    4
#  PS4     -   "      "    5
#  PS5     -   "      "    6
#  PS6     -   "      "    7
#  PS7     -   "      "    8
#  PS8     -   "      "    9
#  PS9     -   "      "    10
#
#
#  Output:
#  FormulaValue  - The value of the formula ( a string).
#
#  ResNInt - Number of output integers ( 0 to 10)
#  ResNRea - Number of output reals    ( 0 to 10)
#  ResNStr - Number of output strings  ( 0 to 10)
#  RI0     - Output integer 1
#  RI1     -   "      "     2
#  RI2     -   "      "     3
#  RI3     -   "      "     4
#  RI4     -   "      "     5
#  RI5     -   "      "     6
#  RI6     -   "      "     7
#  RI7     -   "      "     8
#  RI8     -   "      "     9
#  RI9     -   "      "    10
#  RR0     - Output real    1
#  RR1     -   "      "     2
#  RR2     -   "      "     3
#  RR3     -   "      "     4
#  RR4     -   "      "     5
#  RR5     -   "      "     6
#  RR6     -   "      "     7
#  RR7     -   "      "     8
#  RR8     -   "      "     9
#  RR9     -   "      "    10
#  RS0     - Output string  1
#  RS1     -   "      "     2
#  RS2     -   "      "     3
#  RS3     -   "      "     4
#  RS4     -   "      "     5
#  RS5     -   "      "     6
#  RS6     -   "      "     7
#  RS7     -   "      "     8
#  RS8     -   "      "     9
#  RS9     -   "      "    10
#
#
#
import string
import kcs_dex
import kcs_ui
import kcs_util
import kcs_assembly
import kcs_model
import KcsAssembly
import KcsModel

ok = kcs_util.success()
not_ok = kcs_util.failure()

#-----------------------------------------------------------------------------
#  Help methods to ease data extraction calls used below
#-----------------------------------------------------------------------------
def getIntegerValue(est):
  int = -9999;
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 1:
      int = kcs_dex.get_int()
  return int

def getRealValue(est):
  real = -999999.99;
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 2:
      real = kcs_dex.get_real()
  return real

def getStringValue(est):
  string = "****"
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ == 3:
      string = kcs_dex.get_string()
  return string

def getReaListValue(est):
  retval = [0];
  res = kcs_dex.extract(est)
  if res == ok:
    typ = kcs_dex.next_result()
    if typ > 10:
      retval = [typ-10]
      for i in range(typ-10):
        retval.append(kcs_dex.get_indexedreal(i))
  return retval

#-----------------------------------------------------------------------------
#  getCompInd - to get a component index from a component number
#               to be used in data extraction
#-----------------------------------------------------------------------------
def getCompInd( ModelName, DexPartType, PartId, DexSubPartType, SubPartId):
  inds = []
  compind = 0
  subcompind = 0
  est = "HULL.PANEL('" + ModelName + "')." + DexPartType + "(" + str(divmod(abs(PartId),1000)[1]) + ").COMP_ID"
  comp_no = getIntegerValue(est)
  if comp_no == PartId:
    compind = divmod(abs(PartId),1000)[1]
  else:
    est = "HULL.PANEL('" + ModelName + "').N" + DexPartType
    no_of = getIntegerValue(est)
    for no in range( 1, no_of, 1):
      est = "HULL.PANEL('" + ModelName + "')." + DexPartType + "(" + str(no) + ").COMP_ID"
      comp_no = getIntegerValue(est)
      if comp_no == PartId:
        compind = no
        break
  if DexSubPartType != "":
    est = "HULL.PANEL('" + ModelName + "')." + DexPartType + "(" + str(compind) + ")." + DexSubPartType + "(" + str(divmod(abs(SubPartId),1000)[1]) + ").COMP_ID"
    subcomp_no = getIntegerValue(est)
    if subcomp_no == SubPartId:
      subcompind = divmod(abs(SubPartId),1000)[1]
    else:
      est = "HULL.PANEL('" + ModelName + "')." + DexPartType + "(" + str(compind) + ").N" + DexSubPartType
      no_of = getIntegerValue(est)
      for no in range( 1, no_of, 1):
        est = "HULL.PANEL('" + ModelName + "')." + DexPartType + "(" + str(compind) + ")." + DexSubPartType + "(" + str(no) + ").COMP_ID"
        comp_no = getIntegerValue(est)
        if comp_no == SubPartId:
          subcompind = no
          break

  inds.append( compind)
  inds.append( subcompind)
  return inds



#-----------------------------------------------------------------------------
#  Interface method - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def getFormula(ModelType,ModelName,PartType,PartId,SubPartType,SubPartId,ReflCode,FormulaNumber,ParNInt,ParNRea,ParNStr,PI0,PI1,PI2,PI3,PI4,PI5,PI6,PI7,PI8,PI9,PR0,PR1,PR2,PR3,PR4,PR5,PR6,PR7,PR8,PR9,PS0,PS1,PS2,PS3,PS4,PS5,PS6,PS7,PS8,PS9):

  model = KcsModel.Model(ModelType,ModelName)
  model.SetPartType(PartType)
  model.SetPartId(PartId)
  model.SetReflCode(ReflCode)

  FormulaValue = ''
  ResNInt = 0
  ResNRea = 0
  ResNStr = 0
  RI0 = 0
  RI1 = 0
  RI2 = 0
  RI3 = 0
  RI4 = 0
  RI5 = 0
  RI6 = 0
  RI7 = 0
  RI8 = 0
  RI9 = 0
  RR0 = 0.0
  RR1 = 0.0
  RR2 = 0.0
  RR3 = 0.0
  RR4 = 0.0
  RR5 = 0.0
  RR6 = 0.0
  RR7 = 0.0
  RR8 = 0.0
  RR9 = 0.0
  RS0 = ''
  RS1 = ''
  RS2 = ''
  RS3 = ''
  RS4 = ''
  RS5 = ''
  RS6 = ''
  RS7 = ''
  RS8 = ''
  RS9 = ''


  if FormulaNumber == 10000:
#-----------------------------------------------------------------------------
#
#   Formula 10000
#
#   The only purpose of this rule is to show an example of a formula
#   free for definition.
#
#   By using the model defined upon call ( parameters ModelType,
#   ModelName, PartType, PartId, SubPartType, SubPartId and ReflCode)
#   the value of the formula may be calculated ( FormulaValue).
#   This may be done by using for example data extraction commands.
#-----------------------------------------------------------------------------
    FormulaValue = 'TestOfFormula10000'
    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula


  if FormulaNumber == 10001:
#-----------------------------------------------------------------------------
#
#   Formula 10001
#
#   The purpose of this rule is to define a formula indicating
#   grinding info for holes in plates.
#   If the plate referenced by ModelName has a hole with grinding
#   then FormulaValue = '*' otherwise FormulaValue = ''
#-----------------------------------------------------------------------------
    est = "HULL.PLATE('" + ModelName + "').HOLE_GRINDING"
    resp = getStringValue(est)
    if resp == "YES":
      FormulaValue = '*'
    else:
      FormulaValue = ''
    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula


  if FormulaNumber == 10002:
#-----------------------------------------------------------------------------
#
#   Formula 10002
#
#   The purpose of this rule is to define a formula indicating
#   bending info for plates and profiles converted to plates.
#   The FormulaValue returned will be:
#
#   'F' for folded flanges
#   'H' for curved welded flanges and curved stiffeners
#   'S' for knuckled plates
#   'G' for corrugated plates
#   'B' for double-curved and single-curved plates
#   'Z' for assembled plates
#   ''  otherwise
#-----------------------------------------------------------------------------
    est = "HULL.PLATE('" + ModelName + "').FOLDED"
    resp = getStringValue(est)
    if resp == "YES":
      FormulaValue = 'F'
    else:
      est = "HULL.PLATE('" + ModelName + "').BENT"
      resp = getStringValue(est)
      if resp == "YES":
        FormulaValue = 'H'
      else:
        est = "HULL.PLATE('" + ModelName + "').CORRUGATION"
        resp = getStringValue(est)
        if resp == "YES":
          FormulaValue = 'G'
        else:
          est = "HULL.PLATE('" + ModelName + "').KNUCKLED"
          resp = getStringValue(est)
          if resp == "Plate is knuckled":
            FormulaValue = 'S'
          else:
            est = "HULL.PLATE('" + ModelName + "').CURVED"
            resp = getStringValue(est)
            if resp == "YES":
              FormulaValue = 'B'
            else:
              est = "HULL.PLATE('" + ModelName + "').ASSPART"
              resp = getStringValue(est)
              if resp == "YES":
                FormulaValue = 'Z'
              else:
                FormulaValue = ''

    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula


  if FormulaNumber == 10003:
#-----------------------------------------------------------------------------
#
#   Formula 10003
#
#   The purpose of this rule is to define a formula
#   creating nesting part names.
#
#   If the nested part belongs to a symmetric panel
#   then the partname valid for both sides will derived
#   by 'merging' the portside partname and the starboard partname
#   eg:
#
#   '222-FR50B-K1' + '232-FR50B-K1' => FormulaValue = '222/232-FR50B-K1' and
#   '101-GR8A-B2'  + '101-GR8P-B2'  => FormulaValue = '101-GR8A/GR8P-B2'
#
#   If the nested part does not belong to a symmetric panel
#   then FormulaValue equals the partname of the nested part.
#-----------------------------------------------------------------------------
    est = "HULL.PLATE('" + ModelName + "').PART_ID.LONG"
    resp = getStringValue(est)
    FormulaValue = ''
    if resp != "****":
#-----------------------------------------------------------------------------
#     A partname was retrieved.
#     If the panel is symmetrical the result from data extraction contains:
#     - the partname for the portside part,
#     - a delimiter consisting of '@@' and
#     - the partname for the starboard part.
#-----------------------------------------------------------------------------
      FormulaValue = resp
      DelimiterA = '@@'
      PartNameList = string.splitfields(resp,DelimiterA)
      if len(PartNameList) == 2:
        PSPartName = PartNameList[0]
        SBPartName = PartNameList[1]
#-----------------------------------------------------------------------------
#       A portside partname and a starboard partname was retrieved.
#       Split the two partnames into substrings delimited by '-'.
#-----------------------------------------------------------------------------
        DelimiterB = '-'
        PSPartNameList = string.splitfields(PSPartName,DelimiterB)
        SBPartNameList = string.splitfields(SBPartName,DelimiterB)
        lenPS = len(PSPartNameList)
        lenSB = len(SBPartNameList)
        DelimiterA = '/'
        FormulaValue = string.joinfields(PartNameList,DelimiterA)
        if lenPS == lenSB and lenPS > 2:
#-----------------------------------------------------------------------------
#       The portside partname and the starboard partnames should be 'merged'
#       if the third ( and following) substrings are equal and
#       if the first or second substring also are equal.
#-----------------------------------------------------------------------------
          bMerge = "YES"
          for i in range(2, lenPS - 1):
            if PSPartNameList[i] != SBPartNameList[i]:
              bMerge = "NO"
          if PSPartNameList[0] != SBPartNameList[0] and PSPartNameList[1] != SBPartNameList[1]:
            bMerge = "NO"
          if PSPartNameList[0] == SBPartNameList[0] and PSPartNameList[1] == SBPartNameList[1]:
            bMerge = "NO"
          if bMerge == "YES":
#-----------------------------------------------------------------------------
#           Merge partnames.
#-----------------------------------------------------------------------------
            if PSPartNameList[0] != SBPartNameList[0]:
              PSPartNameList[0] = PSPartNameList[0] + "/" + SBPartNameList[0]
            if PSPartNameList[1] != SBPartNameList[1]:
              PSPartNameList[1] = PSPartNameList[1] + "/" + SBPartNameList[1]
            FormulaValue = string.joinfields(PSPartNameList,DelimiterB)
    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula


  if FormulaNumber == 10004:
#-----------------------------------------------------------------------------
#
#   Formula 10004
#
#   The purpose of this rule is to define a formula for
#   working stage information.
#   FormulaValue is extracted as assembly attribute 'Working Location'
#-----------------------------------------------------------------------------
    est = "HULL.PLATE('" + ModelName + "').AS_ALL"
    resp = getStringValue(est)
    FormulaValue = ''
    if resp != "****":
#-----------------------------------------------------------------------------
#     An assembly was retrieved.
#     Get the assembly attribute 'Working Location'.
#-----------------------------------------------------------------------------
      AssemblyName = "-" + resp
      try:
        AssemblyObject = kcs_assembly.assembly_properties_get(AssemblyName)
        WorkingLoc = AssemblyObject.GetWorkingLocation()
        FormulaValue = WorkingLoc
      except:
        WorkingLoc = ""
    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula


  elif FormulaNumber == 5000:
#-----------------------------------------------------------------------------
#
#   Formula 5000
#
#   This rule has currently no support in Tribon. Its only purpose is to show
#   an example of a formula with 'extra' input and output.
#
#   It is supposed that 10 integers ( PI0, PI1,..,PI9),
#   10 reals ( PR0, PR1,..,PR9) and 10 strings ( PS0, PS1,..,PS9)
#   are defined in Tribon upon call of this script. This means that
#   parameters ParNInt, ParNRea and ParNStr all have value 10.
#
#   It is also supposed that Tribon will handle extra output of
#   10 integers ( RI0, RI1,..,RI9), 10 reals ( RR0, RR1,..,RR9) and
#   10 strings ( RS0, RS1,..,RS9). This means that parameters ResNInt,
#   ResNRea and ResNStr are set to 10 by this script.
#-----------------------------------------------------------------------------
    FormulaValue = 'Formula5000Value'
    ResNInt = 10
    ResNRea = 10
    ResNStr = 10
    RI0 = PI0 * 2
    RI1 = PI1 * 2
    RI2 = PI2 * 2
    RI3 = PI3 * 2
    RI4 = PI4 * 2
    RI5 = PI5 * 2
    RI6 = PI6 * 2
    RI7 = PI7 * 2
    RI8 = PI8 * 2
    RI9 = PI9 * 2
    RR0 = PR0 * PR0
    RR1 = PR1 * PR1
    RR2 = PR2 * PR2
    RR3 = PR3 * PR3
    RR4 = PR4 * PR4
    RR5 = PR5 * PR5
    RR6 = PR6 * PR6
    RR7 = PR7 * PR7
    RR8 = PR8 * PR8
    RR9 = PR9 * PR9
    RS0 = PS0
    RS1 = PS1
    RS2 = PS2
    RS3 = PS3
    RS4 = PS4
    RS5 = PS5
    RS6 = PS6
    RS7 = PS7
    RS8 = PS8
    RS9 = PS9

    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula
  elif FormulaNumber == 5001:
#-----------------------------------------------------------------------------
#
#   Formula 5001
#
#   This rule has currently no support in Tribon. Its only purpose is to show
#   an example of a formula with 'extra' input and output.
#
#   This rule translates from french to english.
#
#   Parameters PS0, PS1,..,PS9 are french words.
#   Resulting strings RS0, RS1,..,RS9 are translations into english
#
#-----------------------------------------------------------------------------
    FormulaValue = 'Not found'
    ResNInt = 0
    ResNRea = 0
    ResNStr = ParNStr

#-----------------------------------------------------------------------------
#
#  Define words in dictionary.
#
#-----------------------------------------------------------------------------
    french={}
    french['Amincis ou rablure']='Scarf'
    french['Anguillers']='limber holes'
    french['Appareil']='device'
    french['Appareil propulsif']='propelling plant'
    french['Arborescene']='treeing'
    french['Bigramme']='double letter monogram'
    french['Bilan thermique']='Heat balance'
    french['Borde']='plating'
    french['Bouchain']='Bilge'
    french['Bouge']='Camber'
    french['Breche']='hatch'
    french['Carenage']='regular overhaul'
    french['Carene']='underwater hull'
    french['Carlingage']='seating'
    french['Chaise d arbre']='propeller strut'
    french['Chanfrein d aboutissement']='abutment bevel'
    french['Cheminement']='routing'
    french['Chemineurs']='cable layers'
    french['Cloisonnement']='comparmentation'
    french['Cloisons']='bulkheads CPE Main Watertight Bulkhead'
    french['Cotation des plans']='dimension marking'
    french['Coupe au maitre']='midShips section'
    french['Couple']='frame'
    french['Crosses de gouvernail']='rudder skegs'
    french['Decoupures']='openings'
    french['Demantelement']='decommissioning'
    french['Desarmement ou retrait de service actif']='decommissioning or put out of commission'
    french['Disponibilite']='readiness'
    french['Dossier de definition']='description file'
    french['Ecubier']='hawse pipe'
    french['Element type']='standard part'
    french['Emmenagement']='layout'
    french['Ensemble']='assembly'
    french['Entree et sortie d eau']='water inlet and discharge'
    french['Epontille']='stanchion'
    french['Etablissement']='Facility'
    french['etanche']='watertight'
    french['Etudes']='designs'
    french['Fascicule de bornage']='list of connection terminals'
    french['Filieres']='trades'
    french['Flambement']='buckling'
    french['Fond de plan']='layout plan'
    french['Gabariage']='molding'
    french['Gabarit']='template'
    french['Gousset']='bracket'
    french['Habitabilite']='living spaces'
    french['Hiloire']='girder'
    french['Identifiant']='identifier'
    french['Indisponibilite']='down time'
    french['Installations']='Installations'
    french['Latte']='batten'
    french['Liaison']='connection link'
    french['Lissage']='fairing'
    french['Lisse']='handrail'
    french['Local']='compartment except for engine room etc'
    french['Localisation']='location'
    french['Logigramme']='Logic diagram'
    french['Membrures']='framing'
    french['Mise en plan']='drafting tools'
    french['Navire Batiment']='Ship'
    french['Ouverture']='opening'
    french['Paroi']='Partition bulkhead wall'
    french['Passage']='Passage'
    french['Plan de degauchissement']='Staightening plane'
    french['Pointe']='plotting'
    french['Ponts']='decks'
    french['PPAR']='AP'
    french['Profiles']='sections'
    french['Projeteur']='project engineer'
    french['Quille de roulis']='bilge keel'
    french['Raidisseurs']='stringers'
    french['Refonte']='major overhaul or refit'
    french['Repere deduits']='derived identifers'
    french['Repere d ensemble']='overall identifers'
    french['Reperes d overtures']='opening identifiers'
    french['Resistant']='resistant/solid'
    french['Resistante']='resistant/solid'
    french['Schema de principe']='flow chart'
    french['Sens de laminage']='rolling direction'
    french['Simulation de conduite']='Piloting Steering Management simulation'
    french['Sortie d arbre']='spectacle frame'
    french['Specialite']='trade'
    french['Stade de Conception']='Design Stage'
    french['Stade de Realisation']='Production Stage'
    french['Standard d echange']='interchange standard'
    french['Stations a terre']='shore establishments'
    french['Tapin']='plug'
    french['Trace d habillage']='cladding mark appelation AFT- pas sure'
    french['Traditionnel']='conventional'
    french['Transversee de coque']='Hull gland'
    french['Triedre Navire']='Ship frame of reference'
    french['Troncon de tuyautage']='piping section'
    french['Vaigre']='ceiling plate'
    french['Varangue']='frame of floor'
    french['Virure']='strakes'

    if ParNStr >= 10:
      if french.has_key(PS9):
        RS9 = french[PS9]
        FormulaValue = 'Found'
    if ParNStr >= 9:
      if french.has_key(PS8):
        RS8 = french[PS8]
        FormulaValue = 'Found'
    if ParNStr >= 8:
      if french.has_key(PS7):
        RS7 = french[PS7]
        FormulaValue = 'Found'
    if ParNStr >= 7:
      if french.has_key(PS6):
        RS6 = french[PS6]
        FormulaValue = 'Found'
    if ParNStr >= 6:
      if french.has_key(PS5):
        RS5 = french[PS5]
        FormulaValue = 'Found'
    if ParNStr >= 5:
      if french.has_key(PS4):
        RS4 = french[PS4]
        FormulaValue = 'Found'
    if ParNStr >= 4:
      if french.has_key(PS3):
        RS3 = french[PS3]
        FormulaValue = 'Found'
    if ParNStr >= 3:
      if french.has_key(PS2):
        RS2 = french[PS2]
        FormulaValue = 'Found'
    if ParNStr >= 2:
      if french.has_key(PS1):
        RS1 = french[PS1]
        FormulaValue = 'Found'
    if ParNStr >= 1:
      if french.has_key(PS0):
        RS0 = french[PS0]
        FormulaValue = 'Found'

    Formula = (FormulaValue,ResNInt,ResNRea,ResNStr,RI0,RI1,RI2,RI3,RI4,RI5,RI6,RI7,RI8,RI9,RR0,RR1,RR2,RR3,RR4,RR5,RR6,RR7,RR8,RR9,RS0,RS1,RS2,RS3,RS4,RS5,RS6,RS7,RS8,RS9)
    return Formula
  else:
    return None

#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
if __name__ == "__main__":
  print "_TBhook_Formula"
  print getFormula("plane panel","ES123-2","plate",2001,"",0,0,5000,10,10,10,0,1,2,3,4,5,6,7,8,9,0.0,1.1,2.2,3.3,4.4,5.5,6.6,7.7,8.8,9.9,"a","b","c","d","e","f","g","h","i","j")
  print getFormula("plate","ES999-HOLE-GRINDING-1P","",0,"",0,0,10001,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
  print getFormula("plate","ES123-2-1P","",0,"",0,0,10001,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
  print getFormula("plate","ES123-SHELL2-1P","",0,"",0,0,10002,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
  print getFormula("plate","ES233-721-1P","",0,"",0,0,10003,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
  print getFormula("plate","ES233-722-1P","",0,"",0,0,10003,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
  print getFormula("plate","ES233-722-1P","",0,"",0,0,10004,0,0,0,0,0,0,0,0,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,"","","","","","","","","","")
