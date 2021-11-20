import pandas as pd

class AntiPluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        '''
        :param preferences: pandas dataframe with the voting preferences
        :return: final ranking eg : [A,B,C,D]
        '''
        #initializer ranking dictionary with zeros
        ranking = dict.fromkeys(preferences.iloc[:, 0].values, 0)
        for _, votes in preferences.iteritems():
            for i in range(len(votes) - 1):
                ranking[votes[i]] += 1

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

