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

        # temp_bs, fd = Api.get_player_box_score(name=self.player, date_obj=date)
        # box_score = BoxScore(temp_bs, fd)
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
        for tbs in team_box_scores:
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
            data['location'].extend(tbs.get_locations())
            data['opponent'].extend(tbs.get_opponents())
            data['outcome'].extend(tbs.get_outcomes())
            data['seconds_played'].extend(tbs.get_seconds_played())
            data['attempted_three_point_field_goals'].extend(tbs.get_attempted_three_point_field_goals())
            data['attempted_free_throws'].extend(tbs.get_attempted_free_throws())
            data['attempted_field_goals'].extend(tbs.get_attempted_field_goals())
            data['steals'].extend(tbs.get_steals())
            data['blocks'].extend(tbs.get_blocks())
            data['turnovers'].extend(tbs.get_turnovers())
            data['personal_fouls'].extend(tbs.get_personal_fouls())
            data['game_score'].extend(tbs.get_game_scores())
            data['date'].extend(tbs.get_dates())

        # print(data)
        df = pd.DataFrame(data)
        df.to_csv('test.csv')


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
