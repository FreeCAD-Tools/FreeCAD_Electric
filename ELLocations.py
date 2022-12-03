# -*- coding: utf-8 -*-
###############################################################################
#
#  ELLocations.py
#
#  Copyright 2022 <>
#
###############################################################################
import os

_dir = os.path.dirname(__file__)
iconPath = os.path.join(_dir, 'Icons')
templatesPath = os.path.join(_dir, 'Templates')
symbolsPath = os.path.join(_dir, 'Symbols')
LanguagePath = os.path.join(_dir, 'translations')

def getIconPath(file):
   return os.path.join(iconPath, file)
   
def getSymbolPath(file):
   return os.path.join(symbolsPath, file)