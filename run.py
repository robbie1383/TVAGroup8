import pandas as pd
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

# Compute things
print("Social Ranking:", votingScheme.outcomeRanking(preferences))
print("Voting Winner:", votingScheme.outcome(preferences))

# Definde happiness function
def happiness(voter : str, preferences, outcome: [str]) -> [float]:
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return:
    """
    pass

# Define strategic voting function
def strategicVoting(voter : str, preferences, votingScheme) :
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :return:
    """

    outcomeRanking = votingScheme.outcomeRanking(preferences)
    voterRanking = preferences[voter]
    print(voterRanking)

strategicVoting("Voter 1", preferences, votingScheme)