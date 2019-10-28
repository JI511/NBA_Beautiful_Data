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

    def run(self, date=None):
        """
        Runs the application.

        :param datetime.datetime date: The date to attempt searching.
        """
        # todo create logger
        if date is None:
            date = datetime.datetime.today()

        # temp_bs, fd = Api.get_player_box_score(name=self.player, date_obj=date)
        # box_score = BoxScore(temp_bs, fd)
        # print(box_score.to_string())

        team_box_scores = []

        daily_box_scores, found_date = Api.get_daily_box_scores(date_obj=date)
        for team in daily_box_scores.keys():
            team_box_scores.append(TeamBoxScore(box_scores=daily_box_scores[team],
                                                team_box_score=[],
                                                team_name=team,
                                                date=found_date))
            # team_box_scores[-1].create_points_graph()

        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv)
        new_df = Api.create_data_frame_from_team_box_scores(team_box_scores=team_box_scores)
        if df is None:
            print('There was not an existing data frame.')
            df = new_df
        else:
            print('Appending new data frame.')
            temp_df = df.append(new_df, sort=False)
            temp_df.drop_duplicates(inplace=True)
            df = temp_df
            print(df.shape)
        df.to_csv(my_csv)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
