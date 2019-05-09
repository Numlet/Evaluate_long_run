#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 16:40:32 2018

@author: jvergara
"""

import sys
print (sys.argv)
import glob
import os
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
from define_parameters import years, run_path

path=run_path

if path[-1]!='/':path+'/'
folders=glob.glob(path+'*')
folders=[f for f in folders if f[-2:]!='nc']
already_calculated=[folder for folder in folders if folder[-2:]=='mm']
folders=[f for f in folders if f[-2:]!='mm']
folders=[f for f in folders if os.path.isdir(f)]
print(folders)
for folder in folders:
#    if folder[:-2]=='nc':continue
    print (folder)

    bottom_folder='/'.join(folder.split('/')[:-1])
    print(bottom_folder)
    os.chdir(bottom_folder)
    folder_name=folder.split('/')[-1]
    jle.Create_folder(folder_name+'_mm')

    os.chdir(folder)
    for year in years:    
        for month in jle.months_number_str:
#        print(month)
#        files_in_month=glob.glob('lffd'+year+month+'*')
            print(folder)
            files=glob.glob('lffd'+year+month+'????????.nc')
#        print(files)
            nfiles=len(files)
            days=jle.Days_in_month(year,month)
            if int(nfiles)/int(days) not in [24, 8, 4, 1 ]: 
                print(nfiles, 'not all files encounter for month:',month)
                continue
            cmd='cdo ensmean '+'lffd'+year+month+'????????.nc '+'../'+folder_name+'_mm/lffd'+year+month+'.nc'
            print (cmd)
            if os.path.isfile('../'+folder_name+'_mm/lffd'+year+month+'.nc'):
                print('../'+folder_name+'_mm/lffd'+year+month+'.nc ||| already exists, skipping' )
                continue
            else:
                print (cmd)
                os.system(cmd)
        
        for i in range(len(jle.seasons)):
            print (jle.seasons[i])
            months=[jle.months_number_str[ind] for ind in jle.season_indexes[i]]
            ds1='../'+folder_name+'_mm/lffd'+year+months[0]+'.nc'
            ds2='../'+folder_name+'_mm/lffd'+year+months[1]+'.nc'
            ds3='../'+folder_name+'_mm/lffd'+year+months[2]+'.nc'
            cmd='cdo ensmean '+ds1+' '+ds2+' '+ds3+' '+'../'+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc'
            if os.path.isfile('../'+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc'):
                print('../'+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc ||| already exists, skipping' )
                continue
            else:
                print (cmd)
                os.system(cmd)




#    for month in jle.months_number_str:
##        print(month)
##        files_in_month=glob.glob('lffd'+year+month+'*')
#        cmd='cdo ensmean '+'lffd'+year+month+'*  '+'../'+folder_name+'_mm/lffd'+year+month+'.nc'
#        print (cmd)
#        os.system(cmd)


#dict_files={}
#for file in files_in_month:
#    dict_files[file]=file
#array=jle.nc_variable_time_agregate(dict_files,'TQV',printing=1)
