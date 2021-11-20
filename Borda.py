import pandas as pd
import numpy as np


class BordaVoting:

    # Compute the social ranking of candidates, eg : [A, B, C, D]
    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        rank = {}
        info = np.array(preferences).transpose()[1:].transpose().tolist()
        for num_candidates in range(len(info)):
            for candidate in info[num_candidates]:
                if candidate in rank.keys():
                    rank[candidate] += rank[candidate] + len(info) - num_candidates
                else:
                    rank[candidate] = len(info) - num_candidates
        outcome_rank = list(rank.keys())
        return outcome_rank

    # Compute the final outcome of the vote, eg : A
    def outcome(self, preferences: pd.DataFrame) -> str:
        return self.outcomeRanking(preferences)[0]
