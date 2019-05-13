import os
from define_parameters import *

a=os.system('python run_monthly_means_for_years.py')
print('Monthly means created')


b=os.system('python regrid_run.py CMSAF')
print('Run regrided to CMSAF')

c=os.system('python evaluate_CMSAF.py')
print('CMSAF Finished')
if not a and not b and not c:
    print('SUCCESFULLY! (maybe)')

print('Starting with EOBS')
b=os.system('python regrid_run.py EOBS')
print('Run regrided to EOBS')
b=os.system('python evaluate_EOBS.py')

print('Metoswiss evaluation')
b=os.system('python regrid_run.py meteoswiss_1k')
print('Run regrided to meteoswiss_1k')
b=os.system('python evaluate_meteoswiss_1k.py')

#python eobs_evaluation_monthly.py
#python eobs_evaluation_seasons.py
