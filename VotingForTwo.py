import pandas as pd


class VotingForTwo:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]

        # Bug NEEDS FIXING - Giannis

        voterno = preferences.shape[1]
        # In case NO VOTES were cast for a specific candidate in either of the two preferences,
        # there's an error, as the series cannot include an index value not present in both
        a = preferences.iloc[0].value_counts(
        ) + preferences.iloc[1].value_counts()
        # If a candidate isn't in both, set their votes as 0 and not NaN.
        a = a.fillna(0)
        a = a.sort_values(ascending=False)
        # print(a.index)
        # print(list(a))
        return list(a.index.tolist())

    def outcome(self, preferences: pd.DataFrame) -> str:
        outcome = self.outcomeRanking(preferences)
        # most_voted_votes = list(outcome)[0]
        # if most_voted_votes / preferences.shape[1] - 1 > 0.5:
        #     return outcome.index[0]
        # else:
        #     return "None"
        return outcome[0]

    def happiness(self, preferences: pd.DataFrame, outcome: str) -> [float]:
        # Compute the happiness of all voters based on a given outcome
        pass
