# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import os
import pandas as pd
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
        date = datetime.datetime(year=2019, month=10, day=25)

        # box_score = BoxScore(Api.get_player_box_score(name=self.player, date_obj=date))
        # print(box_score.to_string())

        team_box_scores = []
        daily_box_scores, found_date = Api.get_daily_box_scores(date_obj=date)
        for team in daily_box_scores.keys():
            team_box_scores.append(
                TeamBoxScore(box_scores=daily_box_scores[team],
                             team_box_score=[],
                             team_name=team,
                             date=found_date))
            # print(team_box_scores[-1].to_string())
            team_box_scores[-1].create_points_graph()
            break
        data = {
            'player_name': team_box_scores[-1].get_players(),
            'points': team_box_scores[-1].get_points(),
            'rebounds': team_box_scores[-1].get_rebounds()
        }
        print(data)
        df = pd.DataFrame(data)
        if not os.path.exists('test.csv'):
            df.to_csv('test.csv')


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
