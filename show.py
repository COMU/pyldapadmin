#!/usr/bin/python
# -*- coding: utf-8 -*-
from cgi import escape
import ldap,server_info,template_page
def index(req):
    try:
        if (server_info.get_info(req)== 0):
            server = server_info.set_info(req)
        else:
            server=server_info.get_info(req)
            if server == 0:
                return server_info.get_info(req)
  #  try:
        ldap_server = ldap.initialize('ldap://'+server[2])
        ldap_server.protocol_version = ldap.VERSION3
        ldap_server.bind_s(server[0],server[1])
        ldap_server.unbind()
        return """<html><body>
       <p><a href="./list.py"><img src="./img/list.png"> list</a></p>
       <p><a href="./delete_user.py"><img src="./img/trash.png"> delete</a></p>
       <p><a href="./add.py"><img src="./img/user.png"> add user</a></p>
       <p><a href="./search.py"><img src="./img/search.png"> search </a></p>
       <p><a href="./server_info.py"><img src="./img/exit.png">logout</a></p>
               </body></html>"""

    except:
       return template_page.error()
