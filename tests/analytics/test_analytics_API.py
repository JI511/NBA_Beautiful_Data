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
import sys
sys.path.append(os.getcwd())  # this was needed to run the coverage library outside of pycharm
# third party imports
from basketball_reference_web_scraper.data import Team
# relative imports
from src import analytics_API as Api


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
    # def test_get_player_box_score_nominal(self):
    #     """
    #     The function `get_player_box_score` shall build a player box score date when given a date that the desired
    #     player played on.
    #     """
    #     test_date = datetime.datetime(year=2019, month=10, day=22)
    #     bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
    #                                         date_obj=test_date)
    #     self.assertEqual(bs['name'], 'LeBron James')
    #     self.assertEqual(bs['team'].name, 'LOS_ANGELES_LAKERS')
    #     self.assertEqual([date.day, date.month, date.year], [test_date.day, test_date.month, test_date.year])
    #
    # def test_get_player_box_score_cycle_date(self):
    #     """
    #     The function `get_player_box_score` shall iterate over 3 decreasing dates by default to find the player box
    #     score if the date provided does not yield a result.
    #     """
    #     test_date = datetime.datetime(year=2019, month=10, day=23)
    #     bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
    #                                         date_obj=test_date)
    #     self.assertEqual(bs['name'], 'LeBron James')
    #     self.assertEqual(bs['team'].name, 'LOS_ANGELES_LAKERS')
    #     self.assertEqual([date.day, date.month, date.year], [test_date.day - 1, test_date.month, test_date.year])
    #
    # def test_get_player_box_score_not_found(self):
    #     """
    #     The function `get_player_box_score` shall return None if the player box score data is not found.
    #     """
    #     test_date = datetime.datetime(year=2019, month=10, day=21)
    #     bs, date = Api.get_player_box_score(name='LeBron James', logger=self.logger,
    #                                         date_obj=test_date)
    #     self.assertEqual(bs, None)

    # ------------------------------------------------------------------------------------------------------------------
    # get_team_box_score tests
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # get_daily_box_scores tests
    # ------------------------------------------------------------------------------------------------------------------
    # def test_get_daily_box_scores_nominal(self):
    #     """
    #     The function `get_daily_box_scores` shall get all player box scores for a specified day grouped by team.
    #     """
    #     test_date = datetime.datetime(year=2019, month=10, day=22)
    #     team_dict, date = Api.get_daily_box_scores(date_obj=test_date)
    #     keys = [key for key in team_dict.keys()]
    #     self.assertEqual(keys, ['LOS_ANGELES_LAKERS', 'LOS_ANGELES_CLIPPERS',
    #                      'NEW_ORLEANS_PELICANS', 'TORONTO_RAPTORS'])
    #     self.assertEqual(len(team_dict[keys[0]]), 10)
    #     self.assertEqual([date.day, date.month, date.year], [test_date.day, test_date.month, test_date.year])

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
    # filter_df_on_team_names tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_filter_df_on_team_names_nominal(self):
        """
        The function `filter_df_on_team_names` shall filter the given data frame only where the box score data is from
        one of the given team names.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        team_df = Api.filter_df_on_team_names(df, ['Los Angeles Lakers'])
        self.assertEqual(team_df.shape[0], 3)
        team_df = Api.filter_df_on_team_names(df, ['Los Angeles Lakers', 'Chicago Bulls'])
        self.assertEqual(team_df.shape[0], 4)

    # ------------------------------------------------------------------------------------------------------------------
    # get_most_recent_update_data tests
    # ------------------------------------------------------------------------------------------------------------------
    # todo

    # ------------------------------------------------------------------------------------------------------------------
    # get_team_result_on_date tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_get_team_result_on_date_nominal(self):
        """

        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        date = datetime.datetime(day=25, month=10, year=2019)
        res = Api.get_team_result_on_date('Los Angeles Lakers', date, df)
        self.assertEqual('95-86', res)

    # todo add test for team or date not found?

    # ------------------------------------------------------------------------------------------------------------------
    # create_scatter_plot_with_trend_line tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_create_scatter_plot_with_trend_line_nominal(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_svg_save(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  save_path='svg_buffer')
        self.assertEqual(41174, len(plot_path))

    def test_create_scatter_plot_with_trend_line_data_frames(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot, return
        the outlier DataFrame object, and return the total filtered DataFrame object.
        """
        my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, outlier_df, total_df = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                                  y_key='points',
                                                                                  df=df,
                                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))
        self.assertEqual(outlier_df.shape[0], 5)
        self.assertEqual(total_df.shape[0], 55)

    def test_create_scatter_plot_with_trend_line_save_path(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot if given a
        specific path.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        save_path = os.path.join(self.logs_dir, 'test.png')
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  save_path=save_path)
        self.assertTrue(os.path.exists(plot_path))
        self.assertTrue(os.path.exists(save_path))
        self.assertEqual(plot_path, save_path)

    def test_create_scatter_plot_with_trend_line_no_trend_line(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  trend_line=False,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_seconds_filter(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot when provided a
        minimum and maximum seconds value.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  min_seconds=300,
                                                                  max_seconds=600,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_minutes_filter(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot when provided with
        a minimum and maximum minutes value.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  min_seconds=10,
                                                                  max_seconds=30,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_filter_teams(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot with a filtered data
        frame based on team name.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  teams=['Los Angeles Lakers'],
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_outliers(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot with labeled outliers.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  num_outliers=5,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_scatter_plot_with_trend_line_no_grid(self):
        """
        The function `create_scatter_plot_with_trend_line` shall create and save a scatter plot without using a grid.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _, _ = Api.create_scatter_plot_with_trend_line(x_key='minutes_played',
                                                                  y_key='points',
                                                                  df=df,
                                                                  grid=False,
                                                                  save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    # ------------------------------------------------------------------------------------------------------------------
    # create_date_plot tests
    # ------------------------------------------------------------------------------------------------------------------
    def test_create_date_plot_nominal(self):
        """
        The function `create_date_plot` shall create and save a date plot when provided nominal data.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_date_plot_nominal_params(self):
        """
        The function `create_date_plot` shall create and save a date plot when provided nominal data and optional
            **kwarg arguments.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            min_seconds=300,
                                            max_seconds=2200,
                                            num_outliers=7,
                                            grid='x',
                                            mean_line=False)
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_date_plot_y_grid(self):
        """
        The function `create_date_plot` shall create and save a date plot with a y axis grid only when provided
        with nominal data and grid = 'y'.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            grid='y')
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_date_plot_invalid_grid(self):
        """
        The function `create_date_plot` shall create and save a date plot with a default grid when provided
        with nominal data and grid is not one of the following: both, x, or y.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            grid='BAD')
        self.assertTrue(os.path.exists('%s.png' % plot_path))

    def test_create_date_plot_invalid_player_name(self):
        """
        The function `create_date_plot` shall return a plot path of invalid player name when given a player name
        that is not in the pandas.DataFrame object provided.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Bad Name',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            grid='both')
        self.assertEqual(plot_path, 'Invalid player name of Bad Name')

    def test_create_date_plot_player_substring(self):
        """
        The function `create_date_plot` shall return a plot path of invalid player name when given a substring of a
        player name that exists in the pandas.DataFrame object provided.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            grid='both')
        self.assertEqual(plot_path, 'Invalid player name of Anthony')

    def test_create_date_plot_invalid_min_seconds(self):
        """
        The function `create_date_plot` shall create and save a plot with default max and min seconds when provided
        an invalid min seconds value.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            min_seconds='a')
        self.assertTrue('Max/Min seconds incorrect type' in plot_path)

    def test_create_date_plot_invalid_max_seconds(self):
        """
        The function `create_date_plot` shall create and save a plot with default max and min seconds when provided
        an invalid max seconds value.
        """
        my_csv = 'player_box_scores.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
        plot_path, _ = Api.create_date_plot(player='Anthony Davis',
                                            y_key='points',
                                            df=df,
                                            save_path=self.logs_dir,
                                            max_seconds='a')
        self.assertTrue('Max/Min seconds incorrect type' in plot_path)

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
