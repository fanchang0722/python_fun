#!/bin/sh
SN=`adb devices |cut -d' ' -f2 |cut -d' ' -f1`
echo $SN
