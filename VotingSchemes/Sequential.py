import pandas as pd
import numpy as np
import itertools
from random import randrange

class Sequential:
    agenda = []

    def setAgenda(self, agenda : [str]):
        # Set the agenda
        if len(pd.Series(agenda)[pd.Series(agenda).duplicated()].values) > 0 :
            print("Agenda contains duplicates")
            return False
        self.agenda = agenda
        return True

    def randomAgenda(self, preferences: pd.DataFrame) -> [str]:
        # Create a random agenda from the candidates specified in the preferences
        candidates = preferences["Voter 1"]
        permutations = list(itertools.permutations(list(candidates)))
        return permutations[randrange(len(permutations))]

    def outcome(self, preferences: pd.DataFrame) -> str:
        # Compute the final outcome of the vote, eg : A
        if len(self.agenda) == 0: self.setAgenda(self.randomAgenda(preferences))
        previous = self.agenda[0]
        for round in range(1, len(self.agenda)):
            opponent = self.agenda[round]
            # Count which candidate is preferred more
            count = 0
            for voter in preferences.columns:
                previousIndex = np.where(preferences[voter] == previous)[0]
                opponentIndex = np.where(preferences[voter] == opponent)[0]
                if previousIndex < opponentIndex:
                    count += 1
                else:
                    count -= 1
            if count < 0:
                previous = opponent
        return previous

    def outcomeRanking(self, preferences: pd.DataFrame) -> [str]:
        print("Sequential Voting does not support social ranking computations. Only the winner will be displayed.")
        return [self.outcome(preferences)]

    def toString(self):
        return "Sequential Voting Scheme"