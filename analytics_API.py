# ----------------------------------------------------------------------------------------------------------------------
# Analytics API
# ----------------------------------------------------------------------------------------------------------------------

# imports
import datetime
from basketball_reference_web_scraper import client
from basketball_reference_web_scraper.data import Team
from box_score import BoxScore


def get_play_box_score(name, date_obj=None, timeout=3):
    """
    Gets the box score for the desired player.

    :param name: Name of the player to search for.
    :param datetime.datetime date_obj: Datetime object for starting day to search.
    :param int timeout: Number of days to search before giving up.
    :return: Box score for the player if found.
    :rtype: dict
    """
    date = date_obj
    if date_obj is None:
        date = datetime.datetime.today()
    bs = None
    while True:
        if timeout > 0:
            print('Attempting date: %s' % date.strftime('%y-%m-%d'))
            found = False
            box_scores = client.player_box_scores(day=date.day, month=date.month, year=date.year)
            print('Total players on this date: %s' % len(box_scores))
            for box_score in box_scores:
                if name in box_score['name'].lower():
                    bs = box_score
                    print(bs)
                    found = True
                    break
            if found:
                break
            date -= datetime.timedelta(days=1)
            timeout -= 1
        else:
            print("Timeout reached.")
            break
    return bs

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
