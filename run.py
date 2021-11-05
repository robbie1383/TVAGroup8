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
