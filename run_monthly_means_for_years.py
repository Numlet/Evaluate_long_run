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
from define_parameters import years, run_path, original_files

path=original_files
saving_path=run_path
print(path)
print(saving_path)
if path[-1]!='/':path+'/'
folders=glob.glob(path+'*')
folders=[f for f in folders if f[-2:]!='nc']
already_calculated=[folder for folder in folders if folder[-2:]=='mm']
folders=[f for f in folders if f[-2:]!='mm']
folders=[f for f in folders if os.path.isdir(f)]
print(folders)

for folder in folders:
    print (folder)
    if 'restart' in folder:continue
    bottom_folder='/'.join(folder.split('/')[:-1])
    print(bottom_folder)
    os.chdir(bottom_folder)
    folder_name=folder.split('/')[-1]
    print(folder_name)
    jle.Create_folder(saving_path+folder_name+'_mm')
    for year in years:    
        print(folder+'/'+year)
        os.chdir(folder+'/'+year)
        for month in jle.months_number_str:
            print(folder)
            files=glob.glob('lffd'+year+month+'????.nc')
            nfiles=len(files)
            days=jle.Days_in_month(year,month)
            if int(nfiles)/int(days) not in [24, 8, 4, 1 ]: 
                print(nfiles, 'not all files encounter for month:',month)
                continue
            cmd='cdo ensmean '+'lffd'+year+month+'????.nc '+saving_path+folder_name+'_mm/lffd'+year+month+'.nc'
            print (cmd)
            if os.path.isfile(saving_path+folder_name+'_mm/lffd'+year+month+'.nc'):
                print(saving_path+folder_name+'_mm/lffd'+year+month+'.nc ||| already exists, skipping' )
                continue
            else:
                print (cmd)
                a=os.system(cmd)
        for i in range(len(jle.seasons)):
            print (jle.seasons[i])
            months=[jle.months_number_str[ind] for ind in jle.season_indexes[i]]
            ds1=saving_path+folder_name+'_mm/lffd'+year+months[0]+'.nc'
            ds2=saving_path+folder_name+'_mm/lffd'+year+months[1]+'.nc'
            ds3=saving_path+folder_name+'_mm/lffd'+year+months[2]+'.nc'
            cmd='cdo ensmean '+ds1+' '+ds2+' '+ds3+' '+saving_path+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc'
            if os.path.isfile(saving_path+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc'):
                print(saving_path+folder_name+'_mm/lffd'+year+'_'+jle.seasons[i]+'.nc ||| already exists, skipping' )
                continue
            else:
                print (cmd)
                a=os.system(cmd)




