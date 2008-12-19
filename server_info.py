#!/usr/bin/python
# -*- coding: utf-8 -*-
from mod_python import Cookie
import time
secret = "my_secret"
def index(req):
    secret = 'my_secret'
    marshal_cookies = Cookie.get_cookies(req, Cookie.MarshalCookie, secret=secret)
    returned_marshal = marshal_cookies.get('marshal', None)
    if(returned_marshal):
        returned_marshal.expires= time.time()
        Cookie.add_cookie(req, returned_marshal)
        return '<html><body>return to main place <a href="./">here</a></body></html>'
    else:
        return '<html><title></title><body>there is nothing <a href="./">back</a></body></html>'

def set_info(req):
        server_info=[]
        from cgi import escape
        name = escape(req.form['word'])
        host = escape(req.form['host_name'])
        password = escape(req.form['pas'])
        base_dn = escape(req.form['base_dn'])
        language = req.form['language']
        send_marshal = Cookie.MarshalCookie('marshal', {'key1':name, 'key2':password,'key3':host,'key4':base_dn,'key5':language}, secret)
        send_marshal.expires = time.time() +  4 * 60 * 60
        Cookie.add_cookie(req, send_marshal)
        server_info.append(name)
        server_info.append(password)
        server_info.append(host)
        server_info.append(base_dn)
        server_info.append(language)
        return server_info


def get_info(req):
    marshal_cookies = Cookie.get_cookies(req, Cookie.MarshalCookie, secret=secret)
    returned_marshal = marshal_cookies.get('marshal', None)
    if(returned_marshal):
        server_info=[]
        name = returned_marshal.value['key1']
        password = returned_marshal.value['key2']
        host = returned_marshal.value['key3']
        base_dn = returned_marshal.value['key4']
        language = returned_marshal.value['key5']
        server_info.append(name)
        server_info.append(password)
        server_info.append(host)
        server_info.append(base_dn)
        server_info.append(language)
        return server_info
    else:
        return 0
