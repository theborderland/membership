#!/usr/bin/env python3

from borderland_tool.get_pretix import get_pretix
from borderland_tool.smep import TransferTool


def smep(args):
    pretix = get_pretix(args)
    smep = TransferTool(pretix)
    smep.update()
    smep.display()
