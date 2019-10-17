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
        self.player_name = bs_dict['name']
        self.made_fg = bs_dict['made_field_goals']
        self.made_threes = bs_dict['made_three_point_field_goals']
        self.made_ft = bs_dict['made_free_throws']
        self.points = self.__calculate_points(made_fg=self.made_fg,
                                              made_three=self.made_threes,
                                              made_ft=self.made_ft)
        self.offensive_rebounds = bs_dict['offensive_rebounds']
        self.defensive_rebounds = bs_dict['defensive_rebounds']
        self.rebounds = self.__calculate_rebounds(o_reb=self.offensive_rebounds,
                                                  d_reb=self.defensive_rebounds)
        self.assists = bs_dict['assists']
        self.team = bs_dict['team']

    def to_string(self):
        """
        Converts the box score object into an easily readable string.
        :return: Box score data
        :rtype: str
        """
        box_score = ''
        box_score += 'Name: %s\n' % self.player_name
        box_score += 'Points: %s\n' % self.points
        box_score += 'Rebounds: %s\n' % self.rebounds
        box_score += 'Assists: %s\n' % self.assists
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

    @staticmethod
    def __calculate_rebounds(o_reb, d_reb):
        """
        Calculates the number of rebounds from offensive and defensive rebounds

        :param o_reb: Number of offensive rebounds.
        :param d_reb: Number of defensive rebounds.
        :return: The number of rebounds.
        :rtype: int
        """
        return o_reb + d_reb

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
