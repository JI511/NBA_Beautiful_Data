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


def get_player_box_score(name, date_obj=None, timeout=3):
    """
    Gets the box score for the desired player.

    :param str name: Name of the player to search for.
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
            print('Attempting date: %s' % date_obj.strftime('%y-%m-%d'))
            found = False
            box_scores = client.player_box_scores(day=date_obj.day, month=date_obj.month, year=date_obj.year)
            print('Total players on this date: %s' % len(box_scores))
            for box_score in box_scores:
                if name in box_score['name'].lower():
                    print(box_score.keys())
                    bs = box_score
                    found = True
                    break
            if found:
                break
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            print("Timeout reached.")
            break
    return bs, date_obj


def get_team_box_scores(team, date_obj=None, timeout=3):
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


def create_scatter_plot_with_trend_line(x_key, y_key, df, save_path=None, show_plot=False):
    """
    Creates a scatter plot for two different series of a pandas data frame.

    :param str x_key: The column name in the data frame to use for the x axis.
    :param str y_key: The column name in the data frame to use for the x axis.
    :param df: The data frame object.
    :param str save_path: The path to save the png file created.
    :param bool show_plot: Indicates if the png should be shown during execution.
    :return: The save path of the created png, otherwise None.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    temp_df = df[[x_key, y_key]]
    series_size = temp_df[y_key].shape[0]
    temp_df.plot(kind='scatter', x=x_key, y=y_key,
                 title='%s vs %s (%s samples)' % (x_key.title().replace('_', ' '),
                                                  y_key.title().replace('_', ' '),
                                                  series_size),
                 grid=True, ax=ax)
    ax.set_xlabel(x_key.title().replace('_', ' '))
    ax.set_ylabel(y_key.title().replace('_', ' '))
    # add point labels
    if series_size > 10:
        thresh = sorted(temp_df[y_key].to_list())[-10]
    else:
        thresh = 0
    for k, v in temp_df.iterrows():
        if v.values[1] >= thresh:
            temp_split = k.split(' ')
            name = '%s. %s' % (temp_split[0][:1], temp_split[1])
            ax.annotate(name, v)

    # create trend line
    x = df[x_key]
    y = df[y_key]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")
    # makes things fit on graph window
    plt.tight_layout()

    # handle output
    if save_path is not None:
        if os.path.isdir(save_path):
            if not os.path.exists(os.path.join(save_path, 'plots')):
                os.mkdir(os.path.join(save_path, 'plots'))
            plt.savefig(os.path.join(save_path, 'plots', '%s_VS_%s' % (x_key, y_key)))
    if show_plot:
        plt.show()


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
