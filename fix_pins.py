# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 18:23:08 2016

@author: Madeleine
"""

with open('schaumburg16.txt', 'r') as src:
    with open('schaumburg16n.txt', 'w') as dest:
        for line in src:
            dest.write('%s%s\n' % ('0', line.rstrip('\n')))
