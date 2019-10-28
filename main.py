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
parser.set_defaults(yesterday=True)
args = parser.parse_args()

date = datetime.datetime.now()
if args.yesterday:
    date -= datetime.timedelta(days=1)

app = application.Application()
app.run(date=date)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
