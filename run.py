import pandas as pd
import itertools
from Borda import BordaVoting
from PluralityVoting import PluralityVoting
from VotingForTwo import VotingForTwo
from AntiPluralityVoting import AntiPluralityVoting
from Sequential import Sequential

# Read the input from the .csv file.
inputFile = "example.csv"  # for future command line IO
preferences = pd.read_csv(inputFile)
# Choose the voting scheme
votingOptions = [BordaVoting(), PluralityVoting(),
                 AntiPluralityVoting(), VotingForTwo(), Sequential()]
votingSchemeChoice = 1  # for future command line IO
votingScheme = votingOptions[votingSchemeChoice]

# Define happiness function
happinessMetricOption = 0  # for future command line IO  0 = Steep, 1 = Middle, 2 = Linear ect...


def happiness(voter: str, preferences, outcome: str, happinessMetric: int) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"  *Giannis comment - Why string and not index value?
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return: the happiness of a given voter with a given outcome
    """
    preferencesVoter = preferences[voter].tolist()
    m = len(preferencesVoter)
    # calculate how many steps the winner is removed from the current voter's preference list
    s = preferencesVoter.index(outcome)

    if happinessMetric == 0:  # steep curve and is halved for every step of removal.
        return m / ((2 ** s) * m)
    if happinessMetric == 1:  # linear curve
        return (m - s) / m
    # Needs debugging!!
    if happinessMetric == 2:  # middle curve. First step is halved, the rest linear.
        if s == 0:
            return (m * 0.5 + (m - s) * 0.5) / m
        else:
            return ((m - s) * 0.5) / m


# Define overall happiness
def overallHappiness(preferences, outcome: str, happinessMetric) -> float:
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
def strategicVoting(voter: str, preferences, votingScheme, happinessMetric):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :return: a strategic voting option of the form :
             [newVoterRanking, outcome, trueHappiness, newHappiness,
                 newOverallHappiness, trueOverallHappiness]
    """
    voterRanking = preferences[voter]
    permutations = list(itertools.permutations(list(voterRanking)))
    strategies = []
    for alternative in permutations:
        newPreferences = preferences.copy()
        newPreferences[voter] = alternative
        outcome = votingScheme.outcome(newPreferences)
        option = [alternative, outcome,
                  happiness(voter, preferences, outcome, happinessMetric),
                  happiness(voter, newPreferences, outcome, happinessMetric),
                  overallHappiness(newPreferences, outcome, happinessMetric),
                  overallHappiness(preferences, outcome, happinessMetric)]
        strategies.append(option)
    return strategies


def risk(preferences, happinessMetric):
    """
    :param preferences: pandas dataframe with the voting preferences
    :return
    """
    overall_risk_count = 0
    overall_strategy_voting_options = 0
    for voter in preferences.columns:
        strategies = strategicVoting(voter, preferences, votingScheme, happinessMetric)
        for strategy in strategies:
            overall_strategy_voting_options += 1
            # risk happen if the new overall happiness reduced by the strategy voting
            if (strategy[4] < strategy[5]) & (strategy[2] < strategy[3]):
                overall_risk_count += 1
    return overall_risk_count / overall_strategy_voting_options

# TEST THINGS HERE
#print("Social Ranking:", votingScheme.outcomeRanking(preferences))
print("Voting Winner:", votingScheme.outcome(preferences))
# print(strategicVoting("Voter 1", preferences, votingScheme))
print("Happiness of voters :",
      overallHappiness(preferences, votingScheme.outcome(preferences), happinessMetricOption))
print("Risks  :", risk(preferences, happinessMetricOption))
