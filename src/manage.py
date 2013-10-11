#!/usr/bin/env python
import os
import sys

"""
Classijango coding standard:

Classes: Camelcase with the first word to upper
    Example: class UserProfile():

Functions / (Static) Methods: Camelcase with the first word to lower
    Example: def camelCaseMethod()

Vars: Lowercase with underscore
    Example: query_string = ''

Consts: Uppercase
    Example: UPLOAD_RATE = ''

"""

# Do not generate bytecodes in developer mode
sys.dont_write_bytecode = True

print '*** CLASSIJANGO APP ***'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classifieds.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
