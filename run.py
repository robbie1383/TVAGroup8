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

# for future command line IO  0 = Steep, 1 = Middle, 2 = Linear ect...
happinessMetricOptions = 0


def happiness(voter: str, preferences, outcome: [str], happinessMetric: int) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"  *Giannis comment - Why string and not index value?
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return: the happiness of a given voter with a given outcome
    """

    # retrieve the preferences of the current voter
    a = preferences.loc[:, voter].tolist()

    # calculate the number of candidates/voting options
    n = len(outcome)
    # calculate how many steps the winner is removed from the current voter's preference list
    s = a.index(outcome[0])

    # For each happinessMetric apply a different happiness calculation function. Max happiness = 1
    if happinessMetric == 0:
        # Happiness is defined on a steep curve and is halved for every step of removal.
        return n/((2 ** s)*n)
    elif happinessMetric == 1:
        # Happiness is defined on a linear curve
        return (n-s)/n
    elif happinessMetric == 2:  # Needs debugging!!
        # Happiness is defined on a middle curve. First step is halved, the rest linear.
        if s == 0:
            return (n*0.5 + (n-s)*0.5) / n
        else:
            return ((n-s)*0.5) / n
    else:
        return 0


# Define overall happiness


def overallHappiness(preferences, outcome: [str], happinessMetric) -> float:
    """
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: social ranking, eg : [A, B, C, D]
    :return:
    """
    # sum the happiness of all individual voters

    # initialise variable that holds total happiness sum
    summedHappiness = 0

    # calculate happiness for each individual voter and add the result to the sum
    for voter in preferences.columns:
        # Print is only for visualisation, should be removed. Happiness is calculated two times on purpose since next line is reduntant.
        print("Happiness of :", voter, " is :", happiness(voter,
                                                          preferences, outcome, happinessMetric))
        # Sum total happiness.
        summedHappiness = summedHappiness + happiness(voter,
                                                      preferences, outcome, happinessMetric)

    # return normalised happiness
    return summedHappiness/len(preferences.columns)

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
print("Happiness of voters :", overallHappiness(
    preferences, votingScheme.outcomeRanking(preferences), happinessMetricOptions))
