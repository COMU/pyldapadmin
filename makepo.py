#!/usr/bin/python
from os import system

system("xgettext -s --no-wrap --files-from=app.fil --output=program.pot")
for lang in ["tr", "en"]:
        system("msgmerge -U %s.po program.pot" % lang)
