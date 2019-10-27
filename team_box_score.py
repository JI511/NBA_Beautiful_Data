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
    def __init__(self, box_scores, team_box_score, team_name, date):
        """
        Setup for the TeamBoxScore class.

        :param list box_scores: Player box scores.
        :param list team_box_score: Team box score stats.
        :param str team_name: The team name of the associated box scores.
        :param datetime.datetime date: The data from the box score.
        """
        self.player_box_scores = [BoxScore(box_score, date) for box_score in box_scores]
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

    def create_points_graph(self, save_fig=False):
        """
        Creates a bar graph showing points for each player on the team box score.

        :param save_fig: Indicates if the plot should be saved to disk.
        """
        ez_plot.create_bar_graph(x_data=self.get_players(), y_data=self.get_points(),
                                 x_lab='Players', y_lab='Points', title='%s Points' % self.team)

    # ------------------------------------------------------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------------------------------------------------------
    def get_players(self):
        """
        Gets a list of player names on the team box score.

        :return: Player names
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.player_name)
        return players

    def get_points(self):
        """
        Gets a list of player points of the team box score.

        :return: Player points
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.points)
        return players

    def get_rebounds(self):
        """
        Gets a list of player rebounds of the team box score.

        :return: Player rebounds
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.rebounds)
        return players

    def get_dates(self):
        """
        Gets a list of dates the box scores are from.

        :return: Dates as strings.
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.get_date_string())
        return players

    def get_assists(self):
        """
        Gets a list of player assists of the team box score.

        :return: Player assists
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.assists)
        return players

    def get_made_field_goals(self):
        """
        Gets a list of player made field goals of the team box score.

        :return: Player made field goals
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.made_fg)
        return players

    def get_made_three_point_field_goals(self):
        """
        Gets a list of player made three point field goals of the team box score.

        :return: Player made three point field goals
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.made_threes)
        return players

    def get_made_free_throws(self):
        """
        Gets a list of player made free throws of the team box score.

        :return: Player made free throws
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.made_ft)
        return players

    def get_offensive_rebounds(self):
        """
        Gets a list of player offensive rebounds of the team box score.

        :return: Player offensive rebounds
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.offensive_rebounds)
        return players

    def get_defensive_rebounds(self):
        """
        Gets a list of player defensive rebounds of the team box score.

        :return: Player defensive rebounds
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.defensive_rebounds)
        return players

    def get_teams(self):
        """
        Gets a list of player team of the team box score.

        :return: Player teams
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.player_team)
        return players

    def get_locations(self):
        """
        Gets a list of player locations (home or away) of the team box score.

        :return: Player locations
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.location)
        return players

    def get_opponents(self):
        """
        Gets a list of player opponents of the team box score.

        :return: Player opponents
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.opponent)
        return players

    def get_outcomes(self):
        """
        Gets a list of player outcomes (win or lose) of the team box score.

        :return: Player outcomes
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.outcome)
        return players

    def get_seconds_played(self):
        """
        Gets a list of player seconds played of the team box score.

        :return: Player seconds played
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.seconds_played)
        return players

    def get_attempted_three_point_field_goals(self):
        """
        Gets a list of player attempted three point field goals of the team box score.

        :return: Player attempted three point field goals
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.attempted_threes)
        return players

    def get_attempted_field_goals(self):
        """
        Gets a list of player attempted field goals of the team box score.

        :return: Player attempted field goals
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.attempted_fg)
        return players

    def get_attempted_free_throws(self):
        """
        Gets a list of player attempted free throws of the team box score.

        :return: Player attempted free throws
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.attempted_ft)
        return players

    def get_steals(self):
        """
        Gets a list of player steals of the team box score.

        :return: Player steals
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.steals)
        return players

    def get_blocks(self):
        """
        Gets a list of player blocks of the team box score.

        :return: Player blocks
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.blocks)
        return players

    def get_turnovers(self):
        """
        Gets a list of player turnovers of the team box score.

        :return: Player turnovers
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.turnovers)
        return players

    def get_personal_fouls(self):
        """
        Gets a list of player personal fouls of the team box score.

        :return: Player personal fouls
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.personal_fouls)
        return players

    def get_game_scores(self):
        """
        Gets a list of player game scores of the team box score.

        :return: Player game scores
        :rtype: list
        """
        players = []
        for bs in sorted(self.player_box_scores, key=lambda x: x.player_name):
            players.append(bs.game_score)
        return players

# ----------------------------------------------------------------------------------------------------------------------
# End
# ----------------------------------------------------------------------------------------------------------------------
