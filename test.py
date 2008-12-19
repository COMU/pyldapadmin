#!/usr/bin/python
# -*- coding: utf-8 -*-
import gettext

#lang1 = gettext.translation('test' ,'locale' ,languages=['en'])
def index():
    import sys,os
    return os.path.dirname(os.path.abspath(__file__))
    #return pathname
#index()
#print a
