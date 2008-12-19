#!/usr/bin/python
# -*- coding: utf-8 -*-
from cgi import escape
import gettext,os
import server_info
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
import ldap,server_info,template_page
def index(req):
   # return dir
    try:
        if (server_info.get_info(req)== 0):
            server = server_info.set_info(req)
        else:
            server=server_info.get_info(req)
            if server == 0:
                return server_info.get_info(req)

        language=gettext.translation('messages',dir, languages=[server[4]])
        _=language.ugettext
        ldap_server = ldap.initialize('ldap://'+server[2])
        ldap_server.protocol_version = ldap.VERSION3
        ldap_server.bind_s(server[0],server[1])
        ldap_server.unbind()
        return template_page.page_header()+"""<link rel=stylesheet href="deneme.css" type="text/css" media=screen><body><div id="sayfa"><div id="baslik"></div><div id="anabolge"><div id="yanmenu"
       <p><a href="./list.py"><img src="./img/list.png">"""+ _('List')+"""</a></p>
       <p><a href="./delete_user.py"><img src="./img/trash.png">"""+_(' delete')+"""</a></p>
       <p><a href="./add.py"><img src="./img/user.png">"""+_('add user')+"""</a></p>
       <p><a href="./search.py"><img src="./img/search.png">"""+_('search')+""" </a></p>
       <p><a href="./server_info.py"><img src="./img/exit.png">"""+_('logout')+"""</a></p></div>
       <div id="icerik">
           <h1>Main page</h2><br/><br/>
       </div></div></div>
               </body></html>"""

    except:
        page = template_page.page_header()+'<title>'+_('error page')+'</title></head><body><p><img alt="error" src="./img/error.png"/>'+ _('there is some problem please')+' <a href="./">'+_('try')+'</a> '+_('again')+'.</p></body></html>'
        server_info.index(req)
        return page
