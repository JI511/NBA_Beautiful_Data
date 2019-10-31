# ----------------------------------------------------------------------------------------------------------------------
# Application
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import logging
import numpy as np
import matplotlib.pyplot as plt
import analytics_API as Api
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
        self.logger = logging.getLogger(__name__)

    def run(self, date=False, should_log=False):
        """
        Runs the application.

        :param datetime.datetime date: The date to attempt searching.
        :param bool should_log: Indicates if logging should be used.
        """
        if should_log:
            logging.basicConfig(filename='log.ini', level=logging.INFO)
        if not date:
            date = datetime.datetime.now()
        self.logger.info("Executing datetime: %s" % date)

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
        df = Api.get_existing_data_frame(my_csv, logger=self.logger)
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
            temp_df.drop_duplicates(inplace=True)
            temp_size = temp_size - temp_df.shape[0]
            self.logger.info('Dropped %s duplicates' % temp_size)
            print('Dropped %s duplicates' % temp_size)
            df = temp_df
            print(df.shape)
        df['minutes_played'] = df['seconds_played'].apply(Api.convert_to_minutes)
        df.to_csv(my_csv)

        # plt.rcParams.update({'font.size': 20, 'figure.figsize': (10, 8)})
        # x_key = 'minutes_played'
        # y_key = 'game_score'
        # df.plot(kind='scatter', x=x_key, y=y_key, title='%s vs %s' % (x_key, y_key), grid=True)
        # x = df[x_key]
        # y = df[y_key]
        # z = np.polyfit(x, y, 1)
        # p = np.poly1d(z)
        # plt.plot(x, p(x), "r--")
        # plt.show()


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
