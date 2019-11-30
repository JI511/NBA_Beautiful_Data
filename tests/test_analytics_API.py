# ----------------------------------------------------------------------------------------------------------------------
#    Analytics API tests
# ----------------------------------------------------------------------------------------------------------------------

# imports
import unittest
import tempfile
import os
import shutil
import logging
import datetime

from analytics import analytics_API as Api
from basketball_reference_web_scraper.data import Team


class TestAnalyticsApi(unittest.TestCase):
    """
    Test functions for the Analytics API functions.
    """
    def setUp(self):
        """
        Initialize test specific variables.
        """
        self.logger = logging.getLogger(__name__)
        self.logs_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Performs any necessary clean up.
        """
        if os.path.exists(self.logs_dir):
            shutil.rmtree(self.logs_dir)

    # ------------------------------------------------------------------------------------------------------------------
    # get_player_box_score tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_get_player_box_score_nominal(self):
        """
        The function `get_player_box_score` shall build a player box score date when given a date that the desired
        player played on.
        """
        test_date = datetime.datetime(year=2019, month=10, day=22)
        bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
                                            date_obj=test_date)
        self.assertEqual(bs['name'], 'LeBron James')
        self.assertEqual(bs['team'].name, 'LOS_ANGELES_LAKERS')
        self.assertEqual([date.day, date.month, date.year], [test_date.day, test_date.month, test_date.year])

    def test_get_player_box_score_cycle_date(self):
        """
        The function `get_player_box_score` shall iterate over 3 decreasing dates by default to find the player box
        score if the date provided does not yield a result.
        """
        test_date = datetime.datetime(year=2019, month=10, day=23)
        bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
                                            date_obj=test_date)
        self.assertEqual(bs['name'], 'LeBron James')
        self.assertEqual(bs['team'].name, 'LOS_ANGELES_LAKERS')
        self.assertEqual([date.day, date.month, date.year], [test_date.day - 1, test_date.month, test_date.year])

    def test_get_player_box_score_not_found(self):
        """
        The function `get_player_box_score` shall return None if the player box score data is not found.
        """
        test_date = datetime.datetime(year=2019, month=10, day=21)
        bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
                                            date_obj=test_date)
        self.assertEqual(bs, None)

    # ------------------------------------------------------------------------------------------------------------------
    # get_team_box_score tests
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # get_daily_box_scores tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_get_daily_box_scores_nominal(self):
        """
        The function `get_daily_box_scores` shall get all player box scores for a specified day grouped by team.
        """
        test_date = datetime.datetime(year=2019, month=10, day=22)
        team_dict, date = Api.get_daily_box_scores(date_obj=test_date)
        keys = [key for key in team_dict.keys()]
        self.assertEqual(keys, ['LOS_ANGELES_LAKERS', 'LOS_ANGELES_CLIPPERS',
                         'NEW_ORLEANS_PELICANS', 'TORONTO_RAPTORS'])
        self.assertEqual(len(team_dict[keys[0]]), 10)
        self.assertEqual([date.day, date.month, date.year], [test_date.day, test_date.month, test_date.year])

    # ------------------------------------------------------------------------------------------------------------------
    # get_assist_turnover_ratio tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_get_assist_turnover_ratio_nominal(self):
        """
        The function `get_assist_turnover_ratio` shall calculate the ratio given nominal data
        """
        assists = 10
        turnovers = 5
        self.assertEqual(2.0, Api.get_assist_turnover_ratio(assists, turnovers))
        assists = 8
        self.assertEqual(1.6, Api.get_assist_turnover_ratio(assists, turnovers))

    def test_get_assist_turnover_ratio_zero_turnovers(self):
        """
        The function `get_assist_turnover_ratio` shall return the number of assists if the number of turnovers is 0.
        """
        assists = 10
        turnovers = 0
        self.assertEqual(10.0, Api.get_assist_turnover_ratio(assists, turnovers))

    # ------------------------------------------------------------------------------------------------------------------
    # get_team_date_df tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_get_team_date_nominal(self):
        """
        The function `get_team_date` shall retrieve a pandas.DataFrame object containing the player box score
        information of a given day and team.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        team_df = Api.get_team_date_df(df, 'CHICAGO_BULLS', datetime.datetime(day=23, month=10, year=1996))
        self.assertEqual(team_df.shape[0], 0)
        team_df = Api.get_team_date_df(df, 'CHICAGO_BULLS', datetime.datetime(day=22, month=10, year=1996))
        self.assertEqual(team_df.shape[0], 1)

    # ------------------------------------------------------------------------------------------------------------------
    # create_scatter_plot_with_trend_line tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_create_scatter_plot_with_trend_line_nominal(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                            y_key='points',
                                                            df=df,
                                                            save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_outliers(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                            y_key='points',
                                                            df=df,
                                                            outliers=5,
                                                            save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_no_grid(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot without using a grid.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                            y_key='points',
                                                            df=df,
                                                            grid=False,
                                                            save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    # ------------------------------------------------------------------------------------------------------------------
    # create_bar_plot tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_create_bar_plot_nominal(self):
        """
        The function `create_bar_plot` shall create and save a bar plot.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path = Api.create_bar_plot(df, ['points', 'rebounds'], save_path=self.logs_dir,
                                        team=Team.LOS_ANGELES_LAKERS.name,
                                        date=datetime.datetime(day=22, month=10, year=2019))
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_bar_plot_one_column(self):
        """
        The function `create_bar_plot` shall create and save a bar plot when only one column is provided.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path = Api.create_bar_plot(df, ['points'], save_path=self.logs_dir,
                                        team=Team.LOS_ANGELES_LAKERS.name,
                                        date=datetime.datetime(day=22, month=10, year=2019))
        self.assertTrue(os.path.exists('%s.png' % plot_path))

# ----------------------------------------------------------------------------------------------------------------------
#    End
# ----------------------------------------------------------------------------------------------------------------------
