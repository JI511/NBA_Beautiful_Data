# ----------------------------------------------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------------------------------------------

# imports
import application
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--yesterday', help='The date to search will be the previous day.',
                    dest='yesterday', action='store_true')
parser.add_argument('--log', help='Indicates if logging/log file should be used.',
                    dest='log', action='store_true')
parser.add_argument('--plot', help='Indicates if plots should be created.',
                    dest='plot', action='store_true')
parser.add_argument('--gather_new', help='Indicates if new player box score data should be searched for.',
                    dest='gather_new', action='store_true')
parser.set_defaults(yesterday=False, log=False, plot=False, gather_new=False)
args = parser.parse_args()

date = datetime.datetime.now()
if args.yesterday:
    date -= datetime.timedelta(days=1)
else:
    date = False

app = application.Application()
app.run(date=date, should_log=args.log, plot=args.plot, gather_new=args.gather_new)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
