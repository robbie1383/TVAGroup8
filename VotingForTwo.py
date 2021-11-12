import pandas as pd

class VotingForTwo:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]
        pass

    def outcome(self, preferences: pd.DataFrame) -> str:
        voterno = preferences.shape[1] - 1
        # In case NO VOTES were cast for a specific candidate in either of the two preferences,
        # there's an error, as the series cannot include an index value not present in both
        a = preferences.iloc[0].value_counts() + preferences.iloc[1].value_counts()
        a = a.fillna(0) # If a candidate isn't in both, set their votes as 0 and not NaN.
        a = a.sort_values(ascending=False)
        most_voted_votes = list(a)[0]
        if most_voted_votes / voterno > 0.5:
            return a.index[0]
        else:
            return "None"

        pass
