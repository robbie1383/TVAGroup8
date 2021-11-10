import pandas as pd
import numpy as np
import operator
class PluralityVoting:

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        # Compute the social ranking of candidates, eg : [A, B, C, D]
        prefarray= np.array(preferences)
        prefarray=np.delete(prefarray, [0], 1)
        ranking = dict.fromkeys(preferences.iloc[:,1].values, 0)
        print(len(prefarray))
        print(len(prefarray[0]))
        for i in range (len(prefarray[0])):
            ranking[prefarray[0][i]]+=1
        ranking=dict(sorted(ranking.items(),key=operator.itemgetter(1),reverse=True))
        return ranking.keys()

    def outcome(self, preferences: pd.DataFrame) -> str:
        out=self.outcomeRanking(preferences)
        return list(out)[0]

    def happiness(self, preferences: pd.DataFrame, outcome: str) -> [float]:
        # Compute the happiness of all voters based on a given outcome

        pass

if __name__ == "__main__":
    inputFile = "DataSet.csv"  # for future command line IO
    preferences = pd.read_csv(inputFile)
    plurality = PluralityVoting()
    outcomeRank=plurality.outcomeRanking(preferences)
    print("Outcome preference", outcomeRank)
    outcome = plurality.outcome(preferences)
    print("Outcome",outcome)
