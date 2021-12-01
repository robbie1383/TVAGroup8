import pandas as pd


class VotingForTwo:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]
        # Count for each candidate how many times they are in 1st or 2nd place
        a = preferences.iloc[0].value_counts() + preferences.iloc[1].value_counts()
        # If a candidate isn't in both, set their votes as 0 and not NaN.
        a = a.fillna(0)
        a = a.sort_values(ascending=False)
        return list(a.index.tolist())

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A
        outcome = self.outcomeRanking(preferences)
        return outcome[0]

    def toString(self):
        return "Voting for Two Scheme"