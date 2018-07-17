import sys
sys.path.append('/users/jvergara/python_code')
import Jesuslib_eth as jle
import datetime
from dateutil.relativedelta import relativedelta


pspc_data_folder='/store/c2sm/pr04/jvergara/postprocessing_data/'

run_path='/project/pr04/davidle/results_clim/lm_c/'
run_path='/store/c2sm/pr04/jvergara/RUNS_IN_SCRATCH/0.11_DEEP/lm_c/'
folder_in_path='1h/'
output_path='/store/c2sm/pr04/jvergara/EOBS_CONV_ON_OFF/0.11_DEEP/'
jle.Create_folder(output_path)

native_grid_file=pspc_data_folder+'CLM_lm_c_grid.txt'
native_grid_file=pspc_data_folder+'CLM_lm_0.11_conv_on_off.txt'
target_grid_file=pspc_data_folder+'e-obs_rr_9_grid.txt'


year='2006'

plots_folder='/users/jvergara/evaluation_eobs/0.11_DEEP/'

jle.Create_folder(plots_folder)


def initial_final_day_index_EOBS(year,month,n_months=1):
    d0=datetime.datetime(1950,1,1)
    ds=datetime.datetime(int(year),int(month),1)
    de=ds+relativedelta(months=n_months)
    return (ds-d0).days, (de-d0).days
