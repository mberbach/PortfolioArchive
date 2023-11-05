#!/bin/bash

time ls /stat129/download990xml_20*.zip | parallel 'python3 noProfit129v4ser.py {}' > serOutTes.csv
