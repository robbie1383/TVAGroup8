import operator

import pandas as pd
import numpy as np


class BordaVoting:

    # Compute the social ranking of candidates, eg : [A, B, C, D]
    def outputScores(self, preferences: pd.DataFrame) -> [str]:
        ranking = {}
        info = np.array(preferences)
        for num_candidates in range(len(info)):
            for candidate in info[num_candidates]:
                if candidate in ranking.keys():
                    ranking[candidate] += ranking[candidate] + len(info) - num_candidates
                else:
                    ranking[candidate] = len(info) - num_candidates
        ranking = dict(sorted(ranking.items(), key=operator.itemgetter(1), reverse=True))
        return ranking

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        ranking = self.outputScores(preferences)
        outcome_rank = list(ranking.keys())
        return outcome_rank
    
    # Compute the final outcome of the vote, eg : A
    def outcome(self, preferences: pd.DataFrame) -> str:
        return self.outcomeRanking(preferences)[0]

    def toString(self):
        return "Borda Voting Scheme"
