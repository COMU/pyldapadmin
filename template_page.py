#!/usr/bin/python
# -*- coding: utf-8 -*-
def page_header():
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr" lang="tr"><head><meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>"""
def error():
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="tr" lang="tr"><head><meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/><title>error page</title></head><body><img src="./img/error.png">there is some problem please <a href="./">try</a> again.</body></html>"""
