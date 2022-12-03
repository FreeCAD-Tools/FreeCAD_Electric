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
pathToIconsFolder = os.path.join(_dir, 'Icons')
pathToTemplatesFolder = os.path.join(_dir, 'Templates')
pathToSymbolsFolder = os.path.join(_dir, 'Symbols')
pathToTranslationsFolder = os.path.join(_dir, 'translations')

def getIconPath(file):
   return os.path.join(pathToIconsFolder, file)

def getSymbolPath(file):
   return os.path.join(pathToSymbolsFolder, file)

def getTemplatePath(file):
   return os.path.join(pathToTemplatesFolder, file)