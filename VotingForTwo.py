import pandas as pd

class VotingForTwo:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]
        pass

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A
        pass

    def happiness(self, preferences: pd.DataFrame, outcome: str) -> [float]:
        # Compute the happiness of all voters based on a given outcome
        pass