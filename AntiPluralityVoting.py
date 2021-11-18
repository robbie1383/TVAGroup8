import pandas as pd

class AntiPluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        '''
        :param preferences: pandas dataframe with the voting preferences
        :return: final ranking eg : [A,B,C,D]
        '''

        #initializer ranking dictionary with zeros
        ranking = dict.fromkeys(preferences.iloc[:, 0].values, 0)

        # dictionary with scores
        first = True
        for voter in preferences._iter_column_arrays():
            if first:
                first = False
                continue
            for i in range(len(voter) - 1):
                ranking[voter[i]] += 1

        # sort first by score then alphabetically
        '''Note that we have here a sorted dictionary. It might become very useful in the future'''
        ranking = dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))

        #get only the preferences and not the equivalent votes
        outcomeRanking = list(ranking.keys())

        return outcomeRanking

    def outcome(self, preferences: pd.DataFrame) -> str:
        '''
        :param preferences: pandas dataframe with the voting preferences
        :return: single winner
        '''
        # Compute the final outcome of the vote, eg : A
        score = self.outcomeRanking(preferences)
        return score[0]
