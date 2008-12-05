#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import template_page,server_info
import ldap
from re import match
def index(req):
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page=template_page.page_header()+'<title>adding</title></head><body>'
    list=req.form.keys()
    record=()
    obje=[]
    record_obje=[]
    record_att_value=()
    record_att=[]
    record+=('objectclass',)
    for att in list:
        if ( match('objectclass',att)):
            obje.append(cgi.escape(att.split('objectclass')[1]))
        else:
            if(att == 'rdn'):
                rdn=cgi.escape(req.form[att])
            else:
                try:
                    if( cgi.escape(req.form[att]) != ''):
                        record_att_value=(cgi.escape(att),[cgi.escape(req.form[att])])
                        record_att.append(record_att_value)
                except:
                    return req.form[att]
    record+=(obje,)
    record_obje.append(record)
    for final_att in record_att:
        record_obje.append(final_att)
    try:
        ldap_server.bind_s(server[0],server[1])
        ldap_server.add_s(rdn,record_obje)
        page+='adding successfull complete.<a href="./show.py"> return</a>'
    except ldap.LDAPError, e:
        if (e.message['desc'] == 'Already exists'):
            return page+'<p><img alt="error" src="./img/error.png"/>it already there'+' </p><p> go main<a href="./show.py">page</a></p></body></html>'
        elif (e.message['info'] == 'no write access to parent'):
            return page+'<p><img alt="error" src="./img/error.png"/>no write access to parent</p><p> go main <a href="./show.py">page</a></p></body></html>'
        return template_page.error()
    return page+'</body></html>'

