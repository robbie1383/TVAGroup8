import pandas as pd
import numpy as np
import operator


class VotingForTwo:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: social ranking of candidates based on preferences
        """
        ranking = self.outputScores(preferences)
        return list(ranking.keys())

    def outputScores(self, preferences: pd.DataFrame):
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a dictionary containing the scores of all candidates
        """
        ranking = dict.fromkeys(preferences.iloc[:, 0].values, 0)
        for voter in preferences._iter_column_arrays():
            for i in range(len(voter) - 1):
                ranking[voter[0]] += 1
                ranking[voter[1]] += 1
        ranking = dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))
        return ranking

    def outcome(self, preferences: pd.DataFrame) -> str:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a string containing the winning candidate
        """
        outcome = self.outcomeRanking(preferences)
        return outcome[0]

    def toString(self):
        return "Voting for Two Scheme"
