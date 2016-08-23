# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:45:56 2016

@author: Madeleine

RT_SELENIUM.py

 A program to retrieve all the data for a property packet. Takes a PIN at
 start-up and can take a new PIN while the program is running. Can also read
 PINs from a file.

Modification history:
 5/26/16  - began coding
 5/27/16  - having issues with 'court()' function
 6/1/16   - added helper functions from CREATE_PIN.py
 6/18/16  - added code input to bor(), revised code to fit PEP8 standards,
             revised docstrings
 6/22/16  - added return to bor() for capabilities in BOR_SEARCH.py,
             added window sizing/positioning parameters to bor(), also
             capability to quit search from code input
 6/23/16  - tried court() again, still can't get it to work, so it now just
             navigates to the search page; added keywords to collc() & maps(),
             print dash PIN in court(); added zoom kywd to bor()
 6/28/16  - added return statements for ccao() and tax() to get the URLs for
             STICKER_INFO.py
 7/3/16   - added zoom to ccrd()
 7/6/16   - tried to revise bor() for case of No Data
 7/8/16   - added implicit wait to ccrd(), fixed ElementNotVisible exception!
 7/20/16  - removed url returns from ccao() and tax(), added 'a' option to menu
             enabling adding PINs while going through a file, added sys.exit()
             in order to completely quit loop even when using a file
 8/4/16   - added code to options()'s 'a' option that uses ADD_PIN.py,
             fixed court() by adding implicitly_wait!
 8/8/16   - increased implicitly_wait() time in court()
 8/10/16  - fixed tax() for new website and removed all uses of tax_info()
 8/12/16  - removed 'b' option for options(), made sqft calculation part of
             sticker info
 8/19/16  - changed all implicitly_wait()s to 30 seconds
 8/22/16  - added sq ft calculator to add option in menu
 8/23/16  - added delinqs() to options for Delinquent Property Tax Search
"""

import sys
import locale
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from create_pin import create_pin
from sticker_info import *
from add_pin import *

locale.setlocale(locale.LC_ALL, '')


def ccao(pin):
    """Navigates to the Cook County Assessor's Office website and performs a
    PIN search for the specified PIN.
    """
    link = "http://www.cookcountyassessor.com/Property.aspx?mode=details&pin="\
        + pin
    browser = webdriver.Chrome()
    browser.get(link)


def bor(pin_segs, zoom=0):
    """Navigates to the Cook County Board of Review website and performs a
    search for the inserted PIN.
    """
    browser = webdriver.Chrome()
    browser.set_window_position(0, 0)
    browser.set_window_size(640, 720)
    browser.get('http://www.cookcountyboardofreview.com/html/decision.php')
    for p in range(5):
        tag = 'PIN' + str(p+1)
        prop = browser.find_element_by_name(tag)
        prop.send_keys(pin_segs[p])
    prop.send_keys(Keys.RETURN)
    code = input('Code: ')
    if code == 'q':
        browser.close()
        return None
    elif len(code) != 6:
        code = input('Try again: ')
    browser.find_element_by_xpath('//*[@id="form_captcha"]/div/div[6]/input').\
        send_keys(code, Keys.RETURN)
    if zoom == 1:
        browser.execute_script("document.body.style.zoom='50%'")
    else:
        browser.execute_script("document.body.style.zoom='100%'")
    return browser


def ptab(dash_pin):
    """Searches the PTAB website with the PIN."""
    browser = webdriver.Chrome()
    browser.get('http://www.ptab.illinois.gov/asi/default.asp')
    browser.find_element_by_xpath('//*[@id="PropPin"]').send_keys(dash_pin,
                                                                  Keys.RETURN)


def court(pin_segs):
    """Searches the Cook County Circuit Court website for the given PIN."""
    browser = webdriver.Chrome()
    browser.set_window_position(0, 0)
    browser.set_window_size(640, 720)                         # This changes based on personal computer screen size.
    browser.get("http://12.218.239.52/V2/COUNTY/Default.aspx")
    browser.find_element_by_id(
        'ctl00_ContentPlaceHolder1_PinSearchLinkButton').click()
    browser.implicitly_wait(30)
    xpath = '//*[@id="ctl00_ContentPlaceHolder1_PinSearch1_PINTextBox'
    for p in range(5):
        px = xpath + str(p + 1) + '"]'
        browser.find_element_by_xpath(px).send_keys(pin_segs[p])
    browser.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_SearchButton"]'
                ).send_keys(Keys.RETURN)


def tax(segs):
    """Performs a search for the PIN at the Cook County Property Tax Portal."""
    link = 'http://cookcountypropertyinfo.com/pinresults.aspx'
    browser = webdriver.Chrome()
    browser.get(link)
    browser.find_element_by_xpath(
        '/html/body/header/div[3]/nav/ul/li[2]/a'
        ).click()
    for p in range(5):
        box = 'pin2Box' + str(1 + p)
        browser.find_element_by_id(box).send_keys(segs[p])
    browser.find_element_by_xpath(
        '//*[@id="PINAddressSearch2_btnPIN2"]'
        ).click()


def delinqs(segs):
    """Searches for tax delinquencies."""
    browser = webdriver.Chrome()
    browser.set_window_position(0, 0)
    browser.set_window_size(640, 680)
    browser.get('http://www.cookcountyclerk.com/tsd/delinquenttaxsearch/Pages/'
                'DelinquentTaxSearch.aspx')
    box_id = 'ctl00_ctl17_g_0686ce41_28c4_4973_9bc4_3fc9c61345ec_ctl00_txtPin'
    for p in range(5):
        box = box_id + str(1 + p)
        browser.find_element_by_id(box).send_keys(segs[p])
 

def collc():
    """Searches for a corporation or LLC with the ilsos.gov Corporate/LLC
    Search feature.
    """
    browser = webdriver.Chrome()
    browser.get('https://www.ilsos.gov/corporatellc/')
    browser.find_element_by_xpath('//*[@id="showButton"]/input').click()
#    name = browser.find_element_by_xpath('//*[@id="searchkeyword"]')
#    name.send_keys(corp, Keys.RETURN)
#    return None


def ccrd(pin_segs):
    """Searches the Cook County Recorder of Deeds database for the given PIN"""
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get("http://162.217.184.82/i2/default.aspx")
    browser.implicitly_wait(30)
    css = '#SearchFormEx1_PINTextBox'
    for p in range(5):
        new_css = css + str(p)
        prop = browser.find_element_by_css_selector(new_css)
        prop.send_keys(pin_segs[p])
    prop.send_keys(Keys.RETURN)


def viewer(pin):
    """Finds the PIN on the Cook Viewer property map."""
    browser = webdriver.Chrome()
    browser.maximize_window()
#    browser.get("http://cookviewer1.cookcountyil.gov/jsviewer/index.html")
    browser.get(
        'http://cookviewer1.cookcountyil.gov/jsviewer/mapviewer.html?search=' +
        pin
        )
    browser.find_element_by_xpath(
        '//*[@id="basemap-btn"]'
        ).send_keys(Keys.RETURN)
    browser.find_element_by_xpath(
        '//*[@id="searchButton"]'
        ).send_keys(Keys.RETURN)
    browser.implicitly_wait(30)
    browser.find_element_by_xpath(
        '//*[@id="galleryNode_aerial"]/a/img'
        ).click()


def buffs(pin, segs):
    """Navigates data.CookCountyAssessor.com to retrieve buff cards for the
    PIN.
    """
    browser = webdriver.Chrome()
#    browser.get('http://data.cookcountyassessor.com/search/')
#    browser.find_element_by_name('NameBox').send_keys(
#        'ntsoni', Keys.TAB, 'ntso4578p', Keys.RETURN
#        )
#    browser.find_element_by_xpath(
#        '//*[@id="AutoNumber88"]/tbody/tr[3]/td/font/a'
#        ).send_keys(Keys.RETURN)
#    browser.find_element_by_name('NameBox').send_keys(
#        'ntsoni', Keys.TAB, 'ntso4578p', Keys.RETURN
#        )
    browser.get(
        'http://data.cookcountyassessor.com/search/viewcard/viewcard.aspx?pin='
        + pin
        )


def maps(address):
    """Finds a streetview on Google Maps if a photo isn't provided."""
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(
        'https://www.google.com/maps/@41.8796305,-87.6396435,529m/\
        data=!3m1!1e3'
        )
    browser.find_element_by_xpath(
        '//*[@id="searchboxinput"]'
        ).send_keys(address, Keys.RETURN)


menu = '-----------------------------------------------------\n\
0: Cook County Assessor       5: Recorder of Deeds\n\
1: Board of Review            6: Corporate LLC Search \n\
2: PTAB                       7: Cook Viewer \n\
3: Circuit Court              8: Buff cards \n\
4: Property Tax Portal        9: Google Maps \n\
-----------------------------------------------------\n\
i: sticker info               d: display PIN \n\
n: new PIN                    a: add new PIN (in file) \n\
q: quit \n\
-----------------------------------------------------'


def options(pin, pin_segs, dash_pin, file=0):
    """
    Display the options to operate on a PIN.

    Parameters
    ----------
    pin : string
        PIN in one string
    pin_segs : list
        PIN divided into its segments
    dash_pin : string
        PIN with dashes dividing segments
    *file : 0 or 1
        1 indicates reading from file for next PIN

    Returns
    -------
    none
    """
    while True:
        print()
        print(menu)
        print()
        choice = input('Choose an option: ')
        if choice == '':
            continue
        if choice in '0123456789':
            choice = float(choice)
        if choice == 0:
            ccao(pin)
        if choice == 1:
            bor(pin_segs)
        if choice == 2:
            ptab(dash_pin)
        if choice == 3:
            court(pin_segs)
        if choice == 4:
            tax(pin_segs)
        if choice == 5:
            ccrd(pin_segs)
        if choice == 6:
            # corp = input('Enter name of corporation or LLC: ')
            collc()
        if choice == 7:
            viewer(pin)
        if choice == 8:
            buffs(pin, pin_segs)
        if choice == 9:
            address = input('Please enter the address: ')
            maps(address)
        if choice == 'i':
            print()
            print('===================================')
            ao_info(pin, 1)
            print('===================================')
        if choice == 'n':
            if file == 1:
                return None
            else:
                new_pin = create_pin()
                pin_segs = new_pin[0]
                dash_pin = new_pin[1]
                pin = new_pin[2]
        if choice == 'd':
            print()
            print(dash_pin)
        if choice == 'q':
            if file == 1:
                sys.exit('Search ended.')
            else:
                return None
        if choice == 'a':
            # new_pin = create_pin()
            # pin_segs = new_pin[0]
            # dash_pin = new_pin[1]
            # npin = new_pin[2]

            # The following code adds up the AV, MV, & taxes for multiple PINs
            n = int(input('How many additional PINs in parcel? '))
            print(dash_pin)
            bav = ao_info(pin, 0, 1)[0]
            bmv = ao_info(pin, 0, 1)[1]
            comb = add_mult(n, bav, bmv)
            tot_av = locale.currency(comb[0], grouping=True)
            tot_mv = locale.currency(comb[1], grouping=True)
 
            sqft = int(input('Square feet: '))
            psf = comb[1]/sqft
            price = locale.currency(psf, grouping=True)

            print()
            print('================================')
            print('Combined AV:', tot_av)
            print('Combined MV:', tot_mv)
            print()
            print(price + '/SF')
