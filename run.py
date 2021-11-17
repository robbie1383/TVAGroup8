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
votingOptions = [BordaVoting(), PluralityVoting(),
                 AntiPluralityVoting(), VotingForTwo()]
votingSchemeChoice = 3  # for future command line IO
votingScheme = votingOptions[votingSchemeChoice]

# Define happiness function
happinessMetricOptions = 0  # for future command line IO  0 = Steep, 1 = Middle, 2 = Linear ect...
def happiness(voter: str, preferences, outcome: [str], happinessMetric: int) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"  *Giannis comment - Why string and not index value?
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return: the happiness of a given voter with a given outcome
    """
    preferencesVoter = preferences[voter].tolist()
    m = len(outcome)
    # calculate how many steps the winner is removed from the current voter's preference list
    s = preferencesVoter.index(outcome[0])

    if happinessMetric == 0:  # steep curve and is halved for every step of removal.
        return m/((2 ** s)*m)
    if happinessMetric == 1:  # linear curve
        return (m-s)/m
    # Needs debugging!!
    if happinessMetric == 2:  # middle curve. First step is halved, the rest linear.
        if s == 0:
            return (m*0.5 + (m-s)*0.5) / m
        else:
            return ((m-s)*0.5) / m


# Define overall happiness
def overallHappiness(preferences, outcome: [str], happinessMetric) -> float:
    """
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return:
    """
    sum = 0
    for voter in preferences.columns:
        sum += happiness(voter, preferences, outcome, happinessMetric)
    return sum

# Define strategic voting function
def strategicVoting(voter: str, preferences, votingScheme):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :return: a strategic voting option of the form :
             [newVoterRanking, outcome, newHappiness,
                 newOverallHappiness, trueOverallHappiness]
    """
    voterRanking = preferences[voter]
    permutations = list(itertools.permutations(list(voterRanking)))
    strategies = []
    for alternative in permutations:
        newPreferences = preferences.copy()
        newPreferences[voter] = alternative
        outcomeRanking = votingScheme.outcomeRanking(newPreferences)
        option = [alternative, votingScheme.outcome(newPreferences), happiness(voter, newPreferences, outcomeRanking), overallHappiness(
            newPreferences, outcomeRanking), overallHappiness(preferences, outcomeRanking)]
        strategies.append(option)
    return strategies


# TEST THINGS HERE
print("Social Ranking:", votingScheme.outcomeRanking(preferences))
print("Voting Winner:", votingScheme.outcome(preferences))
# print(strategicVoting("Voter 1", preferences, votingScheme))
print("Happiness of voters :", overallHappiness(preferences, votingScheme.outcomeRanking(preferences), happinessMetricOptions))
