#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap
import server_info,template_page
import os
import ldap.modlist as modlist
import ldap
import gettext
import server_info
dir=os.path.dirname(os.path.abspath(__file__))+'/locale'

def form(req):
   return """\
<html><body>
<form enctype="multipart/form-data" action="./upload" method="post">
<p>File: <input type="file" name="file"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body></html>
"""

def upload(req):
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
        #ldap_server.unbind()
   except:
        page = template_page.page_header()+'<title>error page</title></head><body><p><img alt="error" src="./img/error.png"/>there is some problem please <a href="./">try</a>again.</p></body></html>'
        server_info.index(req)
        return page
   try: # Windows needs stdio set for binary mode.
      import msvcrt
    #  import ldap.modlist as modlist


      msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
      msvcrt.setmode (1, os.O_BINARY) # stdout = 1
   except ImportError:
      pass
   #try:
    #    if (server_info.get_info(req)== 0):
     #       server = server_info.set_info(req)
    #    else:
      #      server=server_info.get_info(req)
      #      if server == 0:
      #          return server_info.get_info(req)

       # language=gettext.translation('messages',dir, languages=[server[4]])
       # _=language.ugettext
       # ldap_server = ldap.initialize('ldap://'+server[2])
       # ldap_server.protocol_version = ldap.VERSION3
       # ldap_server.bind_s(server[0],server[1])

   # A nested FieldStorage instance holds the file
   fileitem = req.form['file']
   add=[]
   error=[]
   temp = 1
   # Test if the file was uploaded
   if fileitem.filename:
       if( fileitem.filename.split(".")[-1].lower() == "txt" or fileitem.filename.split(".")[-1].lower() == "ldif"):
           line=fileitem.file.readline()
           line = line.split(":")
           while (temp):
               attrs = {}
               attrs["objectClass"]=[]
               #return str(type(line))
             #  while (type(line) == 'str' ):
              #     line = fileitem.file.readline()
               if ( line[0] == "dn"):
                   dn = line[1]
                   dn=dn.replace(" ","")
                   add.append( dn)
                   while(1):
                       line=fileitem.file.readline()
                       if not(line):
                            temp = 0
                            break
                       try:
                            line = line.split(":")
                            value = line[1]
                            value=value.replace(" ","")
                            if(line[0] == "dn" ):
                                break
                            if not (line[0] == "objectClass" ):
                                attrs[line[0]]=value.split("\n")[0]
                            else:
                                attrs[line[0]].append(value.split("\n")[0])
                       except:
                            if (line ==''):
                                temp = 0
                                break
                            else:
                                pass
                   try:
                      ldif = modlist.addModlist(attrs)
                      ldap_server.add_s(dn,ldif)
                   except ldap.LDAPError, e:
                       return e
                       error.append(dn)
                      # return "yppl"
               else:
                   line = fileitem.file.readline()
                   line = line.split(":")
            #http://www.grotan.com/ldap/python-ldap-samples.html örnek
           ###okuma bitti 
           #return readed_lines
       else:
          message = 'wrong file type'
      # strip leading path from file name to avoid directory traversal attacks
      # build absolute path to files directory
   else:
      message = 'No file was uploaded'
   ldap_server.unbind_s()
   return """<html><body><p>%s <br/> %s</p>
    <p><a href="./form">Upload another file</a></p>
    </body></html>""" % (add,error)
