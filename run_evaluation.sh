python regrid_run.py
echo 'end of regrid step'
python monthly_concatenation.py
echo 'end of concatenation. Starting with plots'
python eobs_evaluation_monthly.py
python eobs_evaluation_seasons.py
