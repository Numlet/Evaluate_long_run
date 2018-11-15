import os
from define_parameters import *

a=os.system('python /users/jvergara/python_code/Calculate_monthly_means/run_monthly_means.py %s %s '%(run_path, year))
print('Monthly means created')


b=os.system('python regrid_run.py CMSAF')
print('Run regrided to CMSAF')

c=os.system('python evaluate_CMSAF.py')
print('CMSAF Finished')
if not a and not b and not c:
    print('SUCCESFULLY! (maybe)')

print('Starting with EOBS')
#b=os.system('python regrid_run.py EOBS')
print('Run regrided to EOBS')

#python eobs_evaluation_monthly.py
#python eobs_evaluation_seasons.py
