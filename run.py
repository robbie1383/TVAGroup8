import pandas as pd
import itertools
from random import randrange
from VotingSchemes.Borda import BordaVoting
from VotingSchemes.PluralityVoting import PluralityVoting
from VotingSchemes.VotingForTwo import VotingForTwo
from VotingSchemes.AntiPluralityVoting import AntiPluralityVoting
from VotingSchemes.Sequential import Sequential


def happiness(voter: str, preferences, outcome, happinessMetric: int) -> float:
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: a candidate that won some election
    :param happinessMetric: happiness function calculation scheme
    :return: happiness of one voter in the given scenario
    """
    preferencesVoter = preferences[voter].tolist()
    nrOutcomes = len(preferencesVoter)
    winnerRank = preferencesVoter.index(outcome)

    if happinessMetric == 0:  # steep curve and is halved for every step of removal.
        return nrOutcomes / ((2 ** winnerRank) * nrOutcomes)
    if happinessMetric == 1:  # linear curve
        return (nrOutcomes - winnerRank) / nrOutcomes
    if happinessMetric == 2:  # middle curve. First step is halved, the rest linear.
        if winnerRank == 0:
            return (nrOutcomes * 0.5 + (nrOutcomes - winnerRank) * 0.5) / nrOutcomes
        else:
            return ((nrOutcomes - winnerRank) * 0.5) / nrOutcomes


def overallHappiness(preferences, outcome, happinessMetric : int) -> float:
    """
    :param preferences: pandas dataframe with the voting preferences
    :param outcome: a candidate that won some election
    :param happinessMetric: happiness function calculation scheme
    :return: overall happiness of all voters
    """
    sum = 0
    for voter in preferences.columns:
        sum += happiness(voter, preferences, outcome, happinessMetric)
    return sum


def strategicVoting(voter: str, preferences, votingScheme, happinessMetric : int):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :param happinessMetric: happiness function calculation scheme
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


def risk(voter : str, preferences, votingScheme, happinessMetric : int, ):
    """
    :param voter: string representing the voted, eg : "Voter 1"
    :param preferences: pandas dataframe with the voting preferences
    :param votingScheme: initialized voting scheme
    :param happinessMetric: happiness function calculation scheme
    :return:
    """
    overall_risk_count = 0
    overall_strategy_voting_options = 0
    strategies = strategicVoting(voter, preferences, votingScheme, happinessMetric)
    for strategy in strategies:
        overall_strategy_voting_options += 1
        # risk happen if the new overall happiness reduced by the strategy voting
        if (strategy[4] < strategy[5]) & (strategy[2] > strategy[3]):
            overall_risk_count += 1
    return overall_risk_count / overall_strategy_voting_options


def inputChecker(preferences) :
    n = len(preferences.index)
    options = [chr(ord("A") + i) for i in range(n)]
    for column in preferences.columns:
        if "Voter " not in column :
            print("\nColumn name <<", column, ">> is not specified correctly. Use <<Voter n>> for the column names.\n")
            return False
        optionsCopy = options.copy()
        for element in preferences[column]:
            if pd.isnull(element):
                print("\nColumn name <<", column, ">> contains an empty rating.\n")
                return False
            if element in optionsCopy:
                optionsCopy.remove(element)
            else :
                print("\nColumn name <<", column, ">> contains two votes for candidate", element, ".\n")
                return False
    return True

def inputPreferences():
    # Read the input from the .csv file.
    correct = False
    while not correct :
        print("This software uses .csv files as input. Please enter the name of your file as <name>.csv below.")
        print("If you wish to use the pre-defined example, press Enter.")
        inputFile = input(">> ")
        if len(inputFile) == 0:
            inputFile = "example.csv"
        preferences = pd.read_csv(inputFile)
        check = inputChecker(preferences)
        if check : correct = True
        else : print("Input file contains problems. Try again.")
    print("\nPreview of the file used:")
    print(preferences.head(5))
    return preferences


def inputVotingScheme():
    # Choose the voting scheme
    votingOptions = [BordaVoting(), PluralityVoting(), AntiPluralityVoting(), VotingForTwo(), Sequential()]
    print("\nSelect one of the voting schemes below by entering its number id.")
    for scheme in range(len(votingOptions)):
        print(scheme, ":", votingOptions[scheme].toString())
    print("If you wish to use a random voting scheme, press Enter.")
    votingSchemeChoice = "start"
    while not (votingSchemeChoice in "01234" or len(votingSchemeChoice) == 0):
        votingSchemeChoice = input(">> ")

    if len(votingSchemeChoice) == 0: votingSchemeChoice = randrange(5)
    votingScheme = votingOptions[int(votingSchemeChoice)]
    print("\nVoting scheme selected is", votingScheme.toString())
    return votingScheme

def inputHappiness():
    # Choose happiness function
    print("\nSelect what kind of happiness function you want to use by entering its number id.")
    print("0 : Steep curve happiness : ")
    print("1 : Linear curve happiness : ")
    print("2 : Middle curve happiness : ")
    print("If you wish to select a random curve, press Enter.")
    happinessChoice = "start"
    while not (happinessChoice in "012" or len(happinessChoice) == 0):
        happinessChoice = input(">> ")
    if len(happinessChoice) == 0:
        happinessChoice = randrange(3)
    happinessChoice = int(happinessChoice)
    if happinessChoice == 0: print("\nHappiness function selected uses a steep curve.")
    if happinessChoice == 1: print("\nHappiness function selected uses a linear curve.")
    if happinessChoice == 2: print("\nHappiness function selected uses a middle curve.")
    return happinessChoice


def createCommands(votingScheme):
    options = "help0123456"
    commands = "\nSelect one of the commands below by selecting its number id."
    commands += "\n0 : Quit the program."
    commands += "\n1 : Print the social ranking of this scenario."
    commands += "\n2 : Print the winner of this scenario."
    commands += "\n3 : Print the strategic voting options for some voter."
    commands += "\n4 : Print the happiness of some voter or all voters."
    commands += "\n5 : Print the overall happiness of this scenario."
    commands += "\n6 : Print the risk of strategic voting for some voter."
    if type(votingScheme) is Sequential:
        options += "7"
        commands += "7 : Update the voting agenda."
    commands += "\nhelp : Prints a list of all the commands."

    return options, commands

def main():
    print("Welcome to the voting simulator.")

    # Set scenario parameters
    preferences = inputPreferences()
    votingScheme = inputVotingScheme()
    happinessChoice = inputHappiness()

    # Command loop
    options, commands = createCommands(votingScheme)
    print(commands)
    command = input("\n>> ")
    while command != "0":
        if command not in options:
            print("Command", command, "is not supported. Use <help> for a list of commands.")

        if command == "help":
            print(commands)

        if command == "1":
            print("Social ranking of this scenario is :")
            print(votingScheme.outcomeRanking(preferences))

        if command == "2":
            print("Winning candidate in this scenario is :")
            print(votingScheme.outcome(preferences))

        if command == "3":
            print("Enter the number id of the voter you want to use.")
            voter = input(">> ")
            voter = "Voter " + voter
            if voter not in preferences.columns :
                print("This voter does not exist.")
            else :
                print("The strategic voting options for this voter are :")
                print("[newVoterRanking, newOutcome, trueHappiness, newHappiness, newOverallHappiness, trueOverallHappiness]")
                strategies = strategicVoting(voter, preferences, votingScheme, happinessChoice)
                for s in strategies: print(s)

        if command == "4":
            print("Enter the number id of the voter you want to use. Enter <all> to get a list of all.")
            voter = input(">> ")
            outcome = votingScheme.outcome(preferences)
            if voter == "all":
                list = []
                for v in preferences.columns:
                    list.append(happiness(v, preferences, outcome, happinessChoice))
                print(preferences.columns.tolist())
                print(list)
            else :
                voter = "Voter " + voter
                if voter not in preferences.columns:
                    print("This voter does not exist.")
                else:
                    print("The happiness value for", voter, "is :")
                    print(happiness(voter, preferences, outcome, happinessChoice))

        if command == "5":
            print("The overall happiness in this scenario is :")
            outcome = votingScheme.outcome(preferences)
            print(overallHappiness(preferences, outcome, happinessChoice))

        if command == "6":
            print("Enter the number id of the voter you want to use. Enter <all> to get a list of all.")
            voter = input(">> ")
            outcome = votingScheme.outcome(preferences)
            if voter == "all":
                list = []
                for v in preferences.columns:
                    list.append(risk(v, preferences, votingScheme, happinessChoice))
                print(preferences.columns.tolist())
                print(list)
            else:
                voter = "Voter " + voter
                if voter not in preferences.columns:
                    print("This voter does not exist.")
                else:
                    print("The risk of strategic voting for", voter, "is :")
                    print(risk(voter, preferences, votingScheme, happinessChoice))

        command = input("\n>> ")

    print("Simulation ended.")


if __name__ == "__main__":
    main()