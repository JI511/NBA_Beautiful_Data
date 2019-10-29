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
parser.set_defaults(yesterday=False, log=False)
args = parser.parse_args()

date = datetime.datetime.now()
if args.yesterday:
    date -= datetime.timedelta(days=1)

app = application.Application()
app.run(date=date)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
