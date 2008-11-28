#!/usr/bin/python
# -*- coding: utf-8 -*-
import attr
import ldap
import template_page,server_info
#from mod_python import Cookie
def index(req):
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page='<html><head><title>adding...</title></head><body>'
    try:
        ldap_server.bind_s(server[0],server[1])
        ldap_schema_object=attr.get_att(server[0],server[1],server[2])
        ldap_server.unbind()
        Schema=ldap_schema_object.keys()
        Schema.sort(key=str.lower)
        page+='<form action="./add_user.py" method="post">'
        page+='<select name="objectclass_menu" multiple>'
        for key in Schema:
            if (ldap_schema_object[key]["KIND"] == 'AUXILIARY'):
                page+='<option value='+key+'>'+key+'</option>'
            elif(ldap_schema_object[key]["KIND"] == 'STRUCTURAL'):
                page+='<option value='+key+' style="font-weight:bold">'+key+'</option>'
        page+='<input type="submit" value="continue">'
        page+='</select></form></body></html>'
        return page
    except:
        return template_page.error()
