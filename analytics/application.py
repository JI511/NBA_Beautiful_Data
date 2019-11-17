# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import logging
import os
from . import analytics_API as Api
from .team_box_score import TeamBoxScore
from basketball_reference_web_scraper.data import Team


class Application(object):
    """
    This class handles running the application
    """
    def __init__(self):
        """
        Setup for the application.
        """
        self.player = 'LeBron James'.lower()
        self.logger = logging.getLogger(__name__)

    def run_with_date_range(self, start_date, end_date):
        """
        Create a csv file of player box scores from a date range.

        :param str start_date: The date to begin searching.
        :param str end_date: The date to end searching, exclusive, meaning this date will not be searched
            and will only trigger ending.
        """
        logging.basicConfig(filename='date_range_log.ini', level=logging.INFO)
        start_split = start_date.split('_')
        start = datetime.datetime(year=int(start_split[0]),
                                  month=int(start_split[1]), day=int(start_split[2]))

    def run(self, date=False, should_log=False, plot=True, gather_new=False):
        """
        Runs the application.

        :param datetime.datetime date: The date to attempt searching.
        :param bool should_log: Indicates if logging should be used.
        :param bool plot: Indicates if plots should be created.
        :param bool gather_new: Indicates if new player box score data should be searched for.
        """
        if should_log:
            logging.basicConfig(filename='log.ini', level=logging.INFO)
        if not date:
            date = datetime.datetime.now()
        self.logger.info("Executing datetime: %s" % date)
        print(date)

        # temp_bs, fd = Api.get_player_box_score(name=self.player, date_obj=date)
        # box_score = BoxScore(temp_bs, fd)
        # print(box_score.to_string())

        team_box_scores = []
        my_csv = 'player_box_scores.csv'
        # my_csv = 'small_data_set.csv'
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)

        if gather_new:
            daily_box_scores, found_date = Api.get_daily_box_scores(date_obj=date)
            for team in daily_box_scores.keys():
                team_box_scores.append(TeamBoxScore(box_scores=daily_box_scores[team],
                                                    team_box_score=[],
                                                    team_name=team,
                                                    date=found_date))

            new_df = Api.create_data_frame_from_team_box_scores(team_box_scores=team_box_scores,
                                                                logger=self.logger)
            if df is None:
                print('There was not an existing data frame.')
                df = new_df
            else:
                print('Appending new data frame of shape: %s' % str(new_df.shape))
                self.logger.info('Appending new data frame of shape: %s' % str(new_df.shape))
                temp_df = df.append(new_df, sort=False)
                temp_size = temp_df.shape[0]
                # add new columns with ops from existing data
                temp_df['minutes_played'] = temp_df['seconds_played'].apply(Api.convert_to_minutes)
                temp_df['true_shooting'] = temp_df.apply(
                    lambda x: Api.get_true_shooting(x['points'],
                                                    x['attempted_field_goals'],
                                                    x['attempted_three_point_field_goals'],
                                                    x['attempted_free_throws']),
                    axis=1)
                temp_df['assist_turnover_ratio'] = temp_df.apply(
                    lambda x: Api.get_assist_turnover_ratio(x['assists'],
                                                            x['turnovers']),
                    axis=1)
                temp_df.drop_duplicates(inplace=True)
                temp_size = temp_size - temp_df.shape[0]
                self.logger.info('Dropped %s duplicates' % temp_size)
                print('Dropped %s duplicates' % temp_size)
                df = temp_df
                print(df.shape)
            df.to_csv(my_csv)

        if plot:
            x_key = 'minutes_played'
            y_key = 'game_score'
            Api.create_scatter_plot_with_trend_line(x_key=x_key, y_key=y_key, df=df, outliers=5,
                                                    show_plot=True, save_path=os.getcwd())
            # items = ['points', 'rebounds', 'assists']
            # team = Team.LOS_ANGELES_LAKERS.name
            # Api.create_bar_plot(df=Api.get_team_date_df(df, team=team, date=date),
            #                     bar_items=items,
            #                     show_plot=True,
            #                     save_path=os.getcwd(),
            #                     team=team,
            #                     date=date)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
