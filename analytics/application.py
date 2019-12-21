# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import logging
import os
import sys
from . import analytics_API as Api


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
            # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        if not date:
            date = datetime.datetime.now()
        self.logger.info("---------- Executing datetime: %s ----------" % date)

        my_csv = 'player_box_scores.csv'
        # my_csv = 'small_data_set.csv'
        df = Api.gather_new_on_date(date, my_csv, self.logger)
        if gather_new:
            if gather_new == 'update_to_current':
                current_date = date
                last_update_date = Api.get_most_recent_update_date(df)
                self.logger.info('Last fetched date: %s', last_update_date)
                while current_date.strftime('%y_%m_%d') != last_update_date.strftime('%y_%m_%d'):
                    self.logger.info('-- Attempting to add date: %s', current_date)
                    df = Api.gather_new_on_date(current_date, my_csv, self.logger)
                    current_date -= datetime.timedelta(days=1)
                    # todo, get older csv to test with, and write unit tests?

        if plot:
            x_key = 'minutes_played'
            y_key = 'game_score'
            Api.create_scatter_plot_with_trend_line(x_key=x_key, y_key=y_key, df=df, num_outliers=5,
                                                    min_seconds=60*25, max_seconds=60*35,
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
