#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,gettext
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
def page_header():
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr" lang="tr"><head><meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>"""
def error(lang):
    language=gettext.translation('messages',dir, languages=[lang])
    _=language.ugettext
    return page_header()+'<title>'+_('error page')+'</title></head><body><p><img alt="error" src="./img/error.png"/>'+ _('there is some problem please')+' <a href="./show.py">'+_('try')+'</a> '+_('again')+'.</p></body></html>'
