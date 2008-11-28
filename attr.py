#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import ldap.schema
import ldapurl
def get_att(name,password,host):
#if __name__=='__main__':
    url = ldapurl.LDAPUrl('ldap://', host+':389', '', name)
    ldap_server = ldap.initialize('ldap://'+host+':389')
    ldap_server.bind_s(name, password)
    subentrydn = ldap_server.search_subschemasubentry_s()
    entry = ldap_server.read_subschemasubentry_s(subentrydn,url.attrs)
    schema = None
    attributes = {}
    objectclass = {}
    if subentrydn!=None:
        schema = ldap.schema.SubSchema(entry)
        attlist = schema.listall(ldap.schema.AttributeType)
        for item in attlist:
            a = schema.get_obj(ldap.schema.AttributeType, item)
            attnamelist = a.names
            for att in attnamelist:
                attributes[att.lower()] = {"DESC": a.desc,
                "SINGLE": a.single_value,
                "SYNTAX": a.syntax,
                "NAME": att,
                "COLLECTIVE": a.collective,
                "EQUALITY": a.equality,
                "OBSOLETE": a.obsolete,
                "OID": a.oid,
                "ORDERING": a.ordering, "SUP": a.sup,
                "SYNTAX_LEN": a.syntax_len,
                "USAGE": a.usage}
        objlist = schema.listall(ldap.schema.ObjectClass)
        for oids in objlist:
            a = schema.get_obj(ldap.schema.ObjectClass, oids)
            kind = ""
            if a.kind == 0:
                kind = "STRUCTURAL"
            if a.kind == 1:
                kind = "ABSTRACT"
            if a.kind == 2:
                kind = "AUXILIARY"
            desc = ""
            if a.desc != None:
                desc = a.desc
            must = []
            if len(a.must) != 0:
                must = a.must
            may = []
            if len(a.may) != 0:
                may = a.may
            sup = []
            for item in a.sup:
                if item.lower() != 'top':
                    sup.append(item.lower())
            numericoid = ""
            if a.oid != None:
                numericoid = a.oid

            for name in a.names:
                objectclass[name] = {"DESC":desc,"MUST":must,"MAY": may,"NAME": name,"KIND":kind,"SUP":sup,"OID": numericoid}
    else:
        schema = None

    #print attributes
    ldap_server.unbind()
    return objectclass
