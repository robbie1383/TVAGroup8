import pandas as pd
from collections import Counter


class AntiPluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]

        # initializer a ranking dictionary with zeros ( preferences are found in the first voter)

        #initializer ranking dictionary with zeros
        ranking = dict.fromkeys(preferences.iloc[:,1].values, 0) #start from 1 because 1 is preference

        # dictionary with scores
        first = True
        for voter in preferences._iter_column_arrays():
            if first:
                first=False
                continue
            for i in range(len(voter) - 1):
                ranking[voter[i]] += 1

        # sort first by score then alphabetically
        '''Note that we have here a sorted dictionary. It might become very usefull in the future'''
        ranking = dict(sorted(ranking.items(), key=lambda x: (-x[1], x[0]), reverse=False))

        #get only the preferences and not the equivalent votes
        outcomeRanking = list(ranking.keys())

        return outcomeRanking

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A

        #get score and return winner
        score = self.outcomeRanking(preferences)
        return score[0]

    def happiness(self, preference, outcome: str) -> [float]:
        # Compute the happiness of all voters based on a given outcome

        m = (len(outcome))
        hapiness = 0
        for i in range(0,len(preference)):
            pass
            # print(preference[i])
            # print(np.where(outcome == preference[i]))
        #print(preference)
        #print(outcome)
        pass

if __name__ == "__main__":
    inputFile = "DataSet.csv"  # for future command line IO
    preferences = pd.read_csv(inputFile)

    votingScheme = AntiPluralityVoting()

    ranking = votingScheme.outcomeRanking(preferences)
    print("Social Ranking:", ranking)
    print("Voting Winner:", votingScheme.outcome(preferences))
    i = 1
    print("Hapiness for user:", votingScheme.happiness(preferences.iloc[:,i].values, ranking))
