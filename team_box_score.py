# ----------------------------------------------------------------------------------------------------------------------
# Box Score
# ----------------------------------------------------------------------------------------------------------------------

# imports
from box_score import BoxScore


class TeamBoxScore(object):
    """
    Class for a team box score object
    """
    def __init__(self, box_scores, team_box_score, team_name):
        """
        Setup for the TeamBoxScore class.

        :param list box_scores: Player box scores.
        :param list team_box_score: Team box score stats.
        :param str team_name: The team name of the associated box scores.
        """
        self.player_box_scores = [BoxScore(box_score) for box_score in box_scores]
        self.team_box_score = team_box_score
        self.team = team_name

    def to_string(self):
        """
        Converts the team box score object into a human readable string.

        :return: Team box score data.
        :rtype: str
        """
        builder = "Team: %s\n" % self.team
        builder += '\tPlayers: %s\n' % self.get_players()
        return builder

    def get_players(self):
        """
        Gets a list of player names on the team box score.
        :return: Player names
        :rtype: list
        """
        players = []
        for bs in self.player_box_scores:
            players.append(bs.player_name)
        return players


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
