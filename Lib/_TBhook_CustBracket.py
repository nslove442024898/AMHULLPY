#
#  _TBhook_CustBracket - Customized Bracket panel hook
#
#  If this script is found in the PYTHONPATH it will be used to create bracket
#  panels automatically. The signature of the interface methods must not be changed.
#
import string
import kcs_dex
import kcs_ui
import kcs_util
import kcs_draft
import kcs_hullpan
import KcsPoint2D
import KcsModel

import _TBhook_AutoPanelName

OK = kcs_util.ok()
CANCEL = kcs_util.cancel()


#-----------------------------------------------------------------
#
#    Function GetPanel
#
#    This is a helpfunction for Bracket1.
#    Interactively picks the panel, checking its type and name
#
#    Returns a tuple:
#
#    status can  we continue? (OK, or not OK)
#    panel  boundary panel name
#-----------------------------------------------------------------

def GetPanel(message):
  point = KcsPoint2D.Point2D()
  while 1:
    # Indicate a point in the drawing
    res = kcs_ui.point2D_req(message, point)
    if res[0] == OK:
      try:
        model = KcsModel.Model()
        # Identify, what has been indicated?
        res = kcs_draft.model_identify(point,model)
        # Check the type of the identified model
        if model.Type != "plane panel":
          kcs_ui.message_confirm("Plane panel expected!")
        else:
          # Highlight the model item
          handle = kcs_draft.element_highlight(res[1])
          # Get user confirmation
          ask = kcs_ui.answer_req(message, \
                model.Name+", OK?")
          # Turn the highlight off
          kcs_draft.highlight_off(handle)
          if ask == kcs_util.yes():
            return (OK, model.Name) # OK, panel approved
      except:
        kcs_ui.message_noconfirm("Model not found!")
    else:
      return (CANCEL, "") # User cancelled the input

#-------------------------------------------------------------
#
#    Function Bracket1
#    Example of bracket generating code
#
#-------------------------------------------------------------

def Bracket1(BracketName):


  status = CANCEL
  Result = 0

  position = kcs_ui.string_req("Bracket position ( FR-term or X-Coord)")
  if position[0] == OK:
    FRTerm = str(position[1])
    tanktop = GetPanel("Indicate tanktop")
    if tanktop[0] == OK:
      girder = GetPanel("Indicate girder")
      if girder[0] == OK:
        status = OK

  if status == OK:
    try:
      # Initialise the panel
      kcs_ui.message_confirm( "Initiating panel")
      kcs_hullpan.pan_init(BracketName, "Double bottom plate")
      try:
        # PANEL statement
        st = "PAN, '" + BracketName +  "', SBP, DT=123, BRA, X=" + \
             FRTerm + ";"
        kcs_ui.message_confirm( "Creating panel")
        kcs_hullpan.stmt_exec_single(0, st, BracketName)

        # BOUNDARY statement
        st = "BOU, SUR='MTP'" + "/ '" + tanktop[1] + \
             "'/ '" + girder[1] + "';"
        print(" BOU", st)
        kcs_ui.message_confirm( "Creating boundary")
        kcs_hullpan.stmt_exec_single(0, st, BracketName)

        # PLATE statement
        st = "PLA, MAT=12, MSI=FOR, QUA=A36;"
        print(" PLA", st)
        kcs_ui.message_confirm( "Creating plate")
        kcs_hullpan.stmt_exec_single(0, st, BracketName)

        # NOTCH statement
        st = "NOT, R50, COR=1,2,3;"
        print(" NOT", st)
        kcs_ui.message_confirm( "Creating notch")
        kcs_hullpan.stmt_exec_single(0, st, BracketName)

        # store the panel
        kcs_ui.message_confirm( "Storing bracket panel")
        kcs_hullpan.pan_store_single(BracketName)
        model = KcsModel.Model("plane panel", BracketName)
        try:
          kcs_draft.model_draw(model)
        except:
          kcs_ui.message_confirm("Error redrawing the panel!")

      finally:
        # terminate the scheme
        kcs_ui.message_confirm( "Skipping panel")
        kcs_hullpan.pan_skip_single(BracketName)
        return Result

    except:
      kcs_ui.message_confirm("Error creating the panel!")
      Result = 1
      return Result
  return 1

def BracketMZA(BracketName):
  kcs_ui.message_noconfirm('Bracket Name: '+BracketName)
  deck = GetPanel('Indicate deck panel....')
  kcs_ui.message_debug(deck)
  if deck == None:
    kcs_ui.message_noconfirm('Bracket creation cancelled')
    return 1
  else:
    flange = GetPanel('Indicate web frame flange....')
    if flange == None:
      kcs_ui.message_noconfirm('Bracket creation cancelled')
      return 1
    else:
      position = kcs_ui.string_req("Bracket position ( LP-term or Y-Coord)")
      if position[0] == OK:
        pos = str(position[1])
        try:
          # Initialise the panel
          kcs_ui.message_noconfirm( "Initiating panel")
          kcs_hullpan.pan_init(BracketName, "")
          # PANEL statement
          st = "PAN, '" + BracketName +  "', BRA, Y=" + pos + ";"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=1, INT, '"+deck[1]+"', SID=TOP/ '"+flange[1]+"', SI2=AFT;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=2, DU=-430, DV=15, X=P1, Z=P1;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=3, DU=-144, DV=785, X=P1, Z=P1;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "CUR, 'BOU1', X=P2 / U=P2, V=P2, T=30 / R=250, U=P3, V=P3, T=83;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=11, INT, '"+deck[1]+"', SID=TOP/ '"+flange[1]+"', SI2=FOR;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=12, DU=430, DV=15, X=P11, Z=P11;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "POI,  NO=13, DU=300, X=P3, Z=P3;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "CUR, 'BOU2', X=P12 / U=P12, V=P12, T=150 /R=250, U=P13, V=P13, T=97;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "BOU, Z=P1 / 'BOU1' / Z=P3 / 'BOU2';"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)
          st = "PLA,  MAT=30, MSI=PS;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)

          st = "WEL,  LIM=2, BEV=V22.5T;"
          kcs_hullpan.stmt_exec_single(0, st, BracketName)

          kcs_hullpan.pan_store_single(BracketName)
          kcs_hullpan.pan_skip_single(BracketName)
          return 0
        except:
          return 1
      else:
        return 1

def BracketMZB(BracketName):
  pan1 = GetPanel('Indicate Panel 1 ....')
  kcs_ui.message_debug(pan1)
  if pan1 == None:
    kcs_ui.message_noconfirm('Bracket creation cancelled')
    return 1
  else:
    pan2 = GetPanel('Indicate Panel 2....')
    if pan2 == None:
      kcs_ui.message_noconfirm('Bracket creation cancelled')
      return 1
    else:
      position = kcs_ui.string_req("Bracket position ( LP-term or Z-Coord)")
      if position[0] == OK:
        pos = str(position[1])
        param = kcs_ui.string_req("Key in bracket parameters A,B,C,D", "150,150,300,600")
        if param[0] == OK:
          brparam = param[1].split(',')
          try: 
            # Initialise the panel
            kcs_hullpan.pan_init(BracketName, "")

            st = "PAN, '" + BracketName +  "', BRA, Z=" + pos + ";"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=1, INT, '" + pan1[1] + "', SID=SB/ '" + pan2[1] + "', SI2=FOR;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=2, INT, '" + pan1[1] + "', SID=SB/ '" + pan2[1] + "', SI2=AFT;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=3, INT, '" + pan1[1] + "', SID=PS/ '" + pan2[1] + "', SI2=AFT;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=11, XYZ=P1, X2Y=P2, F=0.5;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=12, XYZ=P2, X2Y=P3, F=0.5;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=21, DU="+str(int(brparam[3])/2)+", DV="+str(int(brparam[0])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=22, DU="+str(int(brparam[3])/2)+", DV=-"+str(int(brparam[0])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=23, DU=-"+str(int(brparam[3])/2)+", DV="+str(int(brparam[0])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=24, DU=-"+str(int(brparam[3])/2)+", DV=-"+str(int(brparam[0])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=31, DU="+str(int(brparam[1])/2)+", DV="+str(int(brparam[2])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=32, DU=-"+str(int(brparam[1])/2)+", DV="+str(int(brparam[2])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=33, DU=-"+str(int(brparam[1])/2)+", DV=-"+str(int(brparam[2])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "POI,  NO=34, DU="+str(int(brparam[1])/2)+", DV=-"+str(int(brparam[2])/2)+", X=P11, Y=P12;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "CUR, 'BOU1', X=P21, Y=P21, XT=P31, YT=P31 / X=P31, Y=P31, XT=P32, YT=P32 /X=P32, Y=P32, XT=P23, YT=P23;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "CUR, 'BOU2', X=P24, Y=P24, XT=P33, YT=P33 /X=P33, Y=P33, XT=P34, YT=P34 /X=P34, Y=P34, XT=P22, YT=P22;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "BOU, X=P23 / 'BOU2' / X=P22 / 'BOU1';"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            st = "PLA,  MAT=20, MSI=BOT;"
            kcs_hullpan.stmt_exec_single(0, st, BracketName)

            return 0
          except:
            return 1
        else:
          return 1
      else:
        return 1

#-----------------------------------------------------------------------------
#    Interface methods - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

BracketList = ["BRACKET1","MZA","MZB",""]

#-----------------------------------------------------------------------------
#     Function getBracketName -
#
#     Returns the bracket name of a choosen symbol numer
#
#----------------------------------------------------------------------------

def getBracketName(BracketNo):
  try:
    return BracketList[BracketNo]
  except:
    return None

#-----------------------------------------------------------------------------
#     Function setBracketContour -
#
#     The Bracket definition function
#     The function should return an integer result
#     code, 0 for success, and 1 as exception
#
#-----------------------------------------------------------------------------

def setBracketContour( BracketNo, BracketName):
  if BracketNo == 0:
    res = Bracket1(BracketName)
    BraRes = res
  elif BracketNo == 1:
    res = BracketMZA(BracketName)
    BraRes = res
  elif BracketNo == 2:
    res = BracketMZB(BracketName)
    BraRes = res
  else:
    BraRes = 1

  return BraRes