import pandas as pd
import itertools
from Borda import BordaVoting
from PluralityVoting import PluralityVoting
from VotingForTwo import VotingForTwo
from AntiPluralityVoting import AntiPluralityVoting

# Read the input from the .csv file.
inputFile = "example.csv"  # for future command line IO
preferences = pd.read_csv(inputFile)

# Choose the voting scheme
votingOptions = [BordaVoting(), PluralityVoting(), AntiPluralityVoting(), VotingForTwo()]
votingSchemeChoice = 0  # for future command line IO
votingScheme = votingOptions[votingSchemeChoice]

# Define happiness function
def happiness(voter : str, preferences, outcome: [str]) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return: the happiness of a given voter with a given outcome
    """
    pass

# Define overall happiness
def overallHappiness(preferences, outcome: [str]) -> float:
    """
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return:
    """
    # sum the happiness of all individual voters
    pass

# Define strategic voting function
def strategicVoting(voter : str, preferences, votingScheme) :
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :return: a strategic voting option of the form :
             [newVoterRanking, outcome, newHappiness, newOverallHappiness, trueOverallHappiness]
    """
    voterRanking = preferences[voter]
    permutations = list(itertools.permutations(list(voterRanking)))
    strategies = []
    for alternative in permutations:
        newPreferences = preferences.copy()
        newPreferences[voter] = alternative
        outcomeRanking = votingScheme.outcomeRanking(newPreferences)
        option = [alternative, votingScheme.outcome(newPreferences), happiness(voter, newPreferences, outcomeRanking), overallHappiness(newPreferences, outcomeRanking), overallHappiness(preferences, outcomeRanking)]
        strategies.append(option)
    return strategies


# TEST THINGS HERE
print("Social Ranking:", votingScheme.outcomeRanking(preferences))
print("Voting Winner:", votingScheme.outcome(preferences))
print(strategicVoting("Voter 1", preferences, votingScheme))