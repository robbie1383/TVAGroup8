import pandas as pd
import numpy as np
import operator


class PluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]
        prefarray = np.array(preferences)
        ranking = dict.fromkeys(preferences.iloc[:, 1].values, 0)
        for i in range(len(prefarray[0])):
            ranking[prefarray[0][i]] += 1
        ranking = dict(sorted(ranking.items(), key=operator.itemgetter(1), reverse=True))
        return list(ranking.keys())

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A
        out = self.outcomeRanking(preferences)
        return list(out)[0]

    def toString(self):
        return "Plurality Voting Scheme"
