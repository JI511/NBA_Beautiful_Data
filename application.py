# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
import analytics_API as api
from box_score import BoxScore


class Application(object):
    """
    This class handles running the application
    """
    def __init__(self):
        """
        Setup for the application.
        """
        self.player = 'LeBron James'.lower()

    def run(self):
        """
        Runs the application.
        """
        print("The Latest box score for Lebron James")
        # date = datetime.datetime.today()
        date = datetime.datetime(year=2019, month=3, day=29)
        box_score = BoxScore(api.get_play_box_score(name=self.player, date_obj=date))
        print(box_score.to_string())



# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
