# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 15:22:17 2016

@author: Madeleine

ADD_PIN.py

 This function finds the total values of Assessed/Market Values for
 parcels of PINs.

Modification history:
 7/21/16  - began coding
 8/4/16   - revised add_pin() to comply with new STICKER_INFO.py changes,
             added add_mult() and degraded add_pin() to a helper function
 8/10/16  - removed tax options
"""

from sticker_info import *
from create_pin import create_pin


def add_pin(pin, av, mv):
    """Calculates the combined Assessed Value and Market Value for two PINs.

    Parameters
    ----------
    pin : string
        A string representing the added PIN
    av : number
        The assessed value of the original (base) PIN
    mv : number
        The market value of the original (base) PIN

    Returns
    -------
    tot_av : number
        The new total Assessed Value
    tot_mv : number
        The new total Market Value
    """
    new_ao = ao_info(pin, 0, 1)
    new_av = new_ao[0]
    new_mv = new_ao[1]

    tot_av = av + new_av
    tot_mv = mv + new_mv
    return tot_av, tot_mv


def add_mult(n, base_av, base_mv):
    """A function that will calculate total AV and MV when a parcel
    has multiple PINs.

    Parameters
    ----------
    n : number
        The number of PINs in the parcel
    base_av : number
        The base PIN's AV
    base_mv : number
        The base PIN's MV

    Returns
    -------
    tot_av : number
        The new total Assessed Value
    tot_mv : number
        The new total Market Value
    """
    tot_av = base_av
    tot_mv = base_mv
    while n != 0:
        pin = create_pin()[2]
        new = add_pin(pin, tot_av, tot_mv)
        tot_av = new[0]
        tot_mv = new[1]
        n -= 1
    return tot_av, tot_mv
