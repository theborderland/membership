#!/usr/bin/env python3

import get_pretix


def smep(args):
    from borderland_tool.smep import TransferTool
    pretix = get_pretix(args)
    smep = TransferTool(pretix)
    smep.update()
    smep.display()
