# ----------------------------------------------------------------------------------------------------------------------
# Analytics API
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
from collections import OrderedDict
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from box_score import BoxScore


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
                    bs = box_score
                    print(bs)
                    found = True
                    break
            if found:
                break
            date_obj -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            print("Timeout reached.")
            break
    return bs


def get_daily_box_scores(date_obj=None, timeout=1):
    """
    Gets all player box scores for a specific day. The default for this is only the one date sepecified.

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
            timeout -= 1
        else:
            break
    return team_dict


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
            timeout -= 1
        else:
            break
    print(teams)
    return teams

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
