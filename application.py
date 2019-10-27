# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import os
import pandas as pd
import analytics_API as Api
from box_score import BoxScore
from constants import Vars
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
        # print("The Latest box score for Lebron James")
        # date = datetime.datetime.today()
        date = datetime.datetime(year=2019, month=10, day=25)

        # box_score = BoxScore(Api.get_player_box_score(name=self.player, date_obj=date))
        # print(box_score.to_string())

        team_box_scores = []
        data = {}
        for stat in Vars.supported_stats:
            data[stat] = []
        daily_box_scores, found_date = Api.get_daily_box_scores(date_obj=date)
        for team in daily_box_scores.keys():
            team_box_scores.append(TeamBoxScore(box_scores=daily_box_scores[team],
                                                team_box_score=[],
                                                team_name=team,
                                                date=found_date))
            # team_box_scores[-1].create_points_graph()
            # break
        for tbs in team_box_scores:
            print('T')
            data['player_name'].extend(tbs.get_players())
            data['points'].extend(tbs.get_points())
            data['rebounds'].extend(tbs.get_rebounds())
            data['assists'].extend(tbs.get_assists())
            data['made_field_goals'].extend(tbs.get_made_field_goals())
            data['made_three_point_field_goals'].extend(tbs.get_made_three_point_field_goals())
            data['made_free_throws'].extend(tbs.get_made_free_throws())
            data['offensive_rebounds'].extend(tbs.get_offensive_rebounds())
            data['defensive_rebounds'].extend(tbs.get_defensive_rebounds())
            data['team'].extend(tbs.get_teams())
            data['date'].extend(tbs.get_dates())

        # print(data)
        df = pd.DataFrame(data)
        # if not os.path.exists('test.csv'):
        df.to_csv('test.csv')


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
