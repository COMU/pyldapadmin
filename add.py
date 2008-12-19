#!/usr/bin/python
# -*- coding: utf-8 -*-
import attr
import ldap,gettext,os
import template_page,server_info
#from mod_python import Cookie
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
def index(req):
    server=server_info.get_info(req)
    language=gettext.translation('messages',dir, languages=[server[4]])
    _=language.ugettext
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page=template_page.page_header()+'<title>'+_('adding...')+'</title></head><body>'
    try:
        ldap_server.bind_s(server[0],server[1])
        ldap_schema_object=attr.get_att(server[0],server[1],server[2])
        ldap_server.unbind()
        Schema=ldap_schema_object.keys()
        Schema.sort(key=str.lower)
        page+='<form action="./add_user.py" method="post"><p>'
        page+='<select multiple="multiple" name="objectclass_menu" size="15" >'
        for key in Schema:
            if (ldap_schema_object[key]["KIND"] == 'AUXILIARY'):
                page+='<option value="'+key+'">'+key+'</option>'
            elif(ldap_schema_object[key]["KIND"] == 'STRUCTURAL'):
                page+='<option value="'+key+'" style="font-weight:bold">'+key+'</option>'
        page+='</select><input type="submit" value="'+_('continue')+'" /></p>'
        page+='</form></body></html>'
        return page
    except:
        return template_page.error(server[4])
