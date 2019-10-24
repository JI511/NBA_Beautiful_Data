# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
import analytics_API as Api
from box_score import BoxScore
from team_box_score import TeamBoxScore


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
        date = datetime.datetime(year=2019, month=10, day=22)

        box_score = BoxScore(Api.get_player_box_score(name=self.player, date_obj=date))
        print(box_score.to_string())
        team_box_scores = TeamBoxScore(Api.get_daily_box_scores(date_obj=date)[Team.LOS_ANGELES_LAKERS.name], )
        print(team_box_scores.to_string())


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
