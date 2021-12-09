import pandas as pd
import numpy as np
import operator


class PluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: social ranking of candidates based on preferences
        """
        prefarray = np.array(preferences)
        ranking = dict.fromkeys(preferences.iloc[:, 1].values, 0)
        for i in range(len(prefarray[0])):
            ranking[prefarray[0][i]] += 1
        ranking = dict(sorted(ranking.items(), key=operator.itemgetter(1), reverse=True))
        return list(ranking.keys())

    def outputScores(self, preferences: pd.DataFrame):
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a dictionary containing the scores of all candidates
        """
        ranking = dict.fromkeys(preferences.iloc[:, 0].values, 0)
        for voter in preferences._iter_column_arrays():
            ranking[voter[0]] += 1
        ranking = dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))
        return ranking

    def outcome(self, preferences: pd.DataFrame) -> str:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a string containing the winning candidate
        """
        out = self.outcomeRanking(preferences)
        return list(out)[0]

    def toString(self):
        return "Plurality Voting Scheme"
