#!/usr/bin/python
# -*- coding: utf-8 -*-
import ldap,server_info
import attr   #getting ldap attribute and objectclass in input schemas.
from mod_python import util
def index(req):
    att_list=[]
    may_att_list=[]
    server=server_info.get_info(req)
    ldap_server = ldap.initialize('ldap://'+server[2])
    ldap_server.protocol_version = ldap.VERSION3
    ldap_schema_object=attr.get_att(server[0],server[1],server[2])
    page='<html><head><title>add record</title></head><body><form action="./adding.py" method="post"><h4>objectclass:</h4>'
    if(str(type(req.form['objectclass_menu'])) == str(util.StringField)):
        page+='<input type="text" name="objectclass'+req.form['objectclass_menu']+'" value="'+req.form['objectclass_menu']+'">'
        att_list.append(ldap_schema_object[str(req.form['objectclass_menu'])]["MUST"])
        may_att_list.append(ldap_schema_object[str(req.form['objectclass_menu'])]["MAY"])
    else:
        for objectc in req.form["objectclass_menu"]:
            page+='<input type="text" name="objectclass'+objectc+'" value="'+objectc+'">'
            if (att_list.count(ldap_schema_object[objectc]["MUST"])==0):
                att_list.append(ldap_schema_object[objectc]["MUST"])
            if (may_att_list.count(ldap_schema_object[objectc]["MAY"])==0):
                may_att_list.append(ldap_schema_object[objectc]["MAY"])
    att_list_changer=[]

#in may and must list (may_att_list and att_list) must only one same attribute.. This is the controller...
    for may_list in may_att_list:
        for make_may_list in may_list:
            if (att_list_changer.count(make_may_list)== 0):
                att_list_changer.append(make_may_list)
    if ((att_list_changer.count('uid')== 1) and (att_list_changer.count('userid'))==1 ):
        att_list_changer.remove('userid')
    may_att_list = att_list_changer
    att_list_changer = []
    for may_list in att_list:
        for make_may_list in may_list:
            if (att_list_changer.count(make_may_list) == 0):
                att_list_changer.append(make_may_list)
    if ((att_list_changer.count('uid')== 1) and (att_list_changer.count('userid'))==1 ):
        att_list_changer.remove('userid')
    att_list = att_list_changer
#################################################
    #remove attribute which is in may list and must list. This attribute is in only must list
    for may_list in att_list:
        if (may_att_list.count(may_list)):
            may_att_list.remove(may_list)
################################################
    page+='<br/>where i put this rec rd:<input type="text" name="rdn">'
    if(type(att_list) == list ):
        page+="<h2>Required Attributes</h2>"
        for att in att_list:
                page+='<p>'+str(att)+':<input type="text" name='+str(att)+'></p>'
        page+='<br/><h2>Optional Attributes</h2>'
       # for counter in range(len(may_att_list)):
        for att in may_att_list:
                if (att == "userPassword"):
                    page+='<p>'+str(att)+':<input type="password" name='+str(att)+'></p>'
                else:
                    page+='<p>'+str(att)+':<input type="text" name='+str(att)+'></p>'
    else:
        pass
    page+='<input type="submit" value="send">'
    page+="</form></body></html>"
    return page
