# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:55:24 2016

@author: Madeleine

PIN_SEARCH.py

 enter description...

Modification history:
 6/13/16 - began coding
 6/23/16 - now prints the new PIN in 'file' loop
 6/28/16 -
"""


from rt_selenium import create_pin
from rt_selenium import options


filename = 'LakeView0816.txt'                   # Change for every search.

pin_list = []
with open(filename) as file:
    for line in file:
        pin_list.append(line.strip().split(','))
pin_list = pin_list[1:]
# Uncomment below to alter PINs without the leading 0:
# pin_list = ['0' + pin_list[x][0] for x in range(len(pin_list))]

choice = input('from file or input? ')

if choice == 'input':
    new_pin = create_pin()
    pin_segs = new_pin[0]
    dash_pin = new_pin[1]
    pin = new_pin[2]
    options(pin, pin_segs, dash_pin)

if choice == 'file':
    for p in range(len(pin_list)):
        new_pin = create_pin(pin_list[p][0])
        pin_segs = new_pin[0]
        dash_pin = new_pin[1]
        pin = new_pin[2]
        print(dash_pin)
        options(pin, pin_segs, dash_pin, 1)
