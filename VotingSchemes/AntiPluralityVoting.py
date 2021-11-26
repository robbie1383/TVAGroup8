import pandas as pd


class AntiPluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]

        # initialize a ranking dictionary with zeros ( preferences are found in the first voter)
        ranking = dict.fromkeys(preferences.iloc[:, 1].values, 0)  # start from 1 because 1 is preference
        # dictionary with scores
        first = True
        for voter in preferences._iter_column_arrays():
            if first:
                first = False
                continue
            for i in range(len(voter) - 1):
                ranking[voter[i]] += 1

        # sort first by score then alphabetically
        '''Note that we have here a sorted dictionary. It might become very usefull in the future'''
        ranking = dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))
        # get only the preferences and not the equivalent votes
        outcomeRanking = list(ranking.keys())

        return outcomeRanking

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A
        score = self.outcomeRanking(preferences)
        return score[0]

    def toString(self):
        return "Anti Plurality Voting Scheme"