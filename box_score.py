# ----------------------------------------------------------------------------------------------------------------------
# Box Score
# ----------------------------------------------------------------------------------------------------------------------

# imports


class BoxScore(object):
    """
    Class for a box score object.
    """
    def __init__(self, bs_dict):
        """
        Setup for the BoxScore class.

        :param dict bs_dict: Dictionary result from the analytics API.
        """
        self.keys = ['name', 'points', 'rebounds', 'assists']
        self.player_name = bs_dict['name']
        self.points = bs_dict['points']
        self.rebounds = bs_dict['rebounds']
        self.assists = bs_dict['assists']

    def to_string(self):
        """
        Converts the box score object into an easily readable string.
        :return: Box score data
        """
        print('Name: %s' % self.player_name)
        print('Points: %s' % self.points)
        print('Rebounds: %s' % self.rebounds)
        print('Assists: %s' % self.assists)

    def __calculate_points(self, made_fg, made_three, made_ft):
        """
        Calculates the number of points scored from the combinations of all made baskets.

        :param made_fg:
        :param made_three:
        :param made_ft:
        :return: The number of points scored.
        :rtype: int
        """
        pass

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
