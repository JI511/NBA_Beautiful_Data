# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team


class Application(object):
    """
    This class handles running the application
    """
    def __init__(self):
        """
        Setup for the application.
        """
        self.player = 'LeBron James'

    def run(self):
        """
        Runs the application.
        """
        print("The Latest box score for Lebron James")
        date = datetime.datetime.today()
        date = datetime.datetime(year=2019, month=4, day=4)
        while True:
            print('Attempting date: %s' % date.strftime('%y-%m-%d'))
            if self.get_box_score(day=date.day, month=date.month, year=date.year):
                break
            date -= datetime.timedelta(days=1)

    def get_box_score(self, day, month, year):
        found = False
        box_scores = client.player_box_scores(day=day, month=month, year=year)
        print('Total players on this date: %s' % len(box_scores))
        for box_score in box_scores:
            # print(box_score)
            if self.player in box_score['name']:
                print(box_score)
                found = True
                break
        return found

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
