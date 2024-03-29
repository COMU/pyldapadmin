#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap,template_page,server_info
from cgi import escape
import os,gettext
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
def index(req):
    server = server_info.get_info(req)
    language=gettext.translation('messages',dir, languages=[server[4]])
    _=language.ugettext
    page = template_page.page_header()
    page += '<title>'+_('export')+'</title></head><body>'
    page+='<div>\
    <form method="post" action="export.py/searching">\
    <h3>'+_('export options')+':</h3>\
    <p>ldap server: <b>'+server[2]+'</b></p>\
    <p>'+_('search scope')+':\
    <select name="scope" style="width: 200px">\
        <option selected="selected" value="ldap.SCOPE_SUBTREE">'+_('Sub (entire subtree)')+'</option>\
        <option value="ldap.SCOPE_ONELEVEL">'+_('One (one level beneath base)')+'</option>\
        <option value="ldap.SCOPE_BASE">'+_('Base (base dn only)')+'</option>\
    </select></p>\
    <p>'+_('Show Attributtes')+': <input type="text" name="att" value="*"/></p>\
    <p>'+_('base')+': <input type="text" name="base" value="'+server[3]+'"/></p>\
    <p>'+_('filter')+':<input type="text" name="filter" value="objectClass=*"/></p>\
    <p><input type="submit" value="'+_('search')+'"/></p>\
    </form></div></body></html>'
    return page
def searching(req):
    server=server_info.get_info(req)
    language=gettext.translation('messages',dir, languages=[server[4]])
    _=language.ugettext
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    page = template_page.page_header()+'<title>'+_('export')+'...</title></head><body>'
    try:
        ldap_server.bind_s(server[0],server[1])
        att = req.form['att']
        att = att.split(',')
        scope = req.form['scope']
        base = escape(req.form['base'])
        filter = escape(req.form['filter'])
        textarea=""
        if(scope == 'ldap.SCOPE_SUBTREE' ):
            result = ldap_server.search_s(base ,ldap.SCOPE_SUBTREE, filter, att)
        elif(scope == 'ldap.SCOPE_ONELEVEL' ):
            result = ldap_server.search_s(base ,ldap.SCOPE_ONELEVEL, filter, att)
        elif(scope == 'ldap.SCOPE_BASE'):
            result = ldap_server.search_s(base ,ldap.SCOPE_BASE, filter, att)
        for result in result:
            textarea+="dn: %s\n" %(str(result[0]))
            textarea+=""
            for key in result[1].keys():
                for att_value in result[1][key]:
                    textarea+='%s: %s\n' %(key,att_value)

            textarea+="\n"
        page+='<textarea cols=40 rows=20 wrap="soft" readonly="readonly">'+textarea+'</textarea>'
        page+='<p><a href="../login.py">'+_('back')+'</a></p>'
        page+='</body></html>'
        ldap_server.unbind()
        return page
    except:
        return template_page.error(server[4])
