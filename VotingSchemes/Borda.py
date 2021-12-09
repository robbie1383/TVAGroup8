import operator

import pandas as pd
import numpy as np


class BordaVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: social ranking of candidates based on preferences
        """
        ranking = self.outputScores(preferences)
        outcome_rank = list(ranking.keys())
        return outcome_rank

    def outputScores(self, preferences: pd.DataFrame):
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a dictionary containing the scores of all candidates
        """
        ranking = {}
        info = np.array(preferences)
        for num_candidates in range(len(info)):
            for candidate in info[num_candidates]:
                if candidate in ranking.keys():
                    ranking[candidate] += len(info) - num_candidates - 1
                else:
                    ranking[candidate] = len(info) - num_candidates - 1
        ranking = dict(sorted(ranking.items(), key=operator.itemgetter(1), reverse=True))
        return ranking

    def outcome(self, preferences: pd.DataFrame) -> str:
        """
        :param preferences: preferences: pandas dataframe with the voting preferences
        :return: a string containing the winning candidate
        """
        return self.outcomeRanking(preferences)[0]

    def toString(self):
        return "Borda Voting Scheme"
