#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap,template_page,server_info,os,gettext
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
def index(req):
    server=server_info.get_info(req)
    language=gettext.translation('messages',dir, languages=[server[4]])
    _=language.ugettext


    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page=template_page.page_header()+'<title>search page</title></head><body>'
    try:
        ldap_server.bind_s(server[0],server[1])
        base_dn = server[3]
        filter = '(objectclass=*)'
        attrs = ['*']
        res=ldap_server.search_s(base_dn , ldap.SCOPE_SUBTREE, filter, attrs)
        for result in res:
            page+="<p><b>%s</b>:" %(str(result[0]))
            page+="<br/>"
            for key in result[1].keys():
                page+="%s:<br/>" %(key)
                for att_value in result[1][key]:
                    page+='<input type="text" value="%s"/> ' %(att_value)
                page+="<br/>"
            page+="</p>"
        page+='<p><a href="./show.py">back</a></p>'
        page+='</body></html>'
        ldap_server.unbind()
        return page
    except ldap.LDAPError, e:
        return str(e)
    except:
        return tamplete_page.error()
