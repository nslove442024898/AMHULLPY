## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import KcsElementHandle
import ctx_menu6

import kcs_draft

def run(*args):
    if not hasattr(kcs_draft, 'ContextSubpictures'):
        return
    if kcs_draft.ContextSubpictures == None:
        return
    if len(kcs_draft.ContextSubpictures) < 2:
        return

    ctx_menu6.MoveElement(kcs_draft.ContextSubpictures[1])

    kcs_draft.dwg_repaint()
