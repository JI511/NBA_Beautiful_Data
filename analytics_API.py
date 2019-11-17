# ----------------------------------------------------------------------------------------------------------------------
# Analytics API
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from basketball_reference_web_scraper import client
from constants import Vars


def get_player_box_score(name, logger, date_obj=None, timeout=3):
    """
    Gets the box score for the desired player.

    :param str name: Name of the player to search for.
    :param logger: Logging object.
    :param datetime.datetime date_obj: Datetime object for starting day to search.
    :param int timeout: Number of days to search before giving up.
    :return: Box score for the player if found.
    :rtype: dict
    """
    name = name.lower()
    if date_obj is None:
        date_obj = datetime.datetime.today()
    bs = None
    while True:
        if timeout > 0:
            logger.info('Attempting date: %s' % date_obj.strftime('%y-%m-%d'))
            found = False
            box_scores = client.player_box_scores(day=date_obj.day, month=date_obj.month, year=date_obj.year)
            for box_score in box_scores:
                if name in box_score['name'].lower():
                    bs = box_score
                    found = True
                    break
            if found:
                break
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            logger.info("Timeout reached.")
            break
    return bs, date_obj


def get_team_box_score(team, date_obj=None, timeout=3):
    """
    Gets the team box score data for a specific day.

    :param str team: The team to search for.
    :param datetime.datetime date_obj: Datetime object for starting day to search.
    :param int timeout: Number of days to search before giving up.
    :return:
    """
    if date_obj is None:
        date_obj = datetime.datetime.today()
    team_bs = None
    while True:
        if timeout > 0:
            team_bs = client.team_box_scores(day=date_obj.day, month=date_obj.month, year=date_obj.year)
            # todo
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            break
    return team_bs


def get_daily_box_scores(date_obj=None, timeout=1):
    """
    Gets all player box scores for a specific day. The default for this is only the one date specified.

    :param datetime.datetime date_obj: Datetime object for starting day to search.
    :param int timeout: Number of days to search before giving up.
    :return: All box scores sorted by team.
    :rtype: OrderedDict
    """
    team_dict = OrderedDict()
    if date_obj is None:
        date_obj = datetime.datetime.today()
    while True:
        if timeout > 0:
            teams = get_teams_played_on_date(date_obj=date_obj)
            if len(teams) > 0:
                all_box_scores = client.player_box_scores(day=date_obj.day, month=date_obj.month, year=date_obj.year)
                for team in teams:
                    team_dict[team] = []
                for player in all_box_scores:
                    team_dict[player['team'].name].append(player)
                break
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            break
    return team_dict, date_obj


def get_teams_played_on_date(date_obj=None, timeout=1):
    """
    Gets a list of all teams that played on the provided date.

    :param datetime.datetime date_obj: Datetime object for starting day to search.
    :param int timeout: Number of days to search before giving up.
    :return: The active teams on the given date.
    :rtype: list
    """
    teams = []
    if date_obj is None:
        date_obj = datetime.datetime.today()
    while True:
        if timeout > 0:
            team_box_scores = client.team_box_scores(day=date_obj.day, month=date_obj.month, year=date_obj.year)
            if len(team_box_scores) > 1:
                teams = [entry['team'].name for entry in team_box_scores]
                break
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            break
    return teams


def convert_to_minutes(seconds_played):
    """
    Converts seconds into minutes.

    :param seconds_played:
    :return:
    """
    minutes = seconds_played / 60.0
    return round(minutes, 2)


def get_true_shooting(points, fga, tpfga, fta):
    """
    Calculates true shooting percentage.

    :param int points: Points
    :param int fga: Field goals attempted
    :param int tpfga: Three point field goals attempted
    :param int fta: Free throws attempted
    :return:  True shooting percentage
    :rtype: float
    """
    try:
        ts = points / (2.0 * ((fga + tpfga) + 0.44 * fta))
    except ZeroDivisionError:
        ts = 0
    return round(ts, 3)


def get_assist_turnover_ratio(assists, turnovers):
    """
    Calculates the ratio of assists to turnovers.

    :param assists: Number of assists.
    :param turnovers: Number of turnovers.
    :return:
    """
    try:
        ratio = float(assists) / turnovers
    except ZeroDivisionError:
        ratio = float(assists)
    return round(ratio, 2)


def check_supported_stats(stats):
    """
    Checks a list of strings to determine if the stat type is supported.

    :param stats: The stats to check.
    :return: Indicates if all provided stats are acceptable.
    :rtype: bool
    """

    valid = True
    for stat in stats:
        if stat not in Vars.supported_stats:
            valid = False
            break
    return valid


def convert_team_name(team):
    """
    Converts team string into proper casing format

    :param str team: Team enum name
    :return: Converted string
    """
    return team.title().replace('_', ' ')

# ----------------------------------------------------------------------------------------------------------------------
# Pandas interactions
# ----------------------------------------------------------------------------------------------------------------------


def get_existing_data_frame(csv_path, logger):
    """
    Determines if a data frame already exists, and returns the data frame if true. Returns None if does not exist.

    :param str csv_path: Path of the csv file.
    :param logger: Instance of logger object.
    :return: Data frame if exists, None otherwise
    :rtype: pd.DataFrame
    """
    df = None
    if os.path.exists(csv_path):
        logger.info("Existing data frame found.")
        df = pd.read_csv(csv_path, index_col=0)
    return df


def create_data_frame_from_team_box_scores(team_box_scores, logger):
    """
    Creates a pandas data frame object from a list of team box score objects.

    :param list team_box_scores: Team box score objects
    :param logger: Instance of logger object
    :return: Pandas data frame
    :rtype: pd.DataFrame
    """
    logger.info("Appending new data frame from %s teams" % len(team_box_scores))
    data = {}
    index = []
    for stat in Vars.supported_stats:
        data[stat] = []
    for tbs in team_box_scores:
        index.extend(tbs.get_players())
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

    if data['team']:
        teams = list(set(data['team']))
        for team in teams:
            logger.info('\t%s' % team)
    df = pd.DataFrame(data, index=index)
    return df


def get_team_date_df(df, team, date):
    """
    Attempts to make a pandas data frame of all player box scores on a certain day.

    :param pandas.DataFrame df: The data frame to search.
    :param str team: The team to search for.
    :param datetime.datetime date: The date to search on.
    :return: Team data frame if found
    """
    team_df = None
    if isinstance(date, datetime.datetime):
        converted_date = date.strftime('%y_%m_%d')
        team_df = df[(df['date'] == converted_date) & (df['team'] == team)]
    return team_df


def create_scatter_plot_with_trend_line(x_key, y_key, df, outliers=5, save_path=None, show_plot=False):
    """
    Creates a scatter plot for two different series of a pandas data frame.

    :param str x_key: The column name in the data frame to use for the x axis.
    :param str y_key: The column name in the data frame to use for the x axis.
    :param pandas.DataFrame df: The data frame object.
    :param int outliers: The number of outliers to label on the plot.
    :param str save_path: The path to save the png file created.
    :param bool show_plot: Indicates if the png should be shown during execution.
    :return: The save path of the created png, otherwise None.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    temp_df = df[[x_key, y_key]]
    series_size = temp_df[y_key].shape[0]
    if series_size > outliers:
        thresh = sorted(temp_df[y_key].to_list())[-outliers]
    else:
        thresh = 0

    outlier_df = temp_df[temp_df[y_key] >= thresh]
    main_df = temp_df[temp_df[y_key] < thresh]
    title = '%s vs %s (%s samples)' % (x_key.title().replace('_', ' '),
                                       y_key.title().replace('_', ' '),
                                       series_size)
    # plot main df
    main_df.plot(kind='scatter', x=x_key, y=y_key, grid=True, ax=ax)
    outlier_df.plot(kind='scatter', x=x_key, y=y_key, grid=True, ax=ax)

    ax.set_xlabel(x_key.title().replace('_', ' '))
    ax.set_ylabel(y_key.title().replace('_', ' '))
    # add point labels

    for k, v in outlier_df.iterrows():
        temp_split = k.split(' ')
        name = '%s.%s.' % (temp_split[0][:1], temp_split[1][:3])
        ax.annotate(name, v, xytext=(5, -5), textcoords='offset points')

    # create trend line
    x = df[x_key]
    y = df[y_key]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", label='Trend')

    # makes things fit on graph window
    plt.title(title)
    plt.tight_layout()
    plt.legend(loc='best')

    # handle output
    plot_path = None
    if save_path is not None:
        if os.path.isdir(save_path):
            if not os.path.exists(os.path.join(save_path, 'plots')):
                os.mkdir(os.path.join(save_path, 'plots'))
            ymd = datetime.datetime.now().strftime("%y%m%d")
            plot_path = os.path.join(save_path, 'plots', '%s_VS_%s_%s' % (x_key, y_key, ymd))
            plt.savefig(plot_path)
    if show_plot:
        plt.show()
    return plot_path


def create_bar_plot(df, bar_items, save_path=None, show_plot=False, team=None, date=None):
    """
    Creates a stacked bar graph with any number of column names for a team.

    :param pandas.DataFrame df: Data frame to use.
    :param list bar_items: Column names within the data frame.
    :param str save_path: The path to save the png file created.
    :param bool show_plot: Indicates if the png should be shown during execution.
    :param str team: Optional team name to add to plot title.
    :param datetime.datetime date: Optional date to add to plot title.
    :return: Save path if save successful.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    margin_bottom = np.zeros(df.shape[0])
    colors = ['#17408B', '#C9082A', '#552084', '#FDBA21']
    title = ''
    for index, item in enumerate(bar_items):
        values = df[item].to_list()
        df.plot.bar(y=item, ax=ax, stacked=True, bottom=margin_bottom, color=colors[index], rot=45, label=item)
        margin_bottom += values
        title += '%s ' % item.title()

    if team is not None:
        if isinstance(team, str):
            title = '%s %s' % (convert_team_name(team), title)

    if date is not None:
        if isinstance(date, datetime.datetime):
            title = '%s %s' % (title, date.strftime('%y_%m_%d'))

    ax.set_title(title)
    plt.tight_layout()

    # handle output
    plot_path = None
    if save_path is not None:
        if os.path.isdir(save_path):
            if not os.path.exists(os.path.join(save_path, 'plots')):
                os.mkdir(os.path.join(save_path, 'plots'))
            if date is None:
                ymd = datetime.datetime.now().strftime("%y%m%d")
                plot_path = os.path.join(save_path, 'plots', '%s_%s' % (title.replace(' ', '_'), ymd))
            else:
                plot_path = os.path.join(save_path, 'plots', title.replace(' ', '_'))
            plt.savefig(plot_path)
    if show_plot:
        plt.show()
    return plot_path


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
