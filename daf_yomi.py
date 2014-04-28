#! /usr/bin/env python

"""
Python code for performing calculations related to Daf Yomi

Designed for Python 2

Written by Moshe Kaplan on 2014-04-28
"""

import datetime
import collections

# Raw data
MESECHTOS_BLATT = collections.OrderedDict([
    ('Berachos', 63),
    ('Shabbos', 156),
    ('Eruvin', 104),
    ('Pesachim', 120),
    ('Shekalim', 21),
    ('Yoma', 87),
    ('Succah', 55),
    ('Beitzah', 39),
    ('Rosh Hashanah', 34),
    ('Taanis', 30),
    ('Megillah', 31),
    ('Moed Katan', 28),
    ('Chagigah', 26),
    ('Yevamos', 121),
    ('Kesubos', 111),
    ('Nedarim', 90),
    ('Nazir', 65),
    ('Sotah', 48),
    ('Gittin', 89),
    ('Kiddushin', 81),
    ('Bava Kamma', 118),
    ('Bava Metzia', 118),
    ('Bava Basra', 175),
    ('Sanhedrin', 112),
    ('Makkos', 23),
    ('Shevuos', 48),
    ('Avodah Zarah', 75),
    ('Horayos', 13),
    ('Zevachim', 119),
    ('Menachos', 109),
    ('Chullin', 141),
    ('Bechoros', 60),
    ('Arachin', 33),
    ('Temurah', 33),
    ('Kereisos', 27),
    ('Meilah', 36),
    ('Niddah', 72)])

TOTAL_BLATT = sum(MESECHTOS_BLATT.values())

# The first few cycles were only 2702 blatt. After that it became 2711. Even with
# that, the math doesn't play nicely with the dates before the 11th cycle :(
# From Cycle 11 onwards, it was simple and sequential
CYCLE_11_START = datetime.date(1997, 9, 29)

###############################################################################
# Conversion functions
###############################################################################

def date_to_number(date):
    """Turns a date into a number representing the daf"""
    days_since_start = (date - CYCLE_11_START).days
    if days_since_start < 0:
        raise Exception("This calculator only goes back to cycle 11 (1997-09-29)")
    return days_since_start % (TOTAL_BLATT)

def number_to_daf(number):
    """Turns the number representing the daf into the day's daf"""
    
    # Store the value in case of an error
    original_number = number
    
    if number < 0:
        raise Exception("Invalid number %d is <= 0" % original_number)

    number = number % (TOTAL_BLATT)
    
    for mesechta, blatt in MESECHTOS_BLATT.items():
        if number >= blatt:
            number -= blatt
        else:
            return mesechta, number + 2
    else:
        raise Exception("It somehow couldn't find the blatt for number=%d ?" % original_number)
        
def dafstring_to_number(dafstring):
    """Takes a string in "Mesechta blatt" format and converts it to a number"""
    mesechta, blatt = dafstring.rsplit(' ', 1)
    number = 0
    # TODO: Come up with better variable names than k,v
    for k, v in MESECHTOS_BLATT.items():
        if mesechta.lower() == k.lower():
            number += int(blatt) - 2
            return number
        else:
            number += v
    else:
        raise Exception("Dafstring '%s' is not a known mesechta!" % dafstring)
    
###############################################################################
# Utility functions
###############################################################################

def daf_for_date(date):
    """Calculates the daf for a given datetime.date"""
    number = date_to_number(date)
    todays_mesachta, todays_daf = number_to_daf(number)
    return todays_mesachta, todays_daf

def todays_daf():
    """Determines today's daf"""
    return daf_for_date(datetime.date.today())

def how_far_behind(current_position):
    """Calculates how many blatt behind you are. Only operates within a single cycle"""
    current_number = dafstring_to_number(current_position)
    world_number = date_to_number(datetime.date.today())
    return world_number - current_number

def blatt_per_day_to_catch_up(current_position, end_date):
    """Calculates how many blatt you need to do each day to catch up by end_date"""
    remaining_blatt = how_far_behind(current_position)
    remaining_days = (end_date - datetime.date.today()).days
    return remaining_blatt*1.0/remaining_days

def catch_up_by(current_position, blatt_per_day):
    """Calculates when you'll catch up by, given a pace"""
    remaining_blatt = how_far_behind(current_position)
    surplus = blatt_per_day - 1
    days = remaining_blatt/surplus
    return datetime.date.today() + datetime.timedelta(days)

# Test code:
def run_tests():
    if number_to_daf(0) != (MESECHTOS_BLATT.keys()[0], 2):
        raise Exception("Day 0 is Brachos!")

    if number_to_daf(63) != (MESECHTOS_BLATT.keys()[1], 2):
        raise Exception("Day 63 is Shabbos!")
    
    # Daf for generic date
    if daf_for_date(datetime.date(2014, 4, 28)) != ('Beitzah', 29):
        raise Exception("Generic date test failed!")
        
    # Text to number
    initial_number = 500
    dafstring = "%s %d" % number_to_daf(initial_number)
    number = dafstring_to_number(dafstring)
    if number != initial_number :
        raise Exception("Text to number failed! initial_number=%d, dafstring=%s, result=%d"
            % initial_number, dafstring, number)

run_tests()
print todays_daf()
print catch_up_by("Beitzah 17", 2)
