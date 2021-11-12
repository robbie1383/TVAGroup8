import pandas as pd
import numpy as np

class BordaVoting:

    # Compute the social ranking of candidates, eg : [A, B, C, D]
    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        rank = {}
        info = np.array(preferences).transpose()[2:].transpose().tolist()
        for num_candidates in range(len(info)):
            for candidate in info[num_candidates]:
                if candidate in rank.keys():
                    rank[candidate] += rank[candidate] + len(info) - num_candidates
                else:
                    rank[candidate] = len(info) - num_candidates
        outcome_rank = list(rank.keys())
        return outcome_rank

    def get_outcome(self, preferences: pd.DataFrame) -> str:
        info = np.array(preferences).transpose()[2:].transpose().tolist()
        outcome = self.outcomeRanking(info)[0]
        return outcome

"""
    # Compute the happiness of all voters based on a given outcome
    def happiness(self, preferences: pd.DataFrame, outcome: [str]) -> [float]:
        info = np.array(preferences).transpose()[2:].transpose().tolist()
        can_num = len(info)
        voter_num = len(info[0])
        happiness = [0 for i in range(voter_num)]
        for i in range(can_num):
            for j in range(voter_num):
                delta = i - outcome.index(info[i][j])
                happiness_weight = can_num - i
                happiness[j] = happiness[j] + delta * happiness_weight
        return happiness
"""