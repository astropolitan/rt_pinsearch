# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 10:04:53 2016

@author: Madeleine


CREATE_PIN.py

 A helper function that constructs a Property Identification Number.

Mod history:
 6/1/16  - created code, added to RT_SELENIUM.py and RT_TREASURER.py,
             added 'dash(pin)' for PINs with dashes,
             added optional argument to create_pin()
 6/13/16 - revised code for PEP8 standards
"""


def dash(pin):
    """Helper function to navigate PINs already with dashes in the number."""
    while len(pin) != 18:
        if pin == 'q':
            break
        elif len(pin) == 13:
            pin += '-0000'
        else:
            pin = input('Please enter a valid PIN: ')
    dash_pin = pin
    pin1 = pin[0:2]
    pin2 = pin[3:5]
    pin3 = pin[6:9]
    pin4 = pin[10:13]
    pin5 = pin[14:]
    pin = pin1 + pin2 + pin3 + pin4 + pin5
    pin_segs = [pin1, pin2, pin3, pin4, pin5]
    return pin_segs, dash_pin, pin


def create_pin(inp=0):
    """Function that constructs a PIN. Takes an optional argument of a PIN as
    a string. If no PIN is entered, will ask for a PIN to be input."""
    if inp == 0:
        pin = input('Enter PIN: ')
        if pin == 'q':
            return
    else:
        pin = inp
    if '-' in pin:
        dashp = dash(pin)
        pin_segs = dashp[0]
        dash_pin = dashp[1]
        pin = dashp[2]
    else:
        while len(pin) != 14:
            if len(pin) == 10:
                pin += '0000'
            else:
                pin = input('Please enter a valid PIN: ')
            if pin == 'q':
                break
        pin1 = pin[0:2]
        pin2 = pin[2:4]
        pin3 = pin[4:7]
        pin4 = pin[7:10]
        pin5 = pin[10:]
        dash_pin = str(pin1) + '-' \
            + str(pin2) + '-' \
            + str(pin3) + '-' \
            + str(pin4) + '-' \
            + str(pin5)
        pin_segs = [pin1, pin2, pin3, pin4, pin5]
    return pin_segs, dash_pin, pin
