#!/usr/bin/env python
import os
import sys

"""
Do not generate bytecodes in developer mode
"""
sys.dont_write_bytecode = True

print '*** CLASSIJANGO APP ***'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "classifieds.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
