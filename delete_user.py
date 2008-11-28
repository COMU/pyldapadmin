#!/usr/bin/python
# -*- coding: utf-8 -*-
import mod_python,server_info
import ldap
def index(req):
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page='<html><head><title>delete</title></head><body>'
    try:
        ldap_server.bind_s(server[0],server[1])
        base_dn=server[3]
        counter=0
        filter = '(objectclass=*)'
        attrs = ["*"]
        result=ldap_server.search_s(base_dn,ldap.SCOPE_SUBTREE,filter,attrs)
        page+='<form method="post" action="delete_user.py/remove"><div align="center">'
        for dn in result:
            page+='<input type="checkbox" name="remove" value="'+dn[0]+'">'+dn[0]+'<br/>'
            counter+=1
        page+='<input type="submit" value="submit">'
        page+='</body></html>'
    except:
        page+='there is some problem please <a href="./">try</a> again.</body></html>'
    ldap_server.unbind()
    return page
def remove(req):
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page='<html><head><title>delete</title></head><body>'
    ldap_server.bind_s(server[0],server[1])
    try:
        if(str(type(req.form["remove"][0])) == str(mod_python.util.StringField)):
            for list in req.form["remove"]:
                ldap_server.delete_s(list)
                page+=list+'<br/> removed<br/>'
        else:
            ldap_server.delete_s(req.form["remove"])
            page+=req.form["remove"]+' removed<br/>'
    except ldap.LDAPError, e:
        page+= e.message['info']
        if (e.message['desc'] == 'No such object'):
            page+=e.message['desc']
        if (e.message['info'] == 'no write access to parent'):
            page +='<br/><img src="../img/gpg.png">'
    page+=' <a href="../show.py">back</a>'
    page+='</body></html>'
    ldap_server.unbind()
    return page
