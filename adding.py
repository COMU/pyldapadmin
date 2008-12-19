#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
import template_page,server_info,os
import ldap,gettext
from re import match
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
def index(req):
    server=server_info.get_info(req)
    language=gettext.translation('messages',dir, languages=[server[4]])
    _=language.ugettext
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page=template_page.page_header()+'<title>'+_('adding')+'</title></head><body>'
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
        page+=_('adding successfull complete')+'.<a href="./show.py">'+ _('return')+'</a>'
    except ldap.LDAPError, e:
        if (e.message['desc'] == 'Already exists'):
            return page+'<p><img alt="error" src="./img/error.png"/> '+_('it already there')+' </p><p> '+_('go main')+'<a href="./show.py">'+_('page')+'</a></p></body></html>'
        elif (e.message['info'] == 'no write access to parent'):
            return page+'<p><img alt="error" src="./img/error.png"/>'+_('no write access to parent')+'</p><p>'+_('go main')+' <a href="./show.py">'+_('page')+'</a></p></body></html>'
        return template_page.error(server[4])
    return page+'</body></html>'

