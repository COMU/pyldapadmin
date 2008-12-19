#!/usr/bin/python
# -*- coding: utf-8 -*-
import template_page
def index():
   s =template_page.page_header()+ """\
<body>
<form method="post" action="./show.py">
<p>ldap host: <input type="text" name="host_name"></p>
<p>username: <input type="text" name="word"></p>
<p>password: <input type="password" name="pas"></p>
<p>base_dn: <input type="text" name="base_dn"></p>
<p>language: 
<select NAME="language">
<option value="tr"> Turkçe</option>
<option selected="selected" value="en"> English</option>
</select> 

</p>
<p><input type="submit" value="Submit"</p>
</form></body></html>
"""
   return s
