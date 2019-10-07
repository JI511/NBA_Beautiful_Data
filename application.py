# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
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
        pass

    def run(self):
        """
        Runs the application.
        """
        self.get_box_score()

    def get_box_score(self):
        box_scores = client.player_box_scores(day=13, month=6, year=2019)
        print('***** BOX SCORES *****')
        for box_score in box_scores[:10]:
            print(box_score)

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
