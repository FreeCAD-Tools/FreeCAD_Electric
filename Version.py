# -*- coding: utf-8 -*-
###############################################################################
#
#  Utils.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import FreeCAD

def ofFreeCAD():
    major = FreeCAD.Version()[0]
    minor = FreeCAD.Version()[1]
    revision = FreeCAD.Version()[2]
    if revision.isnumeric():
        version = minor + "." + revision
    else:
        version = minor    
    return float(version)

#def FreeCADVersionIsHigherOrEqualThan(major,minor,revision):
#    return True

#def FreeCADGitVersionIsHigherOrEqualThan(number):
#    return True