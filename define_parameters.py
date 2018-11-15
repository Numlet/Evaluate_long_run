import sys
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import glob


pspc_data_folder='/store/c2sm/pr04/jvergara/postprocessing_data/'

#name='GA_run'

name='namelist_testing_1'
run_path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/namelist_test_v1/lm_f/'

#run_path='/project/pr04/davidle/results_clim/lm_c/'
#run_path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/0.11_DEEP/lm_c/'
#run_path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/GA_fine_spinup_and_evaluation/lm_f/'
folder_in_path='1h_second/'
output_path='/store/c2sm/pr04/jvergara/CMSAF_evaluation/'+name+'/'
jle.Create_folder(output_path)

native_grid_file=pspc_data_folder+'CLM_lm_c_grid.txt'
native_grid_file=pspc_data_folder+'CLM_lm_0.11_conv_on_off.txt'
native_grid_file=pspc_data_folder+'CLM_lm_f_GA.txt'
target_grid_file=pspc_data_folder+'Satellite_CMSAF_grid.txt'
grid_cmsaf=pspc_data_folder+'Satellite_CMSAF_grid.txt'
grid_eobs=pspc_data_folder+'e-obs_rr_9_grid.txt'

mask_relaxation_zone=np.load('/store/c2sm/pr04/jvergara/CONV_ON_OFF/eobs_mask_relaxation_zone.npy')

sample_nc_path=glob.glob(run_path+'1h/'+'*')[0]

apply_rz_mask=0
year='2000'

plots_folder='/users/jvergara/evaluation_CMSAF/'+name+'/'

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
