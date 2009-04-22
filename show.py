#!/usr/bin/python
# -*- coding: utf-8 -*-
from cgi import escape
import gettext,os
import server_info
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'
import ldap,server_info,template_page
def index(req):
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
        return template_page.page_header()+"""<link rel="stylesheet" href="deneme.css" type="text/css" media="screen"/>
        <link rel="SHORTCUT ICON" href="img/icon.ico"/>
        <script type="text/javascript">
        function a(){
        document.getElementById("main_frame").data= "./list.py";
        }
        function b(){
        document.getElementById("main_frame").data= "./delete_user.py";
        }
        function c(){
        document.getElementById("main_frame").data= "./add.py";
        }
        function d(){
        document.getElementById("main_frame").data= "./search.py";
        }
        function e(){
        document.getElementById("main_frame").data= "./export.py";
        }
        function f()
        {
        document.getElementById("main_frame").data="./file_input.py/form"
        }
        </script>
        <title> pyldapadmin</title>
        </head>
        <body>
       <div id="sayfa"><div id="baslik"></div><div id="anabolge"><div id="yanmenu">
       <p><a href="#" onclick="a()" ><img src="./img/list.png" alt=""/><br/>"""+ _('List')+"""</a></p>
       <p><a href="#" onclick="b()"><img src="./img/trash.png" alt=""/><br/>"""+_(' delete')+"""</a></p>
       <p><a href="#" onclick="c()"><img src="./img/user.png" alt=""/><br/>"""+_('add user')+"""</a></p>
       <p><a href="#" onclick="d()"><img src="./img/search.png" alt=""/><br/>"""+_('search')+""" </a></p>
       <p><a href="#" onclick="e()"><img src="./img/download.png" alt=""/><br/>"""+_('export')+""" </a></p>
       <p><a href="#" onclick="f()"><img src="./img/import.png" alt=""/><br/>"""+_('import')+""" </a></p>

       <p><a href="./server_info.py" onclick=""><img src="./img/exit.png" alt=""/><br/>"""+_('logout')+"""</a></p></div>
       <div id="icerik">
           <object id="main_frame" data="login.py"  width="100%" height="400px"></object>
       </div></div><div id="altlik"></div></div>
               </body></html>"""
    except UnboundLocalError,e:
        return template_page.page_header()+'<title>error page</title></head><body><p><img alt="error" src="./img/error.png"/>there is some problem please<a href="./">try</a>again.</p></body></html>'
    except:
        page = template_page.page_header()+'<title>'+_('error page')+'</title></head><body><p><img alt="error" src="./img/error.png"/>'+ _('there is some problem please')+' <a href="./">'+_('try')+'</a> '+_('again')+'.</p></body></html>'
        server_info.index(req)
        return page
