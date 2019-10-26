# ----------------------------------------------------------------------------------------------------------------------
# Box Score
# ----------------------------------------------------------------------------------------------------------------------

# imports
from box_score import BoxScore
import ez_plot


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
        # sorted(trial_list, key=lambda x: trial_dict[x])
        self.player_box_scores = [BoxScore(box_score) for box_score in box_scores]
        self.team_box_score = team_box_score
        self.team = team_name.title().replace('_', ' ')

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
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            print(bs.player_name)
            players.append(bs.player_name)
        return players

    def get_points(self):
        """
        Gets a list of player points of the team box score.

        :return: Player names
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.points)
        return players

    def create_points_graph(self, save_fig=False):
        """
        Creates a bar graph showing points for each player on the team box score.

        :param save_fig: Indicates if the plot should be saved to disk.
        """
        ez_plot.create_bar_graph(x_data=self.get_players(), y_data=self.get_points(),
                                 x_lab='Players', y_lab='Points', title='%s Points' % self.team)


# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
