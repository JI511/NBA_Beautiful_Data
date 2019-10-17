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
        self.made_fg = bs_dict['made_field_goals']
        self.made_threes = bs_dict['made_three_point_field_goals']
        self.made_ft = bs_dict['made_free_throws']
        self.points = self.__calculate_points(made_fg=self.made_fg,
                                              made_three=self.made_threes,
                                              made_ft=self.made_ft)
        self.rebounds = bs_dict['rebounds']
        self.assists = bs_dict['assists']

    def to_string(self):
        """
        Converts the box score object into an easily readable string.
        :return: Box score data
        :rtype: str
        """
        box_score = ''
        box_score += 'Name: %s' % self.player_name
        box_score += 'Points: %s' % self.points
        box_score += 'Rebounds: %s' % self.rebounds
        box_score += 'Assists: %s' % self.assists
        return box_score

    @staticmethod
    def __calculate_points(made_fg, made_three, made_ft):
        """
        Calculates the number of points scored from the combinations of all made baskets.

        :param int made_fg: Number of made field goals.
        :param int made_three: Number of made three point field goals.
        :param int made_ft: Number of made free throws.
        :return: The number of points scored.
        :rtype: int
        """
        points = 0
        fg = made_fg - made_three
        points += (made_three * 3)
        points += (fg * 2)
        points += made_ft
        return points

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
