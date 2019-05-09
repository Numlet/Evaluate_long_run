import sys
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import glob


pspc_data_folder='/store/c2sm/pr04/jvergara/postprocessing_data/'

#name='GA_fine_spinup_and_evaluation'


#######MODIFY THIS PART#############
name='GA_fine_ERA'
run_path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/'+name+'/lm_f/'

years=['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009']


folder_in_path='1h_second/'
output_path='/store/c2sm/pr04/jvergara/CMSAF_evaluation/'+name+'/'
jle.Create_folder(output_path)

native_grid_file=pspc_data_folder+'CLM_lm_f_GA.txt'

grid_cmsaf=pspc_data_folder+'Satellite_CMSAF_grid.txt'

grid_eobs=pspc_data_folder+'e-obs_rr_9_grid.txt'
target_grid_file=pspc_data_folder+'e-obs_rr_9_grid.txt'

grid_meteoswiss_1k='/store/c2sm/pr04/jvergara/RdisaggH_grid.txt'

mask_relaxation_zone=np.load('/store/c2sm/pr04/jvergara/CONV_ON_OFF/eobs_mask_relaxation_zone.npy')


apply_rz_mask=0
#############UNTIL HERE################
plots_folder='/users/jvergara/long_runs_evaluation/'+name+'/'

jle.Create_folder(plots_folder)


def initial_final_day_index_EOBS(year,month,n_months=1):
    d0=datetime.datetime(1950,1,1)
    ds=datetime.datetime(int(year),int(month),1)
    de=ds+relativedelta(months=n_months)
    return (ds-d0).days, (de-d0).days


import matplotlib as mpl

mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['font.size'] = 20
mpl.rcParams['legend.fontsize']= 15
mpl.rcParams['legend.frameon'] = 'False'
