#!/usr/bin/env python

import daf_yomi

import datetime
mesechta, daf = daf_yomi.todays_daf()

todays_date = datetime.datetime.today().date().strftime("%A, %B %d, %Y")
msg =  "The daf for %s is mesechtas %s, daf %s" % (todays_date,mesechta,daf)

print (msg)
