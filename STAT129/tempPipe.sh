#!/bin/bash

time ls /stat129/*.gz | parallel 'zgrep -E "AGE00147708|AGE00147719|UZM00038457|USW00094967|USW00094728" {} | zgrep "TMAX" | cut -d"," -f 1,2,4 | python3 tempTmax2Tavg.py'
