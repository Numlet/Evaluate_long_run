#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 13:15:34 2018

@author: jvergara
"""

import sys
sys.path.append('/users/jvergara/python_code')
#import matplotlib
#matplotlib.use('Agg')
import Jesuslib_eth as jle
import numpy as np
import matplotlib.pyplot as plt
import glob
from netCDF4 import Dataset
import time
import os
import matplotlib.animation as manimation
from pympler import muppy
all_objects = muppy.get_objects()
from pympler import summary
import pickle
import scipy

from define_parameters import pspc_data_folder, output_path

pspc_data_folder='/store/c2sm/pr04/jvergara/postprocessing_data/'

output_path='/store/c2sm/pr04/jvergara/TEMP_REGRID/'
os.chdir(output_path)
year='2006'





#%%

for i in range(12):
    print(jle.months_number_str[i])
    print(jle.month_names[i])
    os.system('rm lffd%s%s_%s*'%(year,jle.months_number_str[i],jle.month_names[i]))
    os.system('ncrcat lffd%s%s* lffd%s%s_%s.nc'%(year,jle.months_number_str[i],year,jle.months_number_str[i],jle.month_names[i]))
    
