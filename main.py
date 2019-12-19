# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

# imports
from analytics import application
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--yesterday', help='The date to search will be the previous day.',
                    dest='yesterday', action='store_true')
parser.add_argument('--log', help='(bool) Indicates if logging/log file should be used.',
                    dest='log', action='store_true')
parser.add_argument('--plot', help='(bool) Indicates if plots should be created.',
                    dest='plot', action='store_true')
parser.add_argument('--gather_new', help='(bool) Indicates if new player box score data should be searched for.',
                    dest='gather_new', action='store_true')
parser.add_argument('--with_date_range', help='Create a csv from a date range. format: start*end, y_m_d*y_m_d.',
                    dest='date_range')
parser.add_argument('--update_to_current', help='Update up to today\'s date from the last collected date.',
                    dest='update_to_current', action='store_true')
parser.set_defaults(yesterday=False, log=False, plot=False, gather_new=False, date_range='', update_to_current=True)
args = parser.parse_args()

date = datetime.datetime.now()
if args.yesterday:
    date -= datetime.timedelta(days=1)

app = application.Application()
if args.date_range == '':
    gather_new = args.gather_new
    if args.update_to_current:
        gather_new = 'update_to_current'
    app.run(date=date, should_log=args.log, plot=args.plot, gather_new=gather_new)
else:
    dates = args.date_range.split('*')
    app.run_with_date_range(start_date=dates[0], end_date=dates[1])


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
