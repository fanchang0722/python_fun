#!/bin/bash
adb pull /data/user/Image-video0-3264x2448-0.yuv $1
avconv -s 3264x2448 -pix_fmt nv12 -i $1 -pix_fmt rgb24 $2
