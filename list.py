#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap,template_page,server_info
def index(req):
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page='<html><head><title>search page</title></head><body>'
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
                    page+='<input type="text" value="%s"> ' %(att_value)
                page+="<br/>"
            page+="</p>"
        page+='<a href="./show.py">back</a>'
        page+='</body></html>'
        ldap_server.unbind()
        return page
    except ldap.LDAPError, e:
        return str(e)
    except:
        return tamplete_page.error()
